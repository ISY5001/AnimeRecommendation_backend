from flask import Flask, request, jsonify,send_from_directory
from flask_cors import CORS, cross_origin
import os

from routes import users
from routes import rating
from routes import anime
from routes import animeGan
from routes import aniverse
from config import mysql
from routes import chatbot

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'content-type'
app_config = mysql.load_config()
mysql = mysql.configure_mysql(app, app_config['mysql'])


@app.route('/chatbot', methods=["OPTIONS","GET","POST"])
def chatbotreply():
    return chatbot.reply()  

@app.route('/')
@app.route("/register", methods=["OPTIONS","GET","POST"])
def register():
    return users.register(mysql)

@app.route("/login", methods=["OPTIONS","GET","POST"])
def login():
    return users.login(mysql)
  
@app.route("/logout")
def logout():
    return users.logout(mysql)

@app.route('/get_avatar/<account_id>', methods=['GET'])
def get_avatar(account_id):
    print('getting avatar')
    return users.get_avatar(mysql,account_id)

@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    print('uploading')
    return users.upload_avatar(mysql)
  
# detail page of a anime
@app.route('/detail', methods=['GET'])
def get_detial():
    animeid = int(request.args.get('animeid', 1))
    return anime.get_anime_detail(mysql, animeid)
#Anime fetch from database
@app.route('/anime', methods=['GET'])
def fetch_anime():
    page = int(request.args.get('page', 1))
    return anime.get_all_animes(mysql, page)

# Recommend Animes 
@app.route('/recommend', methods=['GET', 'POST']) 
def recommend_anime():
    username = request.args.get('username')
    print(username)
    animeId = request.args.get('animeid', -1,type=int)
    if username is None and animeId == -1:
        return anime.get_all_animes(mysql, page=1)
    elif username is not None and animeId == -1:
        return anime.get_recommend_animes(mysql, username)
    elif username is None and animeId != -1:
        return anime.get_recommend_animes_by_anime_id(mysql, animeId)
        # return jsonify({"animeid": animeId}), 200
    else:
        return anime.get_all_animes(mysql, page=1)

@app.route('/get_userid', methods=['GET','POST'])
def get_userid_endpoint():
    return users.get_userid_from_db(mysql)

@app.route('/rating/fetch_ratings/<account_id>/<anime_id>', methods=['GET'])
def get_user_ratings(account_id, anime_id):
    return rating.fetch_user_ratings(mysql, account_id, anime_id)

@app.route('/rating/upload_ratings', methods=['POST'])
def rate_anime():
    return rating.upload_user_ratings(mysql)

@app.route('/rating/nonzero_rating/<account_id>', methods=['GET'])
def nonzero(account_id):
    return rating.fetch_nonzero_ratings(mysql, account_id)

@app.route('/Anyani/upload_image', methods=['POST'])
def upload_image():
    print("\033[1;35m Received :", request.form['style'],request.files['image'],"\033[0m")
    return animeGan.handle_animeGan()

@app.route('/Anyani/upload_image_aniverse', methods=['POST'])
def upload_image_aniverse():
    return aniverse.handle_animeGan()

@app.route('/content/outputs/<filename>', methods=['GET'])
def get_output_image(filename):
    OUTPUT_FOLDER = os.path.join(os.getcwd(), 'app/data/content/outputs/')
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    # load()
    #for rule in app.url_map.iter_rules():
        #print(f'{rule} allows methods: {", ".join(rule.methods)}')
    app.run(host='0.0.0.0', port=8282)