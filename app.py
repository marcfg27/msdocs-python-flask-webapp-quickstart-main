import os

from flask import (Flask, render_template,
                   send_from_directory,request)
from flask_wtf.csrf import  CSRFProtect
from flask_cors import CORS
from flask_restful import Api,reqparse
from flask_limiter import Limiter
from flask_mail import Mail
app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
app.config['SECRET_KEY'] = '1234'
app.config['Admin_Pass'] = '1234'
app.config['SECRET_KEY2'] = '1234'
#app.config['Salt'] = Salt




CORS(app, resources={r'/*': {'origins': '*'}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
api = Api(app)
def get_user():
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="This field cannot be left blanck")
        data = parser.parse_args()
        username = data['username']

        if username:
            request.username = username
            return username
        else:
            return None
    except:
        return None
mail = Mail()
limiter = Limiter(key_func=get_user,storage_uri="memory://", strategy="fixed-window-elastic-expiry")

#migrate = Migrate(app, db)
#db.init_app(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '1234'
app.config['MAIL_PASSWORD'] = '1234'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True


mail.init_app(app)
limiter.init_app(app)
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
