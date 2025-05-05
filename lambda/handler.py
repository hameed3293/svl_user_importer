import boto3
import os
import requests

# Set up DynamoDB
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

# API Endpoint
url = "https://jsonplaceholder.typicode.com/users"

def handler(event, context):
    data = fetch_users()

    if not data:
        return {
            "statusCode": 500,
            "body": "Failed to fetch or process user data."
        }

    for item in data:
        table.put_item(Item=item)
        print(f"Inserted: {item}")

    return {
        "statusCode": 200,
        "body": f"Inserted {len(data)} records."
    }

def fetch_users():
    try:
        response = requests.get(url)
        response.raise_for_status()
        users = response.json()

        simplified = []
        for record in users[:5]:
            flat = flatten_json(record)
            simplified.append({
                "id": str(flat.get("id")),  
                "name": flat.get("name"),
                "username": flat.get("username"),
                "email": flat.get("email")
            })

        return simplified
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def flatten_json(y, parent_key='', sep='.'):
    items = []
    for k, v in y.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)