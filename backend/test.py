import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://router.huggingface.co/hf-inference/models/Helsinki-NLP/opus-mt-en-fr"
headers = {
    "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

output = query({
    "inputs": "i hate the shit out of this",
})

API_URL = "https://router.huggingface.co/hf-inference/models/Helsinki-NLP/opus-mt-fr-en"
headers = {
    "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

output1 = query({
    "inputs": "je t aime ma cherie",
})

print(output)
print(output1)