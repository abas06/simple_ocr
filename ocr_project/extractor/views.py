from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PIL import Image
import pytesseract
import os
import base64

# PENTING UNTUK PENGGUNA WINDOWS:
# Buka tanda komentar (#) di bawah ini dan arahkan ke path tesseract.exe Anda jika terjadi error "TesseractNotFoundError"
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def index(request):
    context = {}
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']
        
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        allowed_extensions = ['.jpg', '.jpeg', '.png']
        
        if file_extension not in allowed_extensions:
            context['error'] = "Format file tidak diizinkan! Hanya file JPG, JPEG, dan PNG yang diperbolehkan."
            return render(request, 'extractor/index.html', context)
        
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        
        try:
            img = Image.open(file_path)
            extracted_text = pytesseract.image_to_string(img)
            
            # Encode gambar ke base64 SEBELUM file dihapus
            with open(file_path, 'rb') as f:
                img_data = base64.b64encode(f.read()).decode('utf-8')
            
            # Tentukan mime type
            mime_type = 'image/jpeg' if file_extension in ['.jpg', '.jpeg'] else 'image/png'
            
            context['extracted_text'] = extracted_text
            context['img_base64'] = f"data:{mime_type};base64,{img_data}"
            
        except Exception as e:
            context['error'] = f"Gagal memproses gambar: {str(e)}"
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
                
    return render(request, 'extractor/index.html', context)