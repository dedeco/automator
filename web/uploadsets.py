from flask_uploads import UploadSet

reports_upload = UploadSet('reports', extensions=('xls', 'xlsx'))