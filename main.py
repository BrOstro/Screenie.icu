import google
from flask import Flask

from blueprints.admin.admin import admin
from blueprints.uploads.upload import uploads
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(uploads, url_prefix='/uploads')
app.register_blueprint(admin, url_prefix='/admin')

if __name__ == '__main__':
    client = google.cloud.logging.Client()
    client.setup_logging()
    app.run()
