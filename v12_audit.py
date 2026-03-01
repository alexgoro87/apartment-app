"""Step 1: Generate v12_audit.html - interactive audit table with embedded floorplan images."""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DATA_JS = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\data_v12.js"
CATALOG_DIR = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\v12_temp\catalog_pages"
OUTPUT_HTML = r"c:\Users\user\Documents\ALEX\HOME\apartment-app\v12_audit.html"

def load_data():
    with open(DATA_JS, 'r', encoding='utf-8') as f:
        content = f.read()
    json_str = content.split('const apartmentsDataV12 = ')[1].rsplit(';', 1)[0].strip()
    return json.loads(json_str)

def generate_html(data):
    rows = []
    placeholder_count = 0
    for i, a in enumerate(data):
        is_placeholder = a['imageFile'] == 'page_001.png'
        if is_placeholder:
            placeholder_count += 1
        row_class = 'placeholder' if is_placeholder else ''
        img_path = os.path.join(CATALOG_DIR, a['imageFile']).replace('\\', '/')
        
        rows.append(f"""
        <tr class="{row_class}" onclick="showImage('{img_path}', {i})">
            <td>{i+1}</td>
            <td>{a['lot']}</td>
            <td>{a['building']}</td>
            <td>{a['aptNum']}</td>
            <td>{a['floor']}</td>
            <td>{a['rooms']}</td>
            <td>{a['area']}</td>
            <td>{a['balcony']}</td>
            <td>{a['storage']}</td>
            <td>{a['direction']}</td>
            <td>{a['price']}</td>
            <td>{a['type']}</td>
            <td>{a['imageFile']}</td>
        </tr>""")

    total = len(data)
    html = f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<title>V12 Audit Table</title>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background: #1a1a2e; color: #eee; display: flex; height: 100vh; }}
    .table-panel {{ flex: 1; overflow-y: auto; padding: 10px; }}
    .image-panel {{ width: 45%; background: #16213e; border-right: 2px solid #0f3460; overflow-y: auto; padding: 10px; position: sticky; top: 0; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; }}
    .image-panel img {{ max-width: 100%; max-height: 85vh; object-fit: contain; border-radius: 8px; margin-top: 10px; }}
    .image-panel h3 {{ color: #e94560; margin: 10px 0 5px; }}
    .stats {{ background: #0f3460; padding: 10px 15px; border-radius: 8px; margin-bottom: 10px; display: flex; gap: 20px; flex-wrap: wrap; }}
    .stats span {{ font-size: 14px; }}
    .stats .warn {{ color: #e94560; font-weight: bold; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th {{ background: #0f3460; color: #e94560; padding: 8px 4px; position: sticky; top: 0; z-index: 2; }}
    td {{ padding: 6px 4px; border-bottom: 1px solid #2a2a4a; text-align: center; }}
    tr {{ cursor: pointer; transition: background 0.2s; }}
    tr:hover {{ background: #1f4068; }}
    tr.placeholder {{ background: rgba(233, 69, 96, 0.15); }}
    tr.placeholder:hover {{ background: rgba(233, 69, 96, 0.3); }}
    tr.selected {{ background: #0f3460 !important; outline: 2px solid #e94560; }}
    .badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; }}
    .badge-ok {{ background: #2ecc71; color: #000; }}
    .badge-warn {{ background: #e94560; color: #fff; }}
</style>
</head>
<body>
<div class="table-panel">
    <div class="stats">
        <span>סה"כ דירות: <b>{total}</b></span>
        <span class="warn">⚠ ללא שרטוט (page_001): <b>{placeholder_count}</b></span>
        <span>עם שרטוט: <b>{total - placeholder_count}</b></span>
    </div>
    <table>
        <thead>
            <tr>
                <th>#</th><th>מגרש</th><th>מבנה</th><th>דירה</th><th>קומה</th>
                <th>חדרים</th><th>שטח</th><th>מרפסת</th><th>מחסן</th>
                <th>כיוון</th><th>מחיר</th><th>טיפוס</th><th>קובץ</th>
            </tr>
        </thead>
        <tbody>
            {''.join(rows)}
        </tbody>
    </table>
</div>
<div class="image-panel" id="imagePanel">
    <h3>לחץ על שורה לצפייה בשרטוט</h3>
    <p style="color:#888; font-size:13px;">בחר דירה מהטבלה</p>
</div>

<script>
let selectedRow = null;
function showImage(path, idx) {{
    const panel = document.getElementById('imagePanel');
    const rows = document.querySelectorAll('tbody tr');
    if (selectedRow !== null) rows[selectedRow].classList.remove('selected');
    rows[idx].classList.add('selected');
    selectedRow = idx;
    const isPlaceholder = path.endsWith('page_001.png');
    panel.innerHTML = `
        <h3>${{isPlaceholder ? '⚠ PLACEHOLDER – לא שרטוט אמיתי' : '✅ שרטוט'}}</h3>
        <p style="color:#888; font-size:12px;">${{path.split('/').pop()}}</p>
        <img src="file:///${{path}}" onerror="this.src='${{path}}'">
    `;
}}
</script>
</body>
</html>"""
    return html

if __name__ == '__main__':
    data = load_data()
    html = generate_html(data)
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ Generated {OUTPUT_HTML}")
    print(f"   Total apartments: {len(data)}")
    placeholders = sum(1 for a in data if a['imageFile'] == 'page_001.png')
    print(f"   Placeholders (page_001): {placeholders}")
    print(f"   With real drawing: {len(data) - placeholders}")
