import json
import psycopg2
from decouple import config

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=config('DB_NAME'),
    user=config('DB_USER'),
    password=config('DB_PASSWORD'),
    host=config('DB_HOST'),
    port=config('DB_PORT')
)
cursor = conn.cursor()

# Load JSON file
with open('valid_answers.json', 'r') as f:
    data = json.load(f)

# Insert data
for record in data:
    fields = record['fields']
    cursor.execute(
        "INSERT INTO game_validanswer (word, category_id) VALUES (%s, %s)",
        (fields['word'], fields['category'])
    )

# Commit and close
conn.commit()
cursor.close()
conn.close()
