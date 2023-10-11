import streamlit as st
import pymongo
import mysql.connector
from mysql.connector import Error

# Function to create MySQL tables
def create_mysql_tables():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="youtube"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            # Create 'channel' table
            cursor.execute("CREATE TABLE IF NOT EXISTS channel (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), description TEXT)")
            # Create 'playlist' table
            cursor.execute("CREATE TABLE IF NOT EXISTS playlist (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), channel_id INT, FOREIGN KEY (channel_id) REFERENCES channel(id))")
            # Create 'comment' table
            cursor.execute("CREATE TABLE IF NOT EXISTS comment (id INT AUTO_INCREMENT PRIMARY KEY, content TEXT, video_id INT, FOREIGN KEY (video_id) REFERENCES video(id))")
            # Create 'video' table
            cursor.execute("CREATE TABLE IF NOT EXISTS video (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), description TEXT, playlist_id INT, FOREIGN KEY (playlist_id) REFERENCES playlist(id))")
            cursor.close()
    except Error as e:
        st.error(f"Error creating MySQL tables: {e}")
    finally:
        if connection.is_connected():
            connection.close()

# Function to migrate data from MongoDB to MySQL
def migrate_data():
    try:
        mongo_client = pymongo.MongoClient("mongodb+srv://kishorekumar:kishore@cluster0.76cdkbb.mongodb.net/?retryWrites=true&w=majority")
        mongo_db = mongo_client["youtube_data"]
        mongo_collection = mongo_db["channels","videos"]

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="youtube"
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Iterate through MongoDB collection and insert data into MySQL
            for document in mongo_collection.find():
                # Insert data into the corresponding MySQL table
                if document['type'] == 'channel':
                    cursor.execute("INSERT INTO channel (name, description) VALUES (%s, %s)",
                                   (document['name'], document['description']))
                elif document['type'] == 'playlist':
                    cursor.execute("INSERT INTO playlist (name, channel_id) VALUES (%s, %s)",
                                   (document['name'], document['channel_id']))
                elif document['type'] == 'comment':
                    cursor.execute("INSERT INTO comment (content, video_id) VALUES (%s, %s)",
                                   (document['content'], document['video_id']))
                elif document['type'] == 'video':
                    cursor.execute("INSERT INTO video (title, description, playlist_id) VALUES (%s, %s, %s)",
                                   (document['title'], document['description'], document['playlist_id']))

            connection.commit()
            cursor.close()

    except Error as e:
        st.error(f"Error migrating data to MySQL: {e}")
    finally:
        if connection.is_connected():
            connection.close()
        if mongo_client:
            mongo_client.close()

# Streamlit app
st.title("Data Migration from MongoDB to MySQL")

# Button to create MySQL tables
if st.button("Create MySQL Tables"):
    create_mysql_tables()
    st.success("MySQL tables created successfully!")

# Button to migrate data from MongoDB to MySQL
if st.button("Migrate Data from MongoDB to MySQL"):
    migrate_data()
    st.success("Data migration completed!")

# Additional Streamlit UI elements can be added for user interaction, such as input fields and status updates.


