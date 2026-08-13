import re

file_path = '/Users/usefelbedwehy/Downloads/vendor_support_app/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add null guard to updateLearnedCount
old_fn = r'function updateLearnedCount\(\) \{[\s\S]*?\}'
new_fn = '''function updateLearnedCount() {
            const badge = document.getElementById('learnedRulesCountBadge') || document.querySelector('.badge-learning');
            if (badge) badge.innerText = `ذاكرة التعلم (${learnedRules.length})`;
        }'''
html = re.sub(old_fn, new_fn, html)

# 2. Add try-catch inside autoRecordInteraction
old_auto = r'function autoRecordInteraction\(query, resultTitle, resultArMacro\) \{[\s\S]*?\}'
new_auto = '''function autoRecordInteraction(query, resultTitle, resultArMacro) {
            try {
                if (!query) return;
                const cleanQuery = query.toLowerCase().trim();
                const existingIndex = learnedRules.findIndex(r => r.keywords === cleanQuery);
                if (existingIndex >= 0) {
                    learnedRules[existingIndex].count = (learnedRules[existingIndex].count || 1) + 1;
                } else {
                    learnedRules.unshift({
                        keywords: cleanQuery,
                        correctedBody: resultArMacro,
                        title: resultTitle,
                        savedBy: typeof getAgentArabicName === 'function' ? getAgentArabicName() : 'أحمد',
                        date: new Date().toLocaleDateString('ar-EG'),
                        count: 1
                    });
                }
                if (learnedRules.length > 100) learnedRules.pop();
                localStorage.setItem('hs_learned_rules', JSON.stringify(learnedRules));
                updateLearnedCount();
            } catch(e) {
                console.warn('autoRecordInteraction skipped:', e);
            }
        }'''
html = re.sub(old_auto, new_auto, html)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("NULL_GUARDS_FIXED")
