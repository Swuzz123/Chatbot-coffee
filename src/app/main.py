import streamlit as st
import requests
import time
import uuid
import json

st.set_page_config(page_title="Coffee Assistant", page_icon="☕")
st.title("☕ Coffee Assistant")
st.write("Chào mừng bạn đến với quán cà phê của chúng mình!")

# Tạo session_id duy nhất cho từng người dùng
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Lưu lịch sử hội thoại
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

API_URL = "http://localhost:8000/chat"  # FastAPI endpoint

# Custom CSS cho việc hiển thị hình ảnh đẹp hơn
st.markdown("""
    <style>
    .coffee-item {
        padding: 10px;
        border-radius: 10px;
        transition: transform 0.3s ease;
    }
    .coffee-item:hover {
        transform: scale(1.02);
    }
    .coffee-image {
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Hiển thị lịch sử chat cũ
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("images_data") and len(message["images_data"]) > 0:
            
            num_images = len(message['images_data'])
            
            # Create columns for images
            cols = st.columns(min(num_images, 5))
            
            for idx, item in enumerate(message["images_data"][:5]):
                with cols[idx % 5]:
                    if item.get('image_url'):
                        st.image(
                            item['image_url'],
                            use_container_width=True
                        )
                        st.markdown(f"**{item.get('name', 'Coffee')}**")
                        if item.get('price'):
                            st.caption(f"{item['price']:,} VNĐ")   

# Input box chat
if prompt := st.chat_input("Bạn muốn gọi món gì hôm nay?"):
    # Hiển thị tin nhắn người dùng
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Gửi request đến API
    try:
        with st.chat_message("assistant"):
            formatted_history = [
                f"User: {m['content']}" if m['role'] == 'user' else f"Assistant: {m['content']}"
                for m in st.session_state.chat_history
            ]
            
            payload = {
                "query": prompt,
                "chat_history": formatted_history
            }
            
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                assistant_response = data["response"]
                image_urls = data.get("image_urls", [])
                
                # Trích xuất thông tin ảnh từ chat_history để hiển thị
                # images_data = []
                # chat_history_from_api = data.get("chat_history", [])
                
                # # Tìm kiếm prompt của người dùng và context tương ứng trong lịch sử trả về từ API
                # found_context = False
                # for entry in reversed(chat_history_from_api):
                #     if entry.startswith("User: Query:"):
                #         try:
                #             # Trích xuất context (đã được lưu dưới dạng JSON)
                #             context_str = entry.split("Context: ")[1].split("\n\nAnswer:")[0].strip()
                #             context_data = json.loads(context_str.replace("'", '"'))
                            
                #             if context_data.get("image_url") and context_data.get("context"):
                #                 # Trích xuất tên món và URL
                #                 item_contexts = context_data["context"].split("---")
                #                 for i, item_context in enumerate(item_contexts):
                #                     if item_context.strip():
                #                         title = ""
                #                         for line in item_context.strip().split("\n"):
                #                             if line.startswith("Tên:"):
                #                                 title = line.replace("Tên:", "").strip()
                #                                 break
                #                         if title and i < len(context_data["image_url"]):
                #                             images_data.append({
                #                                 "name": title,
                #                                 "url": context_data["image_url"][i]
                #                             })
                #             found_context = True
                #             break
                #         except Exception as e:
                #             print(f"Lỗi khi xử lý context từ history: {e}")
                            
                st.markdown(assistant_response)
                
                # Hiển thị hình ảnh theo hàng ngang nếu có items_with_images
                if image_urls and len(image_urls) > 0:
                    # Tạo columns cho hình ảnh
                    num_items = len(image_urls)
                    cols = st.columns(min(num_items, 5))
                    
                    for idx, item in enumerate(image_urls[:5]):
                        with cols[idx % 5]:
                            if item.get('image_url'):
                                # Container cho mỗi món
                                with st.container():
                                    st.image(
                                        item['image_url'],
                                        use_container_width=True
                                    )
                                    st.markdown(f"**{item.get('name', 'Coffee')}**")
                                    if item.get('price'):
                                        st.caption(f"{item['price']:,} VNĐ")
                
                # Lưu vào lịch sử (cả response và images_data)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": assistant_response,
                    "images_data": image_urls
                })
            else:
                st.error(f"Lỗi API: {response.status_code}")
                
    except Exception as e:
        st.error(f"Lỗi kết nối API: {e}")