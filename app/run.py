from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin


from routes import users
from routes import rating
from routes import anime
from config import mysql
#from routes import chatbot

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'content-type'
app_config = mysql.load_config()
mysql = mysql.configure_mysql(app, app_config['mysql'])

'''
@app.route('/chatbot', methods=["OPTIONS","GET","POST"])
def chatbotreply():
    return chatbot.reply()  
'''
@app.route('/')
@app.route("/register", methods=["OPTIONS","GET","POST"])
def register():
    return users.register(mysql)

@app.route("/login", methods=["OPTIONS","GET","POST"])
def login():
    return users.login(mysql)

#Anime fetch from database
@app.route('/anime', methods=['GET'])
def fetch_anime():
    page = int(request.args.get('page', 1))
    return anime.get_all_animes(mysql, page)

@app.route('/get_userid', methods=['GET','POST'])
def get_userid_endpoint():
    response = users.get_userid_from_db(mysql)
    print(response)
    return response

@app.route('/rating/fetch_ratings/<account_id>/<anime_id>', methods=['GET'])
def get_user_ratings(account_id, anime_id):
    print('ac'+account_id)
    print('an'+anime_id)
    return rating.fetch_user_ratings(mysql, account_id, anime_id)

@app.route('/rating/upload_ratings', methods=['POST'])
def rate_anime():
    print('upload score')
    return rating.upload_user_ratings(mysql)

@app.route('/rating/nonzero_rating/<account_id>', methods=['GET'])
def nonzero(account_id):
    return rating.fetch_nonzero_ratings(mysql, account_id)
  
if __name__ == '__main__':
    # load()
    for rule in app.url_map.iter_rules():
        print(f'{rule} allows methods: {", ".join(rule.methods)}')
    app.run(host='0.0.0.0', port=8282)