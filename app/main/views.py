from flask import render_template, session, redirect, url_for, current_app, request
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
    print(models.getAllPatients())
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
    # patient_id = User.query.filter(Role.id == 2).all() # query all users where they are patients
    current_doctor_id = flask_login.current_user.id
    patient_id = request.form.get('patient')

    writeFile(file.read(), file.filename)

    appointment = request.form.get('appointmentDate')

    speech_to_text.speech_to_text(inputfile='app/audio/' + file.filename, outputfile="app/file/temp_input.txt")
    text_summarizer.summarize_text(input_file='app/file/temp_input.txt', output_file="app/file/temp_output.txt", compression_rate=0.3, number_of_clusters=2)

    models.addProcessedFile(file.filename, patient_id, current_doctor_id)
    
    f = open("app/file/temp_output.txt")
    for line in f:
        file_content = line

    return file_content

@main.route('/download')
def download():
    upload = Files.query.get(12)
    filename = (upload.name)[:-4] + ".txt"
    send_file(BytesIO(upload.processedData), attachment_filename=filename, as_attachment=True)
    return render_template('index.html', form=form)

def writeFile(data, filename):
    with open('app/audio/' + filename, 'wb') as file:
        file.write(data)