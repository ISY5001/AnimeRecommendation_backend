from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import json

def fetch_user_ratings(mysql, username):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM ratings WHERE username = %s', (username,))
    user_ratings = cursor.fetchall()
    if user_ratings:
        return jsonify(user_ratings), 200
    else:
        return jsonify({"msg": "No ratings found for this user!"}), 404
    

def upload_user_ratings(mysql):
    if request.method == 'POST':
        data = request.get_json()
        if data and 'username' in data and 'anime_id' in data and 'scores' in data:
            username = data['username']
            anime_id = data['anime_id']
            scores = data['scores']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            
            # Check if the rating already exists for the anime by the user
            cursor.execute('SELECT * FROM ratings WHERE username = %s AND anime_id = %s', (username, anime_id))
            existing_rating = cursor.fetchone()

            if existing_rating:
                # Update existing rating
                cursor.execute('UPDATE ratings SET scores = %s WHERE username = %s AND anime_id = %s', (scores, username, anime_id))
            else:
                # Insert new rating
                cursor.execute('INSERT INTO ratings (username, scores, anime_id) VALUES (%s, %s, %s)', (username, scores, anime_id))
            
            mysql.connection.commit()
            return jsonify({"msg": "Rating updated successfully!"}), 200
        else:
            return jsonify({"msg": "Please provide all required data (username, anime_id, scores)!"}), 400
    elif request.method == 'OPTIONS':
        # Handle CORS preflight request
        response = jsonify({"msg": "CORS preflight successful"})
        response.status_code = 200
        response.headers["Access-Control-Allow-Methods"] = "POST"  # Allow POST requests
        return response
    else:
        return jsonify({"msg": "Invalid request method!"}), 400

