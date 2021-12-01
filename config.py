import os


class Config(object):
    # CONFIGURE THESE
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    ENABLE_OCR = True

    FILE_DATE_FORMAT = "%Y\\%m\\%d"  # Use https://strftime.org as reference

    LOCAL_TIMEZONE = "US/Central"
    TIMESTAMP_FORMAT = "%b %m, %Y %I:%M %p"

    ALLOW_IMAGES = True
    ALLOWED_IMAGES = ['png', 'jpg', 'jpeg', 'gif']
    IMAGE_PATH = "images"

    ALLOW_VIDEOS = True
    ALLOWED_VIDEOS = ['mp4', 'webm', 'avi']
    VIDEO_PATH = "videos"

    ALLOW_FILES = True
    ALLOWED_FILES = ['txt', 'pdf']
    FILE_PATH = "files"
    # DON'T TOUCH THESE BELOW

    UPLOADS_PATH = "uploads"
    CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']



