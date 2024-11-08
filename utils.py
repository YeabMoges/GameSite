import boto3
import json
import requests
from flask import url_for


def fetch_cached_games():
    """
    Fetch cached trending games data from S3.
    """
    s3 = boto3.client('s3')
    bucket_name = 'your-s3-bucket-name'
    object_key = 'trending_games.json'

    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        games_data = json.loads(response['Body'].read().decode('utf-8'))
        return games_data['results']  # Adjust based on your API structure
    except Exception as e:
        print(f"Error fetching cached games: {e}")
        return []


def fetch_game_details(appids):
    """
    Fetch game details from the Steam Storefront API.
    """
    game_data = []

    for appid in appids:
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            game_info = data[str(appid)]['data']

            game_data.append({
                'name': game_info['name'],
                'header_image': game_info['header_image'],
                'short_description': game_info['short_description'],
                'price': game_info['price_overview']['final_formatted'] if 'price_overview' in game_info else 'Free',
                'store_link': f"https://store.steampowered.com/app/{appid}/"
            })
        else:
            print(f"Failed to fetch details for AppID: {appid}")

    return game_data


def fetch_google_play_games():
    """
    Return placeholder data for trending games from Google Play Store.
    Now includes custom images from the static folder.
    """
    return [
        {
            'name': 'Wuthering Waves',
            'description': 'Open-world action RPG.',
            'image_url': url_for('static', filename='images/wuthering_waves.jpg'),
            'price': 'Free',
            'store_link': 'https://play.google.com/store/apps/details?id=wutheringwaves'
        },
        {
            'name': 'Punishing Gray Raven',
            'description': 'Fast-paced action combat RPG.',
            'image_url': url_for('static', filename='images/punishing_gray_raven.jpg'),
            'price': 'Free',
            'store_link': 'https://play.google.com/store/apps/details?id=punishinggrayraven'
        },
        {
            'name': 'Arknights',
            'description': 'Strategic tower defense game.',
            'image_url': url_for('static', filename='images/arknights.jpg'),
            'price': 'Free',
            'store_link': 'https://play.google.com/store/apps/details?id=arknights'
        }
    ]
