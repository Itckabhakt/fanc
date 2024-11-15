import requests
import json
import os
import time

# Telegram bot details
BOT_TOKEN = '7579433516:AAGRJWxzrsPlkslOFaVN5ZSGaz-bNO4bobs'
CHANNEL_ID = '@channelytgtreee'
JSON_URL = 'https://raw.githubusercontent.com/drmlive/fancode-live-events/main/fancode.json'

# File to store posted match IDs for persistence
POSTED_MATCHES_FILE = 'posted_matches.json'

# Load posted matches from file
def load_posted_matches():
    if os.path.exists(POSTED_MATCHES_FILE):
        with open(POSTED_MATCHES_FILE, 'r') as file:
            return set(json.load(file))
    return set()

# Save posted matches to file
def save_posted_matches(posted_matches):
    with open(POSTED_MATCHES_FILE, 'w') as file:
        json.dump(list(posted_matches), file)

# Initialize posted matches set
posted_matches = load_posted_matches()

# Function to fetch match data
def fetch_match_data():
    response = requests.get(JSON_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch match data. Status code: {response.status_code}")
    return response.json()

# Function to post to Telegram
def post_to_telegram(content, image_url):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
    payload = {
        'chat_id': CHANNEL_ID,
        'caption': content,
        'parse_mode': 'HTML'
    }
    files = {
        'photo': (image_url, requests.get(image_url).content)
    }
    response = requests.post(url, data=payload, files=files)
    if response.status_code != 200:
        raise Exception(f"Error sending photo: {response.text}")
    return response.json()

# Function to format and post the match data
def format_and_post():
    global posted_matches
    data = fetch_match_data()
    matches = data.get('matches', [])

    for match in matches:
        match_id = match.get('match_id')
        if match['status'] == 'LIVE' and match_id and match_id not in posted_matches:
            # Create the formatted message
            message = f"""
<b>{match['event_name']}</b>
<b>{match['match_name']}</b>
──────────────
<b>• Ios/android working upto 1080p</b>
<a href="https://livecrichdm3u8player.pages.dev/?dtv={match['adfree_url']}">Click to Watch</a>

<b>• Tv cast - m3u8</b>
<a href="{match['adfree_url']}">Click to Watch</a>
──────────────
<b>Watch - {CHANNEL_ID}</b>
            """.strip()

            # Send the post with the image URL
            post_to_telegram(message, match['src'])
            posted_matches.add(match_id)  # Track the posted match ID
            print(f"Posted match {match['match_name']} to Telegram.")

    # Save the updated posted matches set
    save_posted_matches(posted_matches)

# Run the script every 5 minutes
if __name__ == '__main__':
    while True:
        format_and_post()
        time.sleep(300)  # Wait 5 minutes
