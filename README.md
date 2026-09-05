# 🧠 AI Video Generator - Python Processing Engine
 
Máy chủ độc lập (Worker) chịu trách nhiệm thực thi các tác vụ tính toán nặng nề nhất: xử lý trí tuệ nhân tạo, kết xuất đồ họa (render) và xử lý âm thanh. Thiết kế tách biệt giúp Backend Node.js không bao giờ bị nghẽn (Block).
 
## 🚀 Trách nhiệm chính (Core Responsibilities)
- **Biên kịch AI:** Gọi API Google Gemini phân tích hình ảnh đầu vào và tự động sáng tạo kịch bản/Prompt ngắn gọn, chuẩn xác.
- **Lồng tiếng (TTS):** Tích hợp Edge-TTS để chuyển kịch bản văn bản thành giọng đọc tự nhiên.
- **Render Hình ảnh (Video Gen):** Giao tiếp với Google Veo API để tạo video động từ hình ảnh và Prompt.
- **Hậu kỳ tự động:** Dùng MoviePy ghép Audio và Video lại với nhau, cắt thời lượng cho đồng bộ.
- **Tiến trình ngầm (Background Tasks):** Sử dụng `asyncio` để không block API Request, tự động gọi Webhook về Node.js khi hoàn tất.
## 🛠 Ngăn xếp công nghệ (Tech Stack)
- **Ngôn ngữ:** Python 3.10+
- **Framework:** FastAPI, Uvicorn
- **AI Integration:** Google GenAI SDK (Gemini & Veo)
- **Media Processing:** MoviePy, Edge-TTS
- **Networking:** HTTPX / Requests
## ⚙️ Hướng dẫn cài đặt
 
1. Clone dự án:
```bash
   git clone <repo_url>
```
 
2. Khởi tạo môi trường ảo (Virtual Environment):
```bash
   python -m venv venv
   source venv/bin/activate  # Trên Windows dùng: venv\Scripts\activate
```
 
3. Cài đặt thư viện (yêu cầu phải có file `requirements.txt`):
```bash
   pip install -r requirements.txt
```
 
4. Đặt khóa Google Gemini API vào file `.env`:
```env
   GEMINI_API_KEY=your_gemini_api_key_here
```
 
5. Chạy AI Server:
```bash
   uvicorn main:app --reload --port 8000
```
 
---
 
*Dự án thuộc Hệ sinh thái AI Video Generator.*
