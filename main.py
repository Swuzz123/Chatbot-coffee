from config.settings import sub_category_keywords, mappings

for main_cat, sub_cats in mappings.items():
    for sub_cat in sub_cats.keys():
        if sub_cat:
            # Check the suggested keywords
            if sub_cat in sub_category_keywords:
                for keyword in sub_category_keywords[sub_cat]:
                    if keyword in query