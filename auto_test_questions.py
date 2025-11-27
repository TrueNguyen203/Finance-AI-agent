import requests

API_URL = "http://localhost:8000/ask"

questions = [
    "Lấy dữ liệu OHLCV 10 ngày gần nhất HPG?",
    "Lấy giá đóng của của mã VCB từ đầu tháng 11 theo khung 1d?",
    "Trong các mã BID, TCB và VCB mã nào có giá mở cửa thấp nhất trong 10 ngày qua",
    "Tổng khối lượng giao dịch (volume) của mã VIC trong vòng 1 tuần gần đây",
    "So sánh khối lượng giao dịch của VIC với HPG trong 2 tuần gần đây",
    "Danh sách cổ đông lớn của VCB",
    "Danh sách ban lãnh đạo đang làm việc của VCB",
    "Các công ty con thuộc VCB",
    "Lấy cho tôi toàn bộ tên các lãnh đạo đang làm việc của VCB",
    "Tính cho tôi SMA9 của mã VIC trong 2 tuần với timeframe 1d",
    "Tính cho tôi SMA9 và SMA20 của mã VIC trong 2 tháng với timeframe 1d",
    "Tính cho tôi RSI14 của TCB trong 1 tuần với timeframe 1m",
    "Tính SMA9 và SMA20 của mã TCB từ đầu tháng 11 đến nay theo timeframe 1m"
]

output_file = "test_results.txt"

with open(output_file, "w", encoding="utf-8") as f:
    for q in questions:
        payload = {"question": q}
        try:
            response = requests.post(API_URL, json=payload)
            data = response.json()

            user_question = data.get("user_question", "")
            tool_used = ", ".join(data.get("tool_used", []))
            answer = data.get("answer", "")

            f.write(f"user_question: {user_question}\n")
            f.write(f"tool_used: {tool_used}\n")
            f.write(f"answer: {answer}\n")
            f.write("-------------------\n\n\n")

        except Exception as e:
            f.write(f"user_question: {q}\n")
            f.write("tool_used: ERROR\n")
            f.write(f"answer: Lỗi khi gọi API: {e}\n")
            f.write("--------\n")

print(f"Đã ghi kết quả vào file {output_file}")
