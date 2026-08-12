#!/bin/bash
# ===================================================
# Auto-Deploy to Surge.sh
# كل ما تحفظ index.html بيترفع أوتوماتيك
# ===================================================

TARGET_FILE="index.html"
SURGE_DOMAIN="hs-vendor-support-suite.surge.sh"
FOLDER="/Users/usefelbedwehy/Downloads/vendor_support_app"

echo "🚀 Auto-Deploy نشط — بيراقب: $TARGET_FILE"
echo "🌐 Domain: $SURGE_DOMAIN"
echo "📂 Folder: $FOLDER"
echo "⏹  عشان توقفه: Ctrl+C"
echo "-------------------------------------------"

# تثبيت surge لو مش موجود
if ! command -v surge &> /dev/null; then
    echo "📦 تثبيت surge..."
    npm install -g surge
fi

# أول deploy فوري
echo "⬆️  Deploying..."
surge "$FOLDER" "$SURGE_DOMAIN"
echo "✅ Done — $(date '+%H:%M:%S')"

# راقب التغييرات
LAST_MODIFIED=$(stat -f "%m" "$FOLDER/$TARGET_FILE")

while true; do
    sleep 2
    CURRENT_MODIFIED=$(stat -f "%m" "$FOLDER/$TARGET_FILE")
    
    if [ "$CURRENT_MODIFIED" != "$LAST_MODIFIED" ]; then
        LAST_MODIFIED=$CURRENT_MODIFIED
        echo ""
        echo "🔄 تغيير اتكشف — $(date '+%H:%M:%S')"
        echo "⬆️  Deploying..."
        surge "$FOLDER" "$SURGE_DOMAIN"
        echo "✅ Done — تم الرفع على $SURGE_DOMAIN"
        echo "-------------------------------------------"
    fi
done
