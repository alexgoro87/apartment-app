import fitz

def main():
    pdf_path = r"C:\Users\user\Documents\ALEX\HOME\קטלוג-משתכן-רמת-רבין.pdf"
    doc = fitz.open(pdf_path)
    print(f"Total pages: {len(doc)}")
    
    for i in range(10, 20):
        page = doc[i]
        text = page.get_text()
        print(f"--- Page {i} ---")
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        for line in lines:
            if "מתחם" in line or "טיפוס" in line:
                print(f"FOUND: {line}")

if __name__ == "__main__":
    main()
