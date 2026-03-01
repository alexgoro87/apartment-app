import json
import re

# Load the comprehensive data from data_v12.js (which contains all 124 apartments)
with open('data_v12.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Extract the JSON array from the JS file
match = re.search(r'const apartmentData = (\[.*?\]);', js_content, re.DOTALL)
if not match:
    print("Could not find the apartmentData array in data_v12.js")
    exit(1)

raw_data = json.loads(match.group(1))
print(f"Loaded {len(raw_data)} raw apartments from data_v12.js.")

building_max_floors = {}

for apt in raw_data:
    building = apt.get('building')
    if not building:
        continue
        
    floor = apt.get('floor')
    
    # Normalize floor
    if floor in ('קרקע', 'עקרק', 0, '0', ''):
        floor_num = 0
    else:
        try:
            floor_num = int(floor)
        except (ValueError, TypeError):
            floor_num = 0
            
    # Track the absolute maximum floor seen for this building, regardless of price/type
    if building not in building_max_floors or floor_num > building_max_floors[building]:
        building_max_floors[building] = floor_num

print("\n// === GENERATED FROM FULL D4/G4 124-APT DATASET ===")
print("const ARCHITECTURAL_TOP_FLOORS = {")
for b in sorted(building_max_floors.keys()):
    print(f"    '{b}': {building_max_floors[b]},")
print("};")
