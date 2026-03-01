import fitz
import os

pdf_path = r"c:\Users\user\Documents\ALEX\HOME\קטלוג-משתכן-רמת-רבין.pdf"
export_dir = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\v12_temp\catalog_pages"

def export_all_pages():
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
        
    doc = fitz.open(pdf_path)
    print(f"Exporting {len(doc)} pages to {export_dir}...")
    
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=150)
        out_path = os.path.join(export_dir, f"page_{i+1:03}.png")
        pix.save(out_path)
        if (i+1) % 10 == 0:
            print(f"Exported {i+1} pages...")

if __name__ == "__main__":
    export_all_pages()
