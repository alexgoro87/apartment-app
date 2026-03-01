import json, re

with open('data_v12.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'const apartmentData = (\[.*?\]);', content, re.DOTALL)
data = json.loads(match.group(1))

ARCH_TOP = {'4R': 4, '8R': 3, '11R': 3}

for b, top in ARCH_TOP.items():
    apts_in_b = [a for a in data if a.get('building') == b]
    top_floor_apts = [a for a in apts_in_b if str(a.get('floor')) == str(top)]
    def get_price(a):
        p = a.get('price', 0)
        if isinstance(p, str):
            import re as re2
            num = re2.sub(r'[^\d]', '', p)
            return int(num) if num else 0
        return int(p) if p else 0

    ml_on_top = [a for a in top_floor_apts if get_price(a) > 0]
    free_on_top = [a for a in top_floor_apts if get_price(a) == 0]
    
    print(f"\n=== {b} (Arch top = floor {top}) ===")
    print(f"  כל הדירות בקומה {top}: {len(top_floor_apts)}")
    print(f"  דירות ML (עם מחיר): {len(ml_on_top)}")
    for a in ml_on_top:
        print(f"    → דירה {a.get('aptNum')}, סוג {a.get('aptType')}, מחיר {a.get('price'):,}")
    print(f"  דירות שוק חופשי: {len(free_on_top)}")
    for a in free_on_top:
        print(f"    → דירה {a.get('aptNum')}, סוג {a.get('aptType')}")
    
    floors = sorted(set(str(a.get('floor')) for a in apts_in_b))
    print(f"  כל הקומות בבניין: {floors}")
