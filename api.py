from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from io import BytesIO
import uuid
import os

from ocr import extract_text_from_images
from gemini_cleaner import clean_text_with_gemini
from docx_generator import create_docx

app = FastAPI(title="AI Vision OCR Multi-Model")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_FOLDER = "temp_docs"
os.makedirs(TEMP_FOLDER, exist_ok=True)

# --- التعديل الجوهري هنا ---
# هنربط فولدر web مباشرة بـ "/" عشان الملفات تتحمل صح
if os.path.exists("web"):
    # البوابة اسمها static والمجلد الحقيقي اسمه web
    app.mount("/static", StaticFiles(directory="web"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = os.path.join("web", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Error: 404 - Web folder or index.html not found!</h1>"
# -------------------------

@app.post("/convert")
async def convert_images(
    files: List[UploadFile] = File(...),
    provider: str = Form("gemini")
):
    try:
        images_data = []
        for file in files:
            content = await file.read()
            images_data.append(BytesIO(content))

        print(f"🔄 Starting OCR process using: {provider}")

        raw_text = extract_text_from_images(images_data, provider=provider)
        
        if not raw_text.strip():
            raise HTTPException(status_code=400, detail="لم يتم العثور على نص")

        print("🪄 Cleaning text with Gemini AI...")
        clean_text = clean_text_with_gemini(raw_text)
        
        unique_id = uuid.uuid4().hex[:8]
        filename = f"Converted_{provider}_{unique_id}.docx"
        output_path = os.path.join(TEMP_FOLDER, filename)
        
        create_docx(clean_text, output_path)

        return FileResponse(
            path=output_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)