from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import logging
import bcolors
import re
import json
import sys
import requests
sys.path.append("/Users/chenzhiwei/Downloads/AnimeRecommendation_backend/app/routes")
from printcolor import RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, RESET
import warnings
warnings.filterwarnings("ignore")
import requests
import re
import concurrent.futures
from bs4 import BeautifulSoup  # You may need to install this package

# API_URL = "https://www.omdbapi.com/"
# API_KEY = "f9bfc5b4"
HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/86.0.4240.111 Safari/537.36'
}

# Function to fetch image URL given an anime URL
def get_url_by_link(anime_url):
    try:
        # Send an HTTP GET request to the provided URL
        with requests.Session() as session:
            response = session.get(anime_url, headers=HEADERS, verify=False)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the image URL using BeautifulSoup (assuming it's in the meta tags)
            img_url = soup.find('meta', property='og:image')['content']
            
            return img_url

    except Exception as e:
        print("[E]", str(e))
        return None

# Function to fetch image URLs for all anime items in parallel
def fetch_image_urls(anime_list):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Create a list of URLs to fetch in parallel
        anime_urls = [anime_item["Link"] for anime_item in anime_list]
        
        # Fetch image URLs in parallel
        image_urls = list(executor.map(get_url_by_link, anime_urls))
        
        # Update the anime_list with image URLs
        for anime_item, img_url in zip(anime_list, image_urls):
            anime_item["poster"] = img_url

    return anime_list

# Your existing get_all_animes function
def get_all_animes(mysql, page=1):
    # ... (Your existing code)
    print(BLUE, "[I] page =", page, RESET)
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM anime where poster is not null limit %s,%s;', ((page-1)*10,10))
        anime_list = cursor.fetchall()
        print(BLUE, "[I] Number of anime found: ", len(anime_list), RESET)
        if anime_list:
            # Fetch image URLs in parallel
            anime_list = fetch_image_urls(anime_list)
            json_response = json.dumps({"Search": anime_list, "totalResults": str(len(anime_list)), "Response": "True"}, indent=2)
            return json_response, 200
        else:
            return jsonify({"msg": "No anime found!"}), 404
    except Exception as e:
        print(RED, "[E] Error fetching anime", str(e), RESET)
        return jsonify({"msg": "Internal server error"}), 500

# API_URL = "https://www.omdbapi.com/"
# # API_URL = "img.omdbapi.com/"
# API_KEY = "f9bfc5b4"
# headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
# def get_url_by_link(anime_url):
#     try:
#         # Send an HTTP GET request to the provided URL
#         response = requests.get(anime_url, headers=headers, verify=False)
#         # Check if the request was successful (status code 200)
#         if response.status_code == 200:
#             # Use regular expressions to find the first occurrence of the image URL
#             img_url_match = re.search(r'https://cdn\.myanimelist\.net/images/anime/(\d+)/(\d+)\.jpg', response.text)
#             if img_url_match:
#                 img_url = img_url_match.group(0)  # Get the matched URL
#                 return img_url
#     except Exception as e:
#         print( RED , "[E]", str(e) , RESET)
#         return None

# def get_all_animes(mysql, page=1):
#     print(BLUE, "[I] page =", page, RESET)
#     try:
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         logging.info(f"Fetching all anime on page: {page}")
#         cursor.execute('SELECT * FROM anime where poster is not null limit %s,%s;', ((page-1)*10,10))
#         anime_list = cursor.fetchall()
#         print(BLUE, "[I] Number of anime found: ", len(anime_list), RESET)
#         if anime_list:
#             for anime_item in anime_list:
#                 anime_item["poster"] = get_url_by_link(anime_item["Link"])
#             json_response = json.dumps({"Search": anime_list, "totalResults":str(len(anime_list)), "Response":"True"}, indent=2)
#             # return jsonify({"animes": anime_list}), 200
#             return json_response, 200
#         else:
#             return jsonify({"msg": "No anime found!"}), 404
#     except Exception as e:
#         # logging.error(f"Error fetching anime: {str(e)}")
#         print(RED, "[E] Error fetching anime", str(e), RESET)
#         return jsonify({"msg": "Internal server error"}), 500

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
