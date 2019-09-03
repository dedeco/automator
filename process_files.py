import os
import uuid
import xlrd
import zipfile

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from web.receipt.models import ReportToExport

from utils import download_file, zip_directories, convert_files_to_pdf, \
                    merge_pdf, create_dir, remove_dir, generate_links

from emails import send_email_success

from app import app

def get_reports_from_DB(database_uri):

    some_engine = create_engine(database_uri)
    Session = sessionmaker(bind=some_engine)
    session = Session()

    Base = declarative_base()

    reports = session.query(ReportToExport).filter_by(status=0).all()
    return session, reports

def process():

    session, reports = get_reports_from_DB(app.config['SQLALCHEMY_DATABASE_URI'])

    for r in reports:

        loc = r.file
         
        try:
            wb = xlrd.open_workbook(app.config['UPLOADED_REPORTS_DEST'] + loc) 
        
            uuid_name, directory = create_dir('downloads', cfg=app.config)

            sheet = wb.sheet_by_index(0) 
            arrayofvalues = sheet.col_values(0)

            
            for i, file in enumerate(arrayofvalues[1:]):
                download_file(i, file, directory)

            zip_name = "report_" + str(r.report_id) + "_" + uuid_name + ".zip"

            zipf = zipfile.ZipFile(app.config['UPLOADED_REPORTS_DEST'] + zip_name, 'w', zipfile.ZIP_DEFLATED)
            zip_directories(directory, zipf)
            zipf.close()

            pdf_name =  "report_" + str(r.report_id) + "_" + uuid_name + ".pdf"

            convert_files_to_pdf(uuid_name, directory, app.config)
            merge_pdf(uuid_name, app.config['UPLOADED_REPORTS_DEST'] + pdf_name, app.config)

            remove_dir(directory)

            urls={}
            urls['ZIP'] = zip_name
            urls['PDF'] = pdf_name

            r.status = 1

            print('Sending email')

            send_email_success(r.email, r.report_id, urls, app.config)

        except FileNotFoundError:
            r.status = 2
            print('File not found')

        session.commit()

        return 

if __name__ == '__main__':
    process()