import json, re, os

with open('data_v12.js', 'r', encoding='utf-8') as f:
    content = f.read()
match = re.search(r'const apartmentData = (\[.*?\]);', content, re.DOTALL)
data = json.loads(match.group(1))

# 1) Show lot -> building mapping
print("=== LOT -> BUILDING MAPPING ===")
combos = {}
for a in data:
    b = a.get('building', '?')
    l = str(a.get('lot', '?'))
    key = (l, b)
    combos[key] = combos.get(key, 0) + 1
for (lot, bld), cnt in sorted(combos.items()):
    print(f"  lot {lot} -> building {bld} ({cnt} apts)")

# 2) Show imageFile that would be generated
print("\n=== IMAGE FILES (from lot + aptType) ===")
images = {}
for a in data:
    lot = str(a.get('lot', '?'))
    apt_type = a.get('aptType') or a.get('type') or 'C'
    img = f"floorplan_{lot}_{apt_type}.png"
    bld = a.get('building', '?')
    key = (bld, img)
    if key not in images:
        images[key] = {'count': 0, 'exists': os.path.exists(f"floorplans/{img}")}
    images[key]['count'] += 1

for (bld, img), info in sorted(images.items()):
    exists = "OK" if info['exists'] else "MISSING!"
    print(f"  {bld}: {img} (x{info['count']}) [{exists}]")

# 3) Check buildings where lot might be wrong (16R should be 103)
print("\n=== BUILDINGS WITH THEIR LOT VALUES ===")
bld_lots = {}
for a in data:
    b = a.get('building', '?')
    l = str(a.get('lot', '?'))
    if b not in bld_lots:
        bld_lots[b] = set()
    bld_lots[b].add(l)
for b in sorted(bld_lots.keys()):
    print(f"  {b}: lot(s) = {', '.join(sorted(bld_lots[b]))}")
