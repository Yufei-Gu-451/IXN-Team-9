from flask import Flask, render_template, session, redirect, url_for, request, send_file
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO

import speech_to_text
import text_summarizer
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'afygawyufgwauyf'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:Shamrock_640@localhost/translAIte"

db = SQLAlchemy(app)

db.init_app(app)

bootstrap = Bootstrap(app)
moment = Moment(app)

class Files(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300))
    # originalData = db.Column(db.LargeBinary)
    processedData = db.Column(db.LargeBinary)

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(64), unique=True)

    users = db.relationship('User', backref='role')
    
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __repr__(self):
        return '<User %r>' % self.username

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Files=Files)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET'])
def index():
    form = NameForm()
    # if form.validate_on_submit():
    #     session['name'] = form.name.data
    #     return redirect(url_for('index'))
    # return render_template('index.html', form=form, name=session.get('name'))
    return render_template('index.html', form=form)

@app.route('/uploadPage', methods=['GET'])
def uploadAudioPage():
    return render_template('uploadPage.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']

    writeFile(file.read(), file.filename)

    speech_to_text.speech_to_text(inputfile='FILE/' + file.filename, outputfile="FILE/temp_input.txt")

    text_summarizer.summarize_text(input_file='FILE/temp_input.txt', output_file="FILE/temp_output.txt", compression_rate=0.3, number_of_clusters=2)

    processedFile = open("FILE/temp_output.txt", "r")
    
    upload = Files(name=file.filename, processedData=processedFile.read().encode())
    processedFile.close()
    
    db.session.add(upload)
    db.session.commit()
    
    return file.filename

@app.route('/download')
def download():
    upload = Files.query.get(12)
    filename = (upload.name)[:-4] + ".txt"
    send_file(BytesIO(upload.processedData), attachment_filename=filename, as_attachment=True)
    return render_template('index.html', form=form)
    
    # return send_file(BytesIO(upload.processedData), attachment_filename=filename, as_attachment=True)
    
    # writeFile(upload.data, upload.name)

    # return upload.name + " written to FILE"


    # return BytesIO(upload.data)

def writeFile(data, filename):
    with open('FILE/' + filename, 'wb') as file:
        file.write(data)

