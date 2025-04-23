### Đối với **Windows/macOS/Linux (Ubuntu)**:
- Cần cài đặt đủ trước khi clone git
- Python **>=3.10**
```
Tải Python: https://www.python.org/downloads/windows/
Chọn bản ≥ 3.10
Tích vào "Add Python to PATH" khi cài
Sau đó kiểm tra:python --version
```
- NodeJS **>=18.x** và npm
```
Tải từ: https://nodejs.org
Chọn bản LTS (recommended)
Tự động cài cả node và npm
Sau khi cài, kiểm tra:
+ node -v
+ npm -v
Reset máy để Path cập nhật
```
- Cài git
```
Tải Git tại: https://git-scm.com
Trong quá trình cài chọn mặc định → Finish
```
---

## ⚙️ Bước 1: Clone project
```bash
git clone https://github.com/Quyenanh87/Chatbot.git
cd Chatbot
```

---

## 🐍 Bước 2: Cài đặt Backend
```bash
cd backend
```

### ✅ Cài Python ảo và thư viện:

#### Nếu dùng Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3-venv -y
sudo apt install python3-pip -y
```

#### Tạo môi trường ảo (tất cả hệ điều hành):
```bash
python3 -m venv venv          # Hoặc: python -m venv venv (trên Windows/macOS)
```

#### Kích hoạt môi trường ảo:
- Windows:
```bash
venv\Scripts\activate
```
- macOS/Linux:
```bash
source venv/bin/activate
```

#### Cài thư viện Python:
```bash
pip install -r ../requirements.txt
```

### ✅ Tạo file `.env`
Tạo file `backend/.env` và thêm API key của Gemini:
```env
GEMINI_API_KEY=your_google_gemini_api_key
Đây là API_key của em bình thường sẽ không để ở đây nhưng em để cho quý công ty dễ test
GEMINI_API_KEY=AIzaSyBPo2R3yqkM0rp62n1JH_0X8SOvYAw9Fr8
```

#### Chạy server FastAPI:
```bash
uvicorn main:app --reload
```
>  Nếu gặp lỗi `Form data requires "python-multipart"`, ctrl + C để thoát và cài thêm:
pip install python-multipart
> Server sẽ chạy tại `http://localhost:8000`

---

## 🌐 Bước 3: Chạy Frontend (React)
Mở 1 terminal khác 
```bash
cd Chatbot/frontend
```
> Nếu Ubuntu chưa cài Nodejs phải cài thêm:
sudo apt install nodejs npm 
> 
### Cài thư viện:
```bash
npm install
```

### Chạy ứng dụng:
```bash
npm start
```

> Ứng dụng sẽ chạy tại `http://localhost:3000`
