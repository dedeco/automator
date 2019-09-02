from wtforms import Form
from wtforms import FileField, TextField, SelectField, IntegerField
from wtforms import validators
from wtforms.fields.html5 import EmailField

type_ =[
    (u'1', u'Pdf'),
    (u'2', u'Zip')
    ]

class UploadForm(Form):
    report_id = IntegerField(u'Id Expense Report', [validators.required()])
    column_number = IntegerField(u'Number Column link', [validators.required()], render_kw={"placeholder": "Start from 0. Default: 0."})
    export_to = SelectField(u"Export to", choices=type_,)
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    file = FileField(u"File", [validators.DataRequired()])
