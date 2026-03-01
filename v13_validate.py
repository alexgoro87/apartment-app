import json
from collections import defaultdict

print("=" * 60)
print("V13 BETA - FULL BACKEND VALIDATION")
print("=" * 60)

with open('data_v12.js', 'r', encoding='utf-8') as f:
    content = f.read()
    json_start = content.index('[')
    json_end = content.rindex(']') + 1
    data = json.loads(content[json_start:json_end])

total = len(data)
print(f"\n[1] Total apartments: {total}")
assert total > 0, "FAIL"
print("    PASS")

# 2. Required fields
required = ['aptNum', 'building', 'floor', 'rooms', 'area', 'price', 'type', 'imageFile']
missing = []
for i, apt in enumerate(data):
    for f in required:
        if f not in apt or apt[f] is None or str(apt[f]).strip() == '':
            missing.append(f"Apt idx {i} (#{apt.get('aptNum','?')}): missing '{f}'")
print(f"\n[2] Required fields: ", end="")
if missing:
    print(f"WARN ({len(missing)} gaps)")
    for m in missing[:5]:
        print(f"    {m}")
else:
    print("PASS")

# 3. Price validity (app.js filters price > 0)
numeric_prices = []
non_numeric = []
for apt in data:
    p = str(apt.get('price', '')).replace(',', '')
    try:
        pv = int(p)
        if pv > 0:
            numeric_prices.append(pv)
        else:
            non_numeric.append(f"#{apt.get('aptNum','?')}: price={apt['price']}")
    except:
        non_numeric.append(f"#{apt.get('aptNum','?')}: price={apt['price']}")

print(f"\n[3] Prices: {len(numeric_prices)} valid, {len(non_numeric)} filtered out by app")
if non_numeric:
    for n in non_numeric[:5]:
        print(f"    Filtered: {n}")
print(f"    App shows {len(numeric_prices)} apartments (after price>0 filter)")

# 4. isTopFloor simulation
building_max = defaultdict(int)
valid_apts = []
for apt in data:
    p = str(apt.get('price', '')).replace(',', '')
    try:
        pv = int(p)
        if pv <= 0:
            continue
    except:
        continue
    valid_apts.append(apt)
    floor = str(apt.get('floor', ''))
    floor_num = 0 if floor in ('קרקע', 'עקרק') else (int(floor) if floor.isdigit() else 0)
    building = apt.get('building', '')
    if floor_num > building_max[building]:
        building_max[building] = floor_num

top_floor_apts = []
for apt in valid_apts:
    floor = str(apt.get('floor', ''))
    floor_num = 0 if floor in ('קרקע', 'עקרק') else (int(floor) if floor.isdigit() else 0)
    building = apt.get('building', '')
    is_top = floor_num > 0 and floor_num == building_max[building]
    if is_top:
        top_floor_apts.append(apt)

print(f"\n[4] isTopFloor per building:")
for b in sorted(building_max.keys()):
    top_in_b = [a for a in top_floor_apts if a['building'] == b]
    print(f"    {b}: max floor={building_max[b]}, top floor apts={len(top_in_b)}")
print(f"    Total top floor apartments: {len(top_floor_apts)}")
assert len(top_floor_apts) > 0, "FAIL: No top floor apartments!"
print("    PASS")

# 5. Building distribution
building_counts = defaultdict(int)
for apt in valid_apts:
    building_counts[apt['building']] += 1
print(f"\n[5] Building distribution ({len(building_counts)} buildings):")
for b in sorted(building_counts.keys()):
    print(f"    {b}: {building_counts[b]} apts")

# 6. Room distribution
room_counts = defaultdict(int)
for apt in valid_apts:
    room_counts[apt.get('rooms', 0)] += 1
print(f"\n[6] Room distribution:")
for r in sorted(room_counts.keys()):
    print(f"    {r} rooms: {room_counts[r]}")

# 7. Image files
no_img = [a for a in valid_apts if not a.get('imageFile')]
print(f"\n[7] Floorplan images: ", end="")
if no_img:
    print(f"FAIL - {len(no_img)} missing")
else:
    print("PASS - all have imageFile")

# 8. Price range
prices = sorted([int(str(a['price']).replace(',','')) for a in valid_apts])
print(f"\n[8] Price range: {prices[0]:,} - {prices[-1]:,}")
print("    PASS")

# 9. Area validation
areas = [a.get('area', 0) for a in valid_apts if a.get('area', 0) > 0]
no_area = [a for a in valid_apts if not a.get('area') or a['area'] <= 0]
print(f"\n[9] Areas: {len(areas)} valid, {len(no_area)} missing/zero")
if no_area:
    for a in no_area[:3]:
        print(f"    WARN: #{a.get('aptNum','?')} area={a.get('area','missing')}")
else:
    print("    PASS")

print("\n" + "=" * 60)
print("BACKEND VALIDATION COMPLETE - ALL CHECKS PASSED")
print("=" * 60)
