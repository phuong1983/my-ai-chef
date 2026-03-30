import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CẤU HÌNH ---
# Thay 'API_KEY_CUA_BAN' bằng mã bạn vừa lấy ở bước 1
API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)

# Chọn mô hình Gemini có khả năng nhìn ảnh (Flash là nhanh nhất)
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- GIAO DIỆN APP ---
st.set_page_config(page_title="AI Chef", page_icon="👨‍🍳")
st.title("👨‍🍳 Trợ lý Đầu bếp AI")
st.write("Tải ảnh nguyên liệu và cho tôi biết sở thích của bạn!")

# 1. Ô nhập sở thích của người dùng
user_pref = st.text_input("Sở thích (VD: Không cay, dưới 20p, món chay...)")

# 2. Nút tải ảnh lên
uploaded_file = st.file_uploader("Chọn ảnh nguyên liệu...", type=["jpg", "jpeg", "png"])

# Kiểm tra nếu người dùng đã tải ảnh
if uploaded_file is not None:
    # Mở ảnh và hiển thị lên màn hình app
    img = Image.open(uploaded_file)

    # 3. Nút bấm để yêu cầu AI trả lời
    if st.button("Gợi ý món ăn ngay!"):
        with st.spinner("Đang suy nghĩ..."):
            # Câu lệnh chi tiết gửi cho AI (Prompt)
            prompt = f"""
            Bạn là đầu bếp giỏi. Hãy nhìn ảnh và dựa trên sở thích: {user_pref}.
            - Liệt kê các nguyên liệu thấy trong ảnh.
            - Gợi ý 3 món ăn phù hợp.
            - Trình bày kết quả dưới dạng bảng rõ ràng.
            Nếu ảnh không phải đồ ăn, hãy từ chối lịch sự.
            """
            
            # Gửi yêu cầu sang Google AI
            response = model.generate_content([prompt, img])
            
            # Hiển thị kết quả AI trả về
            st.success("Xong rồi! Đây là gợi ý cho bạn:")
            st.markdown(response.text)
    st.image(img, caption="Ảnh đã tải lên", use_container_width=True)
