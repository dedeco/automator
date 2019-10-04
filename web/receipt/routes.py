import uuid
import os

from flask import Flask, render_template, current_app, request, flash \
                    , send_file, send_from_directory, abort

from flask_uploads import UploadNotAllowed

from . import receipt_blueprint
from .forms import UploadForm

from .models import ReportToExport

from web import db
from web.uploadsets import reports_upload

@receipt_blueprint.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        f = UploadForm(request.values)
        ff = request.files.get('file', None)
        ff.filename = str(uuid.uuid4()) + os.path.splitext(ff.filename)[1]
        if ff:
            try:
                filename = reports_upload.save(ff)

                fp = reports_upload.path(filename)

                r = ReportToExport(f.report_id.data
                            ,f.column_number.data
                            ,f.email.data
                            ,filename)

                db.session.add(r)
                db.session.commit()

                flash(u"At the end of processing yout will recieve the file by " \
                    "email! ;-)", u"success")

                f = UploadForm()

            except UploadNotAllowed:
                flash(u"Type file not allowed", u"error")
    else:
        f = UploadForm()
    return render_template('receipt/index.html', form=f)


@receipt_blueprint.route('/download/<path:filename>', methods=['GET','POST'])
def download(filename):
    UPLOAD_DIRECTORY = "./tmp/uploads/"
    return send_from_directory(directory=UPLOAD_DIRECTORY
                            , filename=filename
                            , as_attachment=True)