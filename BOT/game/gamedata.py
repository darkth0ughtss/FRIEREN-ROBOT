# BOT/game/gamedata.py

from pymongo import MongoClient
from ..config import MONGO_URL
from datetime import datetime



# Establish a connection to the MongoDB database
client = MongoClient(MONGO_URL)
db = client['THE-BOT']
users_collection = db['users']


def get_user(user_id):
    return users_collection.find_one({"user_id": user_id})

def create_user(user_id, balance):
    user = {"user_id": user_id, "balance": balance, "bank_balance": 0, "level": 1, "experience": 0}
    users_collection.insert_one(user)

def update_user(user_id, update_data):
    users_collection.update_one({"user_id": user_id}, {"$set": update_data})

def update_balance(user_id, new_balance):
    users_collection.update_one({"user_id": user_id}, {"$set": {"balance": new_balance}})
