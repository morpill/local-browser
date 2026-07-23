from flask import Flask, render_template, abort
from config import config

app = Flask(__name__)

@app.route('/')
def index_ep():
    return render_template('browser.html', proxy_port=config.get('PROXY_PORT'))