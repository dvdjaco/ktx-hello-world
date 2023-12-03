# hello_world
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    image_tag = os.environ.get('IMAGE_TAG', 'No tag availabe')
    hello_world = "Kubeops :: Hello, world! :: " + image_tag
    return hello_world

@app.route('/health')
def healthcheck():
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

