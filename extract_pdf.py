import fitz  # PyMuPDF
import os
import re

pdf_path = r"c:\Users\user\Documents\ALEX\HOME\קטלוג-משתכן-רמת-רבין.pdf"
output_dir = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\floorplans"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Mapping between apartment catalog type and PDF page number
pdf_page_map = {
    'A': 42, 'A+': 33, 'A 1': 42, 'A 2': 39, 'A 3': 45, 'A 5': 49, 'A 6': 56,
    'B': 23, 'B-': 54, 'B 1': 28, 'B 2': 29, 'B- 1': 53,
    'C': 13, 'C-': 18, 'C 1': 17, 'C 2': 20, 'C 4': 15, 'C 5': 51, 'C 6': 48, 'C 7': 52, 'C- 1': 19,
    'D': 12, 'D1': 12, 'D2': 12
}

try:
    doc = fitz.open(pdf_path)
    print(f"Successfully opened PDF with {len(doc)} pages.")
    
    for apt_type, page_num in pdf_page_map.items():
        # Sanitize the name just like the JS frontend does
        safe_name = re.sub(r'[^a-zA-Z0-9\+\-]', '_', apt_type)
        output_filename = f"floorplan_{safe_name}.png"
        output_filepath = os.path.join(output_dir, output_filename)
        
        # page_num is 1-indexed in our map
        # fitz uses 0-indexed pages
        actual_page_index = page_num - 1
        
        if actual_page_index < len(doc):
            page = doc[actual_page_index]
            # render page to an image - dpi 150 is a good balance for web
            pix = page.get_pixmap(dpi=150)
            pix.save(output_filepath)
            print(f"Saved {output_filename} (Page {page_num})")
        else:
            print(f"Warning: Page {page_num} out of range for {apt_type}")
            
    doc.close()
    print("PDF extraction completed successfully!")
except Exception as e:
    print(f"Error extracting PDF: {e}")
