# from motor.motor_asyncio import AsyncIOMotorClient
# from pymongo.collection import Collection
# from fastapi import  Depends

# # MongoDB client instance
# mongo_client: AsyncIOMotorClient = None

# # Database name
# DB_NAME = "SereneLanka"

# async def connect_to_mongo():
#     global mongo_client
#     mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")  # Local MongoDB connection
#     print("Connected to MongoDB")

# async def disconnect_from_mongo():
#     global mongo_client
#     if mongo_client:
#         mongo_client.close()
#         print("Disconnected from MongoDB")

# def get_database():
#     """Helper function to get the database instance"""
#     return mongo_client[DB_NAME]

# def get_user_collection(db=Depends(get_database)) -> Collection:
#     return db["users"]

# def get_chat_collection(db=Depends(get_database)) -> Collection:
#     return db["chats"]

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection
from fastapi import Depends

# MongoDB client instance
mongo_client: AsyncIOMotorClient = None

# Database name
DB_NAME = "SereneLanka"

# Connection string for MongoDB Atlas
MONGO_URL = "mongodb+srv://SereneLanka:2002%40Kavi@cluster0.bcd53.mongodb.net/?retryWrites=true&w=majority"

async def connect_to_mongo():
    global mongo_client
    mongo_client = AsyncIOMotorClient(MONGO_URL)  # MongoDB Atlas connection
    print("Connected to MongoDB Atlas")

async def disconnect_from_mongo():
    global mongo_client
    if mongo_client:
        mongo_client.close()
        print("Disconnected from MongoDB Atlas")

def get_database():
    """Helper function to get the database instance"""
    return mongo_client[DB_NAME]

def get_user_collection(db=Depends(get_database)) -> Collection:
    return db["users"]

def get_chat_collection(db=Depends(get_database)) -> Collection:
    return db["chats"]