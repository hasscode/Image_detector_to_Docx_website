from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from io import BytesIO
import uuid
import os

from ocr import extract_text_from_images
from gemini_cleaner import clean_text_with_gemini
from docx_generator import create_docx

app = FastAPI(title="Gemini OCR to DOCX")

# مهم جداً للسماح للصفحة بالاتصال بالسيرفر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_FOLDER = "temp_docs"
os.makedirs(TEMP_FOLDER, exist_ok=True)

@app.post("/convert")
async def convert_images(files: List[UploadFile] = File(...)):
    images = []
    for file in files:
        content = await file.read()
        images.append(BytesIO(content))

    # تنفيذ العملية بالكامل
    raw_text = extract_text_from_images(images)
    if not raw_text.strip():
        return {"error": "لم يتم استخراج نص"}

    clean_text = clean_text_with_gemini(raw_text)
    
    filename = f"{uuid.uuid4()}.docx"
    output_path = os.path.join(TEMP_FOLDER, filename)
    create_docx(clean_text, output_path)

    return FileResponse(
        path=output_path,
        filename="converted_by_gemini.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )