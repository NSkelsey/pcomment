import os
import sys
import json

from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, request, redirect

from models import Response, session, Account
from funcs import validate_register

env = Environment(loader=FileSystemLoader(os.getcwd()+"/templates"))
app = Flask(__name__, static_folder="./static", static_url_path="/static")

@app.route("/", methods=['GET'])
def home():
    accounts = session.query(Account).all()
    return render_template('home.jinja2.html', accounts=accounts)

@app.route("/register/", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = request.form
        params = dict(name=form['name'],
                      email=form['email'],
                      )
        if validate_register(params)[0]:
            new_acc = Account(name=params['name'], email=params['email'])
            session.add(new_acc)
            session.commit()
            return redirect("/")
        else:
            return redirect("/")
    else:
        return render_template('register.jinja2.html') 

@app.route("/a/<account_name>")
def list_responses(account_name):
    a = session.query(Account).filter_by(name=account_name).first()
    responses = session.query(Response).filter_by(from_email=a.email).all()
    return render_template('list_posts.html', responses=responses, account=a)

@app.route("/r/<int:response_id>")
def show_response(response_id):
    response = session.query(Response).filter_by(id=response_id).first()
    account = response.account
    return render_template('post.html', response=response, account=account)

@app.route('/delivered/', methods=['POST'])
def check():
    print request.form.items()
    return "success!"

@app.route("/message/", methods=['POST'])
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
    resp = Response(_from, to,
                    subject, dct['body-plain'],
                    dct['body-html'],)
    session.add(resp)
    session.commit()
    return "yes"

@app.teardown_request
def shutdown_session(exception=None):
    session.remove()

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)

