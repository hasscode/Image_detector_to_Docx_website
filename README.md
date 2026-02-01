🚀 Image to DOCX Converter (Gemini Vision AI)
A professional backend application built with FastAPI that converts images into structured, clean Word documents using state-of-the-art AI Vision.

🌟 Project Overview
This project leverages Google Gemini 1.5 Flash to perform high-accuracy OCR and text cleaning in one step. It transforms messy text from images into a polished, formatted DOCX file.

Key Features:
AI-Powered OCR: Uses Gemini Vision to "see" and read text more accurately than traditional OCR.

Automatic Formatting: AI cleans, fixes grammar, and organizes the text.

Batch Processing: Upload multiple images and get a single merged document.

Flexible AI Backend: Designed to switch between Google Gemini and OpenAI (GPT-4o) easily.

🛠️ Technologies Used
Python 3.10+

FastAPI: High-performance web framework.

Google Gemini API: For Image-to-Text extraction.

Requests: For fast, direct API communication.

python-docx: To generate professional Word files.

📂 Project Structure
Plaintext
image_to_docx/
├── api.py              # FastAPI routes and file handling
├── ocr.py              # Logic for extracting text
├── gemini_vision.py    # Direct API calls to Gemini Flash
├── gemini_cleaner.py   # AI text processing and formatting
├── docx_generator.py   # Word document styling and creation
├── web/                # Frontend (HTML/JS)
├── temp_docs/          # Temporary storage for generated files
├── .env                # API Keys (Excluded from Git)
└── README.md
⚙️ Setup & Installation
Clone the project:

Bash
git clone https://github.com/hasscode/Image_detector_to_Docx_website.git
cd Image_detector_to_Docx_website
Install Dependencies:

Bash
pip install -r requirements.txt
Configure Environment Variables:
Create a .env file in the root directory:

مقتطف الرمز
# Current AI Provider: Google Gemini
GOOGLE_API_KEY=your_gemini_api_key_here

# Future AI Provider: OpenAI (Optional)
# OPENAI_API_KEY=your_openai_api_key_here
Run the Application:

Bash
uvicorn api:app --host 0.0.0.0 --port 10000
🔄 Switching to OpenAI
The project is designed to be Modular. To switch to OpenAI GPT-4o:

Replace GOOGLE_API_KEY with OPENAI_API_KEY in your .env.

Update the ocr.py or gemini_cleaner.py to use the OpenAI Python SDK.

Update requirements.txt to include openai.

📡 API Endpoints
POST /convert: Accepts multiple images, processes them through AI, and returns a downloadable .docx file.