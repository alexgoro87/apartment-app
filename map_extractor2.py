import fitz
import os

pdf_path = r"c:\Users\user\Documents\ALEX\HOME\קטלוג-משתכן-רמת-רבין.pdf"
doc = fitz.open(pdf_path)

out_dir = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\crops"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

html = "<html><body style='background:#fff; color:#000; font-family:sans-serif;'><h1>Page Matching Part 2</h1>\n"
for i in range(39, len(doc)): # Pages 40 to end
    page = doc[i]
    rect = page.rect
    crop_rect = fitz.Rect(0, 0, rect.width, 150)
    
    pix = page.get_pixmap(clip=crop_rect, dpi=150)
    filename = f"crop_{i+1}.png"
    pix.save(os.path.join(out_dir, filename))
    html += f'<div style="margin-bottom:20px;"><h2>Page {i+1}</h2><img src="crops/{filename}" style="border:1px solid red; max-width:100%;"/></div>\n'

html += "</body></html>"
with open(r"c:\Users\user\Documents\ALEX\HOME\apartment-app\mapper2.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Mapping HTML 2 generated at mapper2.html")
doc.close()
