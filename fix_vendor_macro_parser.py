import re

INDEX_PATH = "/Users/usefelbedwehy/Downloads/vendor_support_app/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update normalizeArabic to handle common vendor typos like الخليفه -> الخلفيه
old_norm = """        function normalizeArabic(text) {
            if (!text) return '';
            return text
                .replace(/[أإآا]/g, 'ا')
                .replace(/ة/g, 'ه')
                .replace(/ى/g, 'ي')
                .replace(/[\u064B-\u065F]/g, '')
                .replace(/ؤ/g, 'و')
                .replace(/ئ/g, 'ي')
                .replace(/[\u0640]/g, '')"""

new_norm = """        function normalizeArabic(text) {
            if (!text) return '';
            let t = text
                .replace(/صورة\\s+الخليف[ةه]/gi, 'صورة الخلفية')
                .replace(/صوره\\s+الخليف[ةه]/gi, 'صورة الخلفية')
                .replace(/كفر\\s+(?:المتجر|المحل|المطعم)/gi, 'صورة الغلاف')
                .replace(/بانر\\s+(?:المتجر|المحل|المطعم)/gi, 'صورة الغلاف');
            return t
                .replace(/[أإآا]/g, 'ا')
                .replace(/ة/g, 'ه')
                .replace(/ى/g, 'ي')
                .replace(/[\\u064B-\\u065F]/g, '')
                .replace(/ؤ/g, 'و')
                .replace(/ئ/g, 'ي')
                .replace(/[\\u0640]/g, '')"""

if old_norm in html:
    html = html.replace(old_norm, new_norm, 1)
    print("Updated normalizeArabic with common vendor typos.")
else:
    print("old_norm not found!")

# 2. Fix cleanVendorEmail so it NEVER strips الموضوع or Subject!
old_clean = """            // 1. Remove email chain headers & quoted messages
            cleaned = cleaned.replace(/(?:From|De|Von|من|الموضوع|Subject|Date|التاريخ|To|إلى|Cc|نسخة)\\s*:[^\\n\\r]+/gi, ' ');"""

new_clean = """            // 1. Extract Vendor Form Subject/Topic FIRST (never delete it!)
            const vendorSubjectMatch = rawText.match(/(?:الموضوع|Subject|سبب التواصل|نوع الطلب|نوع المشكلة|الطلب|بخصوص)\\s*[:\\-]\\s*([^\\n\\r]+)/i);
            const vendorSubject = vendorSubjectMatch ? vendorSubjectMatch[1].trim() : '';

            // Strip routing headers, but KEEP Subject/الموضوع content
            cleaned = cleaned.replace(/(?:From|De|Von|Date|التاريخ|Cc|نسخة)\\s*:[^\\n\\r]+/gi, ' ');
            cleaned = cleaned.replace(/(?:To|إلى)\\s*:\\s*[^\\n\\r]+@\\S+/gi, ' ');
            cleaned = cleaned.replace(/(?:From|من)\\s*:\\s*[^\\n\\r]+@\\S+/gi, ' ');
            cleaned = cleaned.replace(/(?:الموضوع|Subject|سبب التواصل|نوع الطلب|نوع المشكلة)\\s*[:\\-]/gi, ' ');"""

# Let's find cleanVendorEmail in html
target_old = "cleaned = cleaned.replace(/(?:From|De|Von|من|الموضوع|Subject|Date|التاريخ|To|إلى|Cc|نسخة)\\s*:[^\\n\\r]+/gi, ' ');"
if target_old in html:
    html = html.replace(target_old, """// Strip routing headers, but KEEP Subject/الموضوع content
            cleaned = cleaned.replace(/(?:From|De|Von|Date|التاريخ|Cc|نسخة)\\s*:[^\\n\\r]+/gi, ' ');
            cleaned = cleaned.replace(/(?:To|إلى)\\s*:\\s*[^\\n\\r]+@\\S+/gi, ' ');
            cleaned = cleaned.replace(/(?:From|من)\\s*:\\s*[^\\n\\r]+@\\S+/gi, ' ');
            cleaned = cleaned.replace(/(?:الموضوع|Subject|سبب التواصل|نوع الطلب|نوع المشكلة)\\s*[:\\-]/gi, ' ');""")
    print("Fixed cleanVendorEmail: Subject & Topic are now fully preserved!")
else:
    print("target_old not found!")

# 3. In generateResponse, extract vendor subject and boost it
old_input_read = """            // Extract Entities First from Raw Text (before sanitization)
            currentDetectedEntities = extractEmailEntities(rawMsg);
            
            // Clean and Sanitize Vendor Email
            let cleanMsg = cleanVendorEmail(rawMsg).toLowerCase();
            let msgNorm = normalizeArabic(cleanMsg);
            let fileTextCombined = extractedFileTexts.map(f => f.name + " " + f.text).join(" ").toLowerCase();
            let fullSearchText = msgNorm + " " + normalizeArabic(fileTextCombined);
            currentActiveQuery = cleanMsg || extractedFileTexts.map(f=>f.name).join(' ');"""

new_input_read = """            // Extract Entities First from Raw Text (before sanitization)
            currentDetectedEntities = extractEmailEntities(rawMsg);
            
            // Extract vendor macro subject/topic if formatted
            const vendorSubjectMatch = rawMsg.match(/(?:الموضوع|Subject|سبب التواصل|نوع الطلب|نوع المشكلة|الطلب|بخصوص)\\s*[:\\-]\\s*([^\\n\\r]+)/i);
            const vendorSubject = vendorSubjectMatch ? vendorSubjectMatch[1].trim() : '';

            // Clean and Sanitize Vendor Email
            let cleanMsg = cleanVendorEmail(rawMsg).toLowerCase();
            
            // If vendor had a specific subject/topic in their macro, boost it at the front of the query!
            if (vendorSubject) {
                cleanMsg = vendorSubject + " " + cleanMsg;
            }
            let msgNorm = normalizeArabic(cleanMsg);
            let fileTextCombined = extractedFileTexts.map(f => f.name + " " + f.text).join(" ").toLowerCase();
            let fullSearchText = msgNorm + " " + normalizeArabic(fileTextCombined);
            currentActiveQuery = cleanMsg || extractedFileTexts.map(f=>f.name).join(' ');"""

if old_input_read in html:
    html = html.replace(old_input_read, new_input_read, 1)
    print("Enhanced generateResponse to prioritize vendor macro subject!")
else:
    print("old_input_read not found!")

# 4. Add keywords for Case 43 for "تغيير صورة الخلفية" and "تغيير صورة الخليفه"
old_case43_keys = "keys: ['تغيير صورة الغلاف للمطعم', 'تعديل الكفر فوتو Cover Photo', 'رفع صورة البانر العريض في التطبيق', 'تغيير صورة خلفية المتجر'"
new_case43_keys = "keys: ['تغيير صورة الخلفية', 'تغيير صورة الخلفيه', 'تغيير صورة الخليفه', 'تغيير صورة الغلاف', 'تعديل صورة الخلفية', 'صورة الخلفية بالصورة الاتية', 'صورة الخلفيه', 'صورة الغلاف للمطعم', 'تعديل الكفر فوتو Cover Photo', 'رفع صورة البانر العريض في التطبيق', 'تغيير صورة خلفية المتجر'"

if old_case43_keys in html:
    html = html.replace(old_case43_keys, new_case43_keys, 1)
    print("Enriched Case 43 with exact vendor macro phrases including background image!")
else:
    print("old_case43_keys not found!")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Finished updating index.html!")
