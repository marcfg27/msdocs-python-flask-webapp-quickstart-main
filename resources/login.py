import hashlib
import hmac
import logging
import secrets
import string
from functools import wraps
from LogManager import LoginLog
from flask import jsonify, make_response, current_app
from flask import request
from flask_limiter import Limiter, RateLimitExceeded
from flask_restful import Resource, reqparse
from markupsafe import escape
from unidecode import unidecode

from acces_control import generate_auth_token
from lock import lock
from models.accounts import AccountsModel

#logging.basicConfig(filename='failed_attempts.log', level=logging.INFO)
#failed_attempts = {}

# mostrar missatges per consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger('').addHandler(console_handler)


'''def get_remote_address():
    if request.headers.getlist("X-Forwarded-For"):
        ip_address = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip_address = request.remote_addr
    return ip_address
    
'''



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

limiter = Limiter(key_func=get_user,storage_uri="memory://", strategy="fixed-window-elastic-expiry")



def catch_exceptions(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except RateLimitExceeded as e:
            LoginLog.login_limit_caller(request.username, request)
            #logging.warning('Rate limit exceeded for username %s in address %s', request.username, request.remote_addr)
            return {'message': str(e)}, 429
        except Exception as e:
            logging.error('Unexpected error during login: %s', e)
            response = jsonify({"message": "An unexpected error occurred during login"})
            response.status_code = 500
            return response
    return wrapper


class Login(Resource):

    def post(self):
        try:
            with lock.lock:
                return {'message': "hello"}, 200

        except Exception as e:
            logging.error('Unexpected error during login: %s', e)
            response = jsonify({"message": "An unexpected error occurred during login"})
            response.status_code = 500
            return response



    def options(self):
        response = make_response()
        r = request
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response


