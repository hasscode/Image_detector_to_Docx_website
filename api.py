from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from io import BytesIO
import uuid
import os

# استيراد الوظائف من ملفاتك (تأكد أن الملفات بنفس هذه الأسماء في مجلدك)
from ocr import extract_text_from_images
from gemini_cleaner import clean_text_with_gemini
from docx_generator import create_docx

app = FastAPI(title="AI Vision OCR")

# إعداد CORS عشان الـ Frontend يعرف يكلم الـ Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# مجلد الملفات المؤقتة
TEMP_FOLDER = "temp_docs"
os.makedirs(TEMP_FOLDER, exist_ok=True)

# ربط مجلد الـ web عشان الـ CSS والـ JS يشتغلوا (المسار /web)
if os.path.exists("web"):
    app.mount("/web", StaticFiles(directory="web"), name="web")

# المسار الرئيسي لعرض الواجهة
@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = os.path.join("web", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Error: 404 - Web folder or index.html not found!</h1>"

# المسار الخاص بتحويل الصور
@app.post("/convert")
async def convert_images(files: List[UploadFile] = File(...)):
    try:
        images_data = []
        for file in files:
            content = await file.read()
            images_data.append(BytesIO(content))

        # 1. استخراج النص من الصور (OCR)
        raw_text = extract_text_from_images(images_data)
        
        if not raw_text.strip():
            raise HTTPException(status_code=400, detail="لم يتم العثور على نص في الصور")

        # 2. تنظيف النص وتنسيقه بواسطة المعالج الذكي (Gemini)
        clean_text = clean_text_with_gemini(raw_text)
        
        # 3. توليد ملف الوورد
        unique_id = uuid.uuid4().hex[:8]
        filename = f"Document_{unique_id}.docx"
        output_path = os.path.join(TEMP_FOLDER, filename)
        
        create_docx(clean_text, output_path)

        # 4. إرسال الملف النهائي للمستخدم
        return FileResponse(
            path=output_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    except Exception as e:
        print(f"Error during conversion: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# لتشغيل السيرفر مباشرة عند تشغيل الملف
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)