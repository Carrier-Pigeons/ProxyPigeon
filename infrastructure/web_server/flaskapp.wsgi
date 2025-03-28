import sys
import os
from flask import request

sys.path.insert(0, '/var/www/html/echo')

def application(environ, start_response):
    os.environ['HTTP_HEADERS_ALL'] = environ['HTTP_HEADERS_ALL']
    
    from flaskapp import app
    return app(environ, start_response)