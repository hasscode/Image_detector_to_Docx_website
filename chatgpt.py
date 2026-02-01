from openai import OpenAI
from dotenv import load_dotenv
import os

# load environment variables from .env
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def clean_text_with_chatgpt(raw_text: str) -> str:
    prompt = f"""
    Clean the following text, fix spelling and grammar mistakes,
    and organize it in a clear professional format:

    {raw_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
