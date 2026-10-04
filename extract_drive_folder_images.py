#!/usr/bin/env python3
"""
HungerStation Google Drive & Folder Image Extractor & Resizer (640x480)
- Extracts images from Google Drive ZIPs, directories, or Excel sheets.
- Preserves categories from subfolders (e.g., البرجر, الشاورما, الفطائر...).
- Resizes every image cleanly to 640x480 (centered letterbox, white background, high quality).
- Strictly names each image: NN_[Category]_[ItemName].jpg
- Bundles into a HungerStation-compliant ZIP file.
- Syncs automatically to Google Drive agent_outputs.
"""
import sys, os, re, io, zipfile, shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

try:
    from PIL import Image
except ImportError:
    print("Run with: uv run --with pillow python extract_drive_folder_images.py [input_path]")
    sys.exit(1)

GDRIVE_OUTPUT_DIR = '/Users/usefelbedwehy/Library/CloudStorage/GoogleDrive-youssryeldmasy59@gmail.com/My Drive/agent_outputs'

def clean_name(s):
    s = str(s or '').strip()
    s = re.sub(r'[\U00010000-\U0010ffff\u2600-\u27bf]', '', s)
    s = re.sub(r'[^\w\u0600-\u06FF-]', '_', s)
    return re.sub(r'_+', '_', s).strip('_')

def resize_image_bytes(img_bytes):
    """Resizes raw image bytes to 640x480 JPEG with centered aspect-fit."""
    img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
    if img.size == (640, 480):
        return img_bytes, False
    
    canvas = Image.new('RGB', (640, 480), (255, 255, 255))
    img.thumbnail((640, 480), Image.Resampling.LANCZOS)
    x = (640 - img.width) // 2
    y = (480 - img.height) // 2
    canvas.paste(img, (x, y))
    
    buf = io.BytesIO()
    canvas.save(buf, format='JPEG', quality=95, optimize=True)
    return buf.getvalue(), True

def process_zip_archive(zip_path, output_dir):
    """Processes a Google Drive ZIP archive preserving subfolder category names."""
    print(f"📦 Unpacking and processing ZIP: {zip_path}")
    image_entries = []
    
    with zipfile.ZipFile(zip_path, 'r') as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            name = info.filename
            if '__MACOSX' in name or '.DS_Store' in name:
                continue
            if not re.search(r'\.(jpe?g|png|webp|bmp)$', name, re.I):
                continue
            
            parts = [p for p in name.split('/') if p]
            fname = parts[-1]
            item_raw = os.path.splitext(fname)[0]
            
            # Detect category from parent directory
            cat = 'عام'
            if len(parts) >= 2:
                cat = parts[-2]
                if cat in ['الصور', 'Images', 'Photos'] and len(parts) >= 3:
                    cat = parts[-3]
            
            content = z.read(info)
            image_entries.append((cat, item_raw, content))
            
    return process_image_records(image_entries, output_dir)

def process_directory(dir_path, output_dir):
    """Processes an unzipped directory preserving subfolder category names."""
    print(f"📂 Scanning directory: {dir_path}")
    image_entries = []
    root_p = Path(dir_path)
    
    for p in root_p.rglob('*'):
        if p.is_dir() or '__MACOSX' in str(p) or p.name.startswith('.'):
            continue
        if not re.search(r'\.(jpe?g|png|webp|bmp)$', p.name, re.I):
            continue
        
        parts = p.relative_to(root_p).parts
        item_raw = p.stem
        cat = 'عام'
        if len(parts) >= 2:
            cat = parts[-2]
            if cat in ['الصور', 'Images', 'Photos'] and len(parts) >= 3:
                cat = parts[-3]
        
        with open(p, 'rb') as f:
            content = f.read()
        image_entries.append((cat, item_raw, content))
        
    return process_image_records(image_entries, output_dir)

def process_image_records(records, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    processed = []
    
    # Sort by category then item name for stable sequence
    records.sort(key=lambda x: (x[0], x[1]))
    
    for idx, (cat, item_name, raw_bytes) in enumerate(records, 1):
        try:
            res_bytes, resized = resize_image_bytes(raw_bytes)
            safe_cat = clean_name(cat) or 'عام'
            safe_item = clean_name(item_name) or f'صنف_{idx}'
            
            fname = f"{idx:02d}_[{safe_cat}]_{safe_item}.jpg"
            fpath = os.path.join(output_dir, fname)
            
            with open(fpath, 'wb') as f:
                f.write(res_bytes)
            
            # Also save in category subfolder
            cat_sub = os.path.join(output_dir, safe_cat)
            os.makedirs(cat_sub, exist_ok=True)
            with open(os.path.join(cat_sub, f"{idx:02d}_{safe_item}.jpg"), 'wb') as f:
                f.write(res_bytes)
                
            processed.append((idx, safe_cat, safe_item, fpath, resized))
            status = "Resized ➔ 640x480" if resized else "Original 640x480"
            print(f"  [{idx:02d}] [{safe_cat}] {safe_item} -> {status}")
        except Exception as e:
            print(f"  ❌ Error processing {item_name}: {e}")
            
    return processed

def package_and_sync(output_dir, base_name='Hungerstation_Images_640x480'):
    zip_path = os.path.join(os.path.dirname(output_dir), f"{base_name}.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(output_dir):
            for file in files:
                full = os.path.join(root, file)
                rel = os.path.relpath(full, output_dir)
                z.write(full, arcname=rel)
                
    print(f"✅ Created ZIP bundle: {zip_path}")
    if os.path.exists(GDRIVE_OUTPUT_DIR):
        dest = os.path.join(GDRIVE_OUTPUT_DIR, f"{base_name}.zip")
        shutil.copy2(zip_path, dest)
        print(f"☁️ Backed up to Google Drive: {dest}")
    return zip_path

def main():
    if len(sys.argv) < 2:
        print("Usage: uv run --with pillow python extract_drive_folder_images.py <path_to_zip_or_folder>")
        # Check if default Downloads/الصور exists
        default_dir = '/Users/usefelbedwehy/Downloads/الصور'
        if os.path.exists(default_dir):
            target = default_dir
        else:
            sys.exit(1)
    else:
        target = sys.argv[1]
        
    out_dir = '/Users/usefelbedwehy/Downloads/processed_menu_images_640x480'
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
        
    if os.path.isfile(target) and target.endswith('.zip'):
        processed = process_zip_archive(target, out_dir)
    elif os.path.isdir(target):
        processed = process_directory(target, out_dir)
    else:
        print(f"Invalid target: {target}")
        sys.exit(1)
        
    print(f"\n🎉 Successfully processed {len(processed)} images to 640x480!")
    zip_path = package_and_sync(out_dir)
    print(f"Done: {zip_path}")

if __name__ == '__main__':
    main()
