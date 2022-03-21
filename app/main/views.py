from flask import render_template, session, redirect, url_for, current_app, request, send_file
import flask_login
# from .. import db
from ..models import User, File, Role
from . import main
from .. import file
from .. import speech_to_text
from .. import text_summarizer
from .forms import AppointmentForm
from .. import models
from datetime import datetime
from io import BytesIO

from flask_login import current_user
from flask import url_for, redirect
from functools import wraps
def requires_roles(*roles):
  def wrapper(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
      if current_user.get_role() not in roles:
        #Redirect the user to an unauthorized notice!
        return redirect(url_for('auth.login'))
      return f(*args, **kwargs)
    return wrapped
  return wrapper

@main.route('/')
def index():
    # print(models.getAllPatients())
  return render_template('index.html')

@main.route('/uploadPage', methods=['GET', 'POST'])
@flask_login.login_required
@requires_roles('doctor')
def uploadAudioPage():
  print(flask_login.current_user.get_role() == 'patient')
  form = AppointmentForm()
  if form.validate_on_submit():
    if form.appointmentDate.data < datetime.date.now():
      return redirect(url_for('uploadAudioPage'))
    else:
      return redirect(url_for('upload'))
  return render_template('uploadPage.html', form=form, patients=models.getAllPatients())

@main.route('/upload', methods=['GET', 'POST'])
@flask_login.login_required
@requires_roles('doctor')
def upload():
  file = request.files['inputFile']
  current_doctor_id = flask_login.current_user.id
  patient_id = request.form.get('patient')
  appointment_date = request.form.get('appointmentDate')

    # print(appointment_date)
    # print(datetime.now())

  writeFile(file.read(), file.filename)

  speech_to_text.speech_to_text(inputfile='app/audio/' + file.filename, outputfile="app/file/input.txt")

  text_summarizer.summarize_text(input_file='app/file/input.txt', output_file="app/file/output.txt", \
  compression_rate=0.3, number_of_clusters=2, algorithm_num=9, distance_num=1)

  models.addProcessedFile(file.filename, patient_id, current_doctor_id, appointment_date)

  patient = models.getPatient(patient_id)
    
  file_content = list()
  f = open("app/file/output.txt")
  for line in f:
    file_content.append(line)

  return render_template('showProcessedAudio.html', lines=file_content, patient=patient)
  

# @main.route('/viewRecords', methods='GET')
# @flask_login.login_required
# @requires_roles('doctor')
# def viewRecords():
#   current_patient_id = flask_login.current_user.id
#   files = models.getPatientFiles(current_patient_id)



@main.route('/viewPatientRecords', methods=['GET', 'POST'])
@flask_login.login_required
def viewPatientRecords():
  headings = ('name', 'appointment date', 'download')
  if flask_login.current_user.has_role('doctor'):
    patient_id = request.form['patient']
    files = models.getPatientFiles(patient_id)
    return render_template('viewPatientRecords.html', files=files)
  if flask_login.current_user.has_role('patient'):
    patient_id = flask_login.current_user.id
    files = models.getPatientFiles(patient_id)
    return render_template('viewPatientRecords.html', files=files)




@main.route('/download', methods=['GET', 'POST'])
@flask_login.login_required
@requires_roles('doctor')
def download():
  file_id = request.form['patientFile']

  patientFile = models.getFile(file_id)

  return send_file(BytesIO(patientFile.processedData), attachment_filename=patientFile.name, as_attachment=True)
    # return redirect(url_for('viewPatients'))

@main.route('/downloadProcessedAudio', methods=['POST'])
@requires_roles('doctor')
def downloadProcessedAudio():
  return send_file("file/output.txt", attachment_filename="transcribed_audio.txt", as_attachment=True)

@main.route('/downloadTranscribedAudio', methods=['POST'])
@requires_roles('doctor')
def downloadTranscribedAudio():
  return send_file('file/input.txt', attachment_filename="processed_audio.txt", as_attachment=True)

@main.route('/viewPatients', methods=['GET'])
@flask_login.login_required
@requires_roles('doctor')
def viewPatients():
  headings = ("first name", "last name", "age", "email", "username")
  return render_template('viewPatients.html', headings=headings, patients=models.getAllPatients())

def writeFile(data, filename):
  with open('app/audio/' + filename, 'wb') as file:
      file.write(data)