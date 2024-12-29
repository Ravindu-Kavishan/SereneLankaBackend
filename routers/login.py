from fastapi import APIRouter, HTTPException, Depends,Response
from pydantic import BaseModel
from functions.database import get_user_collection
from pymongo.collection import Collection
from functions.cookieHandeling import setCookie
from functions.passwordHashing import verify_password

login_router = APIRouter()

# Pydantic model for user login
class LoginRequest(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str


class LoginResponse(BaseModel):
    message: str
    user_id: str


@login_router.post("/login", response_model=LoginResponse)
async def login_user(request: LoginRequest,response: Response, user_collection: Collection = Depends(get_user_collection)):
    # Find user by username or email
    user = await user_collection.find_one({"$or": [
        {"username": request.username},
        {"email": request.email}
    ]})

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify password
    if not verify_password(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create a cookie with user_id
    setCookie(response,user['_id'])
    return {"message": "Login successful", "user_id": str(user["_id"])}
