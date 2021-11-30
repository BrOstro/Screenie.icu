from flask import Flask

from blueprints.uploads.upload import uploads
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(uploads, url_prefix='/uploads')

if __name__ == '__main__':
    app.run()
