from llm.generate import generate_answer

chat_history = []

def main():
    # query = "Quán mình có bán những loại cà phê nào vậy? Có thể cho tôi biết best seller của quán không?"
    query = "Quán mình tui thấy có bán bánh mặn, có loại nào ngon nhỉ?"
    
    print(f"\nQuery: {query}")
    answer = generate_answer(query, chat_history, limit=5)
    print("Answer:", answer)

if __name__ == "__main__":
    main()