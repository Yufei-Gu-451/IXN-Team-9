from flask import Flask, render_template, session, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'afygawyufgwauyf'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:Shamrock_640@localhost/transAIte"

db = SQLAlchemy(app)

db.init_app(app)

bootstrap = Bootstrap(app)
moment = Moment(app)

class Files(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)


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

    newFile = Files(user_id = 1, name = file.filename, data=file.read())
    db.session.add(newFile)
    db.session.commit()
    
    return file.filename
