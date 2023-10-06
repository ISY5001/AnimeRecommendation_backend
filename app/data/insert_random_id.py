# inorder to run the script 
# you need to 
# `pip install mysql-connector-python`
#
import mysql.connector
import random
import string

# MySQL connection configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "chenzhw57",
    "database": "user_data",
}

# Function to generate a random string
def random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

# Create a MySQL connection
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Define the range of IDs you want to insert
start_id = 4
end_id = 73516

for id in range(start_id, end_id + 1):
    username = random_string(10)  # Generate a random username
    password = random_string(8)   # Generate a random password
    email = f"user{id}@example.com"  # Generate a random email

    # Insert the random data into the 'accounts' table
    insert_query = "INSERT INTO accounts (id, username, password, email) VALUES (%s, %s, %s, %s)"
    values = (id, username, password, email)
    cursor.execute(insert_query, values)

# Commit the changes and close the connection
connection.commit()
cursor.close()
connection.close()

