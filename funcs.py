from flask import request
from bs4 import BeautifulSoup

VALID_TAGS = ['strong', 'em', 'p', 'ul', 'li', 'br', 'div', 'blockquote', 'a', 'span', 'pre', 'code']

def validate_register(params):
    return (True, {})

def clean_html_email(html):
    soup = BeautifulSoup(html)
    for tag in soup.findAll(True):
        tag.attrs = None
        if tag.name not in VALID_TAGS:
            tag.extract()
    return soup.renderContents()

