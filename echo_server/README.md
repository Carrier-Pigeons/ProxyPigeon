# Instructions For Setting Up The Echo Server

The echo server runs in a Flask app that is served by WSGI through Apache. Because both WSGI and Flask modify the HTTP requests that pass through them, we created an Apache variable with the original headers that the Flask app can access. We also configured the site to respond to HTTP & HTTPS to better support a wide number of proxies. 

## Enable WSGI
 
Run the following command to enable WSGI: `sudo a2enmod wsgi`

## Create the Apache Variable

TODO: Get Todd to do this

## Create the Flask Server

Create a new directory in the root html folder of the website called echo.  

` mkdir echo && cd echo `

Create two files in that directory: `flaskapp.py` & `flaskapp.wsgi`. 

flaskapp.py:
```
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST']) 
def hello_world():
    headers = os.environ.get('HTTP_HEADERS_ALL')
    combo_string = "<html><body><pre>" + headers + "</pre></body></html>"
    return combo_string

if __name__ == '__main__':
   app.run()
```

flaskapp.wsgi:
```
import sys
import os
from flask import request

sys.path.insert(0, '/var/www/html/echo')

def application(environ, start_response):
    os.environ['HTTP_HEADERS_ALL'] = environ['HTTP_HEADERS_ALL']
    
    from flaskapp import app
    return app(environ, start_response)
```

Both files can be found in this directory. 

## Edit the Apache Config

Add the following lines to the default Apache config:  
```
WSGIScriptAlias /echo /var/www/html/echo/flaskapp.wsgi

<Directory /var/www/html/echo>
        SSLOptions +StdEnvVars
                WSGIProcessGroup flaskapp
                WSGIApplicationGroup %{GLOBAL}
                Order deny,allow
                Allow from all
                Options +ExecCGI
</Directory>
```

Add the following lines to the default Apache SSL config:
```
WSGIDaemonProcess flaskapp threads=5
WSGIScriptAlias /echo /var/www/html/echo/flaskapp.wsgi	

<Directory /var/www/html/echo>
        SSLOptions +StdEnvVars
            WSGIProcessGroup flaskapp
            WSGIApplicationGroup %{GLOBAL}
            Order deny,allow
            Allow from all
        Options +ExecCGI
</Directory>
```

Examples of both config files can be found in this directory. 

## Reload & Restart Apache

`sudo systemctl reload apache2 && sudo systemctl restart apache2`

That's it! Your echo server is ready to go. Try it out by visiting https://your.website/echo. 