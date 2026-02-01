import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

response = requests.get(url)
models = response.json()

print("--- Available Models for your Key ---")
if 'models' in models:
    for m in models['models']:
        print(m['name'])
else:
    print(models)