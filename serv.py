import os
import sys
import json

from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template
from flask import request
from IPython import embed

from models import Response, Session, Account

env = Environment(loader=FileSystemLoader(os.getcwd()+"/templates"))
app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return render_template('home.html', guy='lombardo')

@app.route("/a/<account_name>")
def list(account_name):
    session = Session()
    a = session.query(Account).filter_by(name=account_name).first()
    responses = session.query(Response).filter_by(from_email=a.email).all()
    session.close()
    return render_template('list_posts.html', responses=responses)
    

@app.route('/delivered', methods=['POST'])
def check():
    print 'yay'
    return "success!"

@app.route("/message", methods=['POST'])
def debug():
    print "="*120
    print request.headers
    lst = request.form.items()
    dct = {}
    print lst
    for k,v in lst:
        dct[k] = v
    _from = dct['From']
    to = dct['To']
    subject = dct['Subject']
    session = Session()
    resp = Response(_from, to, subject, dct['stripped-text']) 
    session.add(resp)
    session.commit()
    session.close()
    return "yes"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True,) 
