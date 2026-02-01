# gemini_cleaner.py
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def clean_text_with_gemini(raw_text: str) -> str:
    """
    Clean OCR-extracted text using Google Gemini AI
    """
    if not raw_text.strip():
        return ""
    
    try:
        prompt = f"""Clean this OCR-extracted text. Fix spelling/grammar, remove artifacts, and format professionally:

{raw_text}

Return only the cleaned text."""
        
        response = client.models.generate_content(
            model='gemini-1.5-pro',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=8192,
            )
        )
        
        return response.text
    
    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        print("⚠️ Returning raw text...")
        return raw_text