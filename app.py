import streamlit as st
import google.genai as genai
from google import genai
import os

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])


# 2. HÀM ĐỌC TOÀN BỘ TÀI LIỆU SOP TỪ BẠN B (KIẾN THỨC NỀN - RAG)
def load_knowledge_base():
    knowledge_text = ""
    folder_path = "knowledge_base"
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                with open(
                    os.path.join(folder_path, filename), "r", encoding="utf-8"
                ) as f:
                    knowledge_text += f.read() + "\n\n"
    return knowledge_text


# Tải trước tài liệu vào bộ nhớ
SOP_KNOWLEDGE = load_knowledge_base()

# 3. CẤU HÌNH GIAO DIỆN WEB STREAMLIT
st.set_page_config(page_title="SecOps Chatbot NWC303", page_icon="🛡️")
st.title("🛡️ AI Chatbot Hỗ trợ Sự cố An ninh mạng LAN/Wi-Fi")
st.subheader("Đề tài nghiên cứu môn NWC303 - Nhóm [Tên nhóm bạn]")

# Khởi tạo lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Xin chào! Tôi là trợ lý hỗ trợ sự cố an ninh mạng. Hãy mô tả dấu hiệu lỗi mạng máy tính của bạn đang gặp phải bằng ngôn ngữ tự nhiên, tôi sẽ hướng dẫn bạn xử lý an toàn.",
        }
    ]

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 4. XỬ LÝ KHI USER NHẬP CÂU HỎI
if user_query := st.chat_input(
    "Ví dụ: Mạng bị chậm đột ngột và báo trùng địa chỉ IP..."
):
    # Hiển thị câu hỏi của user
    with st.chat_message("user"):
        st.write(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Gọi mô hình AI Gemini bằng cú pháp đời mới
    try:
        # Gộp tài liệu SOP vào System Instruction để ép AI đọc dữ liệu
        system_instruction = f"""
Bạn là một chuyên gia An ninh mạng (SecOps Engineer) hỗ trợ xử lý sự cố.
Dưới đây là tài liệu quy trình chuẩn (SOP) về các sự cố mạng:
{SOP_KNOWLEDGE}
"""

        # Gọi Client generate nội dung
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_query,
            config={"system_instruction": system_instruction},
        )

        # Lấy văn bản trả về từ Bot
        bot_response = response.text

    except Exception as e:
        bot_response = (
            f"Có lỗi kết nối hệ thống AI: {str(e)}. Vui lòng kiểm tra lại API Key."
        )

    # Hiển thị câu trả lời của Bot
    with st.chat_message("assistant"):
        st.write(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
