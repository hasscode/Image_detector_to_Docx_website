import requests
import base64
import os
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

# استخدام المفتاح الجديد المحدث في ملف .env
API_KEY = os.getenv("GOOGLE_API_KEY")

def image_to_text(image_input) -> str:
    """
    تقبل إما مسار صورة (string) أو صورة في الذاكرة (BytesIO)
    """
    try:
        # 1. تجهيز بيانات الصورة (Base64)
        if isinstance(image_input, str):
            # إذا كان المدخل مسار ملف
            print(f"👀 Processing file: {os.path.basename(image_input)}")
            with open(image_input, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
        elif isinstance(image_input, BytesIO):
            # إذا كان المدخل من الـ API (الذاكرة)
            print(f"👀 Processing image from memory...")
            image_data = base64.b64encode(image_input.getvalue()).decode('utf-8')
        else:
            print("❌ Invalid image input type")
            return ""

        # 2. إعداد الطلب للموديل المستقر المتاح في حسابك
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"

        payload = {
            "contents": [{
                "parts": [
                    {"text": "Extract all text from this image accurately. Maintain formatting. Return only the text."},
                    {"inline_data": {
                        "mime_type": "image/jpeg",
                        "data": image_data
                    }}
                ]
            }]
        }

        # 3. إرسال الطلب
        response = requests.post(url, json=payload)
        result = response.json()

        if response.status_code == 200:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"❌ Error {response.status_code}: {result.get('error', {}).get('message')}")
            return ""

    except Exception as e:
        print(f"❌ Request failed: {e}")
        return ""