from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.get("/")
def home():
    return {"message": "Welcome to the README Generator API!"}

@app.post("/generate")
async def generate_readme(data: dict):
    prompt = data.get("prompt")

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a professional GitHub documentation expert."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.6
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()