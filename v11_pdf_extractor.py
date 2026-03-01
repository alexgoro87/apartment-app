import os
import shutil
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

v11_data_file = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\v11_temp\data_v11.js"
v10_images_dir = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\floorplans"
v11_images_dir = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\floorplans_v11"

def extract_v11_data():
    with open(v11_data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    json_str = content.split('const apartmentsDataV11 = ')[1].split(';\n')[0].strip()
    return json.loads(json_str)

def build_v11_images():
    print("✂️ מתחיל בסריקה ויצירת תיקיית floorplans_v11 מחדש (Sprint 2)...")
    
    if not os.path.exists(v11_images_dir):
        os.makedirs(v11_images_dir)
        
    records = extract_v11_data()
    unique_images = set(r['imageFile'] for r in records)
    
    print(f"📄 נמצאו {len(unique_images)} דגמי שרטוטים ייחודיים מקובץ הנתונים החדש.")
    
    success_count = 0
    missing = []
    
    for img in unique_images:
        src = os.path.join(v10_images_dir, img)
        dst = os.path.join(v11_images_dir, img)
        
        if os.path.exists(src):
            shutil.copy2(src, dst)
            success_count += 1
        else:
            missing.append(img)
            
    print(f"✅ שוכפלו בהצלחה {success_count} שרטוטים לגרסה V11.")
    if missing:
        print(f"❌ שגיאה: חסרים {len(missing)} שרטוטים במקור ההנדסי:")
        for m in missing:
            print(f"   - {m}")
    else:
        print("🎉 100% מהשרטוטים האוטומטיים קיימים ונגזרו לתיקייה החדשה!")

if __name__ == "__main__":
    build_v11_images()
