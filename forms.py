from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, FloatField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])

class InventoryItemForm(FlaskForm):
    part_name = StringField('Part Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    origin_partnumber = StringField('Origin Part Number')
    mcmaster_carr_partnumber = StringField('McMaster-Carr Part Number')
    cost = FloatField('Cost')
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    min_on_hand = IntegerField('Minimum On Hand', validators=[DataRequired()])
    location = StringField('Location')
    manufacturer = StringField('Manufacturer')
    notes = TextAreaField('Notes')
