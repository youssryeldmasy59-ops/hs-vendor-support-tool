import json

with open('index.html', 'r', encoding='utf-8') as f:
    code = f.read()

download_btn_html = '''            <div class="agent-pill" onclick="downloadStandaloneFile()" style="background: rgba(59, 130, 246, 0.15); color: #60A5FA; border-color: rgba(59, 130, 246, 0.4);" title="تحميل الملف المستقل أوفلاين بنقرة واحدة">
                <i class="fa-solid fa-download"></i> <span>تنزيل الملف</span>
            </div>'''

download_js_fn = '''
        function downloadStandaloneFile() {
            const htmlContent = "<!DOCTYPE html>\\n" + document.documentElement.outerHTML;
            const blob = new Blob([htmlContent], { type: "text/html;charset=utf-8" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "Hungerstation_Vendor_Support_Tool.html";
            a.click();
            setTimeout(() => URL.revokeObjectURL(url), 5000);
            showToast("تم تنزيل النسخة المحدثة من التطبيق على جهازك بنجاح! 🚀");
        }
'''

if 'downloadStandaloneFile' not in code:
    # Add button to header controls
    code = code.replace(
        '<div class="header-controls">',
        '<div class="header-controls">\n' + download_btn_html
    )
    # Add JS function before </script>
    code = code.replace('</script>', download_js_fn + '\n    </script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(code)

print('Added 1-Click Download Button to index.html successfully!')
