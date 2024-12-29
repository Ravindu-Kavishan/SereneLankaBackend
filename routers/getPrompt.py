from fastapi import APIRouter, HTTPException, Depends, Response
from pydantic import BaseModel
from functions.RAG.genarateAnswer import ask_question
import requests
import re
from functions.sepereteURLs import categorize_urls


# Define the request model
class GetPromptRequest(BaseModel):
    question: str  # The question field in the request body

# Define the response model
class GetPromptResponse(BaseModel):
    answer: str  # The answer field in the response
    image_urls: list
    website_urls: list
    map_urls: list

# Initialize the router
getPrompt_router = APIRouter()

@getPrompt_router.post("/sendPrompt", response_model=GetPromptResponse)
async def getPrompt_user(
    request: GetPromptRequest,  # Automatically parses JSON body into a Pydantic model
    response: Response,
):
    # Access the question from the request
    question = request.question

    # Example logic: You can process the question and create a response
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # Generate a mock answer (replace this with your actual logic)
    answer = ask_question(question)
    prompt = f"{answer} {question} (Provide only the exact answer based on the given text. Do not include any explanations, unnecessary details, or assumptions. If the provided text does not contain the answer, respond with 'I do not know about it.' For image or website-related questions, return the provided search link without any explanation.)"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    # Set the headers and URL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyDLrw2Yg63sfzmfB0shnrSUt9GwvanUS7c"
    headers = {
        'Content-Type': 'application/json',
    }

    try:
        # Make the POST request
        api_response = requests.post(url, json=payload, headers=headers)
        api_response.raise_for_status()  # Will raise an HTTPError for bad responses

        # Extract the text part from the response
        response_data = api_response.json()
        if "candidates" in response_data and len(response_data["candidates"]) > 0:
            text = response_data["candidates"][0]["content"]["parts"][0]["text"]
            image_urls, website_urls, map_urls = categorize_urls(text)
            return GetPromptResponse(
                answer=text,
                image_urls=image_urls,
                website_urls=website_urls,
                map_urls=map_urls
            )
        else:
            raise HTTPException(status_code=500, detail="No text content found in response")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error calling Gemini API: {e}")