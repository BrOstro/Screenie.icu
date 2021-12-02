import logging
import os
from datetime import datetime, date

from flask import Blueprint, request, current_app, send_from_directory, abort
from google.cloud import storage, vision
from werkzeug.security import safe_join
from werkzeug.utils import secure_filename

uploads = Blueprint('uploads', __name__)


def get_file_info(filename):
    extension = filename.rsplit('.', 1)[1].lower()
    file_allowed = False
    is_image = False
    target_directory = "."

    if current_app.config['ALLOW_IMAGES'] and extension in current_app.config['ALLOWED_IMAGES']:
        file_allowed = True
        is_image = True
        target_directory = current_app.config['IMAGE_PATH']
    elif current_app.config['ALLOW_VIDEOS'] and extension in current_app.config['ALLOWED_VIDEOS']:
        file_allowed = True
        target_directory = current_app.config['VIDEO_PATH']
    elif current_app.config['ALLOW_FILES'] and extension in current_app.config['ALLOWED_FILES']:
        file_allowed = True
        target_directory = current_app.config['FILE_PATH']

    return '.' in filename and file_allowed, target_directory, is_image


@uploads.route("/upload", methods=['POST'])
def upload():
    if request.form.to_dict(flat=False)['secret'][0] == current_app.config['SECRET_KEY']:
        uploaded_file = request.files['sharex']
        if uploaded_file.filename != '':
            allowed, target_filetype_dir, is_image = get_file_info(uploaded_file.filename)
            logging.warning("Upload file name: " + str(uploaded_file.filename))
            if not allowed:
                return "Invalid file type"

            image_content = uploaded_file.read()
            gcs = storage.Client()

            bucket = gcs.get_bucket(current_app.config['CLOUD_STORAGE_BUCKET'])

            date_prefix = date.today().strftime(current_app.config['FILE_DATE_FORMAT'])
            upload_directory = os.path.join(current_app.config['UPLOADS_PATH'], target_filetype_dir)
            upload_directory = os.path.join(upload_directory, date_prefix)
            target_name = safe_join(upload_directory, secure_filename(uploaded_file.filename)).replace('\\', '/')

            metadata = {'Creation': int(datetime.utcnow().timestamp()), 'Text': '', 'Labels': ''}

            if is_image and current_app.config['ENABLE_OCR']:
                ocr_client = vision.ImageAnnotatorClient()
                ocr_image = vision.Image(content=image_content)
                text_response = ocr_client.text_detection(image=ocr_image).text_annotations
                label_response = ocr_client.label_detection(image=ocr_image).label_annotations

                if len(text_response) > 0:
                    text = text_response[0].description
                    metadata['Text'] = text

                if len(label_response) > 0:
                    for label in label_response:
                        metadata['Labels'] += label.description + " "

            blob = bucket.blob(target_name)
            blob.metadata = metadata
            blob.upload_from_string(
                image_content,
                content_type=uploaded_file.content_type
            )
            blob.make_public()
            blob.patch()

            return blob.public_url

    return "Error uploading"


@uploads.route("/<path:filename>")
def download_file(filename):
    allowed, directory, is_image = get_file_info(filename)
    if not allowed:
        return abort(401)

    return send_from_directory(
        'uploads', filename, as_attachment=False
    )
