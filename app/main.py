from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load your OpenAI API key from an environment variable
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

API = FastAPI()

# Define a list of allowed origins for CORS
# Include the origin for your frontend
origins = [
    "http://localhost:5173",  # Add more origins as needed
]

# Add CORSMiddleware to the application
API.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=["POST"],  # Allows only POST method for /respond endpoint
    allow_headers=["Content-Type"],  # Allows only specified headers
)

class UserMessage(BaseModel):
    message: str

@API.post("/respond")
async def respond(user_message: UserMessage):
    if not user_message.message:
        raise HTTPException(status_code=400, detail="No message provided")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message.message},
            ],
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        # Log the exception details to help with debugging
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
