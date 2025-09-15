from llm.generate import generate_answer

def main():
    chat_history = []
    while True:
        query = input("Nhập câu hỏi (hoặc 'exit' để thoát): ")
        if query.lower() == 'exit':
            break
        response = generate_answer(query, chat_history, limit=5)
        print(f"Trả lời: {response}")

if __name__ == "__main__":
    main()