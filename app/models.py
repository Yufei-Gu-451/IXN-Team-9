from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import UserMixin
from . import login_manager


class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300))
    appointment_date = db.Column(db.Date)
    processedData = db.Column(db.LargeBinary)
    
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    patient = db.relationship("User", foreign_keys=patient_id)
    doctor = db.relationship("User", foreign_keys=doctor_id)


    def __repr__(self):
        return '<File %r>' % self.name

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    age = db.Column(db.Integer)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    password_hash = db.Column(db.String(128))
    
    # file = db.relationship("File", backref="user", lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_role(self):
        return Role.query.get(self.role_id).name
        
    def has_role(self, role):
        return role == Role.query.get(self.role_id).name

    def __repr__(self):
        return '<User %r>' % self.username

# class Appointment(db.Model):
#     __tablename__ = 'appointment'
#     id = db.Column(db.Integer, primary_key=True)

#     patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
#     doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def addProcessedFile(filename, patient_id, doctor_id, appointment_date):
    processedFile = open("app/file/output.txt", "r")
    filename = filename.split('.')[0] + ".txt"

    upload = File(name=filename, appointment_date=appointment_date, processedData=processedFile.read().encode(), patient_id=patient_id, doctor_id=doctor_id)
    processedFile.close()
    
    db.session.add(upload)
    db.session.commit()

def getAllPatients():
    patient_role_id = Role.query.filter_by(name='patient').first()
    return User.query.join(User.role).filter(Role.id == 2).all()

def getPatientFiles(patientId):
    return File.query.filter(File.patient_id == patientId).all()

def getFile(fileId):
    return File.query.filter(File.id == fileId).first()