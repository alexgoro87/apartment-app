import json
from collections import defaultdict

# 1. Read data_v12.js to get floors per building in the app
with open('data_v12.js', 'r', encoding='utf-8') as f:
    content = f.read()
    # Strip the JS variable assignment
    json_start = content.index('[')
    json_end = content.rindex(']') + 1
    app_data = json.loads(content[json_start:json_end])

app_floors = defaultdict(set)
for apt in app_data:
    building = apt.get('building', '')
    floor = apt.get('floor', '')
    if building and floor:
        app_floors[building].add(floor)

# 2. Read raw G4 data to get ALL floors (including non-ML)
with open('v12_temp/raw_g4_data.json', 'r', encoding='utf-8') as f:
    g4_data = json.load(f)

g4_floors = defaultdict(set)
for row in g4_data:
    if not isinstance(row, list) or len(row) < 15:
        continue
    building_code = str(row[14]).strip()  # Column 14 = building/structure name
    floor_str = str(row[10]).strip()       # Column 10 = floor
    
    if not building_code or building_code in ('', 'None', 'null'):
        continue
    # Skip header rows
    if any(c in building_code for c in ['\\n', 'הנבמ', 'רפסמ']):
        continue
        
    g4_floors[building_code].add(floor_str)

# 3. Cross-reference
print("=" * 80)
print(f"{'Building':<10} {'App Max Floor':<15} {'App Floors':<25} {'G4 Max Floor':<15} {'G4 Floors':<30} {'Match?'}")
print("=" * 80)

def parse_floor(f):
    if f in ('קרקע', 'עקרק'):
        return 0
    try:
        return int(f)
    except:
        return -1

for building in sorted(set(list(app_floors.keys()) + list(g4_floors.keys()))):
    app_f = app_floors.get(building, set())
    g4_f = g4_floors.get(building, set())
    
    app_max = max([parse_floor(f) for f in app_f]) if app_f else -1
    g4_max = max([parse_floor(f) for f in g4_f]) if g4_f else -1
    
    match = "YES" if app_max == g4_max else "NO - MISMATCH!"
    
    app_floors_str = ', '.join(sorted(app_f, key=lambda x: parse_floor(x)))
    g4_floors_str = ', '.join(sorted(g4_f, key=lambda x: parse_floor(x)))
    
    print(f"{building:<10} {app_max:<15} {app_floors_str:<25} {g4_max:<15} {g4_floors_str:<30} {match}")

print()
print("CONCLUSION: Buildings where G4 max > App max need special handling (non-ML top floor)")
print("Buildings where G4 max == App max can use the app's own dynamic calculation")
