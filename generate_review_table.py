import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

data_file = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\v11_temp\data_v11.js"
output_md = r"C:\Users\user\.gemini\antigravity\brain\a8a89265-7c6f-4346-a55f-523dfd6ff525\v11_data_verification.md"

def extract_v11_data():
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    json_str = content.split('const apartmentsDataV11 = ')[1].split(';\n')[0].strip()
    return json.loads(json_str)

def generate_markdown():
    data = extract_v11_data()
    
    # Sort by Lot and then inside by Building and then Apt
    data = sorted(data, key=lambda x: (x['lot'], int(x['building'].replace('R','').replace('T','').replace('P','')), int(x['aptText'])))
    
    md_content = "# טבלת אימות נתוני V11 (124 דירות)\n\n"
    md_content += "טבלה זו משקפת בצורה שקופה את כל המידע שחולץ אוטומטית מקבצי המקור הרשמיים.\n\n"
    
    md_content += "| מגרש | מבנה | דירה | קומה | חדרים | שטח (מ\"ר) | מרפסת (מ\"ר) | מחסן (מ\"ר) | כיוון | מחיר | טיפוס קטלוג | קישור לשרטוט |\n"
    md_content += "|---|---|---|---|---|---|---|---|---|---|---|---|\n"
    
    for apt in data:
        # absolute path for the image to be clickable in markdown
        img_path = f"file:///C:/Users/user/Documents/ALEX/HOME/apartment-app/floorplans_v11/{apt['imageFile']}"
        
        md_content += f"| {apt['lot']} | {apt['building']} | {apt['aptText']} | {apt['floor']} | {apt['rooms']} | {apt['area']} | {apt['balcony']} | {apt['storage']} | {apt['sunDir']} | {apt['price']:,.0f} ₪ | **{apt['aptType']}** | [צפה בשרטוט ({apt['imageFile']})]({img_path}) |\n"
        
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    print(f"✅ Generated Markdown table with {len(data)} apartments at {output_md}")

if __name__ == '__main__':
    generate_markdown()
