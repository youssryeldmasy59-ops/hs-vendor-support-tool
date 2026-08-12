import json

with open('index.html', 'r', encoding='utf-8') as f:
    code = f.read()

with open('kb_data.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

kb_json_str = json.dumps(kb, ensure_ascii=False)

multi_matcher = '''            // DEDICATED MATCHER: Multi-Intent Combined Request (Layout Change + Add Items)
            const hasLayout = fullSearchText.includes('ترتيب') || fullSearchText.includes('تسلسل') || fullSearchText.includes('layout') || fullSearchText.includes('فئات المنيو') || fullSearchText.includes('ترتيب الفئات');
            const hasAdditions = fullSearchText.includes('إضافات') || fullSearchText.includes('اضافات') || fullSearchText.includes('إضافة أصناف') || fullSearchText.includes('اضافة اصناف') || fullSearchText.includes('أصناف جديدة') || fullSearchText.includes('add items');

            if (hasLayout && hasAdditions) {
                const arKbBody = `نفيدكم بأنه تم استلام طلبكم الخاص بتحديث إعدادات قائمة الطعام لفرعكم، وقد تم تنفيذ التحديثات المدمجة التالية:\\n1️⃣ تم اعتماد وتحديث ترتيب فئات المنيو حسب التسلسل المطلوب.\\n2️⃣ تم إضافة واعتماد الأصناف والإضافات الجديدة المرفقة على التطبيق.`;
                const enKbBody = `Please be informed that your request regarding updating your menu settings has been received and processed as follows:\\n1️⃣ Menu categories have been reordered according to the requested sequence.\\n2️⃣ New items and additions have been added and approved on the app.`;

                const fullArMacro = buildArabicMacro(greetings.arGreeting, arKbBody);
                const fullEnMacro = buildEnglishMacro(greetings.enGreeting, enKbBody);

                displayDualMacro({
                    title: "Multi-Request Menu Update | طلبات متعددة: ترتيب الفئات وإضافة الأصناف والإضافات",
                    ccr: "الرئيسي: Content Update ➔ Menu update ➔ Menu Layout Change | الفرعي: Content Update ➔ Menu update ➔ Add items",
                    arMacro: fullArMacro,
                    enMacro: fullEnMacro,
                    sop: "إجراء الدعم الداخلي للطلبات المدمجة (Multi-Intent SOP):\\n1. فتح بوابة الشركاء والتحقق من الترتيب المطلوب للفئات وتحديث الـ Layout.\\n2. فتح قائمة الأصناف وإضافة المنتجات والإضافات الجديدة والأسعار المرفقة ورابط الصور.\\n3. تحديد الـ Primary CCR (Menu Layout Change) والـ Secondary CCR (Add items) في تذكرة الدعم.",
                    url: "https://hungerstation.knowledgeowl.com/home/menu-layout-change"
                }, isEn);
                autoRecordInteraction(fullSearchText, "طلبات متعددة: ترتيب الفئات وإضافة أصناف", fullArMacro);
                return;
            }'''

if "// DEDICATED MATCHER: Multi-Intent Combined Request" not in code:
    code = code.replace("// DEDICATED MATCHER 1:", multi_matcher + "\n\n            // DEDICATED MATCHER 1:")

# Also update embeddedKB in index.html
old_embedded = code.split('const embeddedKB = ')[1].split(';\n        async function loadKBData()')[0]
code = code.replace('const embeddedKB = ' + old_embedded + ';\n        async function loadKBData()', 'const embeddedKB = ' + kb_json_str + ';\n        async function loadKBData()')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(code)

print('Updated index.html successfully!')
