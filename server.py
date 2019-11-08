import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for, flash
import click
from forms import LoginForm
import os


dburl = "postgresql://nm3150:0611@34.74.165.156/proj1part2"

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
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
        cursor = conn.execute('select cpswd from customer where cid = ' + '\'' + temp_usrname + '\'')
        pswd = ""
        for result in cursor:
            pswd = str(result['cpswd']).strip()
        print(len(pswd))
        print(temp_pswd)
        print(pswd == temp_pswd)
        if pswd != temp_pswd:
            flash('invalid')
            print("here")
            next_page = url_for('index')
            return redirect(next_page)
        else:
            cursor.close()
            flash('success')
            print("here123")
            next_page = url_for('login_success')
            return redirect(next_page)

    return render_template('index.html', **context)

@app.route('/login_success', methods = ['GET', 'POST'])
def login_success():
    context = dict()
    names = []
    cursor = conn.execute('select cname from customer')
    for result in cursor:
        names.append(result['cname'])
    cursor.close()
    context['data'] = names
    return render_template('login-success.html', **context)

if __name__ == "__main__":
    app.run(debug = true, port=8111)
