import json

def calculate_total_price(chat_history, current_context_data):
    """Calculate the total price of items ordered in the chat history."""
    
    total_price = 0
    ordered_items_info = []
    
    # Iterate through chat history messages
    for message in chat_history:
        if "Context: " in message and "Answer: " in message:
            try:
                # Extract JSON string of context
                context_str = message.split("Context:")[1].split("\n\nAnswer:")[0].strip().replace("'", '"')
                
                context_data = json.loads(context_str)
                
                # Iterate through each item in the context to get prices
                if "context" in context_data and "---" in context_data["context"]:
                    items_list = context_data["context"].split("---")
                    for item_str in items_list:
                        if "Tên:" in item_str and "Giá:" in item_str:
                            title = item_str.split("Tên:")[1].split("\n")[0].strip()
                            price = item_str.split("Giá:")[1].split("\n")[0].strip().replace("VNĐ", "").strip()
                        try:
                            price = int(price.replace(",", ""))
                            ordered_items_info.append({"name": title, "price": price})
                            total_price += price
                        except ValueError:
                            continue # Skip if the value is not number
            except Exception as e:
                # Skip messages that are not in right form
                print(f"Error parsing context from history: {e}")
                continue
    
    # Add logic to get the price from the current query's context
    if current_context_data and 'context' in current_context_data:
        context = current_context_data['context']
        if context and "---" in context:
            items_str = context.split("---")
            for item_str in items_str:
                if "Tên:" in item_str and "Giá:" in item_str:
                    title = item_str.split("Tên:")[1].split("\n")[0].strip()
                    price_str = item_str.split("Giá:")[1].split("\n")[0].strip().replace("VNĐ", "").strip()
                    try:
                        price = int(price_str.replace(",", ""))
                        # Kiểm tra xem món này đã có trong lịch sử chưa để tránh trùng lặp
                        is_new_item = True
                        for ordered_item in ordered_items_info:
                            if ordered_item['name'] == title:
                                is_new_item = False
                                break
                        if is_new_item:
                            ordered_items_info.append({"name": title, "price": price})
                            total_price += price
                    except ValueError:
                        continue
            
    return json.dumps({
        "ordered_items": ordered_items_info,
        "total_price": total_price
    })
                        