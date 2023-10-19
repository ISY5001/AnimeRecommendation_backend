from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import logging
from AnimesRecommendation import collaborative_filtering_recommendation
import re
import json
import pandas as pd
from collections import namedtuple

import requests
import re
import concurrent.futures
from bs4 import BeautifulSoup 

import warnings

warnings.filterwarnings("ignore")

HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/86.0.4240.111 Safari/537.36'
}

# Function to fetch image URL given an anime URL
def get_url_by_link(anime_item):
    if anime_item['Poster'] != 'https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png':
        return 
    try:
        # Send an HTTP GET request to the provided URL
        with requests.Session() as session:
            response = session.get(anime_item['Link'], headers=HEADERS, verify=False)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the image URL using BeautifulSoup (assuming it's in the meta tags)
            img_url = soup.find('meta', property='og:image')['content']
            
            print("img_url", img_url)
            # print(img_url)
            anime_item['Poster'] = img_url
            print(anime_item['Poster'])

    except Exception as e:
        print("[E]", str(e))
        return

# Function to fetch image URLs for all anime items in parallel
def modify_poster_urls(anime_list):
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            list(executor.map(get_url_by_link, anime_list))
    except Exception as e:
        print("[E]", str(e))
        return

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

        # fetch poster urls and write back to sql
        modify_poster_urls(anime_list)
        # write back to sql if modified success
        update_query = "UPDATE cleaned_anime_data SET Poster = %s WHERE Anime_id = %s"
        # Loop through the anime_list and execute the update query for each record

        for anime in anime_list:
            poster_url = anime['Poster']
            anime_id = anime['Anime_id']  # Assuming 'id' is the unique identifier for each anime
            cursor.execute(update_query, (poster_url, anime_id))
        mysql.connection.commit()
        print("executed success!")

        logging.info(f"Number of anime found on current page: {len(anime_list)}")
        
        if anime_list:
            return jsonify({"animes": anime_list, "totalResults": total_count}), 200
        else:
            return jsonify({"msg": "No anime found!"}), 404
    except Exception as e:
        logging.error(f"Error fetching anime: {str(e)}")
        return jsonify({"msg": "Internal server error"}), 500
    
def get_recommend_animes(mysql, username='username'):
    # get the highest score anime that user has scored
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
        # result_df['poster'] = 'https://github.githubassets.com/images/modules/logos_page/GitHub-Logo.png'
        # result_df['soup'] = 'soup'
        # result_df['Synopsis'] = 'Synopsis'
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

        anime_list = result 
        # fetch poster urls and write back to sql
        modify_poster_urls(anime_list)
        # write back to sql if modified success
        update_query = "UPDATE cleaned_anime_data SET Poster = %s WHERE Anime_id = %s"
        # Loop through the anime_list and execute the update query for each record
        for anime in anime_list:
            poster_url = anime['Poster']
            anime_id = anime['Anime_id']  # Assuming 'id' is the unique identifier for each anime
            cursor.execute(update_query, (poster_url, anime_id))
        mysql.connection.commit()
        print("executed success!")


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
