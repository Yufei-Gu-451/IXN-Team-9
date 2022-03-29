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
  clinical_specialty = request.form.get('clinicalSpecialty')

  writeFile(file.read(), file.filename)

  # speech_to_text.speech_to_text(inputfile='app/audio/' + file.filename, outputfile="app/file/input.txt")

  # text_summarizer.summarize_text(input_file='app/file/input.txt', output_file="app/file/output.txt", \
  # compression_rate=0.3, number_of_clusters=2, algorithm_num=9, distance_num=1)

  models.addProcessedFile(file.filename, patient_id, current_doctor_id, appointment_date, clinical_specialty)

  patient = models.getPatient(patient_id)
    
  summarized_file_content = list()
  summarized_file = open("app/file/output.txt")
  for line in summarized_file:
    summarized_file_content.append(line)
  
  summarized_file.close()
  
  transcribed_file_content = list()
  transcribed_file = open("app/file/input.txt")
  for line in transcribed_file:
    transcribed_file_content.append(line)

  return render_template('showProcessedAudio.html', transcribed_lines=transcribed_file_content, summarized_lines=summarized_file_content, patient=patient)

@main.route('/confirmProcessing', methods=['POST'])
@flask_login.login_required
@requires_roles('doctor')
def confirmProcessing():
  confirmation = request.form.get('confirmation')
  if confirmation == 'no':
    models.deleteFile(file_id)
    return render_template('confirmationDenied.html')
  if confirmation == 'yes':
    return render_template('index.html')

@main.route('/confirmationDenied', methods=['POST'])
@flask_login.login_required
@requires_roles('doctor')
def confirmationDenied():
  return render_template('confirmationDenied.html')


@main.route('/viewPatientRecords', methods=['GET', 'POST'])
@flask_login.login_required
def viewPatientRecords():
  headings = ('name', 'appointment date', 'clinical specialty', 'download transcribed audio', 'download summarised report')
  if flask_login.current_user.has_role('doctor'):
    patient_id = request.form['patient']
    patient = models.getPatient(patient_id)
    patient_name = patient.first_name + " " + patient.last_name
    files = models.getPatientFiles(patient_id)
    return render_template('viewPatientRecords.html', files=files, patient_name=patient_name, headings=headings)

  if flask_login.current_user.has_role('patient'):
    patient_id = flask_login.current_user.id
    files = models.getPatientFiles(patient_id)
    return render_template('viewPatientRecords.html', files=files, headings=headings)


@main.route('/downloadSummarizedFile', methods=['GET', 'POST'])
@flask_login.login_required
@requires_roles('doctor')
def downloadSummarizedFile():
  file_id = request.form['patientFile']

  patientFile = models.getFile(file_id)

  return send_file(BytesIO(patientFile.processedData), attachment_filename=patientFile.name, as_attachment=True)

@main.route('/downloadTranscribedFile', methods=['GET', 'POST'])
@flask_login.login_required
@requires_roles('doctor')
def downloadTranscribedFile():
  file_id = request.form['patientFile']

  patientFile = models.getFile(file_id)

  return send_file(BytesIO(patientFile.transcribedData), attachment_filename=patientFile.name, as_attachment=True)

@main.route('/downloadProcessedAudio', methods=['POST'])
@requires_roles('doctor')
def downloadProcessedAudio():
  return send_file("file/output.txt", attachment_filename="transcribed_audio.txt", as_attachment=True)

@main.route('/downloadTranscribedAudio', methods=['GET', 'POST'])
@requires_roles('doctor')
def downloadTranscribedAudio():
  return send_file('file/input.txt', attachment_filename="processed_audio.txt", as_attachment=True)

@main.route('/viewPatients', methods=['GET'])
@flask_login.login_required
@requires_roles('doctor')
def viewPatients():
  headings = ("first name", "last name", "date of birth", "email", "username")
  return render_template('viewPatients.html', headings=headings, patients=models.getAllPatients())

@main.route('/personalUserPage', methods=['GET'])
@flask_login.login_required
def personalUserPage():
  headings = ("first name", "last name", "date of birth", "email", "username")

  current_user_id = flask_login.current_user.id

  user = models.getUser(current_user_id)

  return render_template('personalUserPage.html', headings=headings, user=user)

def writeFile(data, filename):
  with open('app/audio/' + filename, 'wb') as file:
      file.write(data)