import re

file_path = '/Users/usefelbedwehy/Downloads/vendor_support_app/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Update renderCaseSidebarList HTML layout
old_sidebar_fn = r'function renderCaseSidebarList\(casesList\) \{[\s\S]*?container\.innerHTML = html;\s*\}'
new_sidebar_fn = '''function renderCaseSidebarList(casesList) {
            const container = document.getElementById('casesContainer');
            if (!container) return;
            const badge = document.getElementById('totalCasesBadge');
            if (badge) badge.innerText = `${casesList.length} حالة معتمدة بالكامل`;

            if (!casesList || casesList.length === 0) {
                container.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--text-muted);">لا توجد نتائج مطابقة لبحثك</div>';
                return;
            }

            let html = '';
            casesList.forEach(c => {
                const usage = typeof caseUsageData !== 'undefined' ? caseUsageData[String(c.id)] : null;
                const usageCount = usage ? usage.count : 0;
                const starBadge = usageCount >= 5 ? '🔥' : usageCount >= 2 ? '⭐' : '';
                html += `
                    <div class="case-item" onclick="selectCase(${c.id})" style="display: flex; flex-direction: column; align-items: flex-start; gap: 4px; border: 1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.03); padding: 12px 14px; border-radius: 8px; cursor: pointer; transition: all 0.2s; width: 100%;">
                        <h4 style="font-size: 0.9rem; font-weight: 700; color: #FFF; margin: 0; text-align: right; line-height: 1.4;">#${c.id} - ${starBadge ? starBadge + ' ' : ''}${c.case_title}</h4>
                        <span style="font-size: 0.75rem; color: #F59E0B; font-weight: 600; text-align: right; word-break: break-word; line-height: 1.3;"><i class="fa-solid fa-sitemap"></i> ${c.ccr || 'Inbound KB Case'}</span>
                    </div>
                `;
            });
            container.innerHTML = html;
        }'''
html = re.sub(old_sidebar_fn, new_sidebar_fn, html)

# Update renderCasesList HTML layout
old_list_fn = r'function renderCasesList\(cases, query\) \{[\s\S]*?output\.innerHTML = html;\s*\}'
new_list_fn = '''function renderCasesList(cases, query) {
            renderCaseSidebarList(cases);
        }'''
html = re.sub(old_list_fn, new_list_fn, html)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("CASE_ITEM_LAYOUT_FIXED")
