from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
# import jwt
# import url
import conf
# import common
# import response
import app

app = Flask(__name__)
CORS(app)

def load():
    c = conf.Config()
    c.routes = [
        "/ping", "/renewal", "/login", "signup",
        "/rating", "/rating/getAll", "/rating/rateAMoive"
    ]
    # c.open_jwt = True;
    conf.set_config(c)
    # handle.init_validate()
# def auth_required(func):
#     @wraps(func)
#     def decorated(*args, **kwargs):
#         if request.path in conf.get_config().routes:
#             return func(*args, **kwargs)

#         if conf.get_config().open_jwt:
#             access_token = request.headers.get("Authorization")
#             if not access_token:
#                 return response.show_error("nologin")

#             try:
#                 ret = app.parse_token(access_token)
#                 uid = str(ret['UserId'])
#                 has = app.check_black(uid, access_token)
#                 if has:
#                     return response.show_error("nologin")
#                 request.uid = ret['UserId']
#             except jwt.ExpiredSignatureError:
#                 return response.show_validator_error("Token expired. Please log in again.")
#             except Exception as e:
#                 return response.show_validator_error(str(e))
#         else:
#             access_token = request.cookies.get(app.COOKIE_TOKEN)
#             if not access_token:
#                 return response.show_error("nologin")
#         return func(*args, **kwargs)

#     return decorated

# register route
@app.route("/renewal", methods=["POST"])
# @auth_required
def renewal():
    # TODO
    pass

@app.route("/logout", methods=["POST"])
# @auth_required
def logout():
    # TODO
    pass

@app.route("/login", methods=["POST"])
def login():
    # TODO
    pass

@app.route("/login/mobile", methods=["POST"])
def login_mobile():
    # TODO
    pass

@app.route("/sendsms", methods=["POST"])
def sendsms():
    # TODO
    pass

@app.route("/signup/mobile", methods=["POST"])
def signup_mobile():
    # TODO
    pass

@app.route("/signup/mobile/exist", methods=["POST"])
def mobile_is_exists():
    # TODO
    pass

@app.route("/rating", methods=["POST"])
# @auth_required
def rating():
    # TODO
    pass

@app.route("/rating/getAll", methods=["POST"])
# @auth_required
def get_all_rating():
    # TODO
    pass

@app.route("/rating/rateAMovie", methods=["POST"])
# @auth_required
def rate_a_movie():
    # TODO
    pass

@app.route("/", methods=["GET"])
def index():
    # TODO
    pass

@app.route("/my/info", methods=["GET"])
# @auth_required
def get_user_info():
    # TODO
    pass

@app.route("/pong", methods=["GET"])
def pong():
    return jsonify({"message": "pong"})

if __name__ == '__main__':
    load()
    app.run(host='0.0.0.0', port=8282)