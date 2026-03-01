"""
deploy.py - Automated deploy script for apartmentsrabin.netlify.app
Usage: py deploy.py
"""
import urllib.request
import json
import os
import zipfile
import tempfile
import sys
sys.stdout.reconfigure(encoding='utf-8')

# ===== Config =====
NETLIFY_TOKEN = 'nfp_atEWr1AhLfUj2ziTk5TfdQceetMLaYxRe07c'
SITE_ID = '9f78393b-92dc-44ee-a5ca-ac3cbe108d0c'
SITE_URL = 'https://apartmentsrabin.netlify.app'
APP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')
# ==================

def build_zip():
    print("📦 מכין עדכון לעלות...")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
    tmp.close()
    
    with zipfile.ZipFile(tmp.name, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(APP_DIR):
            # Skip hidden/system dirs
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'pages_temp', 'floorplans', 'docs']]
            for file in files:
                if file.endswith('.py') and file != 'deploy.py':
                    continue  # Skip other python scripts
                
                # Exclude huge blobs
                ext = file.lower().split('.')[-1]
                if ext in ['pdf', 'zip', 'csv', 'numbers']:
                    continue
                    
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, APP_DIR)
                zf.write(full_path, rel_path)
    
    size_mb = os.path.getsize(tmp.name) / (1024 * 1024)
    print(f"   גודל: {size_mb:.1f} MB")
    return tmp.name


def deploy(zip_path):
    print("🚀 מעלה ל-Netlify...")
    with open(zip_path, 'rb') as f:
        data = f.read()

    req = urllib.request.Request(
        f'https://api.netlify.com/api/v1/sites/{SITE_ID}/deploys',
        data=data,
        headers={
            'Content-Type': 'application/zip',
            'Authorization': f'Bearer {NETLIFY_TOKEN}'
        },
        method='POST'
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        body = json.loads(resp.read())
        deploy_id = body.get('id', 'unknown')
        state = body.get('state', 'unknown')
        return deploy_id, state


if __name__ == '__main__':
    print("=" * 45)
    print("  🏢 Deploy: apartmentsrabin.netlify.app")
    print("=" * 45)
    
    zip_path = build_zip()
    try:
        deploy_id, state = deploy(zip_path)
        print(f"\n✅ הועלה בהצלחה!")
        print(f"   Deploy ID: {deploy_id}")
        print(f"   Status: {state}")
        print(f"   כתובת ציבורית: {SITE_URL}")
        print(f"\n⏳ הדף יתעדכן תוך ~30 שניות.")
    except Exception as e:
        print(f"\n❌ שגיאה: {e}")
        sys.exit(1)
    finally:
        os.unlink(zip_path)
