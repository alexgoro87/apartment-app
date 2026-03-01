"""Step 2 & 3: Fix room counts based on type, and identify placeholder drawings."""
import json
import sys
import csv
import os

sys.stdout.reconfigure(encoding='utf-8')

DATA_JS = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\data_v12.js"
OUTPUT_DIR = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\v12_temp"

# Room count rules by type prefix
ROOM_RULES = {
    'C': 3,   # C, C_1, C_2, C_3, C_4, C_5, C_7, C-, C-_1, C-_2
    'B': 4,   # B, B_1, B_2, B_3, B_4, B_5, B-, B-_1
    'E': 5,   # E, E_1, E_2, E_3, E_4
    'A+': 6,  # A+, A+_1, A+_2, A+_3, A+_4 (MUST check before 'A')
    'A': 5,   # A, A_1, A_2, A_3, A_4, A_5, A_6, A _2
    'D': 6,   # D, D1, D2, D3
}

def get_expected_rooms(apt_type):
    """Get expected room count based on apartment type."""
    t = apt_type.strip()
    # Check A+ before A (longer prefix first)
    if t.startswith('A+'):
        return 6
    for prefix in ['C-', 'B-', 'C', 'B', 'E', 'A', 'D']:
        if t.startswith(prefix):
            return ROOM_RULES.get(prefix, ROOM_RULES.get(prefix[0], None))
    return None

def load_data():
    with open(DATA_JS, 'r', encoding='utf-8') as f:
        content = f.read()
    json_str = content.split('const apartmentsDataV12 = ')[1].rsplit(';', 1)[0].strip()
    return json.loads(json_str)

def fix_rooms(data):
    """Fix room counts and return list of changes."""
    fixes = []
    for a in data:
        expected = get_expected_rooms(a['type'])
        if expected and a['rooms'] != expected:
            fixes.append({
                'building': a['building'],
                'aptNum': a['aptNum'],
                'lot': a['lot'],
                'type': a['type'],
                'floor': a['floor'],
                'rooms_before': a['rooms'],
                'rooms_after': expected,
            })
            a['rooms'] = expected
    return fixes

def find_placeholders(data):
    """Find all apartments using page_001.png as placeholder."""
    placeholders = []
    for a in data:
        if a['imageFile'] == 'page_001.png':
            placeholders.append({
                'lot': a['lot'],
                'building': a['building'],
                'aptNum': a['aptNum'],
                'floor': a['floor'],
                'rooms': a['rooms'],
                'area': a['area'],
                'type': a['type'],
                'direction': a['direction'],
            })
    return placeholders

if __name__ == '__main__':
    data = load_data()
    
    # Step 2: Fix rooms
    fixes = fix_rooms(data)
    fixes_path = os.path.join(OUTPUT_DIR, 'v12_rooms_fixes.csv')
    with open(fixes_path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['building', 'aptNum', 'lot', 'type', 'floor', 'rooms_before', 'rooms_after'])
        w.writeheader()
        w.writerows(fixes)
    
    print(f"=== שלב 2: תיקון חדרים ===")
    print(f"סה\"כ תיקונים: {len(fixes)}")
    for fix in fixes:
        print(f"  {fix['lot']}/{fix['building']} דירה {fix['aptNum']} ({fix['type']}): {fix['rooms_before']} → {fix['rooms_after']}")
    if not fixes:
        print("  ✅ כל הנתונים נכונים – אין צורך בתיקון!")
    print(f"  → נשמר: {fixes_path}")
    
    # Step 3: Find placeholders
    placeholders = find_placeholders(data)
    placeholders_path = os.path.join(OUTPUT_DIR, 'v12_missing_drawings.csv')
    with open(placeholders_path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['lot', 'building', 'aptNum', 'floor', 'rooms', 'area', 'type', 'direction'])
        w.writeheader()
        w.writerows(placeholders)
    
    print(f"\n=== שלב 3: זיהוי Placeholders ===")
    print(f"סה\"כ דירות ללא שרטוט אמיתי: {len(placeholders)}")
    for p in placeholders:
        print(f"  {p['lot']}/{p['building']} דירה {p['aptNum']} קומה {p['floor']} | {p['type']} | {p['rooms']} חד'")
    print(f"  → נשמר: {placeholders_path}")
    
    # Save the data with fixed rooms for later use
    fixed_data_path = os.path.join(OUTPUT_DIR, 'data_v12_rooms_fixed.json')
    with open(fixed_data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n  → נתונים מתוקנים: {fixed_data_path}")
