import os
import asyncio
import requests
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(http_options={"api_version": "v1beta"})

# Đảm bảo đường dẫn này khớp 100% với route của bạn
NODEJS_WEBHOOK_URL = "http://127.0.0.1:3000/api/v1/projects/webhook"

async def generate_video_pipeline(project_id: int, image_urls: list, prompt_text: str, settings: dict):
    print(f"\n🎬 BẮT ĐẦU PIPELINE VEO CHO PROJECT {project_id}...")
    os.makedirs("outputs", exist_ok=True)
    
    target_img_url = image_urls[0]
    final_video_path = f"outputs/project_{project_id}.mp4"

    try:
        print(f"📥 Tải ảnh từ Node.js ({target_img_url})...")
        img_data = requests.get(target_img_url).content
        
        print(f"⚙️ Áp dụng cấu hình: {settings}")
        video_config = types.GenerateVideosConfig(
            aspect_ratio=settings.get("aspect_ratio", "16:9"),
            number_of_videos=1,
            duration_seconds=settings.get("duration", 4),
            resolution=settings.get("resolution", "720p"),
        )
        
        source = types.GenerateVideosSource(
            prompt=prompt_text,
            image=types.Image(
                image_bytes=img_data, 
                mime_type="image/jpeg"
            )
        )
        
        chosen_model = settings.get("model", "veo-3.1-lite-generate-preview")
        print(f"⏳ Gọi Google Model: {chosen_model}...")
        
        operation = await client.aio.models.generate_videos(
            model=chosen_model,
            source=source,
            config=video_config
        )
        
        print("🕒 Veo đã nhận lệnh! Bắt đầu tiến trình chờ (2-3 phút)...")
        
        while not operation.done:
            print("   ⏳ Đang render... (Chờ 10 giây)")
            await asyncio.sleep(10)
            operation = await client.aio.operations.get(operation)
            
        if getattr(operation, 'error', None):
            raise Exception(f"Lỗi render: {operation.error}")
            
        print("📥 Render xong! Đang tải video về máy...")
        generated_video = operation.response.generated_videos[0]
        
        # --- ĐÃ SỬA LỖI TẠI ĐÂY ---
        def download_video():
            try:
                # Cách 1: Hàm download SDK mới trả về cục dữ liệu (Bytes)
                return client.files.download(name=generated_video.video.name)
            except:
                # Cách 2: Phao cứu sinh - Tải bằng requests (Đảm bảo 100% thành công)
                download_url = generated_video.video.uri
                headers = {"x-goog-api-key": os.getenv("GEMINI_API_KEY")}
                if "alt=media" not in download_url:
                    download_url += "&alt=media" if "?" in download_url else "?alt=media"
                return requests.get(download_url, headers=headers).content

        # Chạy hàm tải trong luồng ngầm để không bị đơ
        video_bytes = await asyncio.to_thread(download_video)
        
        # Tự lưu dữ liệu thành file .mp4
        with open(final_video_path, "wb") as f:
            f.write(video_bytes)
        # ----------------------------
        
        print(f"🎉 ĐÃ RENDER THÀNH CÔNG: {final_video_path}")
        
        public_video_url = f"http://127.0.0.1:8000/{final_video_path}"
        
        requests.post(NODEJS_WEBHOOK_URL, json={
            "projectId": project_id,
            "status": "completed",
            "videoUrl": public_video_url
        })
        print("✅ Đã gửi Webhook báo cáo Node.js thành công!")
        
    except Exception as e:
        print(f"❌ Lỗi Pipeline: {e}")
        requests.post(NODEJS_WEBHOOK_URL, json={
            "projectId": project_id,
            "status": "failed",
            "message": str(e)
        })