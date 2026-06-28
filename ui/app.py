from flask import Flask, render_template, abort

app = Flask(__name__)

@app.route('/')
def index_ep():
    return render_template('browser.html')