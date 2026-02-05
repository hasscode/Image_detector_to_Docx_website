from pdf2image import convert_from_bytes

def process_pdf_to_text(pdf_bytes, provider):
    # 1. تحويل الـ PDF لصور في الذاكرة
    images = convert_from_bytes(pdf_bytes, dpi=300)
    
    all_raw_text = ""
    
    # 2. اللوب على الصفحات (Batching)
    for i, image in enumerate(images):
        print(f"📄 Processing Page {i+1}/{len(images)}...")
        
        # تحويل صورة الصفحة لـ BytesIO عشان نبعتها للـ OCR اللي عملناه
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        # استخدام الـ OCR بتاعنا (GPT أو Gemini)
        page_text = extract_text_from_images([img_byte_arr], provider=provider)
        all_raw_text += f"\n\n--- Page {i+1} ---\n\n" + page_text
        
    return all_raw_text