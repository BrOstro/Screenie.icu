import os


class Config(object):
    # CONFIGURE THESE
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    FILE_DATE_FORMAT = "%Y\\%m\\%d"  # Use https://strftime.org as reference
    # DON'T TOUCH THESE BELOW

    UPLOADS_PATH = "uploads"
