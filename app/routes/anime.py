from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import logging
from AnimesRecommendation import collaborative_filtering_recommendation
import re
import json
import pandas as pd
from collections import namedtuple
def get_all_animes(mysql, page=1):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        logging.info(f"Fetching all anime on page: {page}")
        
        # Query to get the total number of animes
        cursor.execute('SELECT COUNT(*) as total_count FROM cleaned_anime_data')
        total_count = cursor.fetchone()['total_count'] # class int
        
        # Adjust the query to fetch all anime based on pagination
        cursor.execute('SELECT * FROM cleaned_anime_data LIMIT %s, 10', ((page-1)*10,))
        
        anime_list = cursor.fetchall()
        # print(anime_list)
        print(type(anime_list))
        
        logging.info(f"Number of anime found on current page: {len(anime_list)}")
        
        if anime_list:
            return jsonify({"animes": anime_list, "totalResults": total_count}), 200
        else:
            return jsonify({"msg": "No anime found!"}), 404
    except Exception as e:
        logging.error(f"Error fetching anime: {str(e)}")
        return jsonify({"msg": "Internal server error"}), 500
    
def get_recommend_animes(mysql, username='username'):
    
    sql_query = """
        select Title from cleaned_anime_data where Anime_id = (
        select anime_id from ratings where account_id = (
        SELECT id FROM accounts WHERE username=%s) order by scores desc limit 1);
        """
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql_query, (username,))
    anime_title = cursor.fetchone()
    print(">>>>>>>>>> user fav movie is ", anime_title['Title'])
    result_df = collaborative_filtering_recommendation.get_recommendation(anime_title['Title'])
    # print(BLUE, res, RESET)
    if not isinstance(result_df, pd.DataFrame) or len(result_df) == 0:
        print(">>>>>>>>>>>> getting null recommendation")
        return get_all_animes(mysql, page=1)
    else:
        result_df['poster'] = 'https://github.githubassets.com/images/modules/logos_page/GitHub-Logo.png'
        result_df['soup'] = 'soup'
        result_df['Synopsis'] = 'Synopsis'
        print(result_df.columns)
        anime_id_list = result_df['Anime_id'].tolist()
        placeholders = ', '.join(['%s'] * len(anime_id_list))
        query = f"SELECT * FROM cleaned_anime_data WHERE Anime_id IN ({placeholders})"
        values = (tuple(anime_id_list),)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, anime_id_list)
        # result_dict = result_df.to_dict(orient='records')
        total_count = len(result_df)
        result = cursor.fetchall()
        query2 = f"SELECT COUNT(*) as total_count FROM cleaned_anime_data WHERE Anime_id IN ({placeholders})"
        cursor.execute(query2, anime_id_list)
        total_count = cursor.fetchone()['total_count'] # class int
        print(type (total_count))
        json_response = jsonify({"animes": result, "totalResults": total_count})

        return json_response, 200


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
