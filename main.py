import os
from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware # Thêm import CORS
from services.veo_service import generate_video_pipeline
import uvicorn 

app = FastAPI()

# 1. Bật CORS để Web Admin (React - cổng 5173) có thể gọi API trực tiếp sang Python (cổng 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Hoặc giới hạn ["http://localhost:5173"] cho an toàn
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

class GenerateRequest(BaseModel):
    projectId: int
    images: list
    prompt_idea: str
    settings: dict

@app.post("/api/generate")
async def generate_video(request: GenerateRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        generate_video_pipeline,
        request.projectId,
        request.images,
        request.prompt_idea,
        request.settings
    )
    return {"message": f"Đã nhận Project {request.projectId}, đang xử lý ngầm..."}

# =======================================================
# HÀM MỚI: API GIÁM SÁT TÀI NGUYÊN CHO ADMIN
# =======================================================
@app.get("/api/admin/health")
async def get_server_health():
    try:
        output_dir = "outputs"
        total_size_bytes = 0
        file_count = 0

        # Kiểm tra và quét thư mục outputs
        if os.path.exists(output_dir):
            for filename in os.listdir(output_dir):
                filepath = os.path.join(output_dir, filename)
                if os.path.isfile(filepath):
                    total_size_bytes += os.path.getsize(filepath)
                    file_count += 1
        
        # Đổi ra Megabyte (MB)
        total_size_mb = total_size_bytes / (1024 * 1024)

        return {
            "status": "online",
            "message": "Server AI đang hoạt động tốt!",
            "storage": {
                "fileCount": file_count,
                "totalSizeMB": round(total_size_mb, 2)
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)