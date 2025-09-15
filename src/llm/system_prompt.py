from retrieval.query_processor import handle_user_query, is_exact_item

def get_relevant_chunk(query):
    results = handle_user_query(query, limit=5)
    
    # Case 2: If retrurn list of sub_category
    if isinstance(results, str):
        return {"context": results, "image_url": []}
    
    if results:
        # Collect image URLs in a list
        image_urls = [item.get("image_url") for item in results if item.get("image_url")]
        
        if len(results) == 1:
            # Case 1: Exact match
            item = results[0]
            context = (
                f"Tên: {item['title']}\n"
                f"Giá: {item['price']} VNĐ\n"
                f"Mô tả: {item['description']}"
            )
            return {"context": context, "image_url": image_urls}
        else:
            # Case 2: General match with multiple items
            context = ""
            for item in results:
                context += (
                    f"Tên: {item['title']}\n"
                    f"Giá: {item['price']} VNĐ\n"
                    f"Mô tả: {item['description']}\n"
                    f"---\n"
                )
            return {"context": context.strip(), "image_url": image_urls}

    return {"context": "Quán của mình hiện không bán món nước này. Anh/chị muốn thử món nào khác không?", "image_url": []}

def make_prompt(query, context):
    # Determine case to create suitable instruction
    is_exact, _ = is_exact_item(query)
    case = 1 if is_exact else 2
    
    if case == 1:
        instruction = (
            """
            Hãy trả lời một cách ấm áp, nhẹ nhàng, tập trung vào món mà khách hàng hỏi.
            Tóm tắt mô tả món dựa trên context, chỉ nói những điểm nổi bật.
            Cuối cùng, hỏi thêm nếu cần. 
            """
        )
    else:
        instruction = (
            """
            Hãy trả lời một cách thân thiện, tự nhiên.
            Nếu context là danh sách các món, tóm tắt và giới thiệu từng món một cách ngắn gọn, chỉ nêu những đặc điểm nổi bật.
            Sau đó, khuyến khích khách hàng chọn một món.
            
            Quan trọng: Vui lòng liệt kê mỗi món sử dụng dấu gạch đầu dòng (-) để đánh dấu từng món theo format sau
            1. **[Tên món]**: [Mô tả]
            2. **[Tên món]**: [Mô tả]
            ...
            """
        )
    
    return (
        f"Query: {query}\n\n"
        f"Context: \n{context}\n\n"
        f"Answer: {instruction}"
    )