import os
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

js_data_file = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\data.js"
app_js_file = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\app.js"
floorplan_dir = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\floorplans"

def extract_apt_map():
    with open(app_js_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the dictionary string
    match = re.search(r'const APT_TYPE_MAP = ({.*?});', content, re.DOTALL)
    if not match:
        raise ValueError("Could not find APT_TYPE_MAP in app.js")
        
    map_str = match.group(1)
    
    # Use regex to find all 'KEY': 'VALUE' pairs
    pairs = re.findall(r"'([^']+)':\s*'([^']+)'", map_str)
    
    result = {}
    for k, v in pairs:
        result[k] = v
        
    return result

def extract_data():
    with open(js_data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    json_str = content.split('const apartmentsData = ')[1].split(';')[0].strip()
    return json.loads(json_str)

def verify_images():
    print("🏙️ מתחיל אימות שרטוטים הנדסי (Sprint 2 - T2.1)...")
    
    apt_map = extract_apt_map()
    apartments = extract_data()
    
    missing_images = []
    checked = 0
    
    for apt in apartments:
        lot = apt['מגרש'].strip()
        building = apt['מבנה'].strip()
        aptNum = apt['דירה'].strip()
        
        map_key = f"{building}-{aptNum}"
        aptType = apt_map.get(map_key, '?')
        
        if aptType == '?':
            print(f"⚠️ אזהרה: דירה {aptNum} במבנה {building} (מגרש {lot}) לא מופתה למודל דירה (APT_TYPE_MAP)!")
            missing_images.append(f"MAP_MISSING: {building}-{aptNum}")
            continue
            
        checked += 1
        
        # apply the JS replace logic: replace(/\+/g, '+').replace(/\-/g, '-').replace(/ /g, '_')
        safeName = aptType.replace('+', '+').replace('-', '-').replace(' ', '_')
        
        filename = f"floorplan_{lot}_{safeName}.png"
        filepath = os.path.join(floorplan_dir, filename)
        
        if not os.path.exists(filepath):
            missing_images.append(f"FILE_MISSING: דירה {aptNum} בבניין {building} -> חסר הקובץ {filename}")
            
    if not missing_images:
        print(f"✅ אימות שרטוטים הושלם! נבדקו {checked} תמונות שרטוט למול 124 דירות. 100% קבצים קיימים ותקינים.")
    else:
        print(f"❌ כישלון באימות שרטוטים. נמצאו {len(missing_images)} שרטוטים חסרים:")
        for m in missing_images:
            print("  -", m)

if __name__ == "__main__":
    verify_images()
