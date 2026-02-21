import os
import glob
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

PAGES_DIR = "pages_temp"
DEST_DIR = "floorplans"

MISSING_102 = [
    'floorplan_102_C.png', 'floorplan_102_C_1.png', 'floorplan_102_C_2.png', 'floorplan_102_C_3.png',
    'floorplan_102_E.png', 'floorplan_102_E_1.png', 'floorplan_102_E_2.png', 'floorplan_102_E_3.png',
    'floorplan_102_A.png', 'floorplan_102_A_1.png', 'floorplan_102_A_2.png', 'floorplan_102_A_4.png',
    'floorplan_102_A_5.png', 'floorplan_102_A_6.png', 'floorplan_102_B.png', 'floorplan_102_B_1.png',
    'floorplan_102_B_2.png', 'floorplan_102_B_3.png', 'floorplan_102_B_4.png', 'floorplan_102_D.png',
    'floorplan_102_D3.png'
]

MISSING_103 = [
    'floorplan_103_A+_1.png', 'floorplan_103_A+_2.png', 'floorplan_103_A+_3.png', 'floorplan_103_A+_4.png',
    'floorplan_103_B_3.png', 'floorplan_103_B_4.png', 'floorplan_103_C_3.png', 'floorplan_103_C-_2.png'
]

def get_current_page():
    files = sorted(glob.glob(os.path.join(PAGES_DIR, "page_*.png")))
    if not files:
        return None
    return os.path.basename(files[0])

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Floorplan Mapper V8</title>
    <style>
        body { font-family: system-ui; background: #0f172a; color: white; display: flex; margin: 0; height: 100vh; overflow: hidden; }
        .sidebar { width: 350px; background: #1e293b; padding: 20px; overflow-y: auto; border-left: 1px solid #334155; }
        .viewer { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
        img { max-width: 100%; max-height: 80vh; object-fit: contain; background: white; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
        .btn { display: block; width: 100%; text-align: left; padding: 10px; margin-bottom: 8px; background: #3b82f6; color: white; border: none; border-radius: 6px; cursor: pointer; font-family: monospace; font-size: 14px; direction: ltr; }
        .btn:hover { background: #2563eb; }
        .btn.done { background: #10b981; opacity: 0.5; cursor: not-allowed; }
        h3 { margin-top: 0; color: #94a3b8; font-size: 14px; text-transform: uppercase; }
        .skip-btn { background: #ef4444; margin-top: 20px; font-weight: bold; }
        .skip-btn:hover { background: #dc2626; }
    </style>
</head>
<body>
    <div class="viewer">
        <h2>עמוד נוכחי: <span id="current-page">טוען...</span></h2>
        <img id="pdf-image" src="" alt="PDF Page">
        <button class="btn skip-btn" onclick="skipPage()" style="text-align: center; max-width: 300px; padding: 15px;">⏭️ דלג על העמוד (לא שרטוט רלוונטי)</button>
    </div>
    
    <div class="sidebar">
        <h3>מגרש 102 (חסרים)</h3>
        <div id="btns-102"></div>
        <br>
        <h3>מגרש 103 (חסרים)</h3>
        <div id="btns-103"></div>
    </div>

    <script>
        const missing102 = {MISSING_102};
        const missing103 = {MISSING_103};

        async function loadState() {
            const res = await fetch('/state');
            const data = await res.json();
            
            if (!data.currentPage) {
                document.querySelector('.viewer').innerHTML = '<h2>🎉 סיימנו! כל העמודים תויגו. אפשר לסגור את החלון.</h2>';
                return;
            }

            document.getElementById('current-page').innerText = data.currentPage;
            document.getElementById('pdf-image').src = '/pages_temp/' + data.currentPage + '?t=' + Date.now();

            renderButtons('btns-102', missing102, data.completedFiles);
            renderButtons('btns-103', missing103, data.completedFiles);
        }

        function renderButtons(containerId, list, completedFiles) {
            const container = document.getElementById(containerId);
            container.innerHTML = '';
            list.forEach(file => {
                const isDone = completedFiles.includes(file);
                const btn = document.createElement('button');
                btn.className = 'btn' + (isDone ? ' done' : '');
                btn.innerText = file;
                btn.onclick = () => {
                    if (!isDone) mapCurrentPage(file);
                };
                container.appendChild(btn);
            });
        }

        async function mapCurrentPage(targetName) {
            const currentPage = document.getElementById('current-page').innerText;
            await fetch('/map', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ source: currentPage, target: targetName })
            });
            loadState();
        }

        async function skipPage() {
            const currentPage = document.getElementById('current-page').innerText;
            await fetch('/skip', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ source: currentPage })
            });
            loadState();
        }

        loadState();
    </script>
</body>
</html>
"""

class MapperHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # Suppress logging

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html = HTML_TEMPLATE.replace('{MISSING_102}', json.dumps(MISSING_102)).replace('{MISSING_103}', json.dumps(MISSING_103))
            self.wfile.write(html.encode('utf-8'))
        
        elif self.path.startswith('/pages_temp/'):
            filename = os.path.basename(self.path.split('?')[0])
            filepath = os.path.join(PAGES_DIR, filename)
            if os.path.exists(filepath):
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.end_headers()
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                
        elif self.path == '/state':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Find what's already mapped
            completed = []
            if os.path.exists(DEST_DIR):
                completed = [f for f in os.listdir(DEST_DIR) if f.endswith('.png')]
                
            self.wfile.write(json.dumps({
                "currentPage": get_current_page(),
                "completedFiles": completed
            }).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        if self.path == '/map':
            source = data['source']
            target = data['target']
            source_path = os.path.join(PAGES_DIR, source)
            target_path = os.path.join(DEST_DIR, target)
            
            if os.path.exists(source_path):
                os.rename(source_path, target_path)
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')

        elif self.path == '/skip':
            source = data['source']
            source_path = os.path.join(PAGES_DIR, source)
            
            # Just delete it since it's an irrelevant page (like cover or rules)
            if os.path.exists(source_path):
                os.remove(source_path)
                
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"skipped"}')

if __name__ == '__main__':
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
        
    server = HTTPServer(('127.0.0.1', 8080), MapperHandler)
    print("Mapper tool running! Open your browser to: http://127.0.0.1:8080")
    print("Keep this terminal open until you finish tagging.")
    server.serve_forever()
