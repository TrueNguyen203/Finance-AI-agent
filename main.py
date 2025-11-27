from fastapi import FastAPI
from pydantic import BaseModel
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from tools import (
    search_company_overview,
    search_company_shareholders,
    search_company_officers,
    search_company_subsidaries,
    search_company_historical_price,
    calculating_simple_moving_average,
    calculating_relative_strength_index
)

app = FastAPI()

# -------------------------
# Setup Agent
# -------------------------
tools = [
    search_company_overview,
    search_company_shareholders,
    search_company_officers,
    search_company_subsidaries,
    search_company_historical_price,
    calculating_simple_moving_average,
    calculating_relative_strength_index,
]

model = ChatOllama(
    model="gpt-oss:120b-cloud",
    temperature=0,
    max_tokens=512,
)

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="""
        Bạn là nhân viên truy vấn thông tin, so sánh và phân tích tài chính.
        Hãy sử dụng tool để tìm thông tin và trả lời người dùng ngắn gọn dựa theo 1 phần hoặc toàn bộ kết quả trả về từ tool.
        Không lặp lại hay lịch sử hội thoại.
        Hãy luôn trả lời bằng Tiếng Việt.
        Giải thích thật ngắn gọn kèm theo dẫn chứng, sử dụng ma trận thông tin nếu cần.
        Nếu ma trận quá dài hãy chỉ đưa ra phần đầu và phần cuối của ma trận.
        Nếu không có thông tin, hãy trả lời 'Không tìm thấy thông tin'.
    """,
)

# -------------------------
# Request Model
# -------------------------
class Query(BaseModel):
    question: str


# -------------------------
# API Endpoint
# -------------------------
@app.post("/ask")
async def ask_agent(payload: Query):
    user_question = payload.question

    # --- 1. Lấy câu hỏi người dùng ---
    result = agent.invoke({"messages": [{"role": "user", "content": user_question}]})

    # --- 2. Lấy tool đã sử dụng ---
    tools_used = []
    messages = result.get("messages", [])
    for msg in messages:
        if hasattr(msg, "name") and msg.name:
            tools_used.append(msg.name)

    tools_used = list(set(tools_used))

    # --- 3. Lấy câu trả lời cuối cùng của AI ---
    final_answer = None
    for msg in messages:
        if msg.__class__.__name__ == "AIMessage":
            final_answer = msg.content

    return {
        "user_question": user_question,
        "tool_used": tools_used,
        "answer": final_answer
    }
