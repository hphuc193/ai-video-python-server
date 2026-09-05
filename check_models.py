import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Lấy API Key từ file .env của bạn
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("🔍 Đang quét danh sách các Model Google khả dụng cho tài khoản của bạn...\n")

try:
    models = client.models.list()
    has_veo = False
    
    for model in models:
        print(f"📦 Tên Model: {model.name}")
        if 'veo' in model.name.lower():
            has_veo = True
            
    print("\n=======================================")
    if has_veo:
        print("🎉 TUYỆT VỜI! Tài khoản của bạn CÓ hỗ trợ Veo. Hãy copy tên model có chữ 'veo' ở trên thay vào file replicate_service.py nhé!")
    else:
        print("⚠️ TIẾC QUÁ! Tài khoản của bạn chưa được Google cấp quyền dùng Veo (hoặc chưa khả dụng ở khu vực này).")
        
except Exception as e:
    print(f"❌ Lỗi khi lấy danh sách: {e}")