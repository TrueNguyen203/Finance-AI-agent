import os
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from ..tools.search_tools import (
    search_company_overview,
    search_company_shareholders,
    search_company_officers,
    search_company_subsidaries,
    search_company_historical_price,
)

from ..tools.math_tools import (
    calculating_simple_moving_average,
    calculating_relative_strength_index,
    calculating_moving_average_convergence_divergence
)

def setup_agent():
    # --- Listing tools ---
    tools = [
        search_company_overview,
        search_company_shareholders,
        search_company_officers,
        search_company_subsidaries,
        search_company_historical_price,
        calculating_simple_moving_average,
        calculating_relative_strength_index,
        calculating_moving_average_convergence_divergence
    ]

    # --- Setup Agent ---
    model = ChatOllama(
        model="gpt-oss:120b-cloud", #gpt-oss:120b
        temperature=0,
        max_tokens=512,
        base_url="http://ollama:11434" #None if run on local
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
            Nếu ma trận quá dài (dài hơn 30x dòng) hãy chỉ đưa ra phần đầu và phần cuối của ma trận.
            Nếu không có thông tin, hãy trả lời 'Không tìm thấy thông tin'.
        """,
    )
    return agent