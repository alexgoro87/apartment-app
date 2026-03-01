import json
from collections import defaultdict

def main():
    with open('v12_temp/raw_g4_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    max_floors = defaultdict(int)
    
    # data is a list of lists (rows from the table)
    # The columns in G4 PDF are typically:
    # idx 14: building
    # idx 10: floor
    for row in data:
        if not isinstance(row, list) or len(row) < 15:
            continue
            
        building = str(row[14]).strip()
        floor_str = str(row[10]).strip()
        
        # Skip headers or empty
        if not building or building == '/רפסמ\nםש\nהנבמ':
            continue
            
        if floor_str == 'עקרק' or floor_str == 'קרקע':
            floor_num = 0
        else:
            try:
                floor_num = int(floor_str)
            except ValueError:
                continue
                
        if floor_num > max_floors[building]:
            max_floors[building] = floor_num

    print("REAL_BUILDING_FLOORS = {")
    for b in sorted(max_floors.keys(), key=lambda x: int(x) if x.isdigit() else x):
        print(f'    "{b}": {max_floors[b]},')
    print("};")

if __name__ == '__main__':
    main()
