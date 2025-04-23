### Đối với **Windows/macOS/Linux (Ubuntu)**:
- Python **>=3.10**
- NodeJS **>=18.x** và npm
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

> 🔧 Nếu gặp lỗi `Form data requires "python-multipart"`, cài thêm:
```bash
pip install python-multipart
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

> Server sẽ chạy tại `http://localhost:8000`

---

## 🌐 Bước 3: Chạy Frontend (React)
Mở 1 terminal khác 
```bash
cd Chatbot/frontend
```

### Cài thư viện:
```bash
npm install
```

### Chạy ứng dụng:
```bash
npm start
```

> Ứng dụng sẽ chạy tại `http://localhost:3000`