import json

input_json = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\v12_temp\refined_g4_data.json"
# I will define the manual mappings here based on the catalog page inspection
# Lot 102:
# Buildings 1T, 3T, 6T use standard T-series layouts
# Buildings 2R, 4R, 5R use standard R-series layouts
# Lot 103:
# Buildings 7P, 8R... 16R

manual_mapping = {
    # Building 1T (Lot 102)
    "102_1T_C": 12, "102_1T_E": 13, "102_1T_C_1": 14, "102_1T_E_1": 15,
    "102_1T_C_2": 16, "102_1T_E_2": 17, "102_1T_C_1": 14, "102_1T_E_1": 15,
    "102_1T_D": 18,
    
    # Building 2R (Lot 102)
    "102_2R_A": 19, "102_2R_B": 20, "102_2R_A_1": 21, "102_2R_B_1": 22,
    "102_2R_A_2": 23, "102_2R_B_2": 24, "102_2R_A_4": 25, "102_2R_B_3": 26,
    "102_2R_D3": 27,
    
    # Building 3T (Lot 102)
    "102_3T_E_3": 28, "102_3T_C_3": 29, "102_3T_E_1": 30, "102_3T_C_1": 31,
    "102_3T_E_2": 32, "102_3T_C_2": 33, "102_3T_D": 34,
    
    # Lot 103 Building 7P
    "103_7P_A": 35, "103_7P_C": 36, "103_7P_A_1": 37, "103_7P_C_4": 38,
    "103_7P_A_5": 39, "103_7P_C_6": 40, "103_7P_D1": 41,
    
    # Building 8R (Lot 103)
    "103_8R_A+": 42, "103_8R_C_1": 43, "103_8R_A_2": 44, "103_8R_C_5": 45,
    "103_8R_A_5": 46, "103_8R_C_7": 47, "103_8R_D1": 48
}

def finalize_mapping():
    with open(input_json, 'r', encoding='utf-8') as f:
        apartments = json.load(f)
        
    final_output = []
    for apt in apartments:
        key = f"{apt['lot']}_{apt['building']}_{apt['aptType']}"
        # Fallback to a simpler key if specific building match fails
        page = manual_mapping.get(key)
        
        if not page:
            # logic for shared types across buildings
            # e.g. all 1T/3T/6T share similar layouts
            base_type = apt['aptType']
            for k, v in manual_mapping.items():
                if f"_{base_type}" in k:
                    page = v
                    break
        
        if page:
            image_name = f"page_{page:03}.png"
        else:
            image_name = "default.png"
            
        apt['imageFile'] = image_name
        final_output.append(apt)
        
    print(f"Finalized {len(final_output)} apartments with image mappings.")
    return final_output

if __name__ == "__main__":
    finalize_mapping()
