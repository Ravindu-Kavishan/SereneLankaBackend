
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from functions.database import get_user_collection
from functions.passwordHashing import get_hashed_password
from functions.cookieHandeling import setCookie

fP_router = APIRouter()


class ForgetPasswordRequest(BaseModel):
    username: str | None = None

class ChangePasswordRequest(BaseModel):
    username: str
    password: str

@fP_router.post("/forgetpassword")
async def forget_password(
    request: ForgetPasswordRequest,  user_collection = Depends(get_user_collection)
):
    user = await user_collection.find_one({"username": request.username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User found"}

@fP_router.post("/changepassword")
async def change_password(
    request: ChangePasswordRequest,response: Response, user_collection = Depends(get_user_collection)
):
    user = await user_collection.find_one({"username": request.username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = get_hashed_password(request.password)
    result = await user_collection.update_one(
        {"username": request.username}, {"$set": {"password": hashed_password}}
    )

    if result.modified_count == 1:
        setCookie(response, user['_id'])
        return {"message": "Password updated successfully"}
    else:
        raise HTTPException(status_code=400, detail="Password update failed")
