from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import bcolors
import sys
sys.path.append("/Users/chenzhiwei/Downloads/AnimeRecommendation_backend/app/routes")
from printcolor import RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, RESET

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
from routes import rating
from routes import anime
from config import mysql
from routes import chatbot

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


@app.route('/chatbot', methods=["OPTIONS","GET","POST"])
def chatbotreply():
    return chatbot.reply()  
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

#Anime fetch from database
@app.route('/fetchAnimes', methods=['GET'])
def fetch_anime():
    print(BLUE, "into function", RESET)
    page = int(request.args.get('page', 1))
    print(BLUE, "[I] page =", page, RESET)
    return anime.get_all_animes(mysql, page)
#Anime fetch from database
# @app.route('/anime', methods=['GET'])
# def fetch_anime2():
#     page = int(request.args.get('page', 1))
#     print(BLUE, "[I] page =", page, RESET)
#     return anime.get_all_animes(mysql, page)



#@app.route('/getAnime', methods=['GET'])
#def fetch_anime_by_keyword():
#    keyword = request.args.get('keyword', 'One Piece')
#    page = int(request.args.get('page', 1))
#    return get_anime_by_keyword(mysql, keyword, page)

#using ID
#@app.route('/getAnimeByID', methods=['GET'])
#def fetch_anime_by_id():
 #   anime_id = request.args.get('id')
 #   if not anime_id:
 #       return jsonify({"msg": "Please provide an Anime ID!"}), 400
  #  return get_anime_by_id(mysql, anime_id)



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
    for rule in app.url_map.iter_rules():
        print(f'{rule} allows methods: {", ".join(rule.methods)}')
    app.run(host='0.0.0.0', port=8282)
