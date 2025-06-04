from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
import logging

from models.tool import Tool
from tools.cooking_tools import CookingTools

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Initialize FastAPI app
app = FastAPI(title="Cooking Assistant")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

# Initialize cooking tools
cooking_tools = CookingTools()

# Define tools
tools = [
    Tool(
        name="recipe_finder",
        description="Tìm công thức nấu ăn dựa trên nguyên liệu, loại món hoặc độ khó",
        func=cooking_tools.recipe_finder
    ),
    Tool(
        name="ingredient_substitute",
        description="Gợi ý các nguyên liệu thay thế",
        func=cooking_tools.ingredient_substitute
    ),
    Tool(
        name="portion_calculator",
        description="Tính toán khẩu phần cho số người ăn mong muốn",
        func=cooking_tools.portion_calculator
    ),
    Tool(
        name="cooking_timer",
        description="Xem thông tin thời gian nấu của món ăn",
        func=cooking_tools.cooking_timer
    ),
    Tool(
        name="nutrition_info",
        description="Xem thông tin dinh dưỡng của món ăn",
        func=cooking_tools.nutrition_info
    ),
    Tool(
        name="list_ingredients",
        description="Liệt kê nguyên liệu cần thiết cho một món ăn cụ thể",
        func=cooking_tools.list_ingredients
    )
]

def create_cooking_prompt(query: str) -> str:
    """Create prompt for the cooking assistant"""
    tools_desc = "\n".join([f"- {tool.name}: {tool.description}" for tool in tools])
    return f"""Bạn là một Trợ lý Nấu ăn có quyền truy cập vào các công cụ sau:

{tools_desc}

Để sử dụng công cụ, hãy xuất ra JSON theo định dạng này:
{{"tool": "tên_công_cụ", "input": "đầu_vào_công_cụ"}}

Ví dụ:
- Để tìm công thức: {{"tool": "recipe_finder", "input": "cà ri gà"}}
- Để tìm nguyên liệu thay thế: {{"tool": "ingredient_substitute", "input": "trứng"}}
- Để tính khẩu phần: {{"tool": "portion_calculator", "input": "Mì Ý sốt bò bằm, 4"}}

Câu hỏi của người dùng: {query}

Suy nghĩ từng bước:
1. Hiểu người dùng cần hỗ trợ nấu ăn gì
2. Chọn công cụ phù hợp nhất
3. Định dạng đầu vào chính xác cho công cụ

Trả lời bằng tiếng Việt:"""

def execute_tool(tool_name: str, tool_input: str) -> str:
    """Execute a cooking tool"""
    logger.info(f"🔧 Executing tool: {tool_name}")
    logger.info(f"📥 Tool input: {tool_input}")
    
    for tool in tools:
        if tool.name == tool_name:
            # Special handling for portion calculator which needs two parameters
            if tool.name == "portion_calculator" and "," in tool_input:
                recipe, servings = tool_input.split(",")
                result = tool.func(recipe.strip(), int(servings.strip()))
                logger.info(f"📤 Tool output: {result}")
                return result
            result = tool.func(tool_input)
            logger.info(f"📤 Tool output: {result}")
            return result
    
    error_msg = f"Không tìm thấy công cụ {tool_name}"
    logger.error(f"❌ {error_msg}")
    return error_msg

@app.post("/chat")
async def chat(msg: Message):
    try:
        logger.info(f"📝 Received message: {msg.message}")
        
        # Đầu tiên, phân tích xem câu hỏi có cần dùng tool không
        analysis_prompt = f"""Bạn là một đầu bếp thân thiện, vui vẻ và chuyên nghiệp.
Hãy phân tích câu hỏi sau và quyết định cách trả lời phù hợp:

Câu hỏi: {msg.message}

HƯỚNG DẪN:
1. Nếu là câu hỏi thông thường (chào hỏi, hỏi thăm, trò chuyện, giới thiệu, v.v.) -> Trả lời trực tiếp, thân thiện và tự nhiên
2. Nếu là câu hỏi về nấu ăn cần tra cứu, sử dụng một trong các công cụ sau:
   - Tìm công thức: {{"tool": "recipe_finder", "input": "tên món"}}
   - Liệt kê nguyên liệu: {{"tool": "list_ingredients", "input": "tên món"}}
   - Tìm nguyên liệu thay thế: {{"tool": "ingredient_substitute", "input": "nguyên liệu"}}
   - Tính khẩu phần: {{"tool": "portion_calculator", "input": "tên món, số người"}}
   - Xem thời gian nấu: {{"tool": "cooking_timer", "input": "tên món"}}
   - Xem dinh dưỡng: {{"tool": "nutrition_info", "input": "tên món"}}

VÍ DỤ PHÂN LOẠI:
- "chào bạn" -> "Xin chào! Tôi là đầu bếp của bạn đây. Bạn cần giúp gì về nấu ăn không?"
- "nguyên liệu nấu phở" -> {{"tool": "list_ingredients", "input": "phở"}}
- "cách nấu phở" -> {{"tool": "recipe_finder", "input": "phở"}}

Lưu ý: 
- KHÔNG BAO GIỜ hiển thị JSON hoặc tên công cụ trong câu trả lời
- Luôn giữ vai trò là đầu bếp trong mọi câu trả lời
- Trả lời bằng tiếng Việt, thân thiện và tự nhiên
- Có thể đưa ra gợi ý về nấu ăn trong các câu trò chuyện

Trả lời:"""

        initial_response = model.generate_content(analysis_prompt)
        initial_text = initial_response.text.strip()
        logger.info(f"🤖 Initial AI response: {initial_text}")
        
        try:
            # Kiểm tra xem response có chứa JSON không
            json_start = initial_text.find("{")
            json_end = initial_text.rfind("}") + 1
            
            if json_start != -1 and json_end != 0:
                json_str = initial_text[json_start:json_end]
                regular_text = (initial_text[:json_start] + initial_text[json_end:]).strip()
                
                logger.info(f"🔍 Detected tool call in response: {json_str}")
                
                # Parse JSON để sử dụng tool
                tool_call = json.loads(json_str)
                if "tool" in tool_call and "input" in tool_call:
                    tool_result = execute_tool(tool_call["tool"], tool_call["input"])
                    
                    final_prompt = f"""Với vai trò là một đầu bếp thân thiện, hãy trả lời dựa trên thông tin sau:

Câu hỏi: {msg.message}
Thông tin tra cứu: {tool_result}

YÊU CẦU:
1. Trả lời như đang trò chuyện tự nhiên, KHÔNG đề cập đến việc tra cứu hay công cụ
2. Giải thích mọi thứ dễ hiểu, thân thiện
3. Thêm các mẹo và lời khuyên hữu ích nếu phù hợp
4. Khuyến khích người dùng nấu ăn và thử nghiệm
5. Luôn giữ giọng điệu vui vẻ, nhiệt tình của một đầu bếp

Trả lời:"""
                    
                    final_response = model.generate_content(final_prompt)
                    final_text = final_response.text.strip()
                    logger.info(f"🎯 Final response: {final_text}")
                    return {"reply": final_text}
                
            # Nếu không có JSON hoặc không parse được, trả về text thường
            logger.info("📢 No tool call needed, returning direct response")
            return {"reply": initial_text}
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON parse error: {str(e)}")
            return {"reply": initial_text}

    except Exception as e:
        error_msg = f"🔥 Backend error: {str(e)}"
        logger.error(error_msg)
        return JSONResponse(
            status_code=500, 
            content={
                "error": "Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại sau!"
            }
        )