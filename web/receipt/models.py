from sqlalchemy import Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref

from web import db


class ReportToExport(db.Model):
    __tablename__ = 'reports_to_export'

    id = db.Column(db.Integer, primary_key=True)
    report_name = db.Column(db.String(255))
    export_type = db.Column(db.Integer)
    email = db.Column(db.String(255))
    file = db.Column(db.String(255))
    status = db.Column(db.Integer)

    def __init__(self, report_name, export_type, email, file):
        self.report_name = report_name
        self.export_type = export_type
        self.email = email
        self.file = file
        self.status = 0
