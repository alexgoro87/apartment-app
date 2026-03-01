"""
Create catalog_mapping_v3.json - FINAL version with all mappings corrected.
Based on complete visual analysis of catalog pages 28-56.
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data_v12_rooms_fixed.json', 'r', encoding='utf-8') as f:
    apartments = json.load(f)

# ============================================================================
# COMPLETE TYPE-TO-PAGE MAPPING
# ============================================================================
# Key format: (lot, building_suffix_or_pattern, type) -> page
# We use a function to resolve the correct page for each apartment

def get_page_for_apartment(lot, building, apt_type, area):
    """Return the correct catalog page number for this apartment."""
    
    # ---- LOT 102 ----
    if lot == 102:
        mapping = {
            "C": 12,      "E": 13,      "C_1": 14,    "E_1": 15,
            "C_2": 16,    "E_2": 17,    "D": 18,      "A": 19,
            "B": 20,      "A_1": 21,    "B_1": 22,    "A_2": 23,
            "B_2": 24,    "A_4": 25,    "B_3": 26,    "D3": 27,
            "E_3": 32,    "C_3": 35,    "B_4": 30,    "A_5": 40,
            "A_3": 45,    "A_6": 40,    "B_5": 44,    "E_4": 32,
            "C_4": 37,
        }
        return mapping.get(apt_type)
    
    # ---- LOT 103 ----
    if lot == 103:
        bldg_num = int(''.join(c for c in building if c.isdigit()))
        
        # ---- BUILDING 7P (pentahouse) ----
        if building == "7P":
            m = {"A": 46, "C": 47, "A_1": 46, "C_4": 47, "C_6": 48,
                 "A_5": 49, "D1": 18}
            return m.get(apt_type)
        
        # ---- BUILDINGS 8R, 13R, 14R (A+ ground floor family) ----
        if building in ("8R", "13R", "14R"):
            m = {
                # Ground floor types
                "A+": 33,     "A+_2": 33,   "A+_3": 34,
                "C_3": 35,    "C_1": 35,    # C_1 in 103/8R is actually C_3 layout (88.71m²)
                "C_2": 51,    # C_2 in 103/13R ground floor -> use C_5 page
                # Floor 1
                "A _2": 50,   "C_5": 51,    "A_2": 50,
                # Floor 2
                "A_5": 49,    "C_7": 52,
                # Penthouse
                "D1": 18,
            }
            return m.get(apt_type)
        
        # ---- BUILDINGS 10R, 11R (A+ ground floor, B- upper) ----
        if building in ("10R", "11R"):
            m = {
                "A+_1": 33,   "B_1": 54,    # B_1 ground floor -> B- layout
                # Floor 1
                "B-": 54,     "A_2": 50,
                # Floor 2  
                "B-_1": 53,   "A_5": 49,
                # Penthouse
                "D": 18,
            }
            return m.get(apt_type)
        
        # ---- BUILDINGS 9R, 12R, 15R (C- ground floor, A/B- upper) ----
        if building in ("9R", "12R", "15R"):
            m = {
                # Ground floor
                "C-": 53,     "C-_1": 53,   "C-_2": 53,
                "B": 54,      "B_2": 54,    "B_3": 54,    # B variants -> B- layout
                # Floor 1
                "A_3": 55,    "B-": 54,
                # Floor 2
                "A_6": 56,    "B-_1": 53,
                # Penthouse
                "D": 18,      "D2": 27,
            }
            return m.get(apt_type)
        
        # ---- BUILDING 16R (B_4 + A+_4 ground floor) ----
        if building == "16R":
            m = {
                "B_4": 30,    "A+_4": 33,
                "B-": 54,     "A_2": 50,
                "B-_1": 53,   "A_5": 49,
                "D": 18,
            }
            return m.get(apt_type)
    
    return None

# ============================================================================
# PROCESS ALL APARTMENTS
# ============================================================================
mapping_v3 = {}
updated_count = 0
already_correct = 0
errors = []

for apt in apartments:
    lot = apt['lot']
    building = apt['building']
    apt_type = apt['type']
    area = apt['area']
    current_image = apt.get('imageFile', 'page_001.png')
    
    key = f"{lot}_{building}_{apt_type}"
    
    page = get_page_for_apartment(lot, building, apt_type, area)
    
    if page is None:
        errors.append(f"NOT MAPPED: lot={lot}, bldg={building}, type={apt_type}, area={area}, current={current_image}")
        # Keep existing mapping
        page_num = int(current_image.replace('page_', '').replace('.png', ''))
        mapping_v3[key] = page_num
    else:
        mapping_v3[key] = page
        expected_image = f"page_{page:03d}.png"
        if current_image == 'page_001.png':
            updated_count += 1
        elif current_image != expected_image:
            # Was mapped to wrong page (lot 102 page used for lot 103 apt)
            updated_count += 1

# Save mapping_v3
with open('catalog_mapping_v3.json', 'w', encoding='utf-8') as f:
    json.dump(mapping_v3, f, indent=2, ensure_ascii=False)

# Print summary
print(f"\n{'='*60}")
print(f"CATALOG MAPPING V3 - FINAL SUMMARY")
print(f"{'='*60}")
print(f"Total unique type-building combinations: {len(mapping_v3)}")
print(f"Apartments that will be updated: {updated_count}")
print(f"Errors (unmapped): {len(errors)}")
if errors:
    print(f"\nUNMAPPED:")
    for e in errors:
        print(f"  {e}")

# Print full mapping sorted by page
print(f"\n{'='*60}")
print(f"COMPLETE MAPPING:")
print(f"{'='*60}")
for key, page in sorted(mapping_v3.items(), key=lambda x: (x[1], x[0])):
    print(f"  {key:30s} -> page_{page:03d}.png")
