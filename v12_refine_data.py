import json
import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

raw_json = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\v12_temp\raw_g4_data.json"
refined_json = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\v12_temp\refined_g4_data.json"

def refine_g4_data():
    with open(raw_json, 'r', encoding='utf-8') as f:
        raw_rows = json.load(f)
    
    refined_apartments = []
    
    # Based on the visual inspection of the raw JSON:
    # Most rows have 15 elements.
    # index 14: Building (RTL reversed often)
    # index 13: Lot
    # index 12: Apt Number
    # index 11: Apt Type (Slug/Catalog)
    # index 10: Floor
    # index 9: Rooms
    # index 8: Area
    # index 7: Balcony
    # index 6: Calc Area?
    # index 5: Storage Area
    # index 4: Parking count
    # index 2: Price (with commas)
    
    for row in raw_rows:
        if len(row) < 13: continue
        
        try:
            # Apt Number is usually a clean digit
            apt_num_raw = str(row[12] or "").strip()
            if not apt_num_raw.isdigit(): continue
            
            lot = str(row[13] or "").strip()
            # Basic validation: Lot should be 102 or 103 usually
            if lot not in ["102", "103"]: continue
            
            building = str(row[14] or "").strip()
            # Handle RTL reversal if necessary (e.g., 'T1' vs '1T')
            # The PDF extraction often flips text like "1T" to "T1" or vice versa.
            # Building 1T, 2R, 3T, 4R, 5R, 6T, 7P, 8R, 9R, 10R, 11R, 12R, 13R, 14R, 15R, 16R are the known ones.
            if len(building) >= 2:
                if building[0].isdigit() and building[1].isalpha():
                    pass # already correct format like 1T
                elif building[0].isalpha() and building[1].isdigit():
                    # Flip 'T1' to '1T'
                    building = building[1] + building[0]

            apt_type = str(row[11] or "").strip()
            # Type labels can be reversed too (e.g. 1_C instead of C_1)
            # But usually it's "C_1", "E_1", etc.
            
            floor = str(row[10] or "").strip()
            if "עקרק" in floor: floor = "קרקע"
            
            rooms = str(row[9] or "").strip()
            # Safety check: No 1-room apartments.
            if rooms == "1":
                # Check if it was a parsing error where rooms and floor swapped or similar
                # For now, let's just log and skip or investigate
                print(f"Warning: Found 1-room record at Lot {lot} Bldg {building} Apt {apt_num_raw}. Skipping for deep verification.")
                continue

            area = str(row[8] or "").strip().replace(",", "")
            balcony = str(row[7] or "").strip().replace(",", "")
            storage = str(row[5] or "").strip().replace(",", "")
            price = str(row[2] or "").strip().replace(",", "")
            
            apt_obj = {
                "lot": lot,
                "building": building,
                "aptNum": apt_num_raw,
                "aptType": apt_type,
                "floor": floor,
                "rooms": rooms,
                "area": area,
                "balcony": balcony,
                "storage": storage,
                "price": price
            }
            refined_apartments.append(apt_obj)
            
        except (ValueError, IndexError) as e:
            continue

    print(f"✅ Refined {len(refined_apartments)} apartments from raw data.")
    
    # Sort for consistency
    refined_apartments.sort(key=lambda x: (x['lot'], int(re.sub(r'\D', '', x['building'])), int(x['aptNum'])))

    with open(refined_json, 'w', encoding='utf-8') as f:
        json.dump(refined_apartments, f, ensure_ascii=False, indent=4)
        
    return refined_apartments

import re
if __name__ == "__main__":
    refine_g4_data()
