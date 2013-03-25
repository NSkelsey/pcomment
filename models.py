from datetime import datetime
import os

from sqlalchemy import *
from sqlalchemy.orm import  sessionmaker, relationship, scoped_session, backref
from sqlalchemy.ext.declarative import declarative_base
from flask import url_for


sql_url = 'sqlite:///' + os.getcwd() + '/freedom.db'
Base = declarative_base()

engine = create_engine(sql_url, echo=True)
session = scoped_session(sessionmaker(bind=engine,
                                      autoflush=False,
                                      autocommit=False,))

class Account(Base):
    __tablename__ = "account"
    name = Column(String, unique=True)
    email = Column(String, primary_key=True)

    def __init__(self, name, email):
        self.email = email
        self.name = name

    def make_url(self):
        return url_for('list_responses', account_name=self.name)

class Response(Base):
    __tablename__ = "response"
    id = Column(Integer, primary_key=True)
    from_email = Column(String, ForeignKey('account.email'))
    to_email = Column(String)
    subject = Column(String)
    body_plain = Column(String)
    raw_html = Column(String)
    cleaned_html = Column(String)
    date_post = Column(DateTime)
    everything = Column(String)
    account = relationship("Account", backref=backref('responses', order_by=date_post))

    def __init__(self, *args, **kwargs):
        self.from_email = kwargs.get('from_email')
        self.to_email = kwargs.get('to_email')
        self.subject = kwargs.get('subject')
        self.raw_html = kwargs.get('raw_html')
        self.cleaned_html = kwargs.get('cleaned_html')
        self.body_plain = kwargs.get('body_plain')
        self.everything = kwargs.get('everything')
        self.date_post = kwargs.get('date_post', datetime.now())

    def __repr__(self):
        return '<Respo:  %s,\n %s>' % (self.from_email, self.body_plain)

    def make_url(self, full=False):
        if full:
            return 'http://50.17.215.201:5000/r/%d' % self.id
        else:
            return '/r/%d' % self.id

if __name__ == "__main__":
    Base.metadata.create_all(engine)
