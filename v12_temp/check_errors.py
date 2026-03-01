import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data_v12_rooms_fixed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

error_types = ['C_1', 'B', 'B_1', 'B_2', 'B_3', 'C_2']
for a in data:
    if a['lot'] == 103 and a['type'] in error_types:
        print(f"lot={a['lot']} bldg={a['building']} type={a['type']} apt={a['aptNum']} floor={a['floor']} rooms={a['rooms']} area={a['area']} img={a['imageFile']}")
