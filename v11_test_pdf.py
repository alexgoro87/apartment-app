import fitz
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"c:\Users\user\Documents\ALEX\HOME\קטלוג-משתכן-רמת-רבין.pdf"

def analyze_pdf():
    doc = fitz.open(pdf_path)
    print("Searching for model names in PDF pages...")
    
    # We only care about pages 11 to 45 (0-indexed 10 to 44) since first 10 pages are intro
    for i in range(10, 45):
        if i >= len(doc): break
        
        page = doc[i]
        text = page.get_text("text").strip()
        lines = text.split('\n')
        
        # Print top 5 lines of each page, as they usually contain the model type
        print(f"--- Page {i+1} ---")
        for j, line in enumerate(lines[:5]):
            print(f"  Line {j+1}: {line}")

if __name__ == "__main__":
    analyze_pdf()
