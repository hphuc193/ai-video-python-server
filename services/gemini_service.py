import requests
from PIL import Image
from io import BytesIO
import json
import asyncio
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

# Chuyển hàm này thành Async để đồng bộ với toàn bộ hệ thống
async def generate_script_and_prompts(image_urls: list, user_idea: str = ""):
    print(f"🧠 Bắt đầu gọi Gemini phân tích {len(image_urls)} bức ảnh...")
    
    image_parts = []
    for url in image_urls:
        try:
            img_response = requests.get(url)
            img = Image.open(BytesIO(img_response.content))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            image_parts.append(img)
        except Exception as e:
            print(f"❌ Lỗi tải ảnh từ Node.js ({url}): {e}")
            return None
            
    prompt_text = f"""
    Bạn là một đạo diễn video quảng cáo chuyên nghiệp.
    Hãy phân tích các bức ảnh sản phẩm tôi cung cấp kèm theo đây.
    Ý tưởng/Yêu cầu của khách hàng: {user_idea if user_idea else "Làm một video thật phong cách, thu hút sự chú ý"}
    
    Nhiệm vụ của bạn là trả về ĐÚNG ĐỊNH DẠNG JSON với cấu trúc sau:
    {{
        "voiceover": "Kịch bản lời đọc tiếng Việt, dài khoảng 10-15 giây, thật hấp dẫn, bắt tai và khớp với sản phẩm.",
        "video_prompts": [
            "Prompt tiếng anh miêu tả chuyển động, ánh sáng cho ảnh 1",
            "Prompt tiếng anh miêu tả chuyển động, ánh sáng cho ảnh 2"
        ]
    }}
    Chú ý CỰC KỲ QUAN TRỌNG: Số lượng phần tử trong mảng 'video_prompts' phải bằng ĐÚNG {len(image_urls)}.
    """
    
    contents = image_parts + [prompt_text]
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            # Dùng client.aio để chạy bất đồng bộ, không làm đơ server
            response = await client.aio.models.generate_content(
                model='gemini-3.6-flash', # Hoặc gemini-1.5-flash tùy version bạn có
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            data = json.loads(response.text)
            print("✅ Gemini đã viết xong kịch bản!")
            return data
            
        except Exception as e:
            error_msg = str(e)
            if "503" in error_msg or "UNAVAILABLE" in error_msg:
                print(f"⚠️ Google Server đang bận. Đang thử lại lần {attempt + 1}/{max_retries}...")
                await asyncio.sleep(3)
            else:
                print("❌ Lỗi TỪ GEMINI API:", e)
                return None
                
    print("❌ Đã thử lại nhiều lần nhưng server Google vẫn quá tải. Vui lòng thử lại sau!")
    return None