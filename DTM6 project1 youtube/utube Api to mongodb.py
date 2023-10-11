import os
import pymongo
from googleapiclient.discovery import build

# Set your YouTube Data API key
api_key = "**you tube data api key**"

# Initialize the YouTube Data API client
youtube = build("youtube", "v3", developerKey=api_key)

# Set up a MongoDB connection
mongo_client = pymongo.MongoClient("mongodb+srv://kishorekumar:kishore@cluster0.76cdkbb.mongodb.net/?retryWrites=true&w=majority")  # Replace with your MongoDB connection URI
db = mongo_client["youtube_data"]  # Create or connect to your MongoDB database

def fetch_channel_data(channel_id):
    try:
        # Call the YouTube API to get channel details
        channel_response = youtube.channels().list(
            part="snippet,statistics,contentDetails",
            id=channel_id
        ).execute()

        # Extract channel information from the API response
        if "items" in channel_response:
            channel_data = channel_response["items"][0]

            # Insert channel data into MongoDB
            db.channels.insert_one(channel_data)

            return channel_data

    except Exception as e:
        print(f"An error occurred while fetching channel data: {e}")

def fetch_video_data(channel_id):
    try:
        # Call the YouTube API to get videos from the channel's uploads playlist
        uploads_playlist_id = fetch_channel_data(channel_id)["contentDetails"]["relatedPlaylists"]["uploads"]
        playlist_items_response = youtube.playlistItems().list(
            part="snippet",
            playlistId=uploads_playlist_id,
            maxResults=50  # Adjust the number of results as needed
        ).execute()

        # Extract video information from the API response
        for item in playlist_items_response["items"]:
            video_data = item["snippet"]

            # Insert video data into MongoDB
            db.videos.insert_one(video_data)

    except Exception as e:
        print(f"An error occurred while fetching video data: {e}")

# Provide the channel_id of the YouTube channel you want to retrieve and store data for
channel_id = "**youtube channel_id**"
fetch_channel_data(channel_id)
fetch_video_data(channel_id)

# Close the MongoDB connection
mongo_client.close()
#channel 
#channel_id = "UCvyZS6W6zMJCZBVzF-Ei6sw" - a2d
#channel_id = "UCJcCB-QYPIBcbKcBQOTwhiA" - vj sidhu vlogs
#channel_id = "UCueYcgdqos0_PzNOq81zAFg" - parithabangal
#channel_id = "UCXzULCWuvbnjm7Q0F6RBKsw" - engineering facts
#channel_id = "UCk3JZr7eS3pg5AGEvBdEvFg" - village cooking channel
#channel_id = "UCe_-TsRz3GH8UVjN0ApzXJQ" - tech shan Tamil
#channel_id = "UCY6KjrDBN_tIRFT_QNqQbRQ" - madan gowri
#channel_id = "UCLbdVvreihwZRL6kwuEUYsA" - think music india
#channel_id = "UCn4rEMqKtwBQ6-oEwbd4PcA" - sony music south
#channel_id = "UCN2C94LXAg1tXUVdyfz3Itw" - kochi