import mysql.connector
import os
from webcrawl import download_and_rename_anime_poster
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

# Function to download and rename the anime poster and update the database
def download_and_update_posters(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT Anime_id, Link, poster FROM anime  WHERE poster is null  and length(Link) > 10;")
        anime_records = cursor.fetchall()

        for anime_id, link, poster in anime_records:
            print(RESET, "[I] processing ", anime_id, ", poster is ", poster)
            poster_filename = download_and_rename_anime_poster(link, "poster_images")
            print(CYAN , "[I] poster_filename = ", poster_filename  , RESET)
            if poster_filename: 
            # Update the database with the poster filename
                update_query = "UPDATE anime SET poster = %s WHERE Anime_id = %s"
                cursor.execute(update_query, (poster_filename, anime_id))
                connection.commit()
            else:
                pass

        print("Poster download and database update completed")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

if __name__ == "__main__":
    db_connection = connect_to_database()

    if db_connection:
        download_and_update_posters(db_connection)
        db_connection.close()
    else:
        print("Failed to connect to the database")
