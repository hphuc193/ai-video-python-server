import edge_tts
import os
import asyncio # Thêm thư viện asyncio để xử lý thời gian chờ trong hàm async

async def generate_voiceover(text: str, project_id: int):
    print("🎙️ Bắt đầu tạo giọng đọc AI...")
    
    # Sử dụng giọng nữ tiếng Việt mặc định
    voice = "vi-VN-HoaiMyNeural" 
    
    # Tạo thư mục 'outputs' để chứa các file sinh ra nếu chưa có
    os.makedirs("outputs", exist_ok=True)
    
    # Đặt tên file theo ID dự án
    output_file = f"outputs/voice_{project_id}.mp3"
    
    # CƠ CHẾ TỰ ĐỘNG THỬ LẠI (Tối đa 3 lần)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_file)
            
            print(f"✅ Đã lưu xong file âm thanh tại: {output_file}")
            return output_file
            
        except Exception as e:
            error_msg = str(e)
            print(f"⚠️ Máy chủ TTS bận hoặc rớt mạng (Lần {attempt + 1}/{max_retries}): {error_msg}")
            
            if attempt < max_retries - 1:
                print("⏳ Đang thử kết nối lại...")
                await asyncio.sleep(2) # Nghỉ 2 giây rồi thử lại
            else:
                print("❌ Lỗi khi tạo giọng đọc TTS: Đã thử lại nhiều lần nhưng thất bại.")
                return None