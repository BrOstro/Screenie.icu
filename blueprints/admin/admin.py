from datetime import datetime

import pytz
from flask import Blueprint, current_app, render_template
from google.cloud import storage

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route("/")
def admin_panel():
    gcs = storage.Client()

    bucket = gcs.get_bucket(current_app.config['CLOUD_STORAGE_BUCKET'])
    blobs = list(bucket.list_blobs(prefix="uploads"))
    images = []

    for blob in blobs:
        img_timestamp = int(blob.metadata['Creation'])
        img_time = datetime.fromtimestamp(img_timestamp, tz=pytz.timezone(current_app.config['LOCAL_TIMEZONE'])).strftime(current_app.config['TIMESTAMP_FORMAT'])
        img_info = {'URL': str(blob.public_url), 'time': img_time, 'text': str(blob.metadata['Text'])}
        images.append(img_info)

    return render_template('gallery.html', title='Home', images=images)
