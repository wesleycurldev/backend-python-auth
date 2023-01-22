from jwt import encode

from flask import Flask, make_response, request
from flask_cors import CORS

from werkzeug.security import check_password_hash
from datetime import datetime, timedelta

from models.db import db
from repositories.users import UserRepository, UserService, UserDto

from wraps.token import token_required

from dotenv import load_dotenv
from os import environ

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.app_context().push()

@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    
    if auth and 'username' in auth and 'password' in auth:
        repository = UserRepository()
        service = UserService(repository)
        user_dto = UserDto(
            username=auth["username"],
            password=auth["password"]
        )

        user = service.get_user_by_username(user_dto)
        """
            Obs: a senha que está salva para o usuário maistodos foi gerada no padrão pbkdf2:sha256:1000,
            isso significa que para criar o hash foram feito 1000 iterações, por padrão se não for passado o
            :1000 a senha é criada com 50000 iterações influenciando significativamente na performance da rota de login,
            logo temos um trade off por que diminuindo o número de iterações a senha fica menos segura. Para um sistema
            produtivo poderíamos chegar em um meio-termo.
        """
        if user:
            if check_password_hash(user.password, auth["password"]):
                data = {'user': auth["username"], 'exp': datetime.utcnow() + timedelta(minutes=90)}
                token = encode(data, app.config['SECRET_KEY']) 
                return {'token': token}
        
        return make_response('Username or password is wrong', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return make_response('Username and Password is required', 400, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/api/cashback', methods=['POST'])
@token_required
def cashback():
    # repository = BookingRepository()
    # manager = BookingManager(repository)
    # user_dto = UserDto(session['current_user']['user'], session['current_user']['is_admin'])

    # bookings = manager.get_bookings(user_dto)
    return "teste"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)