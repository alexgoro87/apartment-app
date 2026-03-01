import csv
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

csv_file = r"c:\Users\user\Documents\ALEX\HOME\apartments_data_full_124.csv"
js_file = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\data.js"

def load_csv():
    data = []
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def load_js():
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the JSON array from the JS file
    json_str = content.split('const apartmentsData = ')[1].split(';')[0].strip()
    return json.loads(json_str)

def verify():
    print("🚀 מתחיל אימות נתונים ג'4 (Sprint 1 - T1.1)...")
    
    try:
        csv_data = load_csv()
        js_data = load_js()
    except Exception as e:
        print(f"❌ שגיאה בטעינת הקבצים: {e}")
        return

    print(f"📄 נמצאו {len(csv_data)} רשומות בקובץ CSV המקורי.")
    print(f"💾 נמצאו {len(js_data)} רשומות במסד הנתונים של האפליקציה.")

    if len(csv_data) != len(js_data):
        print("❌ שגיאה קריטית: מספר הרשומות לא תואם!")
        return

    mismatches = 0
    checked = 0
    
    # Check that they match exactly (assuming order is the same)
    for i in range(len(csv_data)):
        csv_row = csv_data[i]
        js_row = js_data[i]
        
        # Verify identifiers (Lot, Building, Apartment)
        lot = csv_row['מגרש']
        building = csv_row['מבנה']
        apt = csv_row['דירה']
        
        # Cross reference all exact keys (since JS was built from CSV initially)
        for key, csv_val in csv_row.items():
            checked += 1
            js_val = js_row.get(key)
            
            # Type casting to string for safe comparison
            if str(csv_val).strip() != str(js_val).strip():
                print(f"❌ חריגה זוהתה -> דירה {apt} במבנה {building} (מגרש {lot}):")
                print(f"   שדה '{key}': ג'4 = '{csv_val}' | אפליקציה = '{js_val}'")
                mismatches += 1

    if mismatches == 0:
        print("\n✅ מדהים! כל הנתונים תואמים ב-100%. אפס שגיאות או הקלדות.")
        print(f"📊 סך הכל תאים שנבדקו: {checked}")
    else:
        print(f"\n⚠️ אימות נכשל! נמצאו {mismatches} חריגות בין ג'4 לאפליקציה.")

if __name__ == "__main__":
    verify()
