import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# تعريف العميل باستخدام المفتاح من الـ .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_text_with_gpt(raw_text: str) -> str:
    if not raw_text.strip():
        return ""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o", # نفس الموديل القوي
            messages=[
                {
                    "role": "system",
                    "content": "You are a Professional Medical Documentation Specialist and Senior Radiologist."
                },
                {
                    "role": "user",
                    "content": f"""
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
                }
            ],
            temperature=0.3 # دقة أعلى وهلوسة أقل
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"❌ GPT Cleaner Error: {e}")
        return raw_text