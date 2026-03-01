import json
import os
import sys
import csv

sys.stdout.reconfigure(encoding='utf-8')

data_file = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\v11_temp\data_v11.js"
output_csv = r"C:\Users\user\.gemini\antigravity\brain\a8a89265-7c6f-4346-a55f-523dfd6ff525\v11_data_verification.csv"

def extract_v11_data():
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    json_str = content.split('const apartmentsDataV11 = ')[1].split(';\n')[0].strip()
    return json.loads(json_str)

def generate_csv():
    data = extract_v11_data()
    
    # Sort by Lot and then inside by Building and then Apt
    data = sorted(data, key=lambda x: (x['lot'], int(x['building'].replace('R','').replace('T','').replace('P','')), int(x['aptText'])))
    
    headers = ["מגרש", "מבנה", "דירה", "קומה", "חדרים", "שטח (מ\"ר)", "מרפסת (מ\"ר)", "מחסן (מ\"ר)", "כיוון", "מחיר", "טיפוס קטלוג", "שם קובץ שרטוט", "נתיב מלא לשרטוט"]
    
    # Use utf-8-sig so Excel automatically recognizes Hebrew Characters
    with open(output_csv, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for apt in data:
            img_path = f"C:\\Users\\user\\Documents\\ALEX\\HOME\\apartment-app\\floorplans_v11\\{apt['imageFile']}"
            price_str = f"{apt['price']:,.0f} ₪"
            
            row = [
                apt['lot'],
                apt['building'],
                apt['aptText'],
                apt['floor'],
                apt['rooms'],
                apt['area'],
                apt['balcony'],
                apt['storage'],
                apt['sunDir'],
                price_str,
                apt['aptType'],
                apt['imageFile'],
                img_path
            ]
            writer.writerow(row)
            
    print(f"✅ Generated CSV (Excel) table with {len(data)} apartments at {output_csv}")

if __name__ == '__main__':
    generate_csv()
