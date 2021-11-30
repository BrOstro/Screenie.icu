import os
from datetime import date
from urllib.parse import urlparse

from flask import Blueprint, request, current_app, send_from_directory
from werkzeug.security import safe_join
from werkzeug.utils import secure_filename

uploads = Blueprint('uploads', __name__)


@uploads.route("/upload", methods=['POST'])
def upload():
    if request.form.to_dict(flat=False)['secret'][0] == current_app.config['SECRET_KEY']:
        uploaded_file = request.files['sharex']
        if uploaded_file.filename != '':
            date_prefix = date.today().strftime(current_app.config['FILE_DATE_FORMAT'])
            upload_directory = os.path.join(current_app.config['UPLOADS_PATH'], date_prefix)
            target_name = safe_join(upload_directory, secure_filename(uploaded_file.filename))

            if not os.path.exists(upload_directory):  # If the upload destination doesn't exist, create it
                os.makedirs(upload_directory)

            uploaded_file.save(target_name)
            host = urlparse(request.base_url).hostname
            return os.path.join(host, target_name)
    return "list of accounts"


@uploads.route("/<path:filename>")
def download_file(filename):
    date_prefix = date.today().strftime(current_app.config['FILE_DATE_FORMAT'])
    upload_directory = os.path.join(current_app.config['UPLOADS_PATH'], date_prefix)

    return send_from_directory(
        upload_directory, filename, as_attachment=False
    )
