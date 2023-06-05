import os

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
from flask_wtf.csrf import  CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'

csrf = CSRFProtect(app)

@app.route('/')
def render_vue():
        return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')




if __name__ == '__main__':
   app.run()
