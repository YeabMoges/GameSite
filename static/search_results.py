import pymysql
import os
from dotenv import load_dotenv

load_dotenv()


def connect_to_db():
    """Establish a connection to the RDS database."""
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )


def search_games(query):
    """Search for games across multiple tables using a UNION query."""
    query = query.lower()
    results = []

    if not query:
        return results

    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT appid, name, header_image AS image_url, short_description AS description, price, store_link, last_updated, 'Action' AS category
                FROM action_games WHERE LOWER(name) LIKE %s

                UNION ALL

                SELECT appid, name, header_image AS image_url, short_description AS description, price, store_link, last_updated, 'Adventure' AS category
                FROM adventure_games WHERE LOWER(name) LIKE %s

                UNION ALL

                SELECT appid, name, header_image AS image_url, short_description AS description, price, store_link, last_updated, 'Indie' AS category
                FROM indie_games WHERE LOWER(name) LIKE %s

                UNION ALL

                SELECT appid, name, header_image AS image_url, short_description AS description, price, store_link, last_updated, 'MMO' AS category
                FROM mmo_games WHERE LOWER(name) LIKE %s

                UNION ALL

                SELECT appid, name, header_image AS image_url, short_description AS description, price, store_link, last_updated, 'RPG' AS category
                FROM rpg_games WHERE LOWER(name) LIKE %s

                UNION ALL

                SELECT appid, name, header_image AS image_url, short_description AS description, price, store_link, last_updated, 'Simulation' AS category
                FROM simulation_games WHERE LOWER(name) LIKE %s

                UNION ALL

                SELECT appid, name, header_image AS image_url, short_description AS description, price, store_link, last_updated, 'Sports' AS category
                FROM sports_games WHERE LOWER(name) LIKE %s

                UNION ALL

                SELECT appid, name, header_image AS image_url, short_description AS description, price, store_link, last_updated, 'Strategy' AS category
                FROM strategy_games WHERE LOWER(name) LIKE %s

                UNION ALL

                SELECT appid, name, header_image AS image_url, short_description AS description, price, store_link, last_updated, 'Early Access' AS category
                FROM earlyaccess_games WHERE LOWER(name) LIKE %s

                UNION ALL

                SELECT appid, name, header_image AS image_url, short_description AS description, price, store_link, last_updated, 'Free to Play' AS category
                FROM free_games WHERE LOWER(name) LIKE %s

                UNION ALL

                SELECT id AS appid, name, image_url, description, price, official_link AS store_link, '' AS last_updated, 'Mobile' AS category
                FROM mobile_games WHERE LOWER(name) LIKE %s
            """, [f"%{query}%"] * 11)

            results = cursor.fetchall()
    finally:
        connection.close()

    return results
