import pymysql,requests, os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Access environment variables
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')

GENRE_TABLES = {
    'Action': 'action_games',
    'Adventure': 'adventure_games',
    'Early Access': 'earlyaccess_games',
    'Free to Play': 'free_games',
    'Indie': 'indie_games',
    'Massively Multiplayer': 'mmo_games',
    'RPG': 'rpg_games',
    'Simulation': 'simulation_games',
    'Sports': 'sports_games',
    'Strategy': 'strategy_games'
}

# Connect to the RDS database
def connect_to_server():
    """Connect to the MySQL server (without specifying a database)."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        cursorclass=pymysql.cursors.DictCursor
    )

def connect_to_db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# Create the database if it doesn't exist
def create_database_if_not_exists():
    connection = connect_to_server()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
        connection.commit()
        print(f"Database `{DB_NAME}` ensured.")
    finally:
        connection.close()

# Create table if it doesn't exist
def create_table_if_not_exists(table_name):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    appid INT NOT NULL,
                    name VARCHAR(255) DEFAULT NULL,
                    header_image TEXT,
                    short_description TEXT,
                    price VARCHAR(50) DEFAULT NULL,
                    store_link TEXT,
                    last_updated TIMESTAMP NULL DEFAULT NULL,
                    PRIMARY KEY (appid)
                );
            """
            cursor.execute(create_table_query)
        connection.commit()
    finally:
        connection.close()

# Fetch detailed game info from Steam API using AppID
def fetch_game_details(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get(str(appid), {}).get('data', {})
        return {
            'appid': appid,
            'name': data.get('name', 'Unknown'),
            'header_image': data.get('header_image', 'https://via.placeholder.com/150'),
            'short_description': data.get('short_description', 'No description available.'),
            'price': data.get('price_overview', {}).get('final_formatted', 'Free'),
            'store_link': f"https://store.steampowered.com/app/{appid}/"
        }
    return None

# Function to fetch the top 20 action games from SteamSpy
def fetch_top_genre_games(genre):
    url = f"https://steamspy.com/api.php?request=genre&genre={genre}"
    response = requests.get(url)
    if response.status_code == 200:
        games = response.json()
        top_20_games = list(games.values())[:32]
        detailed_games = []
        for game in top_20_games:
            game_data = fetch_game_details(game['appid'])
            if game_data:
                detailed_games.append(game_data)
        return detailed_games
    return []

# Function to save game data to the action_games table in RDS
def save_to_genre_table(table_name, game_data):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            query = f"""
                INSERT INTO {table_name} (appid, name, header_image, short_description, price, store_link, last_updated)
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

# Main function to fetch and populate each genre table
def main():
    create_database_if_not_exists()
    for genre, table_name in GENRE_TABLES.items():
        print(f"Ensuring table exists for genre: {genre}")
        create_table_if_not_exists(table_name)
        print(f"Fetching and populating table for genre: {genre}")
        top_games = fetch_top_genre_games(genre)
        for game_data in top_games:
            save_to_genre_table(table_name, game_data)
        print(f"Completed populating {table_name}.")

# Run the script
if __name__ == "__main__":
    main()