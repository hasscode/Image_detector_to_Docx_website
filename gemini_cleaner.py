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
                    "text": f"""
                    Role: You are a Professional Medical Documentation Specialist and Senior Radiologist.

Task:
1. Extract & Correct: Fix any typos or OCR artifacts. Ensure 100% accuracy for medical terms.
2. Medical Contextualization: Complete any logical gaps in the medical context (e.g., CRL, BPD, HC, AC, FL).
3. Professional Formatting:
   - Use standard numbers (1, 2, 3) for main sections instead of Roman numerals (I, II, III).
   - Use (1.1, 1.2) for sub-sections if needed.
   - Use standard bullet points (•) for lists instead of asterisks (*).
   - Use Bold Headings (Markdown H1, H2).
   - Group related measurements (Biometry) clearly.
4. Language: Keep medical terms in English.
5. Return ONLY the final formatted document without any introductory text.

Text to process:
{raw_text}"""
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