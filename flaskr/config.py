import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# ? IMPLEMENTED DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://Fasunle@localhost:5432/fyyurapp'
SQLALCHEMY_TRACK_MODFICATIONS = False
