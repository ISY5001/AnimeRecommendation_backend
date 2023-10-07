import mysql.connector
import os
from webcrawl import download_and_rename_anime_poster
import concurrent.futures
import time
from printcolor import RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, RESET

# Function to connect to MySQL database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="chenzhw57",
            database="user_data"
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    return None

# Function to download and rename the anime poster
def download_anime_poster(anime_id, link):
    poster_filename = download_and_rename_anime_poster(link, "poster_images")
    return anime_id, poster_filename

# Function to update the database with poster filenames
def update_database(connection, anime_id, poster_filename):
    try:
        cursor = connection.cursor()
        update_query = "UPDATE anime SET poster = %s WHERE Anime_id = %s"
        cursor.execute(update_query, (poster_filename, anime_id))
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

if __name__ == "__main__":
    db_connection = connect_to_database()

    if db_connection:
        start_id = 317
        end_id = 40000
        anime_records = []

        # Fetch anime records in the specified range
        with db_connection.cursor() as cursor:
            cursor.execute("SELECT Anime_id, Link FROM anime WHERE poster IS NULL and length(Link) > 10;")
            anime_records = cursor.fetchall()

        # Download and update posters using concurrent futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:  # Use ThreadPoolExecutor for threading
            futures = []

            for anime_id, link in anime_records:
                time.sleep(1)
                futures.append(executor.submit(download_anime_poster, anime_id, link))

            for future in concurrent.futures.as_completed(futures):
                anime_id, poster_filename = future.result()
                if poster_filename:
                    update_database(db_connection, anime_id, poster_filename)
                    print(GREEN, "[I] Downloaded and saved, " , "anime_id=", anime_id, ", poster=", poster_filename)

        db_connection.close()
    else:
        print("Failed to connect to the database")
