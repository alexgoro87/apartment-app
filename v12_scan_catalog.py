import fitz
import json
import os
import sys

# Standardize output for Windows terminal
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"c:\Users\user\Documents\ALEX\HOME\קטלוג-משתכן-רמת-רבין.pdf"
input_json = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\v12_temp\refined_g4_data.json"
mapping_output = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\v12_temp\catalog_mapping.json"

def scan_catalog():
    print(f"Scanning Catalog PDF: {pdf_path}")
    doc = fitz.open(pdf_path)
    
    with open(input_json, 'r', encoding='utf-8') as f:
        apartments = json.load(f)
    
    # We need unique keys like (building, type) or just (type) if it's global
    # Let's map unique combinations found in G4
    required_keys = set()
    for apt in apartments:
        # standardizing type name - removing spaces, handling underscores
        t_name = apt['aptType'].strip().replace(" ", "")
        required_keys.add((apt['lot'], apt['building'], t_name))
    
    print(f"Found {len(required_keys)} unique (Lot, Building, Type) combinations to map.")
    
    mapping = {}
    
    for i, page in enumerate(doc):
        text = page.get_text()
        # Look for the combination in page text.
        # Catalog structure usually mentions 'מגרש' and 'בניין' and 'טיפוס'
        for lot, bldg, t_name in required_keys:
            # Simple heuristic: if all identifiers are on the page, it's a match
            # Building in catalog might be "1" instead of "1T" or vice versa
            b_num = re.sub(r'\D', '', bldg)
            
            # Check for Type (e.g. C_1 or C 1)
            t_search = t_name.replace("_", " ")
            
            if lot in text and t_search in text:
                # Lot match and Type match often sufficient for a spread
                mapping[f"{lot}_{bldg}_{t_name}"] = i + 1
                
    with open(mapping_output, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=4)
        
    print(f"Mapped {len(mapping)} combinations to pages.")
    return mapping

import re
if __name__ == "__main__":
    scan_catalog()
