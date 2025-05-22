"""
Script to fetch video details from specified YouTube channels.
Requires a YouTube Data API key to be set in .env file.
"""

import os
from datetime import datetime
from typing import List, Dict
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# YouTube channels to fetch videos from
CHANNELS = [
    "https://www.youtube.com/@IndianFootball/videos",
    "https://www.youtube.com/@IndianSuperLeague/videos",
    "https://www.youtube.com/@playmakerindia/videos"
]

def get_channel_id(youtube, channel_url: str) -> str:
    """Extract channel ID from custom URL."""
    channel_name = channel_url.split('@')[1].split('/')[0]
    
    try:
        request = youtube.search().list(
            part="snippet",
            q=channel_name,
            type="channel",
            maxResults=1
        )
        response = request.execute()
        
        if response['items']:
            return response['items'][0]['snippet']['channelId']
    except HttpError as e:
        print(f"Error fetching channel ID for {channel_url}: {e}")
    
    return None

def get_videos(youtube, channel_id: str, max_results: int = 10) -> List[Dict]:
    """Fetch recent videos from a channel."""
    try:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            order="date",
            type="video",
            maxResults=max_results
        )
        response = request.execute()
        
        videos = []
        for item in response['items']:
            video = {
                'title': item['snippet']['title'],
                'video_id': item['id']['videoId'],
                'published_at': item['snippet']['publishedAt'],
                'channel_title': item['snippet']['channelTitle'],
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
            videos.append(video)
        
        return videos
    
    except HttpError as e:
        print(f"Error fetching videos for channel {channel_id}: {e}")
        return []

def main():
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("Error: YOUTUBE_API_KEY not found in .env file")
        return
    
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    for channel_url in CHANNELS:
        print(f"\nFetching videos from: {channel_url}")
        channel_id = get_channel_id(youtube, channel_url)
        
        if not channel_id:
            print(f"Could not find channel ID for {channel_url}")
            continue
        
        videos = get_videos(youtube, channel_id)
        
        for video in videos:
            published = datetime.fromisoformat(video['published_at'].replace('Z', '+00:00'))
            print(f"\nTitle: {video['title']}")
            print(f"Published: {published.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"URL: {video['url']}")
            print(f"Channel: {video['channel_title']}")
            print("-" * 80)

if __name__ == "__main__":
    main()
