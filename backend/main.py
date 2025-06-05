from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
import logging
from typing import Dict, List, Optional

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
    session_id: Optional[str] = None

# Initialize cooking tools
cooking_tools = CookingTools()

# Initialize conversation memory
conversation_memory: Dict[str, List[dict]] = {}

# Define tools
tools = [
    Tool(
        name="recipe_finder",
        description="Use when user asks for a specific recipe. Input: dish name (e.g. 'pho', 'pasta'). Returns full recipe with steps.",
        func=cooking_tools.recipe_finder
    ),
    Tool(
        name="recipe_recommender",
        description="Use when user needs dish suggestions. Input: cooking time (minutes), difficulty (1-5), servings. Returns suitable recipes.",
        func=cooking_tools.recipe_recommender
    ),
    Tool(
        name="ingredient_substitute",
        description="Use when user asks about ingredient replacements. Input: ingredient name. Returns possible substitutes.",
        func=cooking_tools.ingredient_substitute
    ),
    Tool(
        name="portion_calculator",
        description="Use when user wants to adjust recipe portions. Input: 'dish_name,servings'. Returns adjusted ingredients.",
        func=cooking_tools.portion_calculator
    ),
    Tool(
        name="cooking_timer",
        description="Use when user asks about cooking duration. Input: dish name. Returns cooking time breakdown.",
        func=cooking_tools.cooking_timer
    ),
    Tool(
        name="nutrition_info",
        description="Use when user asks about nutritional values. Input: dish name. Returns nutrition facts per serving.",
        func=cooking_tools.nutrition_info
    ),
    Tool(
        name="list_ingredients",
        description="Use when user asks what ingredients are needed. Input: dish name. Returns complete ingredient list.",
        func=cooking_tools.list_ingredients
    )
]

def create_cooking_prompt(query: str, context: List[dict] = None) -> str:
    """Create prompt for the cooking assistant with conversation context"""
    tools_desc = "\n".join([f"- {tool.name}: {tool.description}" for tool in tools])
    
    context_str = ""
    if context:
        context_str = "\nConversation history:\n" + "\n".join([
            f"{'User' if msg.get('isUser') else 'Chef'}: {msg.get('text', '')}"
            for msg in context[-5:]  # Only keep last 5 messages
        ])
    
    return f"""You are a professional and enthusiastic Chef. Always provide concise, focused responses without unnecessary details.

RESPONSE RULES:
1. Keep responses short and focused (2-3 sentences per point)
2. Focus on the most important information
3. No unnecessary details or embellishments
4. No repetition
5. No flowery language or long exclamations

REQUEST HANDLING RULES:
1. ALWAYS call recipe_finder immediately when the query contains:
   - "want to cook X"
   - "how to make X"
   - "recipe for X"
   - "prepare X"
   - "cook X"
   Where X is the dish name. NO EXCEPTIONS to this rule.

2. For ingredient queries:
   - ALWAYS call list_ingredients immediately
   - DO NOT explain ingredient purposes
   - Keep the list concise

3. For users seeking recipe suggestions:
   - Ask only 3 things: cooking time, difficulty, number of servings
   - Use recipe_recommender for suggestions

4. When recipe is not in database:
   - Respond with a simple "Sorry, I don't have this recipe"
   - Suggest using recipe_recommender
   - DO NOT provide cooking tips when data is missing

5. For nutrition queries:
   - ALWAYS call nutrition_info immediately when query contains:
     - "dinh dưỡng"
     - "calories"
     - "protein"
     - "chất dinh dưỡng"
     - "giá trị dinh dưỡng"
   - DO NOT call list_ingredients for nutrition queries
   - Keep nutrition information clear and concise

QUERY ANALYSIS EXAMPLES:
"want to cook pho" -> Return:
{{"tool": "recipe_finder", "input": "pho"}}

"how to make pasta" -> Return:
{{"tool": "recipe_finder", "input": "pasta"}}

"ingredients for pho" -> Return:
{{"tool": "list_ingredients", "input": "pho"}}

"dinh dưỡng phở bò" -> Return:
{{"tool": "nutrition_info", "input": "phở bò"}}

GOOD RESPONSE EXAMPLES:
- "Sorry, I don't have this recipe. Would you like me to suggest something else?"
- "For pho, you need: beef bones 2kg, beef 500g, rice noodles 1kg, and seasonings"
- "Please tell me your preferred cooking time and number of servings for suggestions"
- "Phở bò contains 450 calories per serving, with 25g protein"

BAD RESPONSE EXAMPLES:
- "Oh wow! Pasta is amazing! Although I don't have the recipe..." (too verbose)
- "To make delicious pho, you need these ingredients. Beef bones are the soul..." (unnecessary details)
- "Let me check the nutritional database..." (mentioning tool usage)

{context_str}

User query: {query}

Thinking steps:
1. Check if query matches cooking patterns
2. If yes -> ALWAYS call recipe_finder, NO EXCEPTIONS
3. If no -> Identify request type and use appropriate tool
4. Keep response concise and focused

Note: Final response to user MUST be in Vietnamese with correct grammar and spelling."""

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
        
        # Get or create conversation history
        session_id = msg.session_id or "default"
        if session_id not in conversation_memory:
            conversation_memory[session_id] = []
        
        # Add user message to history
        conversation_memory[session_id].append({
            "isUser": True,
            "text": msg.message
        })
        
        # Đầu tiên, phân tích xem câu hỏi có cần dùng tool không
        analysis_prompt = create_cooking_prompt(
            msg.message,
            context=conversation_memory[session_id][-5:]  # Truyền 5 tin nhắn gần nhất
        )
        
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
                    
                    final_prompt = f"""With your role as a friendly chef, please respond based on this information:

Question: {msg.message}
Tool result: {tool_result}

REQUIREMENTS:
1. Respond naturally as in a conversation, DO NOT mention lookups or tools.
2. Explain everything in a clear, friendly manner.
3. Add useful tips and advice when appropriate.
4. Encourage users to cook and experiment.
5. Always maintain a cheerful, enthusiastic chef's tone.
6. If the dish is not in the database, respond briefly and don't provide recipes.

Note: Response MUST be in Vietnamese with correct grammar and spelling.

Response:"""
                    
                    final_response = model.generate_content(final_prompt)
                    final_text = final_response.text.strip()
                    logger.info(f"🎯 Final response: {final_text}")
                    
                    # Add bot response to history
                    conversation_memory[session_id].append({
                        "isUser": False,
                        "text": final_text
                    })
                    
                    return {"reply": final_text}
                
            # Nếu không có JSON hoặc không parse được, trả về text thường
            logger.info("📢 No tool call needed, returning direct response")
            
            # Add bot response to history
            conversation_memory[session_id].append({
                "isUser": False,
                "text": initial_text
            })
            
            return {"reply": initial_text}
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON parse error: {str(e)}")
            
            # Add bot response to history even if there's an error
            conversation_memory[session_id].append({
                "isUser": False,
                "text": initial_text
            })
            
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