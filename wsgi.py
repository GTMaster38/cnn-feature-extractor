# WSGI configuration file for production deployment
# This file is used by Gunicorn or uWSGI to serve the Flask application

from app import app

if __name__ == "__main__":
    app.run()
