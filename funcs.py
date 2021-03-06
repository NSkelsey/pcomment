import re
import chardet
import json

import requests
from bs4 import BeautifulSoup

def validate_register(params):
    return (True, {})


VALID_TAGS = ['strong', 'em', 'p', 'ul', 'li', 'br',
        'div', 'blockquote', 'a', 'span', 'pre', 'code', 'b']

# from http://stackoverflow.com/questions/997078/email-regular-expression
email_regex = re.compile('(([0-9a-zA-Z][-\.\w]*[0-9a-zA-Z])*@([0-9a-zA-Z][-\w]*[0-9a-zA-Z]\.+[a-zA-Z]{2,9}))')

f = lambda m: m.groups()[1] + "--at--" + m.groups()[2]

#only for gmail emails right now
def clean_html_email(html):
    #html = unicode(html,'ISO-8859-1')
    html = html.replace(u'\u00A0', " ")
    html = html.replace(u'\xc2', '')
    soup = BeautifulSoup(html)
    for tag in soup.findAll(True):
        tag.attrs = None
        if tag.name not in VALID_TAGS:
            tag.extract()
    html = soup.renderContents()
    html = re.sub(email_regex, f, html)
    return html


GMAIL_RE_EMAIL_TF = re.compile(r'^(?P<name>[^<]*)<(?P<email>[^<]*)>')

def pull_out_name_email(email_text):
    matches = re.search(GMAIL_RE_EMAIL_TF, email_text)
    g = matches.groups()
    if g is not None:
        name, email = matches.groups()
        return (name, email)
    else:
        return email_text

def respond_confirming_post(response, account):
    all_headers = json.loads(response.everything)
    r = requests.post(
            "https://api.mailgun.net/v2/pcomment.mailgun.org/messages",
            auth=("api", "key-3d1gtj048oxhghiwh4v2h9tvx-l3hew7"),
            data={"from": "general@pcomment.mailgun.org",
                "to": [account.email],
                'subject': 'RE: %s' % response.subject,
                'text': 'The email was sucessfully posted. Here is the url (http://50.17.215.201:5000/%s)' % response.make_url(),
                'html': 'The email was sucessfully posted. Here is the <a href="http://50.17.215.201:5000/%s" >url</a>' % response.make_url(),
                'In-Reply-To': all_headers.get('Message-Id'),
                'o:tag':'posted',
                })
    print r
    return True


