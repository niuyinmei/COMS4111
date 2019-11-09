import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
import click
from forms import LoginForm
import os
from model import User, Customer, Employee

dburl = "postgresql://nm3150:0611@34.74.165.156/proj1part2"

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

login = LoginManager(app)
login.login_view = 'login'
@login.user_loader
def load_user(user_id):
    return User(user_id)


SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
engine = create_engine(dburl)
conn = engine.connect()

@click.command()
@click.option('--debug', is_flag=True)
@click.option('--threaded', is_flag=True)
@click.argument('HOST', default='0.0.0.0')
@click.argument('PORT', default=8111, type=int)
def run(debug, threaded, host, port):
    print("here")
    print("running on %s:%d" % (host, port))
    # app.run()

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    context = dict()
    context['title'] = 'Home'
    context['user'] = {'username': 'Jeff'}
    form = LoginForm()
    context['form'] = form

    if form.validate_on_submit():
        temp_usrname = form.username.data
        temp_pswd = form.password.data
        temp_id = form.identity.data
        temp_id_pswd = ''
        if temp_id == 'customer':
            temp_id_pswd = 'c'
        if temp_id == 'employee':
            temp_id_pswd = 'employ'
        cursor = conn.execute('select ' + temp_id_pswd + 'pswd from ' + temp_id + ' where ' + temp_id_pswd + 'id = ' + '\'' + temp_usrname + '\'')
        pswd = ""
        for result in cursor:
            if temp_id == 'customer':
                pswd = str(result['cpswd']).strip()
            if temp_id == 'employee':
                pswd = str(result['employpswd']).strip()
        if pswd != temp_pswd:
            flash('invalid')
            print("here")
            print(form.identity.data)
            next_page = url_for('index')
            return redirect(next_page)
        else:
            cursor.close()
            flash('success')
            current_user = User(temp_usrname)
            login_user(current_user)
            next_page = url_for('login_success_' + temp_id)
            return redirect(next_page)

    return render_template('index.html', **context)

@app.route('/login_success_customer', methods = ['GET', 'POST'])
def login_success_customer():
    context = dict()
    names = []

    cursor = conn.execute('select * from customer where cid = \'' + current_user.id + '\'')
    for result in cursor:
        names.append(result['cname'])
        # customer = Customer(current_user.id, result['cname'].strip(), )
    cursor.close()
    context['data'] = names
    customer = Customer
    context['current_user'] = current_user
    return render_template('login-success-customer.html', **context)

@app.route('/login_success_employee', methods = ['GET', 'POST'])
def login_success_employee():
    context = dict()
    names = []
    cursor = conn.execute('select employname from employee')
    for result in cursor:
        names.append(result['employname'])
    cursor.close()
    context['data'] = names
    return render_template('login-success-employee.html', **context)

if __name__ == "__main__":
    app.run(debug = true, port=8111)
