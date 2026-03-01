import json

with open('data_v12.js', 'r', encoding='utf-8') as f:
    content = f.read()
    json_start = content.index('[')
    json_end = content.rindex(']') + 1
    data = json.loads(content[json_start:json_end])

print("BUILDING 4R PROFILE:")
b4r = [a for a in data if a.get('building') == '4R']
b4r.sort(key=lambda x: (int(x.get('floor')) if str(x.get('floor')).isdigit() else 0, x.get('aptNum')))
for a in b4r:
    print(f"  Apt {a.get('aptNum')}: Floor {a.get('floor')}, Price: {a.get('price')}, Type: {a.get('type')}")

print("\nBUILDING 11R PROFILE:")
b11r = [a for a in data if a.get('building') == '11R']
b11r.sort(key=lambda x: (int(x.get('floor')) if str(x.get('floor')).isdigit() else 0, x.get('aptNum')))
for a in b11r:
    print(f"  Apt {a.get('aptNum')}: Floor {a.get('floor')}, Price: {a.get('price')}, Type: {a.get('type')}")

print("\nALL APARTMENTS WITH NO PRICE:")
no_price = [a for a in data if str(a.get('price', '')).strip() in ('', 'לא צוין')]
for a in no_price:
    print(f"  {a.get('building')} Apt {a.get('aptNum')}: Floor {a.get('floor')}, Type: {a.get('type')}")
