from flask import request
from bs4 import BeautifulSoup
import re


def validate_register(params):
    return (True, {})


VALID_TAGS = ['strong', 'em', 'p', 'ul', 'li', 'br',
              'div', 'blockquote', 'a', 'span', 'pre', 'code']

def clean_html_email(html):
    soup = BeautifulSoup(html)
    for tag in soup.findAll(True):
        tag.attrs = None
        if tag.name not in VALID_TAGS:
            tag.extract()
    return soup.renderContents()


GMAIL_RE_EMAIL_TF = re.compile(r'^(?P<name>[^<]*)<(?P<email>[^<]*)>')

def pull_out_name_email(email_text):
    matches = re.search(GMAIL_RE_EMAIL_TF, email_text)
    g = matches.groups()
    if g is not None:
        name, email = matches.groups()
        return (name, email)
    else:
        return email_text

