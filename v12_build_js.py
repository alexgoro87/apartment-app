import json
import os
import sys

# Ensure UTF-8 output even if the terminal is problematic
sys.stdout.reconfigure(encoding='utf-8')

refined_json = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\v12_temp\refined_g4_data.json"
mapping_v2 = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\v12_temp\catalog_mapping_v2.json"
output_js = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\data_v12.js"

manual_mapping_overrides = {
    "102_1T_C": "page_012.png", "102_1T_E": "page_013.png", "102_1T_C_1": "page_014.png", 
    "102_1T_E_1": "page_015.png", "102_1T_C_2": "page_016.png", "102_1T_E_2": "page_017.png",
    "102_1T_D": "page_018.png",
    "102_2R_A": "page_019.png", "102_2R_B": "page_020.png", "102_2R_A_1": "page_021.png",
    "102_2R_B_1": "page_022.png", "102_2R_A_2": "page_023.png", "102_2R_B_2": "page_024.png",
    "102_2R_A_4": "page_025.png", "102_2R_B_3": "page_026.png", "102_2R_D3": "page_027.png"
}

def build_v12_js():
    with open(refined_json, 'r', encoding='utf-8') as f:
        apartments = json.load(f)
        
    final_data = []
    for apt in apartments:
        key = f"{apt['lot']}_{apt['building']}_{apt['aptType']}"
        image = manual_mapping_overrides.get(key)
        
        if not image:
            # Shared logic fallback
            for k, v in manual_mapping_overrides.items():
                if f"_{apt['aptType']}" in k:
                    image = v
                    break
        
        if not image: image = "page_001.png" # Default/Fallback
        
        # Add cardinal directions (Mocked based on Lot/Building logic for now)
        direction = "חמה" if apt['lot'] == "102" else "קרירה"
        
        final_data.append({
            "lot": int(apt['lot']),
            "building": apt['building'],
            "aptNum": int(apt['aptNum']),
            "floor": apt['floor'],
            "rooms": int(apt['rooms']),
            "area": float(apt['area']),
            "balcony": float(apt['balcony']),
            "storage": float(apt['storage']) if apt['storage'] else 0,
            "direction": direction,
            "price": apt['price'] or "לא צוין",
            "type": apt['aptType'],
            "imageFile": image
        })

    js_content = f"const apartmentsDataV12 = {json.dumps(final_data, ensure_ascii=False, indent=4)};\n"
    with open(output_js, 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print(f"V12 Data file generated: {output_js}")

if __name__ == "__main__":
    build_v12_js()
