import os
from gemini_vision import image_to_text       # تأكد من اسم الملف عندك
from gpt_vision import image_to_text_gpt     # تأكد من اسم الملف عندك

def extract_text_from_images(images_list: list, provider: str = "gemini") -> str:
    """
    الدالة دي هي حلقة الوصل.. بتاخد قايمة الصور واسم الموديل
    وترجع النص كامل.
    """
    full_text = ""
    
    for img_data in images_list:
        if provider == "gpt":
            print("🚀 Calling ChatGPT-4o Vision...")
            text = image_to_text_gpt(img_data)
        else:
            print("🚀 Calling Gemini Flash...")
            text = image_to_text(img_data)
            
        if text:
            # بنضيف فاصل بسيط بين نصوص الصور المختلفة
            full_text += text + "\n\n" + ("-" * 30) + "\n\n"
            
    return full_text