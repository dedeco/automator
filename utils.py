import os, shutil
import re
import uuid
import urllib.request

from fpdf import FPDF
from PIL import Image
from shutil import copyfile, rmtree
from pdfrw import PdfReader, PdfWriter

from selenium import webdriver


def download_file(i, file, directory, cfg):
    new_file_name = '{0:04}'.format(i)
    filename, file_extension = os.path.splitext(file)
    path_file = directory + new_file_name
    local_filename, headers = urllib.request.urlretrieve(file, path_file + file_extension)
    if 'verifyReceipt.php?' in file:
        if os.path.isfile(local_filename):
            os.remove(local_filename)
        screen_path = get_screen_shot(file, path_file + '.png', cfg)


def zip_directories(path, zip_file):
    for root, dirs, files in os.walk(path):
        files.sort()
        for file in files:
            zip_file.write(os.path.join(root, file))


def create_dir(name, cfg, uuid_name=None):
    if not uuid_name:
        uuid_name = str(uuid.uuid4())
    directory = cfg['PREFIX_BASE_DIR'] + name + "/" + uuid_name + "/"
    os.mkdir(directory)
    return uuid_name, directory


def create_dir_person(base, person):
    directory = base + person.replace(" ", "_")
    try:
        os.mkdir(directory)
    except FileExistsError:
        pass
    return directory


def rep_esp(z):
    return re.sub("[!@#$%^&*()[]{};:,./<>?\|`~-=_+ ]", "_", z).replace("/","_")


def remove_dir(directory):
    try:
        rmtree(directory)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


def convert_files_to_pdf(uuid_name, path, cfg):
    for root, dirs, files in os.walk(path):

        uuid_name, directory = create_dir('unmerged', cfg=cfg, uuid_name=uuid_name)

        from_ = cfg['TMP_DOWNLOADS_DEST'] + uuid_name + '/'
        to = cfg['TMP_UNMERGED_DEST'] + uuid_name + '/'

        files.sort()

        for i, file in enumerate(files):
            pdf = FPDF('P', 'mm', 'A4')
            pdf_name = '{0:04}'.format(i) + ".pdf"
            filename, file_extension = os.path.splitext(file)
            if file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
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
                if file_extension in ['.pdf', ]:
                    # print('copying')
                    # print(os.path.join(from_, file), os.path.join(to, pdf_name))
                    copyfile(os.path.join(from_, file), os.path.join(to, pdf_name))
                else:
                    print('file not supported')


def merge_pdf(person_dir, uuid_name, pdf_name, cfg):
    to = cfg['TMP_UNMERGED_DEST'] + uuid_name + '/'
    writer = PdfWriter()
    for root, dirs, files in os.walk(to):
        files.sort()
        for file in files:
            writer.addpages(PdfReader(os.path.join(to, file)).pages)
        writer.write(person_dir + "/" + pdf_name)
    remove_dir(to)


def generate_links(files, cfg):
    urls = []
    for type_, filename in files.items():
        link = cfg['INDEX_URL'] + "/download/" + filename
        urls.append("<a href=" + link + ">" + type_ + "</a>")
    return urls


def do_screen_capturing(url, screen_path, width, height, cfg):
    driver = webdriver.PhantomJS(service_log_path=cfg['PREFIX_BASE_DIR'] + '/log/ghostwriter.log')
    driver.set_script_timeout(30)
    if width and height:
        driver.set_window_size(width, height)
    driver.get(url)
    driver.save_screenshot(screen_path)
    driver.close()
    driver.quit()


def get_screen_shot(url, path_file, cfg):
    width = 1024
    height = 768
    do_screen_capturing(url, path_file, width, height, cfg)
    return True


def remove_all(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
