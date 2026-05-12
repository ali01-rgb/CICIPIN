from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('DB_NAME')]

# Ambil beberapa sample alamat
restaurants = list(db.restaurants.find({}, {'address': 1, 'name': 1}).limit(10))
for r in restaurants:
    print(f"Restaurant: {r.get('name', 'N/A')}")
    print(f"Address: {r.get('address', 'N/A')}")
    print('---')


