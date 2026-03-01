import csv
import json
import re
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

app_js_file = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\app.js"
csv_file = r"c:\Users\user\Documents\ALEX\HOME\apartments_data_full_124.csv"
output_js = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\v11_temp\data_v11.js"

def extract_apt_map():
    with open(app_js_file, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'const APT_TYPE_MAP = ({.*?});', content, re.DOTALL)
    if not match:
        raise ValueError("Could not find APT_TYPE_MAP in app.js")
    map_str = match.group(1)
    pairs = re.findall(r"'([^']+)':\s*'([^']+)'", map_str)
    result = {}
    for k, v in pairs:
        result[k] = v
    return result

def build_v11_data():
    print("🚀 V11 Data Builder SPRINT 1")
    apt_map = extract_apt_map()
    
    data = []
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
            
    # Process and map objects
    v11_records = []
    for item in data:
        lot = str(item.get('מגרש', '')).strip()
        building = str(item.get('מבנה', '')).strip()
        aptNum = str(item.get('דירה', '')).strip()
        
        map_key = f"{building}-{aptNum}"
        aptType = apt_map.get(map_key, '?')
        safeName = aptType.replace('+', '+').replace('-', '-').replace(' ', '_')
        imageFile = f"floorplan_{lot}_{safeName}.png"
        
        # Build pristine object
        record = {
            "id": f"{aptNum}-{building}",
            "rank": int(item.get('דירוג', 999) or 999),
            "lot": lot,
            "building": building,
            "aptText": aptNum,
            "floor": str(item.get('קומה', '')).strip(),
            "rooms": str(item.get('חדרים', '')).strip(),
            "area": float(item.get('שטח', 0) or 0),
            "balcony": float(item.get('מרפסת', 0) or 0),
            "storage": float(item.get('מחסן', 0) or 0),
            "isLast": str(item.get('אחרונה?', '')).strip() == 'כן',
            "sunDir": str(item.get('חמה/קרירה', '')).strip(),
            "parkingDist": str(item.get('מרחק חניה', '')).strip(),
            "price": float(item.get('מחיר', 0) or 0),
            "aptType": aptType,
            "imageFile": imageFile
        }
        
        v11_records.append(record)
        
    os.makedirs(os.path.dirname(output_js), exist_ok=True)
    
    # Write to target js
    with open(output_js, 'w', encoding='utf-8') as wf:
        wf.write("// V11 Master Data Array - Generated automatically from D4/G4\n")
        wf.write("const apartmentsDataV11 = ")
        wf.write(json.dumps(v11_records, ensure_ascii=False, indent=4))
        wf.write(";\n")
        
    print(f"✅ V11 עובד! נוצר קובץ נתונים ממופה היטב עם {len(v11_records)} רשומות בנתיב:")
    print(f"   {output_js}")

if __name__ == "__main__":
    build_v11_data()
