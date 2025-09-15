from config.settings import mappings, sub_category_keywords

# Case 1: If the customer directly asks to buy that item, then respond accurately.
def is_exact_item(query):
    query = query.strip().lower()
    
    for main_cat, sub_cats in mappings.items():
        for sub_cat, items in sub_cats.items():
            for item in items:
                if item.lower() in query:
                    return True, item
                
    return False, None

# Case 2: When the user asks a general question about a type of beverage/food
def get_category_from_query(query):
    query =  query.lower()
    
    # 1. Check suggested keywords for sub_category
    for main_cat, sub_cats in mappings.items():
        for sub_cat in sub_cats.keys():
            if sub_cat:
                if sub_cat in sub_category_keywords:
                    for keywords in sub_category_keywords[sub_cat]:
                        if keywords in query:
                            return main_cat, sub_cat
                        
    # 2. Check directly sub_category
    for main_cat, sub_cats in mappings.items():
        for sub_cat in sub_cats.keys():
            if sub_cat and sub_cat.lower() in query:
                return main_cat, sub_cat
            
    # 3. Check directly main_category
    for main_cat in mappings.keys():
        if main_cat.lower() in query:
            return main_cat, None
        
    # 4. Check keywords by each items (fallback)
    for main_cat, sub_cats in mappings.items():
        for sub_cat, items in sub_cats.items():
            for item in items:
                if item.lower() in query:
                    return main_cat, sub_cat
                
    return None, None
    
    