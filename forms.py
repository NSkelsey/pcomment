from wtforms import Form, TextField, TextAreaField, BooleanField, validators

class EditForm(Form):
    raw_html = TextAreaField('Body', [validators.Length(min=0, max=600000)])
    subject = TextField('Subject', [validators.Length(min=0, max=140)])
    use_html = BooleanField('Use HTML or plaintext?', )


