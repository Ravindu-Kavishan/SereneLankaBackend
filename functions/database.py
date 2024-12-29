from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection
from fastapi import Depends
import urllib.parse

# MongoDB client instance
mongo_client: AsyncIOMotorClient = None

# Database name
DB_NAME = "SereneLanka"

# Connection string for MongoDB Atlas
# URL encode the password to handle special characters
username = "SereneLanka"
password = urllib.parse.quote_plus("ravindu2002")
MONGO_URL = f"mongodb+srv://{username}:{password}@cluster0.bcd53.mongodb.net/?retryWrites=true&w=majority"

async def connect_to_mongo():
    global mongo_client
    try:
        # Use AsyncIOMotorClient instead of MongoClient
        mongo_client = AsyncIOMotorClient(MONGO_URL)
        # Verify connection
        await mongo_client.admin.command('ping')
        print("Connected to MongoDB Atlas successfully")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

async def disconnect_from_mongo():
    global mongo_client
    if mongo_client:
        mongo_client.close()
        print("Disconnected from MongoDB Atlas")

async def get_database():
    """Async helper function to get the database instance"""
    if not mongo_client:
        await connect_to_mongo()
    return mongo_client[DB_NAME]

async def get_user_collection(db = Depends(get_database)) -> Collection:
    return db["users"]

async def get_chat_collection(db = Depends(get_database)) -> Collection:
    return db["chats"]