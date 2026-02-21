import fitz
import os

pdf_path = r"c:\Users\user\Documents\ALEX\HOME\קטלוג-משתכן-רמת-רבין.pdf"
doc = fitz.open(pdf_path)

out_dir = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\crops"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

html = "<html><body style='background:#fff; color:#000; font-family:sans-serif;'><h1>Page Matching</h1>\n"
for i in range(11, 40): # Pages 12 to 40
    page = doc[i]
    rect = page.rect
    
    # We want the top right corner. The pdf text reading had it at top right.
    # The pdf width is usually ~595 for A4. Let's crop the rightmost 250px and top 150px.
    # We will also crop the top-left just in case the PDF is mirrored, but let's stick to top-right first.
    # wait, Hebrew PDF might have the model on the top left if right-to-left. Let's just crop the top 200px of the WHOLE width to be safe!
    crop_rect = fitz.Rect(0, 0, rect.width, 150)
    
    pix = page.get_pixmap(clip=crop_rect, dpi=150)
    filename = f"crop_{i+1}.png"
    pix.save(os.path.join(out_dir, filename))
    html += f'<div style="margin-bottom:20px;"><h2>Page {i+1}</h2><img src="crops/{filename}" style="border:1px solid red; max-width:100%;"/></div>\n'

html += "</body></html>"
with open(r"c:\Users\user\Documents\ALEX\HOME\apartment-app\mapper.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Mapping HTML generated at mapper.html")
doc.close()
