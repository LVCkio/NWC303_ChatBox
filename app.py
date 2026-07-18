import streamlit as st
import google.genai as genai
from google import genai
import os
from PIL import Image

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
st.subheader("Đề tài nghiên cứu môn NWC303 - Nhóm 3")

# Khởi tạo lịch sử chat (phải đặt trước sidebar vì sidebar truy cập messages)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Xin chào! Tôi là trợ lý hỗ trợ sự cố an ninh mạng. Hãy mô tả dấu hiệu lỗi mạng máy tính của bạn đang gặp phải bằng ngôn ngữ tự nhiên, tôi sẽ hướng dẫn bạn xử lý an toàn.",
        }
    ]

# =============================================
# FEATURE 1: SIDEBAR - Team Info, Clear Chat, Export Report
# =============================================
with st.sidebar:
    st.title("🛡️ NWC303 SecOps Chatbot")
    st.markdown("---")

    st.divider()

    # Nút xóa lịch sử chat
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Xin chào! Tôi là trợ lý hỗ trợ sự cố an ninh mạng. Hãy mô tả dấu hiệu lỗi mạng máy tính của bạn đang gặp phải bằng ngôn ngữ tự nhiên, tôi sẽ hướng dẫn bạn xử lý an toàn.",
            }
        ]
        st.rerun()

    st.markdown("---")

    # FEATURE 3: EXPORT INCIDENT REPORT
    def generate_report():
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("  BÁO CÁO SỰ CỐ AN NINH MẠNG - NWC303 SecOps Chatbot")
        report_lines.append("=" * 60)
        report_lines.append("")
        for i, msg in enumerate(st.session_state.messages):
            role_label = "🛡️ TRỢ LÝ" if msg["role"] == "assistant" else "👤 NGƯỜI DÙNG"
            report_lines.append(f"--- [{role_label}] ---")
            report_lines.append(msg["content"])
            report_lines.append("")
        report_lines.append("=" * 60)
        report_lines.append("  KẾT THÚC BÁO CÁO")
        report_lines.append("=" * 60)
        return "\n".join(report_lines)

    st.download_button(
        label="📥 Tải Báo Cáo Sự Cố (TXT)",
        data=generate_report(),
        file_name="incident_report.txt",
        mime="text/plain",
        use_container_width=True,
    )



# =============================================
# HÀM HIỂN THỊ PHẢN HỒI VỚI VISUAL ALERT (FEATURE 4)
# =============================================
def display_bot_response(response_text):
    """Hiển thị phản hồi của bot, kèm cảnh báo khẩn cấp nếu phát hiện."""
    emergency_keywords = ["HÀNH ĐỘNG KHẨN CẤP", "NGẮT KẾT NỐI"]
    is_emergency = any(kw in response_text for kw in emergency_keywords)

    if is_emergency:
        st.error("🚨 CẢNH BÁO KHẨN CẤP: Phát hiện sự cố nghiêm trọng! Hãy thực hiện ngay các bước bên dưới!", icon="🔥")

    st.markdown(response_text)


# Hiển thị lịch sử chat (với custom avatar)
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🛡️"
    with st.chat_message(message["role"], avatar=avatar):
        if message["role"] == "assistant":
            display_bot_response(message["content"])
        else:
            st.write(message["content"])

# =============================================
# FEATURE 2: QUICK ACTION PROMPTS
# =============================================
st.markdown("#### ⚡ Hành động nhanh:")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🚨 Kiểm tra mạng chậm/trùng IP", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "🚨 Kiểm tra mạng chậm/trùng IP"})
        st.rerun()
with col2:
    if st.button("📶 Quét Wi-Fi lạ", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "📶 Quét Wi-Fi lạ"})
        st.rerun()
with col3:
    if st.button("🎣 Web lừa đảo", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "🎣 Web lừa đảo"})
        st.rerun()
with col4:
    if st.button("🎮 Diễn tập Thực chiến", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Hãy đóng vai hacker và đưa ra một tình huống diễn tập Phishing hoặc Malware để tôi xử lý."})
        st.rerun()

# 4. XỬ LÝ KHI USER NHẬP CÂU HỎI VÀ ĐÍNH KÈM FILE
with st.expander("📁 Đính kèm Ảnh màn hình hoặc File Log (Tùy chọn)", expanded=False):
    uploaded_file = st.file_uploader("📎 Kéo thả hoặc chọn file", type=["png", "jpg", "jpeg", "txt", "csv"])

if chat_query := st.chat_input("Ví dụ: Mạng bị chậm đột ngột và báo trùng địa chỉ IP..."):
    st.session_state.messages.append({"role": "user", "content": chat_query})
    st.rerun()

# =============================================
# CENTRAL LOGIC: XỬ LÝ GENERATE KHI TIN NHẮN CUỐI LÀ CỦA USER
# =============================================
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    user_query = st.session_state.messages[-1]["content"]

    # Hiển thị câu trả lời của Bot trong khi chờ
    with st.chat_message("assistant", avatar="🛡️"):
        # Khởi tạo prompt và xử lý file đính kèm
        prompt_contents = [user_query]
        if uploaded_file is not None:
            file_type = uploaded_file.name.split(".")[-1].lower()
            if file_type in ["png", "jpg", "jpeg"]:
                image = Image.open(uploaded_file)
                st.image(image, caption="📸 Ảnh sự cố đính kèm", use_container_width=True)
                prompt_contents.append(image)
            elif file_type in ["txt", "csv"]:
                st.info("📄 Đã đính kèm file log: " + uploaded_file.name)
                log_content = uploaded_file.getvalue().decode("utf-8")
                prompt_contents.append(f"\n--- Attached Log File: {uploaded_file.name} ---\n{log_content}\n--- End of Log File ---")

        # System Instruction cho mô hình AI
        system_instruction = f"""
BẠN LÀ MỘT CHUYÊN GIA AN NINH MẠNG CAO CẤP (SENIOR SECOPS ENGINEER) VÀ LÀ TRỢ LÝ ỨNG CỨU SỰ CỐ MẠNG KHẨN CẤP.

NHIỆM VỤ CỦA BẠN:
Dựa vào Tài liệu Quy trình chuẩn (SOP) được cung cấp dưới đây để hỗ trợ người dùng giải quyết các sự cố mạng:
----------------------------------------
{SOP_KNOWLEDGE}
----------------------------------------

QUY TẮC PHẢN HỒI NÂNG CẤP (BẮT BUỘC):

1. NHẬN DIỆN ĐỐI TƯỢNG (PERSONA ADAPTATION):
   - Nếu người dùng hỏi bằng ngôn ngữ bình dân, không có thuật ngữ kỹ thuật nâng cao -> Hãy đóng vai người hướng dẫn thân thiện, dùng từ ngữ dễ hiểu, không dùng từ chuyên ngành quá sâu, hướng dẫn từng bước click chuột trên giao diện đồ họa (GUI).
   - Nếu người dùng hỏi bằng thuật ngữ kỹ thuật (ví dụ: dùng các từ như "pcap", "wireshark", "mac address", "cli", "config", "cisco") -> Hãy phản hồi với tư cách Chuyên gia với Chuyên gia: Đưa ra phân tích chuyên sâu về gói tin, vị trí kiểm tra log hệ thống.

2. CẤU TRÚC PHẢN HỒI CHUẨN SECOPS (Dùng Markdown để scannable):
   - 🚨 **Mức độ nguy hiểm:** [Thấp / Trung bình / Cao / Khẩn cấp]
   - 🔍 **Chẩn đoán hiện trạng:** [Phân tích ngắn gọn dấu hiệu dựa trên câu hỏi]
   - 🛠️ **Hành động khắc phục (Remediation Steps):** [Chia rõ Bước 1, Bước 2, Bước 3]
   - 💻 **Lệnh thực thi nhanh (Nếu là IT Admin):** Cung cấp các câu lệnh CLI (Windows PowerShell, CMD, Linux, Cisco IOS) hoặc bộ lọc Wireshark nằm trong các khối code (code block) để họ copy dùng ngay.

3. NGUYÊN TẮC AN TOÀN:
   - Nếu phát hiện dấu hiệu của sự cố khẩn cấp (như Phishing chiếm đoạt tài khoản hoặc Ransomware), phải đưa cảnh báo nhấn mạnh bằng chữ IN HOA ở ngay đầu câu trả lời: "HÀNH ĐỘNG KHẨN CẤP: NGẮT KẾT NỐI MẠNG NGAY LẬP TỨC!".

4. CHẾ ĐỘ BẮT BỆNH TƯƠNG TÁC (INTERACTIVE TRIAGE):
   - Nếu người dùng mô tả sự cố quá chung chung (VD: "mạng chậm", "không vào được mạng"), KHÔNG ĐƯỢC đưa ra toàn bộ cách giải quyết ngay.
   - Thay vào đó, hãy hỏi lại 1-2 câu hỏi chẩn đoán ngắn gọn (VD: "Mạng bị chậm ở một máy hay toàn hệ thống?", "Bạn có thấy popup lạ nào không?") để thu hẹp phạm vi lỗi trước khi hướng dẫn.

5. CHẾ ĐỘ PHÂN TÍCH LOG (LOG ANALYZER):
   - Nếu người dùng cung cấp nội dung file log (.txt, .csv), hãy quét toàn bộ và trích xuất ra các IP độc hại, lỗi cấu hình, hoặc các dòng có mức độ nghiêm trọng (CRITICAL/ERROR). Trình bày dưới dạng bảng hoặc danh sách gạch đầu dòng ngắn gọn.

6. CHẾ ĐỘ DIỄN TẬP (RED TEAM SIMULATOR):
   - Nếu người dùng yêu cầu diễn tập, hãy đóng vai Game Master. Đưa ra một kịch bản tấn công giả lập (VD: một đoạn email lừa đảo hoặc log cảnh báo rớt mạng giả) và hỏi người dùng: "Bạn sẽ làm gì bước tiếp theo?".
   - Chấm điểm phản hồi của họ và đưa ra lời khuyên.
"""

        try:
            with st.spinner("Đang phân tích sự cố..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt_contents,
                    config={"system_instruction": system_instruction},
                )
                bot_response = response.text
        except Exception as e:
            bot_response = f"Có lỗi kết nối hệ thống AI: {str(e)}. Vui lòng kiểm tra lại API Key."

        display_bot_response(bot_response)

    # Lưu phản hồi của bot vào session state
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
