import os
import base64
from io import BytesIO
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# تعريف العميل باستخدام المفتاح من الـ .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def image_to_text_gpt(image_input) -> str:
    try:
        if isinstance(image_input, BytesIO):
            image_data = base64.b64encode(image_input.getvalue()).decode('utf-8')
        else:
            with open(image_input, "rb") as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')

        response = client.chat.completions.create(
            model="gpt-4o", # الموديل اللي بيدعم الصور
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract all text from this image accurately."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                    ],
                }
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ GPT Error: {e}")
        return ""