"""Check exactly which apartments have missing floorplans and what their original imageFile field says"""
import json, re

with open('data_v12.js', 'r', encoding='utf-8') as f:
    content = f.read()
match = re.search(r'const apartmentData = (\[.*?\]);', content, re.DOTALL)
data = json.loads(match.group(1))

missing_types = ['A_3', 'B_5', 'C_4', 'E_4']
for apt in data:
    t = apt.get('type', '')
    if t in missing_types and str(apt.get('lot')) == '102':
        print(f"Building {apt['building']}, Apt #{apt.get('aptNum')}, Floor {apt.get('floor')}, "
              f"Type={t}, Lot={apt.get('lot')}, imageFile={apt.get('imageFile','?')}")
