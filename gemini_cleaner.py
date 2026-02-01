import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

def clean_text_with_gemini(raw_text: str) -> str:
    if not raw_text.strip():
        return ""
    
    try:
        # استخدمنا نفس الرابط اللي نفع معاك في الـ Vision بالظبط (gemini-flash-latest)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"

        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Clean and format this medical text professionally. Use bold for headers and fix any OCR errors:\n\n{raw_text}"
                }]
            }]
        }

        response = requests.post(url, json=payload)
        result = response.json()

        if response.status_code == 200:
            # التأكد من مسار النتيجة في الـ JSON
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            # هنا هنطبع الرسالة عشان لو فشل نعرف السبب الحقيقي (فلترة محتوى ولا اسم موديل)
            print(f"❌ Cleaner Error {response.status_code}: {result.get('error', {}).get('message')}")
            return raw_text

    except Exception as e:
        print(f"❌ Cleaner Request failed: {e}")
        return raw_text