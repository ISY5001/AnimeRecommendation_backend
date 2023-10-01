from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import json

# import sys
# sys.path.append("/home/hewen/ISS-workshop/MVP/AnimeRecommendation_backend/app")

# app = Flask(__name__)
# static_path = "app/UI/static/"
# template_path = "app/UI/templates/"
# tmp_path = "/home/hewen/ISS-workshop/MVP/AnimeRecommendation_backend/app/UI/templates/"


# app.secret_key = 'your secret key'

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'dev'
# app.config['MYSQL_PASSWORD'] = 'dev'
# app.config['MYSQL_DB'] = 'user_data'

# mysql = MySQL(app)

def login(mysql):
    if request.method == 'POST':
        data = request.get_json()
        if data and 'username' in data and 'password' in data:
            username = data['username']
            password = data['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                return jsonify({"msg": "success"}), 200
            else:
                return jsonify({"msg" :"Incorrect username / password!"}), 400
        else:
            return jsonify({"msg": "Please provide a username and password!"}), 400
    elif request.method == 'OPTIONS':
        # Handle CORS preflight request
        response = jsonify({"msg": "CORS preflight successful"})
        response.status_code = 200
        response.headers["Access-Control-Allow-Methods"] = "POST"  # Allow POST requests
        return response
    else:
        return jsonify({"msg": "Invalid request method!"}), 400

def register(mysql):
    if request.method == 'POST':
        data = request.get_json()
        if data and "username" in data and "password" in data and "email" in data:
            username = data["username"]
            password = data["password"] 
            email = data["email"]

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Check if the username already exists
            cursor.execute("SELECT * FROM accounts WHERE username = %s", (username,))
            account = cursor.fetchone()

            if account:
                return jsonify({"msg": "Account already exists!"}), 400

            # Add more validation checks here if needed (e.g., password requirements)

            # Insert the new user into the database
            cursor.execute("INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
            mysql.connection.commit()

            return jsonify({"msg": "success"}), 200
        else:
            return jsonify({"msg": "Please provide a username and password!"}), 400
    elif request.method == 'OPTIONS':
        # Handle CORS preflight request
        response = jsonify({"msg": "CORS preflight successful"})
        response.status_code = 200
        response.headers["Access-Control-Allow-Methods"] = "POST"  # Allow POST requests
        return response
    else:
        return jsonify({"msg": "Invalid request method!"}), 400
    
def logout(mysql):
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))


# def register(mysql):
# 	msg = ''
# 	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
# 		username = request.form['username']
# 		password = request.form['password']
# 		email = request.form['email']
# 		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# 		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
# 		account = cursor.fetchone()
# 		if account:
# 			msg = 'Account already exists !'
# 		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
# 			msg = 'Invalid email address !'
# 		elif not re.match(r'[A-Za-z0-9]+', username):
# 			msg = 'Username must contain only characters and numbers !'
# 		elif not username or not password or not email:
# 			msg = 'Please fill out the form !'
# 		else:
# 			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
# 			mysql.connection.commit()
# 			msg = 'You have successfully registered !'
# 	elif request.method == 'POST':
# 		msg = 'Please fill out the form !'
# 	return render_template('register.html', msg = msg)



# Example usage:
# access_token, refresh_token = login("1234567890", "hashed_password")
# result = logout()
# result = signup("new_user", "new_password")
