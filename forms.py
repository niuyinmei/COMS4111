from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import datetime
from flask_table import Table, Col

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    identity = SelectField('Identity: ', choices=[('customer','Customer'),('employee','Employee')])
    submit = SubmitField('Sign In')

class CustomerForm1(FlaskForm):
    start_date = DateField('Start from: ', format = '%Y-%m-%d', default = datetime.datetime(2020, 5, 17), validators = [DataRequired()])
    end_date = DateField('End at: ', format = '%Y-%m-%d',  validators = [DataRequired()])
    submit = SubmitField('Check')

class CustomerTable1(Table):
    bid = Col('Bill ID')
    billpaid = Col('Amount')
    quantity = Col('Quantity')
    employid = Col('Cashier')
    billdate = Col('Date')
    billpmnt = Col('Payment')