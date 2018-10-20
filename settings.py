import os
from os.path import join, dirname
from dotenv import load_dotenv

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')

# Load file from the path.
load_dotenv(dotenv_path)

# Accessing variables
# status = os.getenv('STATUS')
# secret_key = os.getenv('SECRET_KEY')


def get_keys(key):
    if key == "EDMAM_ID":
        return os.getenv(key)
    elif key == "EDMAM_KEY":
        return os.getenv(key)
    elif key == 'YOUTUBE_KEY':
        return os.getenv(key)
    else:
        print("KEY ACCESS ERROR ")
        return -1
