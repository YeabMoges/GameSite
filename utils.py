import boto3
import json


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
