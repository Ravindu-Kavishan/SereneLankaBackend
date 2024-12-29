from fastapi import Response

def setCookie(response: Response, id: str):
    response.set_cookie(
        key="user_id",
        value=id,
        httponly=True,  
        secure=True,  
        samesite="None",  
        max_age=3600,  
        path="/"  
    )
    print("Cookie set successfully")
