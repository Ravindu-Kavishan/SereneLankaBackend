from fastapi import APIRouter, HTTPException, Depends, Request
from pymongo.collection import Collection
from bson import ObjectId
from functions.database import get_chat_collection
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

getSavedChat_router = APIRouter()

# Define the chat model for the response
class Chat(BaseModel):
    id: str  # Use `id` to send back the MongoDB document ID as a string
    question: str
    answer: str
    image_urls: List[HttpUrl] = []  # Validate as a list of valid URLs
    website_urls: List[HttpUrl] = []
    map_urls: List[HttpUrl] = []

class GetChatsResponse(BaseModel):
    chats: List[Chat]  # List of saved chats

@getSavedChat_router.get("/getSavedChats", response_model=GetChatsResponse)
async def get_saved_chats(
    request: Request,  # To access cookies
    chat_collection: Collection = Depends(get_chat_collection),
):
    # Extract `user_id` from cookies
    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID not found in cookies")

    try:
        # Fetch all chats for the user from the database
        saved_chats = await chat_collection.find({"user_id": user_id}).to_list(length=50)

        # Map the MongoDB documents to the response model
        chats = []
        for chat in saved_chats:
            chats.append(
                {
                    "id": str(chat["_id"]),  # Convert ObjectId to string
                    "question": chat.get("question", ""),  # Default to empty string if missing
                    "answer": chat.get("answer", ""),
                    "image_urls": chat.get("image_urls", []),  # Default to an empty list if missing
                    "website_urls": chat.get("website_urls", []),
                    "map_urls": chat.get("map_urls", []),
                }
            )

        # Return the response
        return GetChatsResponse(chats=chats)

    except Exception as e:
        # Log the error and return a 500 response
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
