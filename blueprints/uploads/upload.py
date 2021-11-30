import os
from datetime import date
from urllib.parse import urlparse

from flask import Blueprint, request, current_app, send_from_directory
from werkzeug.security import safe_join
from werkzeug.utils import secure_filename

uploads = Blueprint('uploads', __name__)


def get_file_info(filename):
    extension = filename.rsplit('.', 1)[1].lower()
    file_allowed = False
    target_directory = "."

    if current_app.config['ALLOW_IMAGES'] and extension in current_app.config['ALLOWED_IMAGES']:
        file_allowed = True
        target_directory = current_app.config['IMAGE_PATH']
    elif current_app.config['ALLOW_VIDEOS'] and extension in current_app.config['ALLOWED_VIDEOS']:
        file_allowed = True
        target_directory = current_app.config['VIDEO_PATH']
    elif current_app.config['ALLOW_FILES'] and extension in current_app.config['ALLOWED_FILES']:
        file_allowed = True
        target_directory = current_app.config['FILE_PATH']

    return '.' in filename and file_allowed, target_directory


@uploads.route("/upload", methods=['POST'])
def upload():
    if request.form.to_dict(flat=False)['secret'][0] == current_app.config['SECRET_KEY']:
        uploaded_file = request.files['sharex']
        if uploaded_file.filename != '':
            allowed, target_filetype_dir = get_file_info(uploaded_file.filename)
            if not allowed:
                return "Invalid file type"

            date_prefix = date.today().strftime(current_app.config['FILE_DATE_FORMAT'])
            upload_directory = os.path.join(current_app.config['UPLOADS_PATH'], target_filetype_dir)
            upload_directory = os.path.join(upload_directory, date_prefix)
            target_name = safe_join(upload_directory, secure_filename(uploaded_file.filename))

            if not os.path.exists(upload_directory):  # If the upload destination doesn't exist, create it
                os.makedirs(upload_directory)

            uploaded_file.save(target_name)
            host = urlparse(request.base_url).hostname

            return os.path.join(host, target_name)

    return "Error uploading"


@uploads.route("/<path:filename>")
def download_file(filename):
    return send_from_directory(
        'uploads', filename, as_attachment=False
    )
