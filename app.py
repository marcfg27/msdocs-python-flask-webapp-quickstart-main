import os

from flask import Flask, request, redirect, send_from_directory
from flask import render_template
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from resources.accounts import Accounts, AccountsList, money
from resources.email import eMail, eMail2, eMail3, mail, limiter2
from resources.login import Login, limiter

from acces_control import require_access
#from flask_sslify import SSLify
from flask_wtf.csrf import  CSRFProtect

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

api.add_resource(Accounts, '/account')
api.add_resource(AccountsList, '/accounts')

api.add_resource(Login, '/login')

api.add_resource(eMail, '/email')
api.add_resource(eMail2, '/email2')
api.add_resource(eMail3, '/email3')

api.add_resource(money,'/money')#/<string:username>
@app.route('/')
def render_vue():
        return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')




if __name__ == '__main__':
   app.run()
