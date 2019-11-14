from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, FieldList
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired
import datetime
from flask_table import Table, Col

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    identity = SelectField('Identity: ', choices=[('customer','Customer'),('employee','Employee')])
    submit = SubmitField('Sign In')

class CustomerForm1(FlaskForm):
    start_date = DateField('Start from: ', format = '%Y-%m-%d', default = datetime.datetime(2018, 1, 1), validators = [DataRequired()])
    end_date = DateField('End at: ', format = '%Y-%m-%d', default = datetime.date.today(), validators = [DataRequired()])
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
    suppliers = SelectField('Suppliers: ', choices=[])
    goods = SelectField('Items: ', choices=[])
    fire = SubmitField('Fire')
    check = SubmitField('Check Invoice')
    release = SubmitField('Stop supplement')

class ManagerForm1(FlaskForm):
    suppliername = StringField('Supplier Name', validators = [DataRequired()])
    suppliergood = StringField('Supplier Item', validators = [DataRequired()])
    supplieremail = StringField('Supplier Email', validators = [DataRequired()])
    submit = SubmitField('Add Supplier')

class ManagerForm2(FlaskForm):
    employname = StringField('Name: ', validators = [DataRequired()])
    password = PasswordField('New Password: ', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password: ')
    identity = SelectField('Identity: ', choices=[('tallyman','Tallyman'),('cashier','Cashier'), ('manager','Manager')])
    submit = SubmitField('Add Employee')

class TallymanForm(FlaskForm):
    # goodbatch = StringField('Batch No.: ', validators = [DataRequired()])
    # invoiceid = SelectField()
    pass

class RegisterForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('New Password: ', [DataRequired(), EqualTo('confirm', message='Passwords must match')])
    address = StringField('Address', validators = [DataRequired()])
    confirm  = PasswordField('Repeat Password: ')
    submit = SubmitField('Register')

class MembershipForm(FlaskForm):
    cid = StringField('Customer ID', validators = [DataRequired()])
    mem_field = SelectField('Level: ', choices=[('silver','Silver'),('gold','Gold')])
    submit = SubmitField('Register Membership')

