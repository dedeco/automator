from sqlalchemy import Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref

from web import db

class ReportToExport(db.Model):
    __tablename__ = 'reports_to_export'    

    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer)
    column_number = db.Column(db.Integer)
    export_to =  db.Column(db.Integer)
    email = db.Column(db.String(255))
    file = db.Column(db.String(255))
    status = db.Column(db.Integer)

    def __init__(self, report_id, column_number, email, file):
        self.report_id = report_id
        self.column_number = column_number
        self.export_to = 0
        self.email = email
        self.file = file
        self.status = 0