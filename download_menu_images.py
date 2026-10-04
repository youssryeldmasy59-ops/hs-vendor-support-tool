#!/usr/bin/env python3
"""
Hungerstation Menu Image Downloader & Resizer (640x480)
- Extracts images by item order and category
- Checks dimensions: if already 640x480, leaves original untouched
- If different size: resizes cleanly to 640x480 with high-quality letterbox
- Names images by order and category: 01_[Category]_[ItemName].jpg
- Bundles into a sorted ZIP file
"""
import sys, os, re, io, zipfile, shutil
from concurrent.futures import ThreadPoolExecutor

try:
    import openpyxl, requests
    from PIL import Image
except ImportError:
    print("Dependencies missing. Run with uv: uv run --with pillow --with requests --with openpyxl python download_menu_images.py [excel_file]")
    sys.exit(1)

def extract_gdrive_id(url):
    m = re.search(r'(?:file/d/|open\?id=|uc\?(?:export=download&)?id=)([a-zA-Z0-9_-]+)', str(url))
    return m.group(1) if m else None

def clean_name(s):
    s = str(s or '').strip()
    s = re.sub(r'[\U00010000-\U0010ffff\u2600-\u27bf]', '', s)
    s = re.sub(r'[^\w\u0600-\u06FF-]', '_', s)
    return re.sub(r'_+', '_', s).strip('_')

def process_item_image(item):
    idx, cat, name, url, out_dir = item
    if not url:
        return False, idx, "No URL"

    direct_url = url
    file_id = extract_gdrive_id(url)
    if file_id:
        direct_url = f'https://lh3.googleusercontent.com/d/{file_id}'

    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(direct_url, headers=headers, timeout=25)
        if r.status_code != 200 or len(r.content) < 1000:
            if file_id:
                uc_url = f'https://drive.google.com/uc?export=download&id={file_id}'
                r = requests.get(uc_url, headers=headers, timeout=25)
        
        if r.status_code != 200 or len(r.content) < 1000:
            return False, idx, f"Download failed (HTTP {r.status_code})"

        safe_cat = clean_name(cat) or 'عام'
        safe_name = clean_name(name) or f'صنف_{idx}'
        fname = f"{idx:02d}_[{safe_cat}]_{safe_name}.jpg"
        fpath = os.path.join(out_dir, fname)

        img = Image.open(io.BytesIO(r.content)).convert('RGB')
        
        # Check if already 640x480
        if img.size == (640, 480):
            # Keep original bytes without re-compression
            with open(fpath, 'wb') as f:
                f.write(r.content)
            return True, idx, f"Saved as-is (Already 640x480): {fname}"
        else:
            # Aspect-Fill (Cover) - Zero white borders, photo fills 100% of 640x480 frame
            target_ratio = 640.0 / 480.0
            orig_ratio = img.width / img.height
            if orig_ratio > target_ratio:
                new_width = int(img.height * target_ratio)
                offset = (img.width - new_width) // 2
                img = img.crop((offset, 0, offset + new_width, img.height))
            elif orig_ratio < target_ratio:
                new_height = int(img.width / target_ratio)
                offset = (img.height - new_height) // 2
                img = img.crop((0, offset, img.width, offset + new_height))

            img = img.resize((640, 480), Image.Resampling.LANCZOS)
            img.save(fpath, 'JPEG', quality=96, optimize=True, subsampling=0)
            return True, idx, f"Resized to 640x480 (Cover): {fname}"

    except Exception as e:
        return False, idx, str(e)

def main():
    excel_path = sys.argv[1] if len(sys.argv) > 1 else '/Users/usefelbedwehy/Downloads/08ceb108f030e69fc94f0bc7729890d3ed4de9769faf6a79bd2dc2eea91cf41e.xlsx'
    out_dir = '/Users/usefelbedwehy/Downloads/menu_images_640x480'
    os.makedirs(out_dir, exist_ok=True)

    print(f"Reading menu: {excel_path}")
    wb = openpyxl.load_workbook(excel_path)
    ws = wb.active

    # Find headers
    headers = [str(ws.cell(1, c).value or '').strip() for c in range(1, ws.max_column + 1)]
    print(f"Columns: {headers}")

    col_name = 1
    col_cat = 3
    col_url = 7

    for c, h in enumerate(headers, 1):
        if 'اسم' in h and ('منتج' in h or 'صنف' in h):
            if 'عربي' in h or col_name == 1:
                col_name = c
        elif 'قسم' in h or 'فئة' in h or 'تصنيف' in h:
            col_cat = c
        elif 'رابط' in h or 'صورة' in h or 'صوره' in h:
            col_url = c

    items = []
    for r in range(2, ws.max_row + 1):
        name = str(ws.cell(r, col_name).value or f'صنف_{r-1}').strip()
        cat = str(ws.cell(r, col_cat).value or 'عام').strip()
        url = str(ws.cell(r, col_url).value or '').strip()
        if url.startswith('http'):
            items.append((r - 1, cat, name, url, out_dir))

    print(f"Found {len(items)} items with image links. Processing in exact menu order...")

    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(process_item_image, items))

    success = sum(1 for s, _, _ in results if s)
    print(f"Successfully processed {success}/{len(items)} images into {out_dir}")

    # Create ZIP archive
    zip_path = '/Users/usefelbedwehy/Downloads/menu_images_640x480.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(out_dir)):
            if f.endswith('.jpg'):
                z.write(os.path.join(out_dir, f), arcname=f)

    print(f"ZIP archive saved to: {zip_path}")

    # Sync to Google Drive per User Rule 4
    gdrive_dir = '/Users/usefelbedwehy/Library/CloudStorage/GoogleDrive-youssryeldmasy59@gmail.com/My Drive/agent_outputs'
    if os.path.exists(gdrive_dir):
        shutil.copy2(zip_path, os.path.join(gdrive_dir, 'menu_images_640x480.zip'))
        print(f"Synced ZIP to Google Drive: {gdrive_dir}")

if __name__ == '__main__':
    main()
