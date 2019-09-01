from wtforms import Form
from wtforms import FileField, TextField, SelectField
from wtforms import validators
from wtforms.fields.html5 import EmailField

type_ =[
    (u'1', u'Pdf'),
    (u'2', u'Zip')
    ]

class UploadForm(Form):
    report_id = TextField(u'Id Expense Report')
    column_number = TextField(u'Number Column link')
    export_to = SelectField(u"Export to", choices=type_)
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    file = FileField(u"File", [validators.DataRequired()])
