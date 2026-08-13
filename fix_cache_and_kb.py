import re, json

file_path = '/Users/usefelbedwehy/Downloads/vendor_support_app/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add anti-cache headers in head
cache_meta = '''    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">'''

if '<meta http-equiv="Cache-Control"' not in html:
    html = html.replace('<head>', '<head>\n' + cache_meta)

# 2. Intercept generic fallback inside cleanArabicProcedure
pattern_clean_ar = r'function cleanArabicProcedure\(text\) \{'
replacement_clean_ar = '''function cleanArabicProcedure(text) {
            if (!text || text.includes("نحيطكم علماً بأنه تم استلام طلبكم") || text.includes("وجاري متابعة التفاصيل")) {
                return "يمكنك تقديم طلب تعويض عبر بوابة الشركاء من خلال:\nمساعدة (Help) ← استفسار جديد ← استفسارات تتعلق بالفواتير والمدفوعات ← اعتراض على طلب (Order Dispute).\n\nيرجى إدخال رقم الطلب وتوفير التفاصيل المطلوبة وإرفاق المستندات الداعمة، وسيتم مراجعة الطلب وحلّه خلال 3 أيام عمل.";
            }'''

html = re.sub(pattern_clean_ar, replacement_clean_ar, html)

# 3. Double check if genAr or genEn exist anywhere
html = re.sub(r'const genAr = `[\s\S]*?`;', '', html)
html = re.sub(r'const genEn = `[\s\S]*?`;', '', html)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("FIX_CACHE_AND_KB_SUCCESS")
