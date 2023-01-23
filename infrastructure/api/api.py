from jwt import encode

from flask import Flask, make_response, request
from flask_cors import CORS

from werkzeug.security import check_password_hash
from datetime import datetime, timedelta

from models.db import db
from repositories.users import UserRepository, UserService, UserDto
from external_requests.cashback_processing import cashback_processing

from wraps.token import token_required

from dotenv import load_dotenv
from os import environ
from flasgger import Swagger

load_dotenv()

app = Flask(__name__) 

Swagger(app)
CORS(app)

app.config['SECRET_KEY'] = environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.app_context().push()

@app.route('/login', methods=['POST'])
def login():
    """Endpoint for authentication.
    ---
    tags:
      - auth
    parameters:
      - name: username
        in: path
        type: string
        required: true
      - name: password
        in: path
        type: string
        required: true
    responses:
      200:
        description: token to access other resources
        schema:
          id: login
          type: object
          properties:
            token:
              type: string
    """
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
    """Endpoint to call cashback processing api.
    ---
    tags:
      - cashback
    parameters:
      - name: sold_at
        in: path
        type: datetime
        required: true
      - name: customer
        in: path
        type: dict
        required: true
      - name: total
        in: path
        type: float
        required: true
      - name: products
        in: path
        type: list
        required: true
    responses:
      200:
        description: cashback processing response
        schema:
          id: Cashback
          type: object
          properties:
            code:
              type: string
            error:
              type: boolean
              default: False
            message:
              type: string
    """
    request_body = request.get_json()
    
    cashback_processing_response = cashback_processing(request_body=request_body)

    return cashback_processing_response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
