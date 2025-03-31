# Place in the same directory as app.py
 
workers = 3
bind = '0.0.0.0:5000'
timeout = 120
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'