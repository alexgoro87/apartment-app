"""
Step 5: Rebuild data_v12.js using catalog_mapping_v3.json
Updates all apartments with correct floorplan page images.
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# Load data and mapping
with open('data_v12_rooms_fixed.json', 'r', encoding='utf-8') as f:
    apartments = json.load(f)

with open('catalog_mapping_v3.json', 'r', encoding='utf-8') as f:
    mapping = json.load(f)

# Apply mapping
updated = 0
was_placeholder = 0
was_wrong_page = 0

for apt in apartments:
    key = f"{apt['lot']}_{apt['building']}_{apt['type']}"
    old_image = apt['imageFile']
    
    if key in mapping:
        page = mapping[key]
        new_image = f"page_{page:03d}.png"
        
        if old_image != new_image:
            if old_image == 'page_001.png':
                was_placeholder += 1
            else:
                was_wrong_page += 1
            apt['imageFile'] = new_image
            updated += 1
    else:
        print(f"WARNING: No mapping for {key}")

# Save as data_v12.js format
js_content = "const apartmentData = "
js_content += json.dumps(apartments, indent=2, ensure_ascii=False)
js_content += ";\n"

with open('../data_v12.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

# Also save as JSON for verification
with open('data_v12_final.json', 'w', encoding='utf-8') as f:
    json.dump(apartments, f, indent=2, ensure_ascii=False)

print(f"\n{'='*60}")
print(f"DATA V12 REBUILD - COMPLETE")
print(f"{'='*60}")
print(f"Total apartments: {len(apartments)}")
print(f"Updated: {updated}")
print(f"  - Were placeholder (page_001): {was_placeholder}")
print(f"  - Were wrong page: {was_wrong_page}")
print(f"  - Already correct: {len(apartments) - updated}")
print(f"\nOutput files:")
print(f"  - data_v12.js (production)")
print(f"  - data_v12_final.json (verification)")

# Verify no placeholders remain
remaining_placeholders = sum(1 for a in apartments if a['imageFile'] == 'page_001.png')
print(f"\nRemaining placeholders: {remaining_placeholders}")

# Show distribution of pages used
from collections import Counter
page_dist = Counter(a['imageFile'] for a in apartments)
print(f"\nPage distribution:")
for page, count in sorted(page_dist.items()):
    print(f"  {page}: {count} apartments")
