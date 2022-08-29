from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, TextAreaField, DecimalRangeField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired
from models import *

class EnterCityForm(FlaskForm):
    city = StringField("City", validators=[DataRequired()])
    submit =SubmitField("Search")

class AddCityForm(FlaskForm):
    city = StringField("City", validators=[DataRequired()])
    submit = SubmitField("Add")