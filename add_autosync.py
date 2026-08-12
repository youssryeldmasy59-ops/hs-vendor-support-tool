import json

with open('index.html', 'r', encoding='utf-8') as f:
    code = f.read()

old_fn_start = '''        async function loadKBData() {
            try {
                allCases = embeddedKB;
                searchCases();
            } catch(e) {
                console.error("Error loading KB:", e);
            }
        }'''

new_fn_start = '''        async function loadKBData() {
            try {
                allCases = embeddedKB;
                searchCases();
                
                // Silent Cloud Auto-Sync on Launch
                fetch('https://hs-vendor-support-suite.surge.sh/kb_data.json?t=' + Date.now())
                    .then(res => res.json())
                    .then(remoteKB => {
                        if (remoteKB && remoteKB.length > 0) {
                            allCases = remoteKB;
                            searchCases();
                            showSyncStatusBadge(remoteKB.length);
                        }
                    })
                    .catch(err => console.log('Offline mode active:', err));
            } catch(e) {
                console.error("Error loading KB:", e);
            }
        }

        function showSyncStatusBadge(count) {
            const badge = document.getElementById('syncBadge');
            if (badge) {
                badge.style.display = 'inline-flex';
                badge.innerHTML = `<i class="fa-solid fa-cloud-arrow-down"></i> متزامن أونلاين (${count} حالة)`;
            }
        }'''

if old_fn_start in code:
    code = code.replace(old_fn_start, new_fn_start)

if 'syncBadge' not in code:
    code = code.replace(
        '<div class="stat-badge" onclick="showHistoryModal()" style="cursor: pointer;">',
        '<div class="stat-badge" id="syncBadge" style="display:none; background: rgba(16, 185, 129, 0.15); color: #34D399; border-color: rgba(16, 185, 129, 0.3);"><i class="fa-solid fa-cloud-arrow-down"></i> متزامن أونلاين</div>\n            <div class="stat-badge" onclick="showHistoryModal()" style="cursor: pointer;">'
    )

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(code)

print('Auto-Sync added to index.html successfully!')
