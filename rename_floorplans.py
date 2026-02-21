import os
import glob

def main():
    floorplan_dir = "floorplans"
    if not os.path.exists(floorplan_dir):
        print("Directory 'floorplans' not found!")
        return

    png_files = glob.glob(os.path.join(floorplan_dir, "*.png"))
    renamed_count = 0

    for filepath in png_files:
        filename = os.path.basename(filepath)
        # Skip files that already have a lot prefix like 'floorplan_102_' or 'floorplan_103_'
        if filename.startswith("floorplan_10") and len(filename) > 13 and filename[13] == '_':
            continue
        
        # We assume the current 24 un-prefixed files belong to Lot 103
        if filename.startswith("floorplan_"):
            new_filename = filename.replace("floorplan_", "floorplan_103_", 1)
            new_filepath = os.path.join(floorplan_dir, new_filename)
            
            os.rename(filepath, new_filepath)
            print(f"Renamed: {filename} -> {new_filename}")
            renamed_count += 1
            
    print(f"\nSuccessfully renamed {renamed_count} floorplan(s) for Lot 103.")

if __name__ == "__main__":
    main()
