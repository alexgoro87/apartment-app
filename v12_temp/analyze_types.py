"""Analyze types with real vs placeholder drawings to determine mapping strategy."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\user\Documents\ALEX\HOME\apartment-app\v12_temp\data_v12_rooms_fixed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

real = {}
placeholder = {}
for a in data:
    key = a['type']
    info = str(a['lot']) + '/' + a['building'] + '/apt' + str(a['aptNum'])
    if a['imageFile'] != 'page_001.png':
        real.setdefault(key, set()).add(a['imageFile'])
    else:
        placeholder.setdefault(key, []).append(info)

print('=== TYPES WITH REAL DRAWINGS ===')
for t in sorted(real):
    print('  ' + t + ': ' + str(sorted(real[t])))

print()
print('=== TYPES ONLY IN PLACEHOLDERS (need vision) ===')
for t in sorted(placeholder):
    if t not in real:
        print('  ' + t + ': ' + str(placeholder[t]))

print()
print('=== TYPES WITH BOTH (can infer mapping) ===')
for t in sorted(placeholder):
    if t in real:
        print('  ' + t + ': real=' + str(sorted(real[t])) + ', missing=' + str(placeholder[t]))

# Also print unique placeholder types
print()
unique_missing = sorted(set(t for t in placeholder if t not in real))
print('=== UNIQUE TYPES NEEDING NEW MAPPING: ' + str(len(unique_missing)) + ' ===')
for t in unique_missing:
    print('  ' + t)
