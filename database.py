from pymongo import MongoClient
import bcrypt

# MongoDB connection
client = MongoClient("***REMOVED***")
db = client["user_auth"]
users_collection = db["users"]

def create_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = {"username": username, "password": hashed_password}
    users_collection.insert_one(user)

def authenticate_user(username, password):
    user = users_collection.find_one({"username": username})
    if user:
        return bcrypt.checkpw(password.encode('utf-8'), user["password"])
    return False

def reset_password(username, new_password):
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    result = users_collection.update_one(
        {"username": username}, {"$set": {"password": hashed_password}}
    )
    return result.modified_count > 0
