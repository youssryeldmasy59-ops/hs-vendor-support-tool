import re, json

file_path = '/Users/usefelbedwehy/Downloads/vendor_support_app/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove remote surge.sh fetch in loadKBData
load_kb_old = r'async function loadKBData\(\) \{[\s\S]*?\}'
load_kb_new = '''async function loadKBData() {
            try {
                allCases = typeof embeddedKB !== 'undefined' ? embeddedKB : [];
                if (typeof renderCaseSidebarList === 'function') {
                    renderCaseSidebarList(allCases);
                }
                searchCases();
                renderSmartSuggestions();
            } catch(e) {
                console.error("Error loading KB:", e);
            }
        }'''

html = re.sub(load_kb_old, load_kb_new, html)

# 2. Fix selectCase loose equality
select_case_old = r'function selectCase\(id\) \{[\s\S]*?\}'
select_case_new = '''function selectCase(id) {
            const c = allCases.find(item => item && item.id == id);
            if (!c) return;
            if (typeof trackCaseUsage === 'function') trackCaseUsage(id);
            displayCaseDualMacro(c, { arGreeting: "", enGreeting: "" }, false);
        }'''

html = re.sub(select_case_old, select_case_new, html)

# 3. Ensure initDynamicKB uses embeddedKB cleanly
init_dyn_old = r'function initDynamicKB\(\) \{[\s\S]*?\}'
init_dyn_new = '''function initDynamicKB() {
            allCases = typeof embeddedKB !== 'undefined' ? embeddedKB : [];
            renderCaseSidebarList(allCases);
        }'''

html = re.sub(init_dyn_old, init_dyn_new, html)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("AUTHORITATIVE_KB_FIXED")
