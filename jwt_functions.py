import requests
import jwt
import datetime
import config
import jwt_token


def create_jwt():
    data_jwt = {"email": config.email, "password": config.password}
    jwt_object = requests.post(config.url_jwt, json=data_jwt)
    token = jwt_object.json()["jwt_token"]
    return token


def has_token_expired():
    token_time = datetime.datetime.fromtimestamp(int(jwt_token.timestamp))
    return token_time < datetime.datetime.now()


def write_jwt(token):
    decoded_token = jwt.decode(token, verify=False)
    expiration = str(decoded_token["exp"])
    file = open("/Users/esko/Documents/invoice_reports/jwt_token.py", "w")
    file.write('timestamp = "' + expiration + '"\n')
    file.write('jwt = "' + token + '"\n')
    file.close()
