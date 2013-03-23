import os
import sys
import json

from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, request, redirect

from models import Response, session, Account
from funcs import validate_register, clean_html_email, pull_out_name_email

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



@app.route("/r/<int:response_id>/edit", methods=['POST', 'GET'])
def edit_posted_resp(response_id):
    if request.method == 'POST':
       unclean_html = request.form['body']
       subject = request.form['subject']
       response = session.query(Response).get(response_id)
       response.subject = subject
       response.cleaned_html = clean_html_email(unclean_html)
       session.add(response)
       session.commit()
       return redirect("/r/%s" % response_id)
    else:
        response = session.query(Response).get(response_id)
        account = response.account
        return render_template('edit_post.jinja2.html', response=response, account=account)

@app.route('/delivered/', methods=['POST'])
def check():
    print "message delivered"
    return "success!"

@app.route("/message/", methods=['POST'])
def debug():
    print "="*120
    print "Recieving message"
    print request.headers
    lst = request.form.items()
    dct = {}
    for k,v in lst:
        dct[k] = v
    everything = json.dumps(dct)
    _from = dct['From']
    to = dct['To']
    subject = dct['Subject']
    cleaned_h = clean_html_email(dct['body-html'])
    name, from_email = pull_out_name_email(_from)

    resp = Response(_from, to,
                    subject, body_plain=dct['body-plain'],
                    raw_html=dct['body-html'],cleaned_html=cleaned_h,
                    everything=everything)
    session.add(resp)
    session.commit()
    return "yes"

@app.teardown_request
def shutdown_session(exception=None):
    session.remove()

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)

