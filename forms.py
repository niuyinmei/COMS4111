from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, FieldList
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

class CashierForm(FlaskForm):
    customerid = StringField('Customer ID', validators = [DataRequired()])
    submit = SubmitField('Check')
    clear = SubmitField('Clear')
    goodid = StringField('Item ID')
    quantity = StringField('Quantity')
    submit1 = SubmitField('Add to cart')
    checkout = SubmitField('Checkout')

# a useless form
class CashierGoodForm(FlaskForm):
    goodid = StringField('Item ID', validators = [DataRequired()])
    quantity = StringField('Quantity', validators = [DataRequired()])
    submit1 = SubmitField('Add to cart')

class ManagerForm(FlaskForm):
    workers = SelectField('Workers: ', choices=[])
    suppliers = SelectField('Suppliers: ', validators = [DataRequired()], choices=[('-1', '    ')])
    goods = SelectField('Items: ', choices=[])
