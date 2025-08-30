from retrieval.query_processor import handle_user_query, is_exact_item
from retrieval.milvus_search import is_exact_item

def get_relevant_chunk(query):
    results = handle_user_query(query, limit=5)
    
    # Case 2: If retrurn list of sub_category
    if isinstance(results, str):
        return results
    
    if results:
        if len(results) == 1:
            # Case 1: Exact match
            item = results[0]
            context = (
                f"Tên: {item['title']}\n"
                f"Giá: {item['price']} VNĐ\n"
                f"Mô tả: {item['description']}"
            )
            return context
        else:
            context = ""
            for item in results:
                context += (
                    f"Tên: {item['title']}\n"
                    f"Giá: {item['price']} VNĐ\n"
                    f"Mô tả: {item['description']}"
                    f"-----\n"
                )
            return context.strip()
        
    return "Quán của mình hiện không bán món nước này. Anh/chị muốn thử món nào khác không?"

def make_prompt(query, context):
    # Determine case to create suitable instruction
    is_exact, _ = is_exact_item(query)
    case = 1 if is_exact else 2
    
    if case == 1:
        instruction = (
            "Hãy trả lời một cách ấm áp, nhẹ nhàng như một cuộc hội thoại, tập trung vào món mà khách hàng hỏi. "
            "Giới thiệu món, mô tả lợi ích dựa trên context, và hỏi thêm nếu cần."
        )
    else:
        instruction = (
            "Hãy trả lời một cách thân thiện, tự nhiên. "
            "Nếu context là danh sách loại món, liệt kê chúng và hỏi khách muốn loại nào cụ thể. "
            "Nếu context là danh sách món, giới thiệu ngắn gọn từng món và khuyến khích khách chọn."
        )
    
    return (
        f"Query: {query}\n\n"
        f"Context: \n{context}\n\n"
        f"Answer: {instruction}"
    )