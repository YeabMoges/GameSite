import pymysql
import requests
from datetime import datetime

# Database configuration
DB_HOST = 'gamesite.cg1ttynegix3.us-west-2.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASS = 'VpR6koaUyDcvLK67lcV9'
DB_NAME = 'site_schema'

# Connect to the RDS database
def connect_to_db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# Function to fetch the top 20 action games from SteamSpy
def fetch_top_action_games():
    url = "https://steamspy.com/api.php?request=genre&genre=Action"
    response = requests.get(url)
    if response.status_code == 200:
        games = response.json()
        # Extract AppIDs for top 20 games
        top_20_appids = [int(appid) for appid in list(games.keys())[:20]]
        return top_20_appids
    return []

# Function to fetch detailed game info from Steam API using AppID
def fetch_game_details(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get(str(appid), {}).get('data', {})
        return {
            'appid': appid,
            'name': data.get('name', 'Unknown'),
            'header_image': data.get('header_image', ''),
            'short_description': data.get('short_description', ''),
            'price': data.get('price_overview', {}).get('final_formatted', 'Free'),
            'store_link': f"https://store.steampowered.com/app/{appid}/"
        }
    return None

# Function to save game data to the action_games table in RDS
def save_to_db(game_data):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO action_games (appid, name, header_image, short_description, price, store_link, last_updated)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    name=VALUES(name),
                    header_image=VALUES(header_image),
                    short_description=VALUES(short_description),
                    price=VALUES(price),
                    store_link=VALUES(store_link),
                    last_updated=VALUES(last_updated)
            """
            cursor.execute(query, (
                game_data['appid'],
                game_data['name'],
                game_data['header_image'],
                game_data['short_description'],
                game_data['price'],
                game_data['store_link'],
                datetime.utcnow()
            ))
        connection.commit()
    finally:
        connection.close()

# Main function to fetch and update data for the top 20 action games
def main():
    appids = fetch_top_action_games()
    for appid in appids:
        game_data = fetch_game_details(appid)
        if game_data:
            save_to_db(game_data)
    print("Data fetched and saved successfully.")

# Run the script
if __name__ == "__main__":
    main()