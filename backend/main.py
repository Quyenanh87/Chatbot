from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import aiofiles
import fitz  # PyMuPDF
import google.generativeai as genai

# Load biến môi trường từ .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Cấu hình Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.0-flash")

app = FastAPI()

# Cho phép gọi từ frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

class PdfQARequest(BaseModel):
    question: str

from datetime import datetime

@app.post("/chat")
async def chat(msg: Message):
    try:
        # Lấy thời gian hiện tại
        now = datetime.now()
        date = now.strftime("%A, %d/%m/%Y")
        time = now.strftime("%H:%M")

        # Thêm context vào prompt để LLM biết hôm nay là ngày nào
        context = (
            f"Hôm nay là {date}, hiện tại là {time}.\n\n"
            f"Trả lời câu hỏi sau một cách tự nhiên nhất:\n{msg.message}"
        )

        response = model.generate_content(context)
        return {"reply": response.text.strip() if response.text else "(Không có phản hồi)"}

    except Exception as e:
        print("🔥 Lỗi backend /chat:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})


# Lưu nội dung file PDF vào RAM khi upload
pdf_cache = {}

@app.post("/upload-pdf")
async def upload_pdf(pdf: UploadFile = File(...)):
    try:
        text = ""
        doc = fitz.open(stream=await pdf.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
        pdf_cache[pdf.filename] = text
        return {"status": "PDF đã được lưu tạm thành công.", "filename": pdf.filename}
    except Exception as e:
        print("🔥 Lỗi backend /upload-pdf:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/ask-pdf")
async def ask_from_pdf(filename: str = Form(...), question: str = Form(...)):
    try:
        if filename not in pdf_cache:
            return JSONResponse(status_code=404, content={"error": "PDF chưa được tải lên hoặc đã bị xoá."})

        pdf_text = pdf_cache[filename]
        prompt = f"Dựa trên nội dung sau trong file PDF, hãy trả lời câu hỏi: {question}\n\n{pdf_text[:4000]}"
        response = model.generate_content(prompt)
        return {"answer": response.text.strip() if response.text else "(Không có phản hồi)"}
    except Exception as e:
        print("🔥 Lỗi backend /ask-pdf:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})