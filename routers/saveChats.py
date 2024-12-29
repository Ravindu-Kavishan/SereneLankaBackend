from fastapi import APIRouter, HTTPException, Depends, Response, Request
from pydantic import BaseModel, HttpUrl, ValidationError
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from functions.database import get_chat_collection

savechat_router = APIRouter()

# Define the request model
class GetRequest(BaseModel):
    question: str
    answer: str
    image_urls: list[HttpUrl] = []  # Validate as a list of URLs
    website_urls: list[HttpUrl] = []
    map_urls: list[HttpUrl] = []

# Define the response model
class GetResponse(BaseModel):
    message: str  # The answer field in the response

@savechat_router.post("/savechat", response_model=GetResponse)
async def savechat_user(
    request: Request,  # To access cookies
    body: GetRequest,  # Automatically parses JSON body into a Pydantic model
    response: Response,
    chat_collection: Collection = Depends(get_chat_collection)
):
    # Extract `user_id` from the cookies
    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID not found in cookies")

    # Convert HttpUrl objects to strings
    new_chat = {
        "user_id": user_id,
        "question": body.question,
        "answer": body.answer,
        "image_urls": [str(url) for url in body.image_urls],  # Convert to strings
        "website_urls": [str(url) for url in body.website_urls],  # Convert to strings
        "map_urls": [str(url) for url in body.map_urls],  # Convert to strings
    }

    try:
        # Check for duplicate chat (optional)
        existing_chat = await chat_collection.find_one({
            "user_id": user_id,
            "question": body.question
        })
        if existing_chat:
            raise HTTPException(status_code=400, detail="Chat already exists")

        # Save the document in the database
        await chat_collection.insert_one(new_chat)
        return GetResponse(message="Chat saved successfully")

    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=f"Validation Error: {ve}")
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
