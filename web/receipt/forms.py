from wtforms import Form
from wtforms import FileField, StringField, SelectField, IntegerField
from wtforms import validators
from wtforms.fields.html5 import EmailField

type_ = [
    (u'1', u'Person+Category+Link+Value'),
    (u'2', u'Link')
]


class UploadForm(Form):
    report_name = StringField(u'Name Report', [validators.required()])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    export_type = SelectField("Template", choices=type_)
    file = FileField(u"File", [validators.DataRequired()])

