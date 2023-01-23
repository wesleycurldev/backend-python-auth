from jwt import decode, ExpiredSignatureError

from flask import make_response, request, session
from functools import wraps
from dotenv import load_dotenv
from os import environ

load_dotenv()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            
            try:
                data = decode(token, environ.get("SECRET_KEY"), algorithms=["HS256"])
                session['current_user'] = {'user': data['user']}
            except ExpiredSignatureError:
                return make_response('Signature has expired', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
            except Exception:
                return make_response('Invalid token', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
            
            return f(*args, **kwargs)
        else:
            return make_response('Authorization is required in the header', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return decorated