import zipfile

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import app
from emails import send_email_success
from utils import download_file, zip_directories, convert_files_to_pdf, \
    merge_pdf, create_dir, create_dir_person, rep_esp, remove_all
from web.receipt.models import ReportToExport


def get_reports_from_db(database_uri):
    some_engine = create_engine(database_uri)
    Session = sessionmaker(bind=some_engine)
    session = Session()

    Base = declarative_base()

    reports = session.query(ReportToExport).filter_by(status=0).all()
    return session, reports


def parse_xls_to_pandas(report_file):
    print(report_file)
    df = pd.read_excel(app.config['UPLOADED_REPORTS_DEST'] + report_file, index_col=None, header=None)
    df.columns = ['person', 'category', 'link', 'value']
    a = df.groupby(['person', 'category'])['value'].agg('sum')
    b = df.groupby(['person', 'category'])['link'].apply(list)
    result = pd.concat([a, b], axis=1).reset_index()
    print(result.shape)
    return result


def process():
    session, reports = get_reports_from_db(app.config['SQLALCHEMY_DATABASE_URI'])

    for r in reports:
        loc = r.file
        result = None

        try:
            result = parse_xls_to_pandas(loc)
        except FileNotFoundError:
            r.status = 2
            print('File not found')

        for index, row in result.iterrows():

            uuid_name, directory = create_dir('downloads', cfg=app.config)

            person, cat, value, links = row['person'], row['category'], row['value'], row['link']
            for i, file in enumerate(links):
                download_file(i, file, directory, cfg=app.config)

            pdf_name = rep_esp(person) + "-" + rep_esp(cat) + "-" + rep_esp(str(int(value))) + ".pdf "

            convert_files_to_pdf(uuid_name, directory, app.config)
            person_dir = create_dir_person(app.config.get('TMP_FINAL_DEST'), person)
            merge_pdf(person_dir, uuid_name, pdf_name, app.config)

        zip_name = "report_" + rep_esp(r.report_name) + "_" + uuid_name + ".zip"

        zips = zipfile.ZipFile(app.config['UPLOADED_REPORTS_DEST'] + zip_name, 'w', zipfile.ZIP_DEFLATED)
        zip_directories(app.config['TMP_FINAL_DEST'], zips)
        zips.close()

        urls = {'ZIP': zip_name}

        r.status = 1

        print('Sending email')

        send_email_success(r.email, r.report_name, urls, app.config)

        remove_all(app.config.get('TMP_FINAL_DEST'))

        session.commit()

        return


if __name__ == '__main__':
    process()
