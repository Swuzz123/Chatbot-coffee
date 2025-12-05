# utils/helpers.py
import re
import unicodedata

class QueryClassifier:
  def __init__(self, mappings):
    self.mappings = mappings
    self.main_cats, self.sub_cats, self.items = self.build_lookup_tables()
    
  def normalize_text(self, text):
    # Convert Vietnamese to accent-free + lowercase for robust matching
    text = unicodedata.normalize('NFD', text)
    text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Mn')
    return text.lower().strip()

  def build_lookup_tables(self):
    main_cats, sub_cats, items = set(), set(), set()
    for main_cat, subs in self.mappings.items():
      main_cats.add(main_cat)
      for sub_cat, drinks in subs.items():
        if sub_cat:
          sub_cats.add(sub_cat)
        for drink in drinks:
          items.add(drink)
    return main_cats, sub_cats, items

  def classify_query(self, query):
    query_norm = self.normalize_text(query)

    # Normalize all names for comparison
    norm_main = {self.normalize_text(c): c for c in self.main_cats}
    norm_sub = {self.normalize_text(c): c for c in self.sub_cats}
    norm_items = {self.normalize_text(i): i for i in self.items}

    # Exact beverage (title) match
    for norm_name, original in norm_items.items():
      if norm_name in query_norm:
        return {"type": "item", "keyword": original}

    # Sub-category match
    for norm_name, original in norm_sub.items():
      if re.search(rf"\b{re.escape(norm_name)}\b", query_norm):
        return {"type": "sub_category", "keyword": original}

    # Main category match
    for norm_name, original in norm_main.items():
      if re.search(rf"\b{re.escape(norm_name)}\b", query_norm):
        return {"type": "main_category", "keyword": original}

    return {"type": "unknown", "keyword": None}