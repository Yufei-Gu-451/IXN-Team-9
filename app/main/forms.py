from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields import DateField

class AppointmentForm(FlaskForm):
    # appointmentDate = DateField('Date', format='%d-%m-%Y', validators=[DataRequired()])
    appointmentDate = DateField(
        'Enter date', format='%d-%m-%Y', validators=[DataRequired()]
    )
    submit = SubmitField('Submit')

