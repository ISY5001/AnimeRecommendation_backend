from flask import request, redirect, url_for, session, jsonify
import MySQLdb.cursors

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
                session['password'] = account['password']
                return jsonify({"msg": "success", "account_id": session['id'], "username": session['username'],"password": session['password']}), 200

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

def get_userid_from_db(mysql):
    # Retrieve the username and password from the query parameters
    username = request.args.get('username')
    password = request.args.get('password')

    if username and password:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['password'] = account['password']
            return jsonify({"msg": "success", "account_id": session['id'], "username": session['username'], "password": session['password']}), 200
        else:
            return jsonify({"msg": "Incorrect username / password!"}), 400

    else:
        return jsonify({"msg": "Please provide a username and password!"}), 400



'''
def get_userid_from_db(mysql):
    if request.method == 'GET':
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
                return jsonify({"account_id": session['id']}), 200

            else:
                return jsonify({"msg": "Incorrect username / password!"}), 400
        else:
            return jsonify({"msg": "Please provide a username and password!"}), 400
    elif request.method == 'OPTIONS':
        response = jsonify({"msg": "CORS preflight successful"})
        response.status_code = 200
        response.headers["Access-Control-Allow-Methods"] = "POST"
        return response
    else:
        return jsonify({"msg": "Invalid request method!"}), 400
'''
