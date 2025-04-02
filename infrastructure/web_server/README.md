# Web Server Setup Instructions

We used an Ubuntu 24.01 virtual machine running on Proxmox VE 8.2, which is installed on a Dell PowerEdge R630 (ST: C84SR52). The latest version of Apache installed from the package manager should work fine. 

## DNS

Create a DNS A record that points to the public IP of the server you've set up. For our project we're using `fingerprint.byu.edu`, which points to `128.187.49.100`.

## Install Apache 

```
sudo apt install apache2
```

## Basic Apache Security

Remove `Indexes` from the `apache2.conf` file. 

## Set up HTTPS

You will first need an SSL certificate for the domain the web server will be running under. You can obtain one of these for free from Let's Encrypt. We obtained one for `fingerprint.byu.edu` by sending a CSR to the BYU Networking team. If you are just using a self signed certificate you can skip to the step called "Enable the default ssl configuration".  

After storing the certificate file and the key file on the server, edit `/etc/apache2/sites-available/ssl-default.conf` with the following two lines based on where you stored the files:
```
SSLCertificateFile /your/path/to/domain.crt
SSLCertificateKeyFile /your/path/to/domain.key
```

If a chain file is also needed, edit the following line as well:  
```
SSLCertificateChainFile /your/path/to/CA.crt
```

In our case the three lines look like this:
```
SSLCertificateFile /etc/ssl/certs/fingerprint_byu_edu.crt
SSLCertificateKeyFile /etc/ssl/private/fingerprint_byu_edu.key
SSLCertificateChainFile /etc/apache2/ssl.cert/DigiCertCA.crt
```

Enable the default ssl configuration:  
```
sudo a2ensite default-ssl
```

Enable https on apache:  
```
sudo a2enmod ssl
```

Restart apache to apply changes:
```
sudo systemctl restart apache2
```

## Set Up Header Logging

Please see [mod_http_fingerprint_log](https://github.com/Carrier-Pigeons/mod_http_fingerprint_log) for code and instructions. 

## Install Wordpress And Dependencies

You can find many online tutorials explaining how to set up vanilla Wordpress, but these instructions should get you started. 

The following command can be used to install the Wordpress dependencies:  
```
sudo apt install ghostscript \
                 libapache2-mod-php \
                 mysql-server \
                 php \
                 php-bcmath \
                 php-curl \
                 php-imagick \
                 php-intl \
                 php-json \
                 php-mbstring \
                 php-mysql \
                 php-xml \
                 php-zip
```

Download the latest version of Wordpress, then unzip it and copy it to `/var/www`:  
```
wget https://wordpress.org/latest.zip

unzip latest.zip

sudo cp wordpress /var/www/
```

Navigate to `/var/www`, then remove the existing html folder, and replace it with a symbolic link to the wordpress folder (210 shoutout):  
```
cd /var/www

sudo rm -rf html

sudo ln -s wordpress html
```

Make the www-data user the owner and group of the files:
```
sudo chgrp -R www-data wordpress

sudo chown -R www-data wordpress
```

Now navigate to your website, and complete the setup from there!

# Proxy Testing Page

We built a custom proxy testing page on Wordpress that makes sending requests to the echo server easily. Start with a basic new Wordpress page, then follow these instructions. 

## Create Links

Add a block of buttons to the page. Create a button for each proxy to be tested, and link said button to the header testing page through the proxy. For example, the mitmproxy button would be linked to https://mitmproxy.httpcarrierpigeons.xyz/header-testing. 

## Create Forms

Create three HTML blocks and insert the following code into them. Using the HTML blocks is essential because Wordpress uses absolute links, but in order to get to the echo server through the proxies you must use relative links. 

### Normal GET Request
```html
<pre><a href="/echo/">Echo Site</a></pre>
```

### Complex GET Request
```html
<form action="/echo/" method="get">

  <label for="zwhyisthatzthere">Any random text here:</label>
  <input type="text" id="zwhyisthatzthere" name="zwhyisthatzthere"><br><br>

  <label for="secondquery">Any random text here (again):</label>
  <input type="text" id="secondquery" name="secondquery"><br><br>

  <label for="thirdquery">Any random text here (again again):</label>
  <input type="text" id="thirdquery" name="thirdquery"><br><br>
  
  <label for="options">Standard dropdown:</label>
  <select id="options" name="options">
    <option value="option1">Option 1</option>
    <option value="option2">Option 2</option>
    <option value="option3">Option 3</option>
  </select><br><br>
  
  <input type="submit" value="Search">
</form>
```

### POST Request
```html
<form action="/echo/" method="post">
  <label for="field1">Field 1:</label>
  <input type="text" id="field1" name="field1"><br><br>
  
  <label for="field2">Field 2:</label>
  <input type="text" id="field2" name="field2"><br><br>
  
  <input type="submit" value="Submit">
</form>
```

# Echo Server

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