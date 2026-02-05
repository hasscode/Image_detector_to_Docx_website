import os
import uuid
from io import BytesIO
from typing import List

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import fitz  # المكتبة اللي لسه مثبتها PyMuPDF

# استدعاء ملفات المشروع
from ocr import extract_text_from_images
from gemini_cleaner import clean_text_with_gemini
from gpt_cleaner import clean_text_with_gpt
from docx_generator import create_docx

app = FastAPI(title="AI Vision OCR Multi-Model (PDF Support)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_FOLDER = "temp_docs"
os.makedirs(TEMP_FOLDER, exist_ok=True)

if os.path.exists("web"):
    app.mount("/static", StaticFiles(directory="web"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = os.path.join("web", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Error: 404 - Web folder or index.html not found!</h1>"

@app.post("/convert")
async def convert_files(
    files: List[UploadFile] = File(...),
    provider: str = Form("gemini")
):
    try:
        final_images_to_process = []

        for file in files:
            content = await file.read()
            
            # فحص نوع الملف: هل هو PDF؟
            if file.content_type == "application/pdf" or file.filename.lower().endswith(".pdf"):
                print(f"📄 Processing PDF with PyMuPDF: {file.filename}")
                
                # فتح ملف الـ PDF من الذاكرة
                doc = fitz.open(stream=content, filetype="pdf")
                print(f"🔢 Total Pages found: {len(doc)}")
                
                for i, page in enumerate(doc):
                    # تحويل الصفحة لصورة بجودة عالية (DPI 200)
                    pix = page.get_pixmap(dpi=200)
                    img_data = pix.tobytes("jpeg")
                    final_images_to_process.append(BytesIO(img_data))
                
                doc.close()
            
            # لو الملف صورة عادية (PNG, JPG, الخ)
            else:
                final_images_to_process.append(BytesIO(content))

        if not final_images_to_process:
            raise HTTPException(status_code=400, detail="لم يتم استلام أي ملفات صالحة للتحويل")

        print(f"🔄 Starting OCR for {len(final_images_to_process)} pages using: {provider}")

        # المرحلة الأولى: استخراج النص الخام من كل الصور/الصفحات
        raw_text = extract_text_from_images(final_images_to_process, provider=provider)
        
        if not raw_text.strip():
            raise HTTPException(status_code=400, detail="لم نتمكن من استخراج أي نص من الملفات المرفوعة")

        # المرحلة الثانية: تنظيف وتنسيق النص بناءً على الموديل المختار
        if provider == "gpt":
            print("🪄 Cleaning text with ChatGPT-4o-latest...")
            clean_text = clean_text_with_gpt(raw_text)
        else:
            print("🪄 Cleaning text with Gemini 1.5 Flash...")
            clean_text = clean_text_with_gemini(raw_text)
        
        # المرحلة الثالثة: توليد ملف الـ Word الاحترافي
        unique_id = uuid.uuid4().hex[:8]
        filename = f"Full_Report_{provider}_{unique_id}.docx"
        output_path = os.path.join(TEMP_FOLDER, filename)
        
        create_docx(clean_text, output_path)

        print(f"✅ Success! Generated: {filename}")

        return FileResponse(
            path=output_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    except Exception as e:
        print(f"❌ Critical Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)