import re, json

file_path = '/Users/usefelbedwehy/Downloads/vendor_support_app/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace static sidebar list with dynamic container
sidebar_start_pattern = r'<div id="outputContent">[\s\S]*?</div>\s*</div>\s*<!-- Main Content Column -->'
sidebar_replacement = '''<div id="outputContent" style="max-height: 650px; overflow-y: auto; padding-right: 4px;">
                <div style="background: rgba(255,196,0,0.1); border: 1px solid rgba(255,196,0,0.3); border-radius: 8px; padding: 10px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; color: var(--primary); font-size: 0.9rem;"><i class="fa-solid fa-book-bookmark"></i> Knowledge Base للإينبوند بالكامل:</span>
                    <span style="background: var(--primary); color: #000; font-weight: 800; font-size: 0.8rem; padding: 2px 8px; border-radius: 12px;" id="totalCasesBadge">97 حالة معتمدة</span>
                </div>
                <div id="casesContainer"></div>
            </div>
            </div>
            <!-- Main Content Column -->'''

html = re.sub(sidebar_start_pattern, sidebar_replacement, html)

# 2. Add dynamic rendering function for all 97 cases
dynamic_script = '''
        function renderCaseSidebarList(casesList) {
            const container = document.getElementById('casesContainer');
            if (!container) return;
            const badge = document.getElementById('totalCasesBadge');
            if (badge) badge.innerText = `${casesList.length} حالة معتمدة`;

            if (casesList.length === 0) {
                container.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--text-muted);">لا توجد نتائج مطابقة لبحثك</div>';
                return;
            }

            let html = '<div style="display: flex; flex-direction: column; gap: 8px;">';
            casesList.forEach(c => {
                html += `
                    <div class="case-item" onclick="selectCase(${c.id})" style="border: 1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.02); padding: 10px 12px; border-radius: 8px; cursor: pointer; transition: all 0.2s;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <h4 style="font-size: 0.9rem; font-weight: 700; color: #FFF; margin-bottom: 4px;">#${c.id} - ${c.case_title}</h4>
                        </div>
                        <span style="font-size: 0.75rem; color: #F59E0B; font-weight: 600;"><i class="fa-solid fa-sitemap"></i> ${c.ccr || 'Inbound KB Case'}</span>
                    </div>
                `;
            });
            html += '</div>';
            container.innerHTML = html;
        }

        function initDynamicKB() {
            allCases = typeof embeddedKB !== 'undefined' ? embeddedKB : [];
            renderCaseSidebarList(allCases);
        }

        window.addEventListener('DOMContentLoaded', initDynamicKB);
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            setTimeout(initDynamicKB, 100);
        }
'''

if 'function renderCaseSidebarList' not in html:
    html = html.replace('function selectCase(id) {', dynamic_script + '\n        function selectCase(id) {')

# Update selectCase to fetch from embeddedKB
select_case_old = r'function selectCase\(id\) \{[\s\S]*?\}'
select_case_new = '''function selectCase(id) {
            const c = allCases.find(x => x.id == id);
            if (!c) return;
            const greetings = { arGreeting: "", enGreeting: "" };
            let isEn = false;
            displayCaseDualMacro(c, greetings, isEn);
        }'''

html = re.sub(select_case_old, select_case_new, html)

# Update searchCases to filter all 97 cases live
search_cases_old = r'function searchCases\(query\) \{[\s\S]*?\}'
search_cases_new = '''function searchCases(query) {
            if (!query || !query.trim()) {
                renderCaseSidebarList(allCases);
                return;
            }
            const qNorm = normalizeArabic(query.toLowerCase().trim());
            const filtered = allCases.filter(c => {
                const titleNorm = normalizeArabic((c.case_title || '').toLowerCase());
                const ccrNorm = normalizeArabic((c.ccr || '').toLowerCase());
                const contentNorm = normalizeArabic((c.full_content || '').toLowerCase());
                return titleNorm.includes(qNorm) || ccrNorm.includes(qNorm) || contentNorm.includes(qNorm);
            });
            renderCaseSidebarList(filtered);
        }'''

html = re.sub(search_cases_old, search_cases_new, html)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("COMPLETE_KB_UI_SUCCESS")
