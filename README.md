# Aashayein

> India's journey to FIFA glory.

## YouTube

### Prerequisites

- Python 3.8 or higher
- YouTube Data API key (get it from [Google Cloud Console](https://console.cloud.google.com/apis/credentials))

### Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add your YouTube API key to .env file.
cp .env.example .env
```

### Usage
```bash
python fetch_youtube_videos.py
```
