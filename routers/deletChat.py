from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends, Request
from pymongo.collection import Collection
from functions.database import get_chat_collection
from pydantic import BaseModel
from typing import List

deleteChat_router = APIRouter()


@deleteChat_router.delete("/deleteChat/{chat_id}")
async def delete_chat(
    chat_id: str,
    request: Request,  # To access cookies
    chat_collection: Collection = Depends(get_chat_collection)
):
    # Extract `user_id` from cookies
    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID not found in cookies")

    # Ensure the chat belongs to the logged-in user and delete it
    result = await chat_collection.delete_one({"_id": ObjectId(chat_id), "user_id": user_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Chat not found or does not belong to the user")

    return {"message": "Chat deleted successfully"}
