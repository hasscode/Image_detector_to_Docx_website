# Image to DOCX Converter (OCR + AI)

A backend application built with FastAPI that converts images into a clean Word document using OCR and AI.

---

## Project Description

This project allows users to upload images, extract text using OCR, clean and organize the text using ChatGPT, and download the result as a DOCX file.

---

##  How It Works

1. Upload images
2. Extract text from images using OCR
3. Clean and format text using AI
4. Generate DOCX file
5. Download the final document

---

##  Technologies Used

- Python
- FastAPI
- Tesseract OCR
- OpenAI API
- python-docx

---

##  Project Structure

image_to_docx/
├── api.py
├── ocr.py
├── chatgpt.py
├── docx_generator.py
├── images/
├── output.docx
├── .env
└── README.md



---

##  Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn pytesseract pillow python-docx python-dotenv openai


# Environment Variables

Create a .env file in the project root:
OPENAI_API_KEY=API KEY

# Run Project
uvicorn api:app --reload


# API Endpoints

POST /upload-images

Upload multiple images to the server

POST /convert

Extract text from images

Clean text using AI

Download the generated DOCX file