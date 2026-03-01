import json
import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

js_path = r"c:\Users\user\Documents\ALEX\HOME\data_v12.js"
export_pages_dir = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\v12_temp\catalog_pages"

def generate_chat_table():
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract JSON part
    json_str = content.split('const apartmentsDataV12 = ')[1].split(';\n')[0].strip()
    data = json.loads(json_str)
    
    header = "| מגרש | מבנה | דירה | קומה | חדרים | שטח | מרפסת | מחסן | כיוון | מחיר | טיפוס | שרטוט |"
    separator = "|---|---|---|---|---|---|---|---|---|---|---|---|"
    
    print(header)
    print(separator)
    
    for a in data:
        img_link = f"[צפה](file:///{export_pages_dir}/{a['imageFile']})"
        row = f"| {a['lot']} | {a['building']} | {a['aptNum']} | {a['floor']} | {a['rooms']} | {a['area']} | {a['balcony']} | {a['storage']} | {a['direction']} | {a['price']} | {a['type']} | {img_link} |"
        print(row)

if __name__ == "__main__":
    generate_chat_table()
