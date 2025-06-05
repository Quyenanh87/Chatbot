# Cooking Assistant - AI Chef Chatbot

Cooking Assistant là một chatbot thông minh được thiết kế để hỗ trợ người dùng trong việc nấu ăn. Với giao diện thân thiện và khả năng tương tác bằng tiếng Việt, chatbot có thể giúp bạn với các công thức nấu ăn, mẹo vặt trong bếp, và hướng dẫn chi tiết các bước thực hiện.

## Tính năng chính

- 🗣️ Tương tác bằng tiếng Việt tự nhiên
- 👩‍🍳 Cung cấp công thức nấu ăn chi tiết
- 📝 Hướng dẫn từng bước rõ ràng
- 💡 Chia sẻ mẹo vặt và kinh nghiệm nấu ăn
- 🎨 Giao diện người dùng hiện đại và thân thiện

## Công nghệ sử dụng

### Frontend
- React.js
- Tailwind CSS
- Axios
- Modern UI/UX với Glassmorphism design

### Backend
- FastAPI
- Google Generative AI
- Python 3.8+
- Uvicorn ASGI server

## Cài đặt và Chạy

### Backend

1. Tạo môi trường ảo và kích hoạt:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate   # Windows
```

2. Cài đặt dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Tạo file .env và thêm API key:
```
GOOGLE_API_KEY=your_api_key_here
```

4. Chạy server:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend

1. Cài đặt dependencies:
```bash
cd frontend
npm install
```

2. Chạy development server:
```bash
npm run dev
```

## Cấu trúc thư mục

```
cooking-assistant/
├── backend/
│   ├── data/
│   ├── models/
│   ├── services/
│   ├── tools/
│   ├── main.py
│   └── requirements.txt
└── frontend/
    ├── public/
    ├── src/
    │   ├── components/
    │   ├── assets/
    │   └── App.js
    ├── package.json
    └── tailwind.config.js
```

## API Endpoints

- `POST /chat`: Endpoint chính để tương tác với chatbot
  - Input: `{ "message": "string" }`
  - Output: `{ "reply": "string" }`

## Deployment

### Backend
- Đảm bảo tất cả dependencies trong requirements.txt được cài đặt
- Cấu hình CORS cho domain frontend
- Set up biến môi trường cho API keys

### Frontend
- Build production bundle: `npm run build`
- Đảm bảo API endpoint được cấu hình đúng trong production
- Static files được serve đúng cách

## Môi trường hỗ trợ

- Node.js 16+
- Python 3.8+
- Modern web browsers (Chrome, Firefox, Safari, Edge)



## Tác giả

Lưu Thế Quyền Anh

## License

MIT License
