from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import logging
import bcolors
import re
import json

def get_all_animes(mysql, page=1):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        logging.info(f"Fetching all anime on page: {page}")
        
        # Adjust the query to fetch all anime
        # cursor.execute('SELECT * FROM cleaned_anime_data LIMIT %s, 10', ((page-1)*10,))
        cursor.execute('SELECT * FROM anime LIMIT %s, 10', ((page-1)*10,))
        
        anime_list = cursor.fetchall()
        logging.info(f"Number of anime found: {len(anime_list)}")
        print(bcolors.BLUE + "Number of anime found:", len(anime_list))
        if anime_list:
            return jsonify({"animes": anime_list}), 200
        else:
            return jsonify({"msg": "No anime found!"}), 404
    except Exception as e:
        logging.error(f"Error fetching anime: {str(e)}")
        return jsonify({"msg": "Internal server error"}), 500

'''
def get_anime_by_keyword(mysql, keyword, page=1, limit=10):
    offset = (page - 1) * limit
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM cleaned_anime_data WHERE Title LIKE %s LIMIT %s OFFSET %s', ('%' + keyword + '%', limit, offset))
    results = cursor.fetchall()
    return jsonify(results)

def get_anime_by_id(mysql, anime_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM cleaned_anime_data WHERE Anime_id = %s', (anime_id,))
    result = cursor.fetchone()
    if result:
        return jsonify(result)
    else:
        return jsonify({"msg": "Anime not found!"}), 404
'''
