import requests

from utils import generate_links

from app import app

def send_email_success(links, cfg):
    """Send an email using MailGun"""

    urls = generate_links(links, cfg)

    text = "The file was processed. Here the links to download: " \
        + ' '.join(urls)

    r = requests.post(
        app.config['MAILGUN_URL'],
        auth=("api", app.config['MAILGUN_KEY']),
        data={
            "subject": "File processed!",
            "from": "no-answer@mg.sousaaraujoti.com.br",
            "to": "dedecu@hotmail.com",
            "text": text,
            "html": text,
        },
    )
    print("Enviado!")
    return r