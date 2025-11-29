from fastapi import FastAPI
from pydantic import BaseModel
from .agent import setup_agent


# python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
app = FastAPI()

# -------------------------
# Setup Agent
# -------------------------

agent = setup_agent()


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
