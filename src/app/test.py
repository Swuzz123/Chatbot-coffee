import streamlit as st
import time
import re
import uuid
import webbrowser
import subprocess
import requests
import atexit

st.title("Coffee Assistant ^v^")
st.write("Chào mừng bạn đến với quán cà phê của chúng tôi!")

greeting_phrases = ["xin chào", "hi", "hello", "xin chao", 'chào', 'chao', 'helloo', 'helo']

greeting_response = ("Chào bạn! Chào mừng bạn đến với quán cà phê của chúng mình. "
                     "Bạn có câu hỏi hoặc cần tư vấn gì không ạ? Mình sẽ cố gắng giúp đỡ bạn "
                     "tìm món nước phù hợp nhất với yêu cầu mà quán có. Chúc bạn một ngày tốt lành! 😊🌸")

# Wait for FastAPI to start
time.sleep(2)
st.session_state.fastapi_url = "http://localhost:8000/chat"

# Initialize chat history and image_urls
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "image_urls" not in st.session_state:
    st.session_state.image_urls = []

# Display the chat history
for i, message in enumerate(st.session_state.chat_history):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Hiển thị hình ảnh nếu có
        if i < len(st.session_state.image_urls) and st.session_state.image_urls[i]:
            if isinstance(st.session_state.image_urls[i], str):
                st.image(st.session_state.image_urls[i], width=300)
            elif isinstance(st.session_state.image_urls[i], list):
                cols = st.columns(min(5, len(st.session_state.image_urls[i]))) 
                for col, (url, msg) in zip(cols, [(url, msg) for url, msg in zip(st.session_state.image_urls[i], st.session_state.chat_history[i]["content"].split("\n---\n")) if url]):
                    with col:
                        parts = msg.split("\n")
                        title = next((p.replace("Tên: ", "") for p in parts if p.startswith("Tên: ")), "Unknown")
                        price = next((p.replace("Giá: ", "").replace(" VNĐ", "") for p in parts if p.startswith("Giá: ")), "N/A")
                        st.image(url, width=150)
                        st.write(f"**{title}** - {price} VNĐ")

# Chat input
if prompt := st.chat_input("Quán cà phê có thể giúp bạn chọn món nào nhỉ?"):
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        time.sleep(0.5)
        st.markdown(prompt)

    if clean_input(prompt) in [clean_input(greet) for greet in greeting_phrases]:
        # Greeting response
        with st.chat_message("assistant"):
            full_res = ''
            message_placeholder = st.empty()
            for res in greeting_response.split():
                full_res += res + " "
                message_placeholder.markdown(full_res + "▌")
                time.sleep(0.04)
            message_placeholder.markdown(full_res)
        st.session_state.chat_history.append({"role": "assistant", "content": greeting_response})
        st.session_state.image_urls.append(None)  # Không có ảnh cho greeting
    else:
        # Call FastAPI to get response
        with st.chat_message("assistant"):
            payload = {
                "query": prompt,
                "chat_history": [msg["content"] for msg in st.session_state.chat_history]
            }
            try:
                response = requests.post(st.session_state.fastapi_url, json=payload, timeout=10)
                if response.status_code == 200:
                    api_response = response.json()
                    assistant_response = api_response["response"]
                    image_url = api_response.get("image_url")

                    # Display with typing effect
                    full_res = ''
                    message_placeholder = st.empty()
                    for res in assistant_response.split():
                        full_res += res + " "
                        message_placeholder.markdown(full_res + "▌")
                        time.sleep(0.04)
                    message_placeholder.markdown(full_res)

                    # Add to chat history and image_urls
                    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
                    st.session_state.image_urls.append(image_url)
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except requests.RequestException as e:
                st.error(f"Không thể kết nối với server: {str(e)}")

# Nút xóa lịch sử
if st.button("Xóa lịch sử"):
    clear_session_state()
    st.rerun()