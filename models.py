from datetime import datetime
import os

from sqlalchemy import *
from sqlalchemy.orm import  sessionmaker, relationship, scoped_session, backref
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
from flask import url_for

sql_url = 'sqlite:///' + os.getcwd() + '/freedom.db'
Base = declarative_base()

engine = create_engine(sql_url, echo=True)
session = scoped_session(sessionmaker(bind=engine,
                                      autoflush=True,
                                      autocommit=True,))

class Account(Base):
    __tablename__ = "account"
    name = Column(String, unique=True)
    email = Column(String, primary_key=True)

    def __init__(self, name, email):
        self.email = email
        self.name = name

    def make_url(self):
        return url_for('list', account_name=self.name)

class Response(Base):
    __tablename__ = "response"
    id = Column(Integer, primary_key=True)
    from_email = Column(String, ForeignKey('account.email'))
    to_email = Column(String)
    subject = Column(String)
    text = Column(String)
    date_post = Column(DateTime)
    account = relationship("Account", backref=backref('responses', order_by=date_post))

    def __init__(self, email, to, subject, text):
        self.from_email = email
        self.text = text
        self.to_email = to
        self.subject = subject
        self.date_post = datetime.now()

    def __repr__(self):
        return '<Respo:  %s,\n %s' % (self.from_email, self.text)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
