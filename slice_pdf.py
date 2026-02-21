import sys
import os
import fitz  # PyMuPDF

def main():
    pdf_path = r"C:\Users\user\Documents\ALEX\HOME\קטלוג-משתכן-רמת-רבין.pdf"
    output_dir = r"C:\Users\user\Documents\ALEX\HOME\apartment-app\pages_temp"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Opening PDF...")
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    print(f"Total pages found: {total_pages}")
    print("Slicing pages into high-res PNG images...")

    zoom = 2.0 # Increase resolution
    mat = fitz.Matrix(zoom, zoom)

    for i in range(total_pages):
        page = doc.load_page(i)
        pix = page.get_pixmap(matrix=mat)
        
        # Format page number to be 3 digits, e.g., page_001.png
        output_path = os.path.join(output_dir, f"page_{i+1:03d}.png")
        pix.save(output_path)
        
        # Print progress
        sys.stdout.write(f"\rSaved page {i+1} of {total_pages}")
        sys.stdout.flush()

    print("\nDone! All pages exported to pages_temp/")

if __name__ == "__main__":
    main()
