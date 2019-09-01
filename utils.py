import os
import uuid
import urllib.request

def download_file(file, directory):
    urllib.request.urlretrieve(file, directory + os.path.basename(file))

def zip_directories(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def create_dir(name, cfg, uuid_name=None):
    if not uuid_name:
        uuid_name = str(uuid.uuid4())
    directory = cfg['PREFIX_BASE_DIR'] + name+ "/" + uuid_name +"/"
    os.mkdir(directory)
    return uuid_name, directory

def remove_dir(directory):
    try:
        rmtree(directory)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))

from fpdf import FPDF
from PIL import Image
from shutil import copyfile, rmtree
from pdfrw import PdfReader, PdfWriter

def convert_files_to_pdf(uuid_name, path, cfg):
    
    for root, dirs, files in os.walk(path):

        uuid_name, directory = create_dir('unmerged', cfg=cfg, uuid_name=uuid_name)

        from_ = cfg['TMP_DOWNLOADS_DEST'] + uuid_name + '/'
        to =  cfg['TMP_UNMERGED_DEST'] + uuid_name + '/'

        for i, file in enumerate(files):
            pdf = FPDF('P', 'mm', 'A4')
            pdf_name = "partial_" + '{0:04}'.format(i) + ".pdf"
            filename, file_extension = os.path.splitext(file)
            if file_extension in ['.jpg','.jpeg','.png','.gif']:
                cover = Image.open(os.path.join(root, file))
                width, height = cover.size
                # convert pixel in mm with 1px=0.264583 mm
                width, height = float(width * 0.264583), float(height * 0.264583)
                # given we are working with A4 format size 
                pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}
                # get page orientation from file size 
                orientation = 'P' if width < height else 'L'
                #  make sure file size is not greater than the pdf format size
                width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
                height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']
                pdf.add_page(orientation=orientation)
                pdf.image(os.path.join(from_, file), 0, 0, width, height)
                pdf.output(os.path.join(to, pdf_name), "F")
            else:
                if file_extension in ['.pdf',]:
                    #print('copying')
                    #print(os.path.join(from_, file), os.path.join(to, pdf_name))
                    copyfile(os.path.join(from_, file), os.path.join(to, pdf_name))
                else:
                     print('file not supported')

def merge_pdf(uuid_name, pdf_name, cfg):
    to = cfg['TMP_UNMERGED_DEST'] + uuid_name + '/'
    writer = PdfWriter()
    for root, dirs, files in os.walk(to):
        for inpfn in files:
            writer.addpages(PdfReader(os.path.join(to, inpfn)).pages)
        writer.write(pdf_name)
    remove_dir(to)

from flask import url_for

def generate_links(files, cfg):
    urls = []
    for type_, filename in files.items():
        link = cfg['INDEX_URL']+ "/download/" + filename
        urls.append("<a href="+link+">"+type_+"</a>")
    return urls
