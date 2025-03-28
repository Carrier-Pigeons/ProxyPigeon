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