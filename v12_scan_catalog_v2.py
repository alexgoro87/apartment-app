import fitz
import json
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"c:\Users\user\Documents\ALEX\HOME\קטלוג-משתכן-רמת-רבין.pdf"
input_json = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\v12_temp\refined_g4_data.json"
mapping_output = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\v12_temp\catalog_mapping_v2.json"

def scan_catalog_comprehensive():
    doc = fitz.open(pdf_path)
    with open(input_json, 'r', encoding='utf-8') as f:
        apartments = json.load(f)
    
    required_keys = set()
    for apt in apartments:
        t_name = apt['aptType'].strip()
        required_keys.add((apt['lot'], apt['building'], t_name))
    
    print(f"Goal: Mapping {len(required_keys)} unique combinations.")
    
    mapping = {}
    pages_content = []
    for i, page in enumerate(doc):
        pages_content.append((i + 1, page.get_text()))

    for lot, bldg, t_name in required_keys:
        # Standardize for search: B2 -> B 2, C1 -> C 1, etc.
        t_norm = re.sub(r'([A-Za-z])_?(\d+)', r'\1 \2', t_name)
        t_simple = t_name.replace("_", "")
        
        found = False
        for page_num, text in pages_content:
            # Check for Lot and Type
            # Using regex for flexible spacing
            type_pattern = t_norm.replace(" ", r"\s*")
            if lot in text and re.search(type_pattern, text):
                mapping[f"{lot}_{bldg}_{t_name}"] = page_num
                found = True
                break
        
        if not found:
            # Fallback: Search for just the Type if unique enough
            for page_num, text in pages_content:
                type_pattern = t_norm.replace(" ", r"\s*")
                if re.search(type_pattern, text):
                    mapping[f"{lot}_{bldg}_{t_name}"] = page_num
                    found = True
                    break

    with open(mapping_output, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=4)
        
    print(f"Final Count: Mapped {len(mapping)} / {len(required_keys)} variants.")
    return mapping

if __name__ == "__main__":
    scan_catalog_comprehensive()
