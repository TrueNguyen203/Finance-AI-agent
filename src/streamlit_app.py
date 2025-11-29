import streamlit as st
import requests

# streamlit run src/streamlit_app.py

# -------------------------
# Streamlit Config
# -------------------------
st.set_page_config(page_title="Finance AI Agent", layout="wide")
st.title("💰 Finance AI Agent")
st.markdown("---")

# -------------------------
# API Configuration
# -------------------------
API_URL = "http://localhost:8000/ask"

# -------------------------
# Debug Info
# -------------------------
st.write("✅ Streamlit app đã load thành công")

# -------------------------
# Streamlit UI
# -------------------------
st.subheader("📋 Nhập câu hỏi của bạn:")

user_question = st.text_area(
    "Câu hỏi:",
    placeholder="Ví dụ: Hãy cho tôi biết về các công ty con của VCB",
    height=100
)

if st.button("🔍 Gửi", key="submit"):
    if user_question.strip():
        with st.spinner("⏳ Đang xử lý..."):
            try:
                st.write(f"📤 Gửi request tới: {API_URL}")
                
                # Gọi API
                response = requests.post(
                    API_URL,
                    json={"question": user_question},
                    timeout=120
                )
                
                st.write(f"✅ Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Hiển thị câu hỏi
                    st.subheader("📝 Câu hỏi của bạn:")
                    st.info(data.get("user_question", "N/A"))
                    
                    # Hiển thị tool được sử dụng
                    tools_used = data.get("tool_used", [])
                    if tools_used:
                        st.subheader("🔧 Tool được sử dụng:")
                        st.success(", ".join(tools_used))
                    
                    # Hiển thị câu trả lời
                    st.subheader("💡 Câu trả lời:")
                    answer = data.get("answer", "")
                    if answer:
                        st.markdown(answer)
                    else:
                        st.warning("Không có câu trả lời từ AI")
                    
                    # Debug: Hiển thị toàn bộ response
                    with st.expander("📊 Debug - Response JSON"):
                        st.json(data)
                else:
                    st.error(f"❌ Lỗi API: {response.status_code}")
                    st.error(response.text)
                    
            except requests.exceptions.ConnectionError as e:
                st.error(f"❌ Không thể kết nối đến API tại {API_URL}")
                st.error("💡 Hãy chắc chắn:")
                st.error("1. FastAPI server đang chạy: `python -m uvicorn main:app --reload`")
                st.error("2. Port 8000 không bị chiếm bởi ứng dụng khác")
                st.error(f"Chi tiết lỗi: {str(e)}")
            except Exception as e:
                st.error(f"❌ Lỗi: {str(e)}")
    else:
        st.warning("⚠️ Vui lòng nhập câu hỏi")

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888;">
    <p>Finance AI Agent - Powered by LangChain & Ollama</p>
</div>
""", unsafe_allow_html=True)