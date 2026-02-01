import os
from gemini_vision import image_to_text

def extract_text_from_images(images_list: list) -> str:
    """
    بتاخد قائمة من الصور (سواء مسارات أو ملفات مفتوحة) وبتحولها لنص
    """
    full_text = ""
    
    for img_data in images_list:
        # بننادي دالة Gemini اللي عملناها قبل كدة
        text = image_to_text(img_data)
        if text:
            full_text += text + "\n\n" + ("="*30) + "\n\n"
            
    return full_text