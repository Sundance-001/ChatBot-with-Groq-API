#test groq api with llama3-8b-8192 model
import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("groq_api_key")

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "llama3-8b-8192", 
    "messages": [
        {"role": "system", "content": "You are a nerd obsessed with movies, fighter jets, world war 2, tarantino."},
        {"role": "user", "content": "Tell me facts about cinema and cult movies in a tarantino-esque manner."}
    ]
}

response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

print("Status:", response.status_code)
print("Response:", response.text)
