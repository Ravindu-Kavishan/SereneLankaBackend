from fastapi import APIRouter, HTTPException, Depends,Response
from pydantic import BaseModel, EmailStr
from functions.database import get_user_collection
from functions.passwordHashing import get_hashed_password
from functions.cookieHandeling import setCookie
from pymongo.collection import Collection

signup_router = APIRouter()

# Pydantic models
class SignUpRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class SignUpResponse(BaseModel):
    message: str
    user_id: str


@signup_router.post("/signin", response_model=SignUpResponse)
async def signup_user(
    request: SignUpRequest,
    response: Response,
    user_collection: Collection = Depends(get_user_collection)
):
    # Check if username or email already exists
    existing_user = await user_collection.find_one({
        "$or": [
            {"username": request.username},
            {"email": request.email}
        ]
    })

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    # Hash the password
    hashed_password = get_hashed_password(request.password)

    # Insert the new user into MongoDB
    new_user = {
        "username": request.username,
        "email": request.email,
        "password": hashed_password
    }
    result = await user_collection.insert_one(new_user)

    # Create a cookie with user_id
    user_id = str(result.inserted_id)
    setCookie(response,user_id)

    return {
        "message": "User registered successfully",
        "user_id": user_id
    }
