from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import bcolors
# from flask_cors import CORS
# from functools import wraps
# import jwt
# import url
# import conf
# import common
# import response
# import app

# import sys
# sys.path.append("/home/hewen/ISS-workshop/MVP/AnimeRecommendation_backend/app")


from routes import users
from config import mysql

# app = Flask(__name__)
# app = Flask(__name__, template_folder="static/templates")  # Update the template_folder path
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'content-type'
mysql = mysql.configure_mysql(app)

# def load():
#     c = conf.Config()
#     c.routes = [
#         "/ping", "/renewal", "/login", "signup",
#         "/rating", "/rating/getAll", "/rating/rateAMoive"
#     ]
#     # c.open_jwt = True;
#     conf.set_config(c)


@app.route('/')
@app.route("/register", methods=["OPTIONS", "GET", "POST"])
def register():
    return users.register(mysql)


@app.route("/login", methods=["OPTIONS", "GET", "POST"])
def login():
    return users.login(mysql)

# recommend route


@app.route('/recommend',  methods=["OPTIONS", "GET", "POST"])
def getRecommendation():
    if request.method == "POST":
        # Get the data from the request's JSON body
        data = request.get_json()

        # Extract the username from the data
        username = data.get('username', '')

        print(bcolors.BLUE + "getting recommendations...")
        print(bcolors.BLUE + username)

        # Handle the recommendation logic here
        # ...

        return "return from flask route /recommend"
    else:
        return "GET request not supported"


@app.route("/logout")
# @auth_required
def logout():
    return users.logout(mysql)
# @app.route("/my/info", methods=["GET"])
# # @auth_required
# def get_user_info():
#     # TODO
#     pass

# TODO
# @app.route("/rating", methods=["POST"])
# # @auth_required
# def rating():
#     # TODO
#     pass

# @app.route("/rating/getAll", methods=["POST"])
# # @auth_requiredshu
# def get_all_rating():
#     # TODO
#     pass

# @app.route("/rating/rateAMovie", methods=["POST"])
# # @auth_required
# def rate_a_movie():
#     # TODO
#     pass


if __name__ == '__main__':
    # load()
    app.run(host='0.0.0.0', port=8282)
