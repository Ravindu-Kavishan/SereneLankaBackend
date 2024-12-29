from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from functions.database import connect_to_mongo, disconnect_from_mongo
from routers.login import login_router
from routers.signin import signup_router
from routers.forgetPassword import fP_router
from routers.shereFriends import sF_router
from routers.getPrompt import getPrompt_router
from routers.saveChats import savechat_router
from routers.getSavedChats import getSavedChat_router
from routers.deletChat import deleteChat_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://serenelanka002.netlify.app"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


app.include_router(login_router, prefix="/auth", tags=["Login"])
app.include_router(signup_router, prefix="/auth", tags=["Signin"])
app.include_router(fP_router, prefix="/auth", tags=["Forgetpassword"])
app.include_router(sF_router, prefix="/share", tags=["share"])
app.include_router(getPrompt_router, prefix="/chatbot", tags=["chatbot"])
app.include_router(savechat_router, prefix="/chatbot", tags=["chatbot"])
app.include_router(getSavedChat_router, prefix="/chatbot", tags=["chatbot"])
app.include_router(deleteChat_router, prefix="/chatbot", tags=["chatbot"])


# Connect to MongoDB during startup
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

# Disconnect from MongoDB during shutdown
@app.on_event("shutdown")
async def shutdown_event():
    await disconnect_from_mongo()
