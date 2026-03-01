import pdfplumber
import json
import re
import os
import sys

# Ensure UTF-8 output even if the terminal is problematic
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"c:\Users\user\Documents\ALEX\HOME\הגרלה-2279-ג4-חתום.pdf"
output_json = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\v12_temp\raw_g4_data.json"

def clean_text(text):
    if not text: return ""
    return " ".join(text.split())

def extract_g4_table():
    print(f"Opening G4 PDF: {pdf_path}")
    all_rooms_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            print(f"Processing page {i+1}...")
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if not row or len(row) < 5: continue
                    # Use a regex or check for keywords in a way that handles RTL better
                    row_str = " ".join([str(cell) for cell in row if cell])
                    if "מבנה" in row_str or "מגרש" in row_str or "דירה" in row_str: continue
                    
                    all_rooms_data.append(row)

    print(f"Finished. Extracted {len(all_rooms_data)} rows.")
    
    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(all_rooms_data, f, ensure_ascii=False, indent=4)
    
    return all_rooms_data

if __name__ == "__main__":
    extract_g4_table()
