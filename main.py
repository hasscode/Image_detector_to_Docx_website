import os
from gemini_vision import image_to_text
from docx_generator import create_docx

BASE_DIR = os.path.dirname(__file__)
IMAGES_FOLDER = os.path.join(BASE_DIR, "images")
OUTPUT_FILE = "output_docx_result.docx" # غيرنا الاسم عشان نتجنب الـ Permission Error

def main():
    final_text = ""
    
    if not os.path.exists(IMAGES_FOLDER) or not os.listdir(IMAGES_FOLDER):
        print("❌ Folder 'images' is empty or not found!")
        return

    print("🚀 Starting Professional Image-to-Word Conversion...")

    for filename in sorted(os.listdir(IMAGES_FOLDER)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(IMAGES_FOLDER, filename)
            text = image_to_text(image_path)
            if text:
                final_text += text + "\n\n" + ("-"*30) + "\n\n"

    if final_text.strip():
        print("📄 Saving to Word...")
        create_docx(final_text, OUTPUT_FILE)
        print(f"✅ Success! File saved as: {OUTPUT_FILE}")
    else:
        print("❌ Failed to extract any text.")

if __name__ == "__main__":
    main()