#!/usr/bin/env python3
"""
Upgrades vendor_support_app/index.html with:
1. Bug fix for <script src="...pdf.js"> containing inline code
2. Advanced Email Sanitizer (cleanVendorEmail)
3. Dynamic Entity Extractor (extractEmailEntities)
4. Upgraded Precision Matcher (scoreInboundIntent with stop-words & word boundary matching)
5. Gemini 2.0 Flash integration with unified key & auto-fallback
6. Confidence Score Badge & Top 3 Alternatives UI
7. Entity injection into Arabic & English Macros
"""

import re
import sys

INDEX_PATH = "/Users/usefelbedwehy/Downloads/vendor_support_app/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

print(f"Original content length: {len(content)} bytes")

# 1. FIX PDF.JS SCRIPT TAG BUG
old_pdf_tag = '''    <!-- PDF.js CDN for client-side PDF parsing -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js">
        function downloadStandaloneFile() {'''

new_pdf_tag = '''    <!-- PDF.js CDN for client-side PDF parsing -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
    <script>
        function downloadStandaloneFile() {'''

if old_pdf_tag in content:
    content = content.replace(old_pdf_tag, new_pdf_tag, 1)
    print("Fixed PDF.js script tag bug.")
else:
    print("PDF.js script tag bug pattern not found or already fixed.")

# 2. EMAIL SANITIZER & ENTITY EXTRACTOR
old_clean_input = '''        function cleanInputText(text) {
            return text
                .replace(/احصل على Outlook.*/gi, '')
                .replace(/Get Outlook for.*/gi, '')
                .replace(/Sent from my.*/gi, '')
                .replace(/https?:\/\/\S+/gi, '')
                .trim();
        }'''

new_clean_input_and_entities = '''        // ── ADVANCED EMAIL SANITIZER & ENTITY EXTRACTOR ─────────────────────
        let currentDetectedEntities = {};

        function cleanVendorEmail(text) {
            if (!text) return '';
            let cleaned = text;

            // 1. Remove email chain headers & quoted messages
            cleaned = cleaned.replace(/(?:From|De|Von|من|الموضوع|Subject|Date|التاريخ|To|إلى|Cc|نسخة)\\s*:[^\\n\\r]+/gi, ' ');
            cleaned = cleaned.replace(/-----Original Message-----[\\s\\S]*$/gi, ' ');
            cleaned = cleaned.replace(/---+\\s*(?:Forwarded message|الرسالة المعاد توجيهها)\\s*---+[\\s\\S]*$/gi, ' ');
            cleaned = cleaned.replace(/On\\s+[A-Za-z0-9,\\s:]+wrote\\s*:[\\s\\S]*$/gi, ' ');
            cleaned = cleaned.replace(/في\\s+[\\u0600-\\u06FF0-9,\\s:]+كتب(?:\\(ا\\))?\\s*:[\\s\\S]*$/gi, ' ');
            cleaned = cleaned.replace(/نود إفادتكم بأنه سيتم إرسال استبيان[\\s\\S]*/gis, ' ');
            cleaned = cleaned.replace(/We would like to inform you that an automated survey[\\s\\S]*/gis, ' ');

            // 2. Remove mobile app signatures & links
            cleaned = cleaned.replace(/احصل على Outlook.*/gi, ' ');
            cleaned = cleaned.replace(/Get Outlook for.*/gi, ' ');
            cleaned = cleaned.replace(/Sent from my (?:iPhone|iPad|Galaxy|device).*/gi, ' ');
            cleaned = cleaned.replace(/أُرسلت من (?:الـ iPhone|جهازي).*/gi, ' ');
            cleaned = cleaned.replace(/https?:\\/\\/\\S+/gi, ' ');

            // 3. Remove common closings
            cleaned = cleaned.replace(/(?:مع خالص التحيات|وتفضلوا بقبول فائق الاحترام|مع الشكر والتقدير|مع الشكر|تحياتي|Best regards|Kind regards|Sincerely|Thanks and regards)[\\s\\S]{0,120}$/gi, ' ');

            // 4. Remove contact/call center boilerplates
            cleaned = cleaned.replace(/Delivery Hero Care.+/gi, ' ');
            cleaned = cleaned.replace(/مشاكل الطلبات\\s*:\\s*920033935/gi, ' ');
            cleaned = cleaned.replace(/Order Issues\\s*:\\s*920033935/gi, ' ');

            return cleaned.replace(/\\s+/g, ' ').trim();
        }

        function extractEmailEntities(rawText) {
            if (!rawText) return {};
            const entities = {};

            // 1. Order ID (e.g. #1234567, طلب رقم 123456, Order 12345)
            const orderMatch = rawText.match(/(?:طلب(?:كم)?|الطلب|أوردر|اوردر|Order|order)\\s*(?:رقم|no\\.?|#)?\\s*[:#-]?\\s*(\\d{5,12})/i) ||
                               rawText.match(/#(\\d{6,12})\\b/) ||
                               rawText.match(/\\b(1\\d{7,9}|2\\d{7,9}|3\\d{7,9}|4\\d{7,9}|5\\d{7,9})\\b/);
            if (orderMatch) entities.orderId = orderMatch[1];

            // 2. Store Name or Branch Name
            const storeMatch = rawText.match(/(?:فرع|متجر|مطعم|Store|Branch|Restaurant)\\s*(?:[:#-]|اسم)?\\s*([\\u0600-\\u06FFA-Za-z0-9\\s]{2,30}?)(?=[\\n\\r,،\\.]|رقم|ID|هاتف|$)/i);
            if (storeMatch && storeMatch[1].trim().length > 2) {
                const sName = storeMatch[1].trim();
                if (!['رقم', 'جديد', 'الخاص', 'المعتمد', 'ID'].includes(sName)) {
                    entities.storeName = sName;
                }
            }

            // 3. Store / Branch ID
            const storeIdMatch = rawText.match(/(?:كود|معرف|رقم)\\s*(?:الفرع|المتجر|المطعم|Store|Branch)\\s*[:#-]?\\s*(\\d{3,8})/i) ||
                                  rawText.match(/\\b(?:Branch|Store)\\s*#?\\s*(\\d{3,8})\\b/i);
            if (storeIdMatch) entities.storeId = storeIdMatch[1];

            // 4. Ticket / Case ID
            const ticketMatch = rawText.match(/(?:تذكرة|تذكره|Ticket|Case)\\s*(?:رقم|no\\.?|#)?\\s*[:#-]?\\s*(\\d{5,10})/i);
            if (ticketMatch) entities.ticketId = ticketMatch[1];

            // 5. Phone / Mobile
            const phoneMatch = rawText.match(/\\b(05\\d{8}|9665\\d{8}|\\+9665\\d{8})\\b/);
            if (phoneMatch) entities.phone = phoneMatch[1];

            // 6. SAR Amount
            const amountMatch = rawText.match(/(\\d+(?:\\.\\d{1,2})?)\\s*(?:ريال|SAR|ر\\.س|SR)/i);
            if (amountMatch) entities.amount = amountMatch[1];

            return entities;
        }

        function cleanInputText(text) {
            return cleanVendorEmail(text);
        }'''

if old_clean_input in content:
    content = content.replace(old_clean_input, new_clean_input_and_entities, 1)
    print("Replaced cleanInputText with cleanVendorEmail and extractEmailEntities.")
else:
    print("cleanInputText pattern not found.")

# 3. UPGRADE scoreInboundIntent
old_score_intent = '''        function scoreInboundIntent(query, item) {
            if (!query || !item || !item.keys) return 0;
            const qNorm = normalizeArabic(query.toLowerCase().trim());
            const qWords = qNorm.split(/\\s+/).filter(w => w.length > 1);
            let maxScore = 0;

            for (const rawKey of item.keys) {
                const kNorm = normalizeArabic(rawKey.toLowerCase().trim());
                const kWords = kNorm.split(/\\s+/).filter(w => w.length > 1);
                
                // 1. Exact phrase match
                if (qNorm.includes(kNorm)) {
                    maxScore = Math.max(maxScore, 100 + (kWords.length * 20));
                } else if (kNorm.includes(qNorm) && qNorm.length > 4) {
                    maxScore = Math.max(maxScore, 80 + (qWords.length * 15));
                } else {
                    // 2. Word token match
                    let matchedWords = 0;
                    for (const kw of kWords) {
                        if (qWords.some(qw => qw.includes(kw) || kw.includes(qw))) {
                            matchedWords++;
                        }
                    }
                    if (matchedWords > 0) {
                        const ratio = matchedWords / kWords.length;
                        if (ratio >= 0.5 || matchedWords >= 2) {
                            const score = Math.round(ratio * 60) + (matchedWords * 10);
                            maxScore = Math.max(maxScore, score);
                        }
                    }
                }
            }
            return maxScore;
        }'''

new_score_intent = '''        const _arStopWords = new Set(['في', 'من', 'على', 'عن', 'مع', 'هذا', 'هذه', 'تم', 'كان', 'جديد', 'جديدة', 'التي', 'الذي', 'ان', 'أن', 'او', 'أو', 'لي', 'لنا', 'هو', 'هي', 'ما', 'لا', 'لو', 'كل', 'بعد', 'قبل', 'حتى', 'يا', 'نحن', 'انا', 'قد', 'ثم', 'كم', 'اريد', 'بدي', 'عايز', 'نرجو', 'يرجى', 'الرجاء', 'هل', 'كيف']);
        const _enStopWords = new Set(['the', 'and', 'for', 'with', 'from', 'this', 'that', 'have', 'has', 'our', 'your', 'are', 'was', 'were', 'not', 'can', 'will', 'please', 'hello', 'dear']);

        function stripWordPrefixes(w) {
            return w.replace(/^(?:ال|لل|بال|فال|كال|وال|و|ب|ل)/, '');
        }

        function scoreInboundIntent(query, item) {
            if (!query || !item || !item.keys) return 0;
            const qNorm = normalizeArabic(query.toLowerCase().trim());
            const qWords = qNorm.split(/\\s+/).filter(w => w.length > 1 && !_arStopWords.has(w) && !_enStopWords.has(w));
            let maxScore = 0;

            for (const rawKey of item.keys) {
                const kNorm = normalizeArabic(rawKey.toLowerCase().trim());
                const kWords = kNorm.split(/\\s+/).filter(w => w.length > 1 && !_arStopWords.has(w) && !_enStopWords.has(w));
                
                // 1. Exact phrase match
                if (kNorm.length >= 5 && qNorm.includes(kNorm)) {
                    maxScore = Math.max(maxScore, 120 + (kWords.length * 25));
                    continue;
                } else if (qNorm.length >= 6 && kNorm.includes(qNorm)) {
                    maxScore = Math.max(maxScore, 90 + (qWords.length * 15));
                    continue;
                }

                // 2. High-Precision Token Match (No loose substring false positives)
                let matchedWords = 0;
                for (const kw of kWords) {
                    const kwBase = stripWordPrefixes(kw);
                    for (const qw of qWords) {
                        const qwBase = stripWordPrefixes(qw);
                        if (qw === kw || (kwBase.length >= 3 && qwBase === kwBase)) {
                            matchedWords++;
                            break;
                        } else if (kwBase.length >= 4 && qwBase.length >= 4) {
                            if (qwBase.startsWith(kwBase) || kwBase.startsWith(qwBase)) {
                                matchedWords += 0.85;
                                break;
                            }
                        }
                    }
                }

                if (matchedWords >= 1 && kWords.length > 0) {
                    const ratio = matchedWords / kWords.length;
                    if (ratio >= 0.4 || matchedWords >= 2) {
                        const score = Math.round(ratio * 70) + Math.round(matchedWords * 15);
                        maxScore = Math.max(maxScore, score);
                    }
                }
            }
            return maxScore;
        }'''

if old_score_intent in content:
    content = content.replace(old_score_intent, new_score_intent, 1)
    print("Upgraded scoreInboundIntent with stop-words and token-based matching.")
else:
    print("scoreInboundIntent pattern not found.")

# 4. UPGRADE callGeminiFreeAi
old_call_gemini = '''        async function callGeminiFreeAi(userQuery, matchedCase, greetings) {
            const apiKey = localStorage.getItem('gemini_api_key');
            if (!apiKey) return null;

            const arAgentName = getAgentArabicName();
            const systemPrompt = `أنت مساعد ذكي متخصص لدعم شركاء هنقرستيشن (Hungerstation Vendor Support AI).
وظيفتك: قراءة استفسار الشريك والتأكد من إرسال إيميل رسمي، مهندم، وراقي جداً باللغة العربية.

قواعد صارمة:
1. اتبع نص الإجراء الرسمي المعتمد من KnowledgeOwl للحالة التالية:
   عنوان الحالة: ${matchedCase.case_title}
   الـ CCR: ${matchedCase.ccr}
   الإجراء المعتمد: ${matchedCase.procedure_arabic}
2. ابدأ الإيميل بالتحية المناسبة:
   ${greetings.arGreeting ? greetings.arGreeting : 'شريكنا العزيز\\n\\nشكراً لتواصلكم مع هنقرستيشن.\\n\\n'}
3. لا تكتب أي ملاحظات داخلية أو تعليمات SOP للموظف. اكتب نص الرسالة الموجهة للشريك فقط.
4. انهِ الإيميل بالتوقيع التالي:
   مع الشكر،\\n${arAgentName}\\nهنقرستيشن\\nتفاصيل التواصل:\\nمشاكل الطلبات: 920033935`;

            const payload = {
                contents: [{ parts: [{ text: userQuery }] }],
                systemInstruction: { parts: [{ text: systemPrompt }] }
            };

            try {
                const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const resData = await response.json();
                if (resData.candidates && resData.candidates[0] && resData.candidates[0].content) {
                    return resData.candidates[0].content.parts[0].text;
                }
            } catch(e) {
                console.error("Gemini API Error:", e);
            }
            return null;
        }'''

new_call_gemini = '''        async function callGeminiFreeAi(userQuery, matchedCase, greetings, entities = {}) {
            const apiKey = localStorage.getItem('gemini_api_key') || GEMINI_KEY;
            if (!apiKey) return null;

            const arAgentName = getAgentArabicName();
            let entityContext = '';
            if (entities.orderId) entityContext += `\\nرقم الطلب المستخرج: ${entities.orderId}`;
            if (entities.storeName) entityContext += `\\nاسم المتجر: ${entities.storeName}`;
            if (entities.amount) entityContext += `\\nالمبلغ المستخرج: ${entities.amount} ريال`;

            const systemPrompt = `أنت مساعد ذكي فائق الاحترافية لدعم شركاء هنقرستيشن (Hungerstation Vendor Support AI).
وظيفتك: صياغة إيميل رسمي، مهذب، ودقيق 100% باللغة العربية موجه لشريك هنقرستيشن للإجابة على استفساره.

بيانات الحالة المعتمدة:
- عنوان الحالة: ${matchedCase.case_title}
- الـ CCR التصنيفي: ${matchedCase.ccr}
- الإجراء المعتمد الرسمي: ${matchedCase.procedure_arabic}
${entityContext}

قواعد ملزمة:
1. ابدأ الإيميل بالتحية:
   ${greetings.arGreeting ? greetings.arGreeting : 'شريكنا العزيز\\n\\nشكراً لتواصلكم مع هنقرستيشن.\\n\\n'}
2. ضمن البيانات المستخرجة (مثل رقم الطلب إن وجد) في سياق الرد بسلاسة وبدون أي أقواس فارغة.
3. لا تكتب أي تعليمات داخلية (SOP) للموظف. اكتب نص الرسالة الموجهة للشريك فقط.
4. أضف فقرة الاستبيان والتوقيع الرسمي التالي في النهاية:
نود إفادتكم بأنه سيتم إرسال استبيان تلقائي خاص بهذه التذكرة.
تشير نجمة واحدة إلى أن مستوى الخدمة لم يكن مرضياً، بينما تشير خمس نجوم إلى أن مستوى الخدمة كان مرضياً جداً.
شكراً لتواصلكم معنا.
نتمنى لكم الصحة والعافية.
مع الشكر،
${arAgentName}
هنقرستيشن
تفاصيل التواصل:
مشاكل الطلبات: 920033935`;

            const payload = {
                contents: [{ parts: [{ text: userQuery }] }],
                systemInstruction: { parts: [{ text: systemPrompt }] },
                generationConfig: { temperature: 0.1, maxOutputTokens: 600 }
            };

            try {
                const fetchPromise = fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const timeoutPromise = new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 4500));
                const response = await Promise.race([fetchPromise, timeoutPromise]);
                const resData = await response.json();
                if (resData.candidates && resData.candidates[0] && resData.candidates[0].content) {
                    return resData.candidates[0].content.parts[0].text.trim();
                }
            } catch(e) {
                console.warn("Gemini API skipped or timeout, fallback to template:", e.message);
            }
            return null;
        }'''

if old_call_gemini in content:
    content = content.replace(old_call_gemini, new_call_gemini, 1)
    print("Upgraded callGeminiFreeAi to Gemini 2.0 Flash with entity context and resilient timeout.")
else:
    print("callGeminiFreeAi pattern not found.")

# 5. UPGRADE displayCaseDualMacro SIGNATURE AND LOGIC
old_display_case = '''        async function displayCaseDualMacro(c, greetings, isEn, aiOverrideText = null) {
            if (!c) {
                c = (typeof allCases !== 'undefined' && allCases.length > 0 ? (allCases.find(x => x.id == 58 || x.id == 25) || allCases[0]) : null) || {
                    id: 58,
                    case_title: 'Compensation | تعويض',
                    ccr: 'Billing Inquiries -> Invoice inquiries | الاستعلام عن الفاتوره -> Compensation | تعويض',
                    procedure_arabic: 'يمكنك تقديم طلب تعويض عبر بوابة الشركاء من خلال: مساعدة (Help) ← استفسار جديد ← استفسارات تتعلق بالفواتير والمدفوعات ← اعتراض على طلب (Order Dispute).',
                    procedure_english: 'You can submit a compensation request through the Partner Portal by following these steps: Help -> New Inquiry -> Payments / Billing -> Order Dispute.',
                    internal_sop: 'إجراء الدعم الداخلي (Internal SOP):\\nالتحقق من رقم الطلب والاعتراض عبر بوابة الشركاء.',
                    url: 'https://hungerstation.knowledgeowl.com/home/cases-procedures'
                };
            }
            _macroActive = true;
            const arProcText = c.procedure_arabic || "يمكنك تقديم طلب تعويض عبر بوابة الشركاء من خلال: مساعدة (Help) ← استفسار جديد ← استفسارات تتعلق بالفواتير والمدفوعات ← اعتراض على طلب (Order Dispute).";
            const enProcText = c.procedure_english || "We would like to inform you that your request has been received and is being followed up with the concerned department. We will update you shortly.";
            
                        let finalArMacro = buildArabicMacro(greetings.arGreeting, arProcText);
            let aiBadgeNotice = '';
            
            if (aiOverrideText) {
                finalArMacro = aiOverrideText;
                aiBadgeNotice = `<div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; color: #34D399; padding: 8px 12px; border-radius: 8px; font-size: 0.8rem; font-weight: 700; margin-bottom: 10px; display: flex; align-items: center; gap: 6px;"><i class="fa-solid fa-wand-magic-sparkles"></i> تم التوليد الفائق بذكاء الاصطناعي المجاني (Gemini 1.5 Flash)</div>`;
            } else if (localStorage.getItem('gemini_api_key')) {
                const currentQueryText = (document.getElementById('partnerMessage') ? document.getElementById('partnerMessage').value : '') || (document.getElementById('searchInput') ? document.getElementById('searchInput').value : '');
                const aiGen = await callGeminiFreeAi(currentQueryText, c, greetings);
                if (aiGen) {
                    finalArMacro = aiGen;
                    aiBadgeNotice = `<div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; color: #34D399; padding: 8px 12px; border-radius: 8px; font-size: 0.8rem; font-weight: 700; margin-bottom: 10px; display: flex; align-items: center; gap: 6px;"><i class="fa-solid fa-wand-magic-sparkles"></i> تم التوليد الفائق بذكاء الاصطناعي المجاني (Gemini 1.5 Flash)</div>`;
                }
            }
            const arMacro = finalArMacro;
    
            const enMacro = buildEnglishMacro(greetings.enGreeting, enProcText);
            const arAgentName = getAgentArabicName();
            const enAgentName = getAgentEnglishName();'''

new_display_case = '''        window.selectSuggestedCase = function(caseId) {
            const target = allCases.find(x => x.id == caseId);
            if (target) {
                const partnerMsgVal = (document.getElementById('partnerMessage') ? document.getElementById('partnerMessage').value : '').trim();
                const searchInputVal = (document.getElementById('searchInput') ? document.getElementById('searchInput').value : '').trim();
                const rawMsg = partnerMsgVal || searchInputVal;
                const greetings = detectGreetings(rawMsg);
                const isEn = isEnglishInput(rawMsg);
                displayCaseDualMacro(target, greetings, isEn, null, 100, [], currentDetectedEntities);
                showToast(`🚀 تم التحويل إلى: ${target.case_title}`);
            }
        };

        async function displayCaseDualMacro(c, greetings, isEn, aiOverrideText = null, confidenceScore = 95, alternativeCases = [], detectedEntities = {}) {
            if (!c) {
                c = (typeof allCases !== 'undefined' && allCases.length > 0 ? (allCases.find(x => x.id == 86 || x.id == 58) || allCases[0]) : null) || {
                    id: 86,
                    case_title: 'Unclear Inquiry | استفسار غير واضح',
                    ccr: 'General Inquiries -> Unclear partner request',
                    procedure_arabic: 'نرجو التكرم بتوضيح المشكلة أو تزويدنا برقم الطلب واسم الفرع لنتمكن من خدمتكم بالشكل المطلوب.',
                    procedure_english: 'Please provide more details regarding your inquiry along with the Order ID and Branch Name so we can assist you.',
                    internal_sop: 'طلب تفاصيل إضافية من الشريك.',
                    url: 'https://hungerstation.knowledgeowl.com'
                };
            }
            _macroActive = true;
            let arProcText = c.procedure_arabic || "تم استلام طلبكم وجاري متابعته مع الفريق المختص.";
            let enProcText = c.procedure_english || "We would like to inform you that your request has been received and is being followed up.";

            // Inject entities into procedure if placeholders exist
            if (detectedEntities.orderId) {
                arProcText = arProcText.replace(/\\[رقم الطلب\\]/g, detectedEntities.orderId);
                enProcText = enProcText.replace(/\\[Order ID\\]/g, detectedEntities.orderId);
            }
            if (detectedEntities.storeName) {
                arProcText = arProcText.replace(/\\[اسم المتجر\\]|\\[اسم الشريك\\]/g, detectedEntities.storeName);
                enProcText = enProcText.replace(/\\[Store Name\\]|\\[Partner Name\\]/g, detectedEntities.storeName);
            }
            if (detectedEntities.amount) {
                arProcText = arProcText.replace(/\\[المبلغ\\]/g, detectedEntities.amount + ' ريال');
                enProcText = enProcText.replace(/\\[Amount\\]/g, detectedEntities.amount + ' SAR');
            }
            
            let finalArMacro = buildArabicMacro(greetings.arGreeting, arProcText);
            let aiBadgeNotice = '';
            
            if (aiOverrideText) {
                finalArMacro = aiOverrideText;
                aiBadgeNotice = `<div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; color: #34D399; padding: 8px 12px; border-radius: 8px; font-size: 0.8rem; font-weight: 700; margin-bottom: 10px; display: flex; align-items: center; gap: 6px;"><i class="fa-solid fa-wand-magic-sparkles"></i> تم التوليد الفائق بالذكاء الاصطناعي (Gemini 2.0 Flash)</div>`;
            } else {
                const currentQueryText = (document.getElementById('partnerMessage') ? document.getElementById('partnerMessage').value : '') || (document.getElementById('searchInput') ? document.getElementById('searchInput').value : '');
                if (currentQueryText && currentQueryText.trim().length > 15) {
                    const aiGen = await callGeminiFreeAi(currentQueryText, c, greetings, detectedEntities);
                    if (aiGen) {
                        finalArMacro = aiGen;
                        aiBadgeNotice = `<div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; color: #34D399; padding: 8px 12px; border-radius: 8px; font-size: 0.8rem; font-weight: 700; margin-bottom: 10px; display: flex; align-items: center; gap: 6px;"><i class="fa-solid fa-wand-magic-sparkles"></i> تم التوليد الفائق بذكاء الاصطناعي المباشر (Gemini 2.0 Flash)</div>`;
                    }
                }
            }
            const arMacro = finalArMacro;
    
            const enMacro = buildEnglishMacro(greetings.enGreeting, enProcText);
            const arAgentName = getAgentArabicName();
            const enAgentName = getAgentEnglishName();'''

if old_display_case in content:
    content = content.replace(old_display_case, new_display_case, 1)
    print("Upgraded displayCaseDualMacro with confidence score, alternatives, and Gemini 2.0 auto-run.")
else:
    print("displayCaseDualMacro pattern not found.")

# 6. INJECT CONFIDENCE SCORE & ALTERNATIVES HTML INTO outputContent
old_output_header = '''            const output = document.getElementById('outputContent');
            output.innerHTML = `
                <div class="result-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 10px;">
                        <h3 style="font-size: 1.1rem; font-weight: 700; color: var(--primary);"><i class="fa-solid fa-file-contract"></i> ${c.case_title}</h3>
                    </div>

                    ${attachmentHtml}'''

new_output_header = '''            // Construct Confidence and Entity Badges
            let confColor = confidenceScore >= 80 ? '#10B981' : (confidenceScore >= 60 ? '#F59E0B' : '#EF4444');
            let confIcon = confidenceScore >= 80 ? 'fa-circle-check' : (confidenceScore >= 60 ? 'fa-circle-exclamation' : 'fa-triangle-exclamation');
            let confText = confidenceScore >= 80 ? 'دقة مطابقة عالية' : (confidenceScore >= 60 ? 'دقة متوسطة' : 'احتمالية غير مؤكدة');

            let entitiesBadgesHtml = '';
            if (Object.keys(detectedEntities).length > 0) {
                let pills = [];
                if (detectedEntities.orderId) pills.push(`<span style="background: rgba(59,130,246,0.2); border: 1px solid #3B82F6; color: #93C5FD; padding: 2px 8px; border-radius: 6px; font-size: 0.75rem;"><i class="fa-solid fa-receipt"></i> طلب: #${detectedEntities.orderId}</span>`);
                if (detectedEntities.storeName) pills.push(`<span style="background: rgba(16,185,129,0.2); border: 1px solid #10B981; color: #6EE7B7; padding: 2px 8px; border-radius: 6px; font-size: 0.75rem;"><i class="fa-solid fa-shop"></i> متجر: ${detectedEntities.storeName}</span>`);
                if (detectedEntities.amount) pills.push(`<span style="background: rgba(245,158,11,0.2); border: 1px solid #F59E0B; color: #FCD34D; padding: 2px 8px; border-radius: 6px; font-size: 0.75rem;"><i class="fa-solid fa-money-bill"></i> ${detectedEntities.amount} ريال</span>`);
                if (pills.length > 0) {
                    entitiesBadgesHtml = `<div style="display:flex; gap:6px; flex-wrap:wrap; margin-top:4px;">${pills.join('')}</div>`;
                }
            }

            let alternativesHtml = '';
            if (alternativeCases && alternativeCases.length > 0) {
                alternativesHtml = `
                    <div style="background: rgba(255, 196, 0, 0.08); border: 1px dashed rgba(255, 196, 0, 0.35); border-radius: 10px; padding: 10px 14px; margin-bottom: 12px;">
                        <div style="font-size: 0.8rem; font-weight: 700; color: var(--primary); margin-bottom: 6px; display:flex; align-items:center; gap:6px;">
                            <i class="fa-solid fa-lightbulb"></i> هل يقصد الشريك حالة أخرى؟ اختر الحالة المناسبة لتعديل الرد فوراً:
                        </div>
                        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                            ${alternativeCases.map(alt => `
                                <button type="button" onclick="selectSuggestedCase(${alt.id})" style="background: var(--bg-card); border: 1px solid rgba(255,255,255,0.15); color: #FFF; padding: 6px 12px; border-radius: 8px; font-size: 0.78rem; font-weight: 600; cursor: pointer; transition: all 0.2s; display:inline-flex; align-items:center; gap:6px;" onmouseover="this.style.borderColor='var(--primary)'; this.style.color='var(--primary)';" onmouseout="this.style.borderColor='rgba(255,255,255,0.15)'; this.style.color='#FFF';">
                                    <i class="fa-solid fa-arrow-turn-down-left"></i> #${alt.id} ${alt.case_title}
                                </button>
                            `).join('')}
                        </div>
                    </div>
                `;
            }

            const output = document.getElementById('outputContent');
            output.innerHTML = `
                <div class="result-card">
                    <!-- Confidence & Entity Bar -->
                    <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); padding: 8px 12px; border-radius: 8px; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
                        <div>
                            <span style="color: ${confColor}; font-weight: 700; font-size: 0.85rem; display: inline-flex; align-items: center; gap: 6px;">
                                <i class="fa-solid ${confIcon}"></i> ${confText} (${confidenceScore}%)
                            </span>
                            ${entitiesBadgesHtml}
                        </div>
                        <span style="font-size: 0.75rem; color: var(--text-muted); background: rgba(255,255,255,0.05); padding: 2px 8px; border-radius: 4px;">كود الحالة: #${c.id}</span>
                    </div>

                    ${alternativesHtml}

                    <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 10px;">
                        <h3 style="font-size: 1.1rem; font-weight: 700; color: var(--primary);"><i class="fa-solid fa-file-contract"></i> ${c.case_title}</h3>
                    </div>

                    ${attachmentHtml}'''

if old_output_header in content:
    content = content.replace(old_output_header, new_output_header, 1)
    print("Injected confidence badge & alternative suggestions into result-card header.")
else:
    print("old_output_header pattern not found.")

# 7. UPGRADE generateResponse() FLOW
old_gen_flow_start = '''            let partnerMsgVal = (document.getElementById('partnerMessage') ? document.getElementById('partnerMessage').value : '').trim();
            let searchInputVal = (document.getElementById('searchInput') ? document.getElementById('searchInput').value : '').trim();
            let rawMsg = partnerMsgVal || searchInputVal;
            let greetings = detectGreetings(rawMsg);
            let msg = cleanInputText(rawMsg).toLowerCase();
            let msgNorm = normalizeArabic(msg);
            let fileTextCombined = extractedFileTexts.map(f => f.name + " " + f.text).join(" ").toLowerCase();
            let fullSearchText = msgNorm + " " + normalizeArabic(fileTextCombined);
            currentActiveQuery = msg || extractedFileTexts.map(f=>f.name).join(' ');'''

new_gen_flow_start = '''            let partnerMsgVal = (document.getElementById('partnerMessage') ? document.getElementById('partnerMessage').value : '').trim();
            let searchInputVal = (document.getElementById('searchInput') ? document.getElementById('searchInput').value : '').trim();
            let rawMsg = partnerMsgVal || searchInputVal;
            let greetings = detectGreetings(rawMsg);
            
            // Extract Entities First from Raw Text (before sanitization)
            currentDetectedEntities = extractEmailEntities(rawMsg);
            
            // Clean and Sanitize Vendor Email
            let cleanMsg = cleanVendorEmail(rawMsg).toLowerCase();
            let msgNorm = normalizeArabic(cleanMsg);
            let fileTextCombined = extractedFileTexts.map(f => f.name + " " + f.text).join(" ").toLowerCase();
            let fullSearchText = msgNorm + " " + normalizeArabic(fileTextCombined);
            currentActiveQuery = cleanMsg || extractedFileTexts.map(f=>f.name).join(' ');'''

if old_gen_flow_start in content:
    content = content.replace(old_gen_flow_start, new_gen_flow_start, 1)
    print("Updated generateResponse() input reading and entity extraction.")
else:
    print("old_gen_flow_start pattern not found.")

# 8. UPGRADE INTENT MATCHING & ELIMINATE BLIND FALLBACK TO CASE 58
old_decision_block = '''            if (scoredMapResults.length > 0) {
                const topScore = scoredMapResults[0].score;
                // If top score is dominant, prioritize top 1 directly
                const highScoreMatches = scoredMapResults.filter(r => r.score >= Math.max(80, topScore - 15));
                const uniqueHighCases = [];
                const seenIds = new Set();
                for (const r of highScoreMatches) {
                    if (!seenIds.has(r.id)) {
                        seenIds.add(r.id);
                        uniqueHighCases.push(r.caseObj);
                    }
                }

                if (uniqueHighCases.length === 1) {
                    matchedIntentCase = uniqueHighCases[0];
                } else if (uniqueHighCases.length > 1 && topScore >= 120) {
                    // Check if genuinely different categories
                    const distinctCats = new Set(uniqueHighCases.map(c => c.category));
                    if (distinctCats.size > 1) {
                        detectedCases = uniqueHighCases.slice(0, 2);
                    } else {
                        matchedIntentCase = uniqueHighCases[0];
                    }
                } else {
                    matchedIntentCase = scoredMapResults[0].caseObj;
                }
            }

            if (detectedCases.length > 1) {
                // Multi-Intent Response Builder
                let combinedArProc = "نفيدكم بأنه تم استلام استفساراتكم المتعددة وجاري العمل عليها كالتالي:\\n\\n";
                let combinedEnProc = "Please be informed that we have received your multi-part inquiry and handled each request as follows:\\n\\n";
                let combinedTitles = detectedCases.map(c => c.case_title).join(" + ");
                let combinedCCRs = detectedCases.map(c => c.ccr).join(" | ");

                detectedCases.forEach((c, idx) => {
                    combinedArProc += `${idx + 1}. بخصوص (${c.case_title}):\\n${cleanArabicProcedure(c.procedure_arabic)}\\n\\n`;
                    combinedEnProc += `${idx + 1}. Regarding (${c.case_title}):\\n${cleanEnglishProcedure(c.procedure_english)}\\n\\n`;
                });

                const multiCase = {
                    id: "MULTI_" + Date.now(),
                    case_title: "✨ طلبات متعددة: " + combinedTitles,
                    ccr: "Multi-Intent Inquiry | " + combinedCCRs,
                    procedure_arabic: combinedArProc.trim(),
                    procedure_english: combinedEnProc.trim(),
                    internal_sop: "إجراء الدعم الداخلي (Multi-Intent SOP):\\nمتابعة وتنفيذ كافة الطلبات المحددة أعلاه عبر الشاشات المخصصة.",
                    url: "https://hungerstation.knowledgeowl.com/home/cases-procedures"
                };

                displayCaseDualMacro(multiCase, greetings, isEn);
                autoRecordInteraction(fullSearchText, multiCase.case_title, multiCase.procedure_arabic);
                return;
            } else if (detectedCases.length === 1) {
                matchedIntentCase = detectedCases[0];
            }
if (matchedIntentCase) {
                displayCaseDualMacro(matchedIntentCase, greetings, isEn);
                autoRecordInteraction(fullSearchText, matchedIntentCase.case_title, matchedIntentCase.procedure_arabic);
                return;
            }

            // ── Instant Smart Local Matching ──────────────────────────────
            let scoredCases = allCases.map(c => ({ c, score: smartScore(c, currentActiveQuery) }))
                .filter(x => x.score > 0)
                .sort((a, b) => b.score - a.score);

            if (scoredCases.length > 0 && scoredCases[0] && scoredCases[0].c) {
                // Instant match — zero delay (0.001s)
                displayCaseDualMacro(scoredCases[0].c, greetings, isEn);
                autoRecordInteraction(fullSearchText, scoredCases[0].c.case_title || '', '');
            } else {
                // Fallback directly to Knowledge Base top matching case
                let fallbackCase = (typeof allCases !== 'undefined' && allCases.length > 0 ? (allCases.find(c => c.id === 58) || allCases[0]) : null) || { id: 58, case_title: 'Compensation | تعويض', ccr: 'Billing Inquiries -> Compensation', procedure_arabic: 'يمكنك تقديم طلب تعويض عبر بوابة الشركاء.', procedure_english: 'Submit compensation via Partner Portal.', internal_sop: 'Internal SOP', url: 'https://hungerstation.knowledgeowl.com' };
                displayCaseDualMacro(fallbackCase, greetings, isEn);
                autoRecordInteraction(fullSearchText, fallbackCase.case_title || '', fallbackCase.procedure_arabic || '');
            }'''

new_decision_block = '''            let finalMatchedCase = null;
            let finalConfidence = 50;
            let finalAlternatives = [];

            if (scoredMapResults.length > 0) {
                const topScore = scoredMapResults[0].score;
                finalMatchedCase = scoredMapResults[0].caseObj;
                finalConfidence = Math.min(99, Math.round((topScore / 160) * 100));
                
                // Collect Top 3 alternatives
                const seenIds = new Set([finalMatchedCase.id]);
                for (const r of scoredMapResults.slice(1, 6)) {
                    if (!seenIds.has(r.id)) {
                        seenIds.add(r.id);
                        finalAlternatives.push(r.caseObj);
                        if (finalAlternatives.length >= 3) break;
                    }
                }
            } else {
                // Local Smart Scoring
                let scoredCases = allCases.map(c => ({ c, score: smartScore(c, currentActiveQuery) }))
                    .filter(x => x.score > 0)
                    .sort((a, b) => b.score - a.score);

                if (scoredCases.length > 0) {
                    finalMatchedCase = scoredCases[0].c;
                    finalConfidence = Math.min(92, Math.round((scoredCases[0].score / 120) * 100));
                    finalAlternatives = scoredCases.slice(1, 4).map(x => x.c);
                }
            }

            // If confidence is low or query is ambiguous, consult Gemini 2.0 Flash classifier
            if ((!finalMatchedCase || finalConfidence < 65) && cleanMsg.length > 10) {
                try {
                    const topTenForAi = allCases.slice(0, 15);
                    const geminiMatchedIndices = await classifyWithGemini(cleanMsg, topTenForAi);
                    if (geminiMatchedIndices && geminiMatchedIndices[0] >= 0 && topTenForAi[geminiMatchedIndices[0]]) {
                        finalMatchedCase = topTenForAi[geminiMatchedIndices[0]];
                        finalConfidence = 90;
                    }
                } catch(e) {
                    console.warn("Gemini intent classifier error:", e);
                }
            }

            // Smart Non-Destructive Fallback: Case 86 (Unclear request) instead of blindly dumping Case 58!
            if (!finalMatchedCase) {
                finalMatchedCase = allCases.find(c => c.id === 86) || allCases[0] || {
                    id: 86,
                    case_title: 'طلب غير واضح | Unclear Request',
                    ccr: 'General Inquiries -> Unclear partner request',
                    procedure_arabic: 'نرجو منكم التكرم بتوضيح تفاصيل الاستفسار المطلوب ورقم الطلب أو الفرع لنتمكن من خدمتكم بأفضل شكل ممكن.',
                    procedure_english: 'Please provide us with more details regarding your request, along with the order ID or branch name, so we can assist you effectively.',
                    internal_sop: 'مراجعة بيانات التذكرة وطلب توضيح من الشريك.',
                    url: 'https://hungerstation.knowledgeowl.com'
                };
                finalConfidence = 40;
                finalAlternatives = allCases.slice(0, 3);
            }

            displayCaseDualMacro(finalMatchedCase, greetings, isEn, null, finalConfidence, finalAlternatives, currentDetectedEntities);
            autoRecordInteraction(fullSearchText, finalMatchedCase.case_title || '', finalMatchedCase.procedure_arabic || '');
            return;'''

if old_decision_block in content:
    content = content.replace(old_decision_block, new_decision_block, 1)
    print("Replaced decision block: zero blind fallback to Case 58, added confidence and top 3 alternatives.")
else:
    print("old_decision_block pattern not found.")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Updated index.html successfully! New length: {len(content)} bytes")
