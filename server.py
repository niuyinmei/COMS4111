import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
import click
dburl = "postgresql://nm3150:0611@104.196.18.7/w4111"

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


@click.command()
@click.option('--debug', is_flag=True)
@click.option('--threaded', is_flag=True)
@click.argument('HOST', default='0.0.0.0')
@click.argument('PORT', default=8111, type=int)
def run(debug, threaded, host, port):
    print("here")
    engine = create_engine(dburl)
    conn = engine.connect()
    print("running on %s:%d" % (host, port))
    # app.run()

@app.route('/')
def index():
    engine = create_engine(dburl)
    conn = engine.connect()
    # print("running on %s:%d" % (host, port))
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug = true, port=8111)
