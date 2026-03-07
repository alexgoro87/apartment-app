"""
V22 Full Audit: All 100 ML apartments
Checks: lot mapping, aptType formatting, floorplan existence, required fields, data consistency
"""
import json, re, os

# Load data
with open('data_v12.js', 'r', encoding='utf-8') as f:
    content = f.read()
match = re.search(r'const apartmentData = (\[.*?\]);', content, re.DOTALL)
data = json.loads(match.group(1))

# Expected lot mapping (from G4)
LOT_MAP = {
    '1T': '102', '2R': '102', '3T': '102', '4R': '102', '5R': '102', '6T': '102',
    '7P': '103', '8R': '103', '9R': '103', '10R': '103', '11R': '103',
    '12R': '103', '13R': '103', '14R': '103', '15R': '103', '16R': '103'
}

errors = []
warnings = []
stats = {'total': 0, 'ml': 0, 'free': 0, 'ok': 0, 'errors': 0}

for i, apt in enumerate(data):
    stats['total'] += 1
    bld = apt.get('building', '?')
    lot = str(apt.get('lot', '?'))
    apt_type = apt.get('aptType') or apt.get('type') or ''
    price = apt.get('price', 0)
    floor = apt.get('floor', '?')
    rooms = apt.get('rooms', None)
    area = apt.get('area', None)
    direction = apt.get('direction', '')
    apt_num = apt.get('aptNum', '?')

    # Parse price
    if isinstance(price, str):
        price_num = int(re.sub(r'[^\d]', '', price)) if re.sub(r'[^\d]', '', price) else 0
    else:
        price_num = int(price) if price else 0

    is_ml = price_num > 0
    if is_ml:
        stats['ml'] += 1
    else:
        stats['free'] += 1

    apt_id = f"#{apt_num} {bld} f{floor}"
    apt_errors = []

    # 1. Lot check
    expected_lot = LOT_MAP.get(bld)
    if expected_lot and lot != expected_lot:
        apt_errors.append(f"LOT MISMATCH: has {lot}, expected {expected_lot}")

    # 2. aptType spacing check
    if ' ' in apt_type.strip():
        apt_errors.append(f"APTTYPE SPACE: '{apt_type}' has embedded space")

    # 3. Floorplan file check
    img_file = f"floorplan_{lot}_{apt_type}.png"
    img_path = os.path.join('floorplans', img_file)
    if apt_type and not os.path.exists(img_path):
        apt_errors.append(f"FLOORPLAN MISSING: {img_file}")

    # 4. Required fields (ML apartments only)
    if is_ml:
        if not rooms:
            apt_errors.append("MISSING: rooms")
        if not area:
            apt_errors.append("MISSING: area")
        if not direction:
            apt_errors.append("MISSING: direction")
        if not apt_type:
            apt_errors.append("MISSING: aptType")
        if floor == '?' or floor is None:
            apt_errors.append("MISSING: floor")

    # 5. Sanity checks
    if is_ml:
        if isinstance(rooms, (int, float)) and (rooms < 1 or rooms > 7):
            apt_errors.append(f"SUSPECT: rooms={rooms}")
        if isinstance(area, (int, float)) and (area < 30 or area > 300):
            apt_errors.append(f"SUSPECT: area={area}")
        if price_num < 500000 or price_num > 3000000:
            apt_errors.append(f"SUSPECT: price={price_num}")

    if apt_errors:
        stats['errors'] += 1
        for e in apt_errors:
            errors.append(f"  {apt_id}: {e}")
    else:
        stats['ok'] += 1

# Print report
print("=" * 60)
print("V22 FULL AUDIT REPORT")
print("=" * 60)
print(f"\nTotal apartments in data_v12.js: {stats['total']}")
print(f"  ML (with price): {stats['ml']}")
print(f"  Free market (no price): {stats['free']}")
print(f"\nApartments with issues: {stats['errors']}")
print(f"Apartments OK: {stats['ok']}")
print()

if errors:
    print("ERRORS FOUND:")
    print("-" * 40)
    for e in errors:
        print(e)
else:
    print("NO ERRORS FOUND!")

# Also print per-building summary
print("\n" + "=" * 60)
print("PER-BUILDING SUMMARY (ML apartments only)")
print("=" * 60)
bld_summary = {}
for apt in data:
    price = apt.get('price', 0)
    if isinstance(price, str):
        pn = int(re.sub(r'[^\d]', '', price)) if re.sub(r'[^\d]', '', price) else 0
    else:
        pn = int(price) if price else 0
    if pn <= 0:
        continue
    bld = apt.get('building', '?')
    if bld not in bld_summary:
        bld_summary[bld] = {'count': 0, 'floors': set(), 'types': set(), 'lot': str(apt.get('lot', '?'))}
    bld_summary[bld]['count'] += 1
    bld_summary[bld]['floors'].add(str(apt.get('floor', '?')))
    bld_summary[bld]['types'].add(apt.get('aptType') or apt.get('type') or '?')

for bld in sorted(bld_summary.keys()):
    info = bld_summary[bld]
    floors = ', '.join(sorted(info['floors']))
    types = ', '.join(sorted(info['types']))
    print(f"  {bld} (lot {info['lot']}): {info['count']} apts | floors: {floors} | types: {types}")
