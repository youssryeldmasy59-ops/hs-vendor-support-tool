#!/usr/bin/env python3
"""
Hungerstation Auto Image Downloader & Resizer
Downloads images from Google Drive links in menu Excel files,
cleans their names, numbers them to match menu items, resizes to 800px,
and bundles them into a ready-to-upload ZIP & folder.
"""
import sys, os, re, glob, io, zipfile
from concurrent.futures import ThreadPoolExecutor

try:
    import openpyxl, requests
    from PIL import Image
except ImportError:
    print("Dependencies missing. Run with: uv run --with pillow --with requests --with openpyxl python download_menu_images.py [excel_file]")
    sys.exit(1)

def clean_filename(s):
    s = re.sub(r'[^\w\s]', '', str(s)).strip()
    return re.sub(r'\s+', '_', s)

def extract_gdrive_id(url):
    m = re.search(r'/d/([a-zA-Z0-9_-]+)', str(url))
    if m:
        return m.group(1)
    m = re.search(r'id=([a-zA-Z0-9_-]+)', str(url))
    if m:
        return m.group(1)
    return None

def download_and_process_image(item):
    idx, name, url, out_dir = item
    if not url:
        return None
    file_id = extract_gdrive_id(url)
    if not file_id:
        return None

    # Fetch from Google Drive Direct URL
    headers = {'User-Agent': 'Mozilla/5.0'}
    lh3_url = f'https://lh3.googleusercontent.com/d/{file_id}'
    r = requests.get(lh3_url, headers=headers, timeout=25)
    if r.status_code != 200 or len(r.content) < 1000:
        uc_url = f'https://drive.google.com/uc?export=download&id={file_id}'
        r = requests.get(uc_url, headers=headers, timeout=25)

    if r.status_code != 200 or len(r.content) < 1000:
        print(f"Failed to download image for item {idx}: {name}")
        return None

    # Process and optionally resize image to height 800px (Hungerstation optimal)
    try:
        img = Image.open(io.BytesIO(r.content))
        # Keep aspect ratio, scale so height is 800 (if larger)
        if img.height > 800:
            scale = 800 / img.height
            new_w = int(img.width * scale)
            img = img.resize((new_w, 800), Image.Resampling.LANCZOS)
        
        ext = 'png' if img.format == 'PNG' else 'jpg'
        clean_name = clean_filename(name) or f"item_{idx}"
        filename = f"{idx:02d}_{clean_name}.{ext}"
        filepath = os.path.join(out_dir, filename)

        if ext == 'jpg':
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            img.save(filepath, 'JPEG', quality=92)
        else:
            img.save(filepath, 'PNG')

        return filepath
    except Exception as e:
        # Fallback to raw bytes
        ext = 'png' if 'png' in r.headers.get('content-type', '') else 'jpg'
        clean_name = clean_filename(name) or f"item_{idx}"
        filename = f"{idx:02d}_{clean_name}.{ext}"
        filepath = os.path.join(out_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(r.content)
        return filepath

def process_excel(excel_path, out_dir=None):
    if not out_dir:
        out_dir = os.path.join(os.path.dirname(excel_path), "menu_images")
    os.makedirs(out_dir, exist_ok=True)

    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        print("Empty sheet.")
        return

    # Find name col and link col
    headers = [str(c).strip() if c else '' for c in rows[0]]
    name_col = 0
    link_col = -1

    for c_idx, h in enumerate(headers):
        if any(k in h for k in ['رابط', 'صورة', 'link', 'url', 'image', 'photo', 'drive']):
            link_col = c_idx
        if any(k in h for k in ['اسم', 'name', 'item']):
            name_col = c_idx

    if link_col == -1:
        # Check last column
        link_col = len(headers) - 1

    items = []
    for idx, r in enumerate(rows[1:], start=1):
        if not any(r): continue
        item_name = str(r[name_col] or f"item_{idx}").strip()
        link_val = str(r[link_col] or '').strip() if link_col < len(r) else ''
        if 'drive.google.com' in link_val or 'http' in link_val:
            items.append((idx, item_name, link_val, out_dir))

    print(f"Found {len(items)} items with image links in {os.path.basename(excel_path)}.")
    print("Downloading and processing images...")

    saved_files = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        for res in executor.map(download_and_process_image, items):
            if res:
                saved_files.append(res)

    print(f"Downloaded {len(saved_files)} images successfully into: {out_dir}")

    # Create ZIP
    zip_path = os.path.join(os.path.dirname(out_dir), "menu_images.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in saved_files:
            zipf.write(f, arcname=os.path.basename(f))
    print(f"Created ZIP bundle: {zip_path}")
    return out_dir, zip_path

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    if not target:
        matches = glob.glob("/Users/usefelbedwehy/Downloads/*.xlsx")
        for m in matches:
            if '08ceb' in m:
                target = m
                break
        if not target and matches:
            target = matches[0]
    if target and os.path.exists(target):
        process_excel(target)
    else:
        print("Please provide an Excel file path.")
