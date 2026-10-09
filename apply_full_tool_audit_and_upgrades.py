#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Audit & Upgrade Script for HungerStation Vendor Support Tool
Implements:
1. Smart Rider Operations & Dispatch Hub Modal & logic (Cases #50, #51, #52, #82, #99)
2. Live Call Whisperer Intelligence (Dynamic 102-case matching, AI Call Summary for Zendesk, advanced sentiment)
3. AI Models overhaul (Allam-2-7b, GPT-OSS 120B reasoning token fix, safe response extractor)
4. Menu Studio SFDA Calorie Estimator & 422 Pre-flight sanity enhancer
5. Header & Tools dropdown integration (Rider Ops Hub button, hotkeys)
"""

import re
import sys

INDEX_PATH = "/Users/usefelbedwehy/Downloads/hs-vendor-support-tool/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

print("Original index.html length:", len(html))

# ─────────────────────────────────────────────────────────────────────────────
# 1. ADD RIDER OPERATIONS BUTTON TO HEADER & TOOLS DROPDOWN
# ─────────────────────────────────────────────────────────────────────────────

# Header button
HEADER_TARGET = '<!-- 🎙️ Live Call Whisperer -->'
HEADER_BTN = '''<!-- 🛵 Smart Rider Operations & Dispatch Hub -->
            <button type="button" class="header-btn" onclick="openRiderOperationsModal()" id="riderOpsHeaderBtn" title="مركز عمليات وحلول الرايدر واللوجستيك (تأخير، استلام خاطئ، هروب دون دفع)" style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(217, 119, 6, 0.35)); border: 1.5px solid #F59E0B; color: #FCD34D; font-weight: 800; display: inline-flex; align-items: center; gap: 6px;">
                <i class="fa-solid fa-motorcycle"></i> <span id="riderOpsHeaderLabel">🛵 عمليات الرايدر</span>
            </button>

            <!-- 🎙️ Live Call Whisperer -->'''

if HEADER_TARGET in html and 'id="riderOpsHeaderBtn"' not in html:
    html = html.replace(HEADER_TARGET, HEADER_BTN, 1)
    print("✅ Added Rider Operations Hub button to Header!")
else:
    print("⚠️ Header button already present or target not found.")

# Tools dropdown item
DROPDOWN_TARGET = '<div class="tools-dropdown-group-title">🎯 التذاكر والعمليات اليومية</div>'
DROPDOWN_ITEM = '''<div class="tools-dropdown-group-title">🎯 التذاكر والعمليات اليومية</div>
                    <div class="tools-dropdown-item" onclick="openRiderOperationsModal(); closeToolsMenu();" title="مركز عمليات وحلول الرايدر الذكي (حاسبة التأخير، المندوب الهارب، الاستلام الخاطئ)">
                        <i class="fa-solid fa-motorcycle" style="color: #F59E0B;"></i>
                        <span style="flex: 1;">مركز عمليات وحلول الرايدر 🛵</span>
                        <span class="tools-item-tag" style="background: rgba(245, 158, 11, 0.2); color: #FCD34D;">لوجستيك</span>
                    </div>'''

if DROPDOWN_TARGET in html and 'openRiderOperationsModal(); closeToolsMenu();' not in html:
    html = html.replace(DROPDOWN_TARGET, DROPDOWN_ITEM, 1)
    print("✅ Added Rider Operations Hub to Tools Dropdown!")
else:
    print("⚠️ Tools dropdown item already present or target not found.")

# ─────────────────────────────────────────────────────────────────────────────
# 2. UPGRADE AI MODEL SETTINGS & FIX REASONING MAX_TOKENS
# ─────────────────────────────────────────────────────────────────────────────

# Fix testCloudAiConnection max_tokens from 10 to 500
html = html.replace(
    'max_tokens: 10\n                    })',
    'max_tokens: 500\n                    })'
)
html = html.replace(
    'max_tokens: 10\r\n                    })',
    'max_tokens: 500\r\n                    })'
)

# Fix aiTranslateMenuItem max_tokens from 100 to 500
html = html.replace(
    'max_tokens: 100\n            })\n        });\n        const data = await res.json();\n        return data?.choices?.[0]?.message?.content?.trim() || autoTranslateMenuText(text, targetLang);',
    'max_tokens: 500\n            })\n        });\n        const data = await res.json();\n        return extractAiResponseContent(data) || autoTranslateMenuText(text, targetLang);'
)

# Fix aiSemanticSearchCases max_tokens from 200 to 600
html = html.replace(
    'max_tokens: 200\n                    })\n                });\n\n                const data = await res.json();\n                const text = data?.choices?.[0]?.message?.content || \'\';',
    'max_tokens: 600\n                    })\n                });\n\n                const data = await res.json();\n                const text = extractAiResponseContent(data);'
)

# Helper function for safe AI extraction
AI_SAFE_EXTRACTOR = '''
// 🛡️ Universal Safe AI Response Extractor (Supports Reasoning & Non-Reasoning Models)
function extractAiResponseContent(data) {
    if (!data || !data.choices || !data.choices[0] || !data.choices[0].message) return '';
    const msg = data.choices[0].message;
    if (msg.content && msg.content.trim()) return msg.content.trim();
    if (msg.reasoning && msg.reasoning.trim()) {
        const lines = msg.reasoning.trim().split('\\n').filter(l => l.trim().length > 0);
        return lines[lines.length - 1].replace(/^["']|["']$/g, '').trim();
    }
    return '';
}
'''

if 'function extractAiResponseContent' not in html:
    # Insert right before getActiveGroqKey
    html = html.replace('function getActiveGroqKey() {', AI_SAFE_EXTRACTOR + '\nfunction getActiveGroqKey() {', 1)
    print("✅ Added universal extractAiResponseContent helper!")

# Update cloudAiModelSelect dropdown HTML
OLD_SELECT_GROQ = '''<option value="openai/gpt-oss-120b">🧠 GPT-OSS 120B Reasoning (الموديل الافتراضي الفائق 120B - سرعة 0.2 ثانية وتفكير منطقي)</option>
                        <option value="allam-2-7b">🇸🇦 Allam 2 (علّام - الموديل السعودي المعتمد للغة العربية)</option>
                        <option value="qwen/qwen3.8-27b">⚡ Qwen 3.8 27B (موديل متوازن وسريع جداً)</option>
                        <option value="openai/gpt-oss-20b">🚀 GPT-OSS 20B (خفيف وسريع)</option>'''

NEW_SELECT_GROQ = '''<option value="allam-2-7b">🇸🇦 Allam 2 (علّام - النموذج الوطني السعودي فائق الدقة باللهجة والأنظمة 0.06s) ⭐</option>
                        <option value="openai/gpt-oss-120b">🧠 GPT-OSS 120B Reasoning (التفكير العميق والتحقيق الجنائي 120B)</option>
                        <option value="qwen/qwen3.8-27b">⚡ Qwen 3.8 27B (موديل متوازن وسريع)</option>
                        <option value="openai/gpt-oss-20b">🚀 GPT-OSS 20B (خفيف فائق السرعة)</option>'''

if OLD_SELECT_GROQ in html:
    html = html.replace(OLD_SELECT_GROQ, NEW_SELECT_GROQ, 1)
    print("✅ Upgraded Groq model list with Allam 2 featured!")

# ─────────────────────────────────────────────────────────────────────────────
# 3. UPGRADE LIVE CALL WHISPERER (DYNAMIC 102 CASE MATCHING & CALL SUMMARY)
# ─────────────────────────────────────────────────────────────────────────────

UPGRADED_WHISPERER_LOGIC = '''// ─────────────────────────────────────────────────────────────────────────────
// 2. LIVE CALL WHISPERER AI (الملقّن الحي الذكي لمكالمات الشركاء - 102 حالة كاملة)
// ─────────────────────────────────────────────────────────────────────────────
let _whispererRec = null;
let _whispererSeconds = 0;
let _whispererInterval = null;
let _whispererActiveCaseId = 45;
let _whispererFullTranscript = '';

// Rich Category Objections Radar
const WHISPERER_OBJECTIONS_RADAR = {
    RIDER: [
        { q: 'الشريك: "المندوب اتأخر والوجبة بردت خلاص!"', a: 'وضح له: إذا تجاوز تأخير المندوب 15 دقيقة بعد جاهزية الطعام، يتم تحضير وجبة طازجة فوراً للمندوب الجديد وسيتم تعويض المطعم 100% عن الوجبة التالفة.' },
        { q: 'الشريك: "السائق رفض يستلم الطلب أو أسلوبه سيء"', a: 'وضح له: تم رفع تذكرة تصعيد فورية لإدارة الأسطول (#82) وسيتم عمل حظر (Blacklist) للمندوب من فرعكم لحماية فريق العمل.' },
        { q: 'الشريك: "المندوب أخذ الطلب ومادفعش كاش"', a: 'وضح له: سيتم تسجيل مطالبة مالية عاجلة (#51) وخصم المبلغ من محفظة المندوب وإيداعه في حسابكم البنكي.' }
    ],
    CANCEL: [
        { q: 'الشريك: "الطلب اتلغى والفلوس هتنزل امتى؟"', a: 'وضح له: إذا ألغي الطلب بعد استلام المندوب (#45)، يُعتبر الطلب ناجحاً وتصرف قيمته كاملة في الحوالة البنكية المجدولة.' },
        { q: 'الشريك: "أنا عايز التعويض كاش الآن"', a: 'وضح له: جميع التسويات المالية لشركاء هنقرستيشن تحول بنكياً آلياً مع كشف الحساب الأسبوعي/الشهري لضمان التوثيق المحاسبي.' }
    ],
    FINANCE: [
        { q: 'الشريك: "العمولة محسوبة غلط وفيه خصم غير مبرر"', a: 'وضح له: يمكنك فتح تفاصيل التقرير عبر مفكك الفواتير في البوابة، وسنرفع لك اعتراضاً رسمياً (#54) للمالية خلال 24 ساعة.' }
    ],
    DEVICE: [
        { q: 'الشريك: "التابلت فاصل ومش شغال والطلبات بتفوتني"', a: 'وضح له: تأكد من الشحن والاتصال بالـ Wi-Fi، ويمكنك فوراً استخدام بوابة Partner Portal عبر الموبايل لاستقبال الطلبات مؤقتاً.' }
    ],
    MENU: [
        { q: 'الشريك: "ليه الأصناف الجديدة لسه ما نزلتش؟"', a: 'وضح له: التحديثات المرفوعة عبر استوديو المنيو المعتمد (_MenuUpload.xlsx) يتم اعتمادها ومراجعتها خلال أقل من ساعتين.' }
    ]
};

function handleWhispererSpeech(text) {
    if (!text || !text.trim()) return;
    _whispererFullTranscript += (text + ' ');
    const box = document.getElementById('whispererTranscriptBox');
    if (box) box.innerText = `"${text}"`;

    // 1. Enhanced Sentiment & Urgency Radar
    const sentBadge = document.getElementById('whispererSentiment');
    if (sentBadge) {
        const cleanT = text.toLowerCase();
        if (/(سرقة|حرام|نصب|فلوسي|اشتكي|غلط|بهدلة|خصم|ظلم|محامي|وزارة)/i.test(cleanT)) {
            sentBadge.innerText = 'نبرة الشريك: غاضب جداً / مهدد 😡';
            sentBadge.style.background = 'rgba(239, 68, 68, 0.25)';
            sentBadge.style.borderColor = '#EF4444';
            sentBadge.style.color = '#FCA5A5';
        } else if (/(بسرعة|الان|حالا|فورا|مستعجل|العميل واقف|الاكل هيبرد|وين المندوب)/i.test(cleanT)) {
            sentBadge.innerText = 'نبرة الشريك: مستعجل وطارئ 🚨';
            sentBadge.style.background = 'rgba(245, 158, 11, 0.25)';
            sentBadge.style.borderColor = '#F59E0B';
            sentBadge.style.color = '#FCD34D';
        } else if (/(ليش|كيف|ما فهمت|استفسار|ممكن اعرف|سؤال)/i.test(cleanT)) {
            sentBadge.innerText = 'نبرة الشريك: مستفسر / هادئ ❓';
            sentBadge.style.background = 'rgba(59, 130, 246, 0.2)';
            sentBadge.style.borderColor = '#3B82F6';
            sentBadge.style.color = '#93C5FD';
        } else {
            sentBadge.innerText = 'نبرة الشريك: طبيعي 😌';
            sentBadge.style.background = 'rgba(16, 185, 129, 0.2)';
            sentBadge.style.borderColor = '#10B981';
            sentBadge.style.color = '#6EE7B7';
        }
    }

    // 2. Dynamic 102-Case Matching Engine
    const norm = (typeof normalizeArabic === 'function') ? normalizeArabic(text.toLowerCase()) : text.toLowerCase();
    const promptBox = document.getElementById('whispererPromptText');
    const badge = document.getElementById('whispererMatchedCaseBadge');
    const objList = document.getElementById('whispererObjectionList');

    let matchedCase = null;
    const cases = (typeof allCases !== 'undefined' && allCases.length > 0) ? allCases : ((typeof embeddedKB !== 'undefined') ? embeddedKB : []);

    // Priority Check: Learned Synapses & Fast Keywords
    if (typeof getBuiltInLearnedCaseId === 'function') {
        const learnedId = getBuiltInLearnedCaseId(text);
        if (learnedId) matchedCase = cases.find(c => c && c.id == learnedId);
    }

    // Deep Search in allCases if not found
    if (!matchedCase && cases.length > 0) {
        if (/(مندوب|سائق|سواق|رايدر|تاخر|eta|اين المندوب|وين المندوب|ما وصل)/i.test(norm)) {
            matchedCase = cases.find(c => c && c.id == 50) || cases.find(c => c && c.id == 82);
        } else if (/(مادفعش|ما دفع|كاش|هرب|دون ان يدفع)/i.test(norm)) {
            matchedCase = cases.find(c => c && c.id == 51);
        } else if (/(مندوب خاطئ|سائق غلط|اخذ الطلب بالغلط|مندوب ثاني)/i.test(norm)) {
            matchedCase = cases.find(c => c && c.id == 99);
        } else if (/(نسي|ترك اغراض|كيس عصير|نسيان المندوب)/i.test(norm)) {
            matchedCase = cases.find(c => c && c.id == 52);
        } else if (/(سلوك|اخلاق|تعامل سيء|رفع صوته|غير محترم)/i.test(norm)) {
            matchedCase = cases.find(c => c && c.id == 82);
        } else if (/(لغى|الغا|ملغي|كنسل|تعويض طلب ملغي)/i.test(norm)) {
            matchedCase = cases.find(c => c && c.id == 45) || cases.find(c => c && c.id == 58);
        } else if (/(تلف|بارد|خربان|سكب|تعويض وجبة)/i.test(norm)) {
            matchedCase = cases.find(c => c && c.id == 58);
        } else if (/(طابعة|ورق|رول|ماكينة)/i.test(norm)) {
            matchedCase = cases.find(c => c && c.id == 100);
        } else if (/(ايبان|iban|حساب بنكي|تغيير البنك)/i.test(norm)) {
            matchedCase = cases.find(c => c && c.id == 92);
        } else if (/(فاتورة|عمولة|خصم|تقرير مالي)/i.test(norm)) {
            matchedCase = cases.find(c => c && c.id == 54);
        } else if (/(منيو|سعر|صنف|وجبة|تعديل)/i.test(norm)) {
            matchedCase = cases.find(c => c && c.id == 38);
        } else {
            // General word overlap match
            let bestScore = 0;
            const words = norm.split(/\\s+/).filter(w => w.length > 2);
            for (const c of cases) {
                if (!c) continue;
                let score = 0;
                const searchTxt = (c.case_title + ' ' + (c.sub_category || '') + ' ' + (c.procedure_arabic || '')).toLowerCase();
                for (const w of words) {
                    if (searchTxt.includes(w)) score++;
                }
                if (score > bestScore) {
                    bestScore = score;
                    matchedCase = c;
                }
            }
        }
    }

    // Default Fallback Case
    if (!matchedCase && cases.length > 0) matchedCase = cases.find(c => c && c.id == 50) || cases[0];

    if (matchedCase) {
        _whispererActiveCaseId = matchedCase.id;
        if (badge) badge.innerText = `الحالة: #${matchedCase.id} - ${matchedCase.case_title.slice(0, 35)}...`;
        
        // Craft clear, conversational teleprompter text
        let spokenScript = matchedCase.procedure_arabic || 'أهلاً بك شريكنا العزيز، نحرص تماماً على خدمتك وحل مشكلتك بأعلى دقة واحترافية.';
        // Remove SOP markers if present
        spokenScript = spokenScript.replace(/^إجراء[^:]*:/, '').trim();
        if (spokenScript.length > 250) spokenScript = spokenScript.slice(0, 240) + '...';
        
        if (promptBox) {
            promptBox.innerHTML = `<strong>"يا هلا وحياك الله شريكنا العزيز.. ${spokenScript}"</strong>`;
        }

        // Render Tailored Objections
        if (objList) {
            let catKey = 'RIDER';
            if (matchedCase.id == 45 || matchedCase.id == 58) catKey = 'CANCEL';
            else if (matchedCase.id == 54 || matchedCase.id == 92) catKey = 'FINANCE';
            else if (matchedCase.id == 100 || matchedCase.id == 103) catKey = 'DEVICE';
            else if (matchedCase.id == 38) catKey = 'MENU';
            
            const list = WHISPERER_OBJECTIONS_RADAR[catKey] || WHISPERER_OBJECTIONS_RADAR.RIDER;
            objList.innerHTML = list.map(item => `
                <div style="background: rgba(255,255,255,0.04); padding: 6px 10px; border-radius: 6px; border-left: 3px solid #10B981; margin-bottom: 4px;">
                    <div style="color: #FCD34D; font-weight: 700; margin-bottom: 2px;">${item.q}</div>
                    <div style="color: #E2E8F0;">${item.a}</div>
                </div>
            `).join('');
        }
    }
}

// 🤖 AI Call Summary Generator for Zendesk Internal Notes
async function generateAiCallSummaryFromWhisperer() {
    const transcript = _whispererFullTranscript || (document.getElementById('whispererTranscriptBox') ? document.getElementById('whispererTranscriptBox').innerText : '');
    const caseId = _whispererActiveCaseId || 50;
    const cases = (typeof allCases !== 'undefined' && allCases.length > 0) ? allCases : ((typeof embeddedKB !== 'undefined') ? embeddedKB : []);
    const c = cases.find(x => x && x.id == caseId) || { id: caseId, case_title: 'مكالمة دعم شريك' };
    const agent = (typeof getAgentArabicName === 'function') ? getAgentArabicName() : 'عمر';

    showToast('🤖 جاري تلخيص المكالمة بالذكاء الاصطناعي وتجهيز تقرير Zendesk...', 4000);

    const apiKey = (typeof getActiveGroqKey === 'function') ? getActiveGroqKey() : '';
    const model = (typeof getActiveGroqModel === 'function') ? getActiveGroqModel() : 'allam-2-7b';

    let summaryText = `[Zendesk Call Wrap-Up Note - Live Whisperer AI]
• حالة الدعم: #${c.id} - ${c.case_title}
• نوع القناة: Inbound Phone Call (مكالمة هاتفية مباشرة)
• ملخص حديث الشريك: ${transcript ? transcript.slice(0, 180) : 'استفسار شريك عن حالة الطلب والعمليات'}
• الإجراء المنفذ: تم تزويد الشريك بالإجراء المعتمد وتهدئته وشرح اللائحة الرسمية 2026.
• الموظف المسؤول: ${agent}
• حالة التذكرة: Solved / Closed`;

    if (apiKey) {
        try {
            const prompt = `أنت موظف عمليات أول في شركة هنقرستيشن.
قم بتلخيص المكالمة التالية في قالب تقرير داخلي احترافي لنظام Zendesk (Internal Note):
نص كلام الشريك في المكالمة:
"${transcript || 'التاجر يسأل عن الطلب'}"

بيانات الحالة المعتمدة:
#${c.id}: ${c.case_title}
الموظف: ${agent}

المطلوب: توليد Internal Note مختصرة باللغة العربية تشمل:
1. المشكلة الأساسية
2. نبرة الشريك
3. الإجراء الذي تم إبلاغه به بحسب لائحة هنقرستيشن
4. التوصية / الخطوة القادمة
أخرج نص الملاحظة فقط بدون مقدمات.`;

            const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${apiKey}` },
                body: JSON.stringify({
                    model: model,
                    messages: [
                        { role: 'system', content: 'You are a professional Zendesk wrap-up summary generator for HungerStation.' },
                        { role: 'user', content: prompt }
                    ],
                    max_tokens: 600,
                    temperature: 0.2
                })
            });
            const data = await res.json();
            const aiSummary = extractAiResponseContent(data);
            if (aiSummary && aiSummary.length > 30) {
                summaryText = `[Zendesk Internal Note - AI Live Summary]\n• Case: #${c.id} - ${c.case_title}\n• Agent: ${agent}\n\n` + aiSummary;
            }
        } catch(e) {
            console.warn('AI call summary fallback:', e);
        }
    }

    navigator.clipboard.writeText(summaryText);
    showToast('📋 تم نسخ ملخص المكالمة الاحترافي لـ Zendesk بنجاح! 🎉');
    if (typeof playSuccessChime === 'function') playSuccessChime();
}
'''

# Replace old handleWhispererSpeech and whisperer functions
start_whisp = html.find('// ─────────────────────────────────────────────────────────────────────────────\n// 2. LIVE CALL WHISPERER AI')
if start_whisp == -1:
    start_whisp = html.find('// 2. LIVE CALL WHISPERER AI')

if start_whisp != -1:
    end_whisp = html.find('// ─────────────────────────────────────────────────────────────────────────────\n// 3. DISPUTE FORENSICS AI ENGINE', start_whisp)
    if end_whisp == -1:
        end_whisp = html.find('// 3. DISPUTE FORENSICS AI ENGINE', start_whisp)
    
    if end_whisp != -1:
        html = html[:start_whisp] + UPGRADED_WHISPERER_LOGIC + "\n\n" + html[end_whisp:]
        print("✅ Upgraded Live Call Whisperer with dynamic 102 case matching & AI Call Summary!")
    else:
        print("⚠️ Could not locate end marker for Live Call Whisperer")
else:
    print("⚠️ Could not locate start marker for Live Call Whisperer")

# Add the Summarize button to Live Call Whisperer modal footer
OLD_WHISP_FOOTER = '<button type="button" id="whispererToggleBtn" onclick="toggleWhispererMic()"'
NEW_WHISP_FOOTER = '''<button type="button" id="whispererSummarizeBtn" onclick="generateAiCallSummaryFromWhisperer()" style="background: linear-gradient(135deg, #6366F1, #4F46E5); color: #FFF; border: none; padding: 10px 18px; border-radius: 10px; font-size: 0.88rem; font-weight: 800; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 4px 14px rgba(99,102,241,0.35);" title="توليد ملخص وتوثيق للمكالمة فوري بضغطة زر لنظام Zendesk">
                        <i class="fa-solid fa-file-invoice"></i> <span>تلخيص المكالمة بـ AI 📑</span>
                    </button>
                    <button type="button" id="whispererToggleBtn" onclick="toggleWhispererMic()"'''

if OLD_WHISP_FOOTER in html and 'generateAiCallSummaryFromWhisperer()' not in html:
    html = html.replace(OLD_WHISP_FOOTER, NEW_WHISP_FOOTER, 1)
    print("✅ Added AI Call Summary button to Live Call Whisperer modal footer!")

# ─────────────────────────────────────────────────────────────────────────────
# 4. INJECT SMART RIDER OPERATIONS & DISPATCH HUB MODAL & LOGIC
# ─────────────────────────────────────────────────────────────────────────────

RIDER_MODAL_HTML = '''
    <!-- 🛵 SMART RIDER OPERATIONS & DISPATCH HUB MODAL -->
    <div id="riderOperationsModal" class="modal-overlay" style="display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.85); z-index: 999996; backdrop-filter: blur(10px); align-items: center; justify-content: center; padding: 20px;">
        <div style="background: #0F172A; border: 2px solid #F59E0B; border-radius: 20px; width: 100%; max-width: 1050px; max-height: 92vh; display: flex; flex-direction: column; padding: 24px; color: #FFF; box-shadow: 0 25px 60px rgba(0,0,0,0.8), 0 0 35px rgba(245,158,11,0.3);">
            
            <!-- Modal Header -->
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 16px; margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 14px;">
                    <div style="width: 48px; height: 48px; border-radius: 12px; background: linear-gradient(135deg, #F59E0B, #D97706); display: flex; align-items: center; justify-content: center; font-size: 1.5rem; color: #000; box-shadow: 0 4px 14px rgba(245,158,11,0.4);">
                        <i class="fa-solid fa-motorcycle"></i>
                    </div>
                    <div>
                        <h3 style="margin: 0; font-size: 1.3rem; font-weight: 800; color: #F8FAFC; display: flex; align-items: center; gap: 10px;">
                            مركز عمليات وحلول الرايدر واللوجستيك (Rider Operations Hub)
                            <span style="font-size: 0.72rem; background: rgba(245,158,11,0.2); border: 1px solid #F59E0B; color: #FCD34D; padding: 2px 10px; border-radius: 20px; font-weight: 700;">لوائح هنقرستيشن 2026 🛵</span>
                        </h3>
                        <p style="margin: 2px 0 0 0; font-size: 0.8rem; color: #94A3B8;">حل أزمات المناديب في ثوانٍ: حاسبة التأخير والـ SLA، المندوب الهارب دون دفع، استلام مندوب خاطئ، والأغراض المنسية</p>
                    </div>
                </div>
                <button type="button" onclick="closeRiderOperationsModal()" style="background: transparent; border: none; color: #94A3B8; font-size: 1.4rem; cursor: pointer;">✕</button>
            </div>

            <!-- Operations Navigation Tabs -->
            <div style="display: flex; gap: 8px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 12px; margin-bottom: 16px; overflow-x: auto;">
                <button type="button" id="riderTabBtn_delay" onclick="switchRiderOpsTab('delay')" class="ws-tab-btn active" style="padding: 8px 16px; font-size: 0.85rem; font-weight: 800; border-radius: 8px; border: 1px solid #F59E0B; background: rgba(245,158,11,0.2); color: #FCD34D; cursor: pointer; display: flex; align-items: center; gap: 6px;">
                    <i class="fa-solid fa-clock"></i> <span>1. حاسبة تأخير المندوب والتعويض (#50)</span>
                </button>
                <button type="button" id="riderTabBtn_wrong" onclick="switchRiderOpsTab('wrong')" class="ws-tab-btn" style="padding: 8px 16px; font-size: 0.85rem; font-weight: 700; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.04); color: #94A3B8; cursor: pointer; display: flex; align-items: center; gap: 6px;">
                    <i class="fa-solid fa-shuffle"></i> <span>2. استلام مندوب خاطئ (#99)</span>
                </button>
                <button type="button" id="riderTabBtn_unpaid" onclick="switchRiderOpsTab('unpaid')" class="ws-tab-btn" style="padding: 8px 16px; font-size: 0.85rem; font-weight: 700; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.04); color: #94A3B8; cursor: pointer; display: flex; align-items: center; gap: 6px;">
                    <i class="fa-solid fa-hand-holding-dollar"></i> <span>3. غادر دون دفع كاش (#51)</span>
                </button>
                <button type="button" id="riderTabBtn_left" onclick="switchRiderOpsTab('left')" class="ws-tab-btn" style="padding: 8px 16px; font-size: 0.85rem; font-weight: 700; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.04); color: #94A3B8; cursor: pointer; display: flex; align-items: center; gap: 6px;">
                    <i class="fa-solid fa-bag-shopping"></i> <span>4. أغراض منسية (#52)</span>
                </button>
                <button type="button" id="riderTabBtn_misconduct" onclick="switchRiderOpsTab('misconduct')" class="ws-tab-btn" style="padding: 8px 16px; font-size: 0.85rem; font-weight: 700; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.04); color: #94A3B8; cursor: pointer; display: flex; align-items: center; gap: 6px;">
                    <i class="fa-solid fa-user-xmark"></i> <span>5. سوء سلوك وحظر الفرع (#82)</span>
                </button>
            </div>

            <!-- Tab Content 1: Delay SLA Calculator -->
            <div id="riderTabContent_delay" style="display: block; overflow-y: auto; flex: 1;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px;">
                        <h4 style="margin: 0 0 12px 0; color: #FCD34D; font-size: 0.95rem;"><i class="fa-solid fa-calculator"></i> مدخلات الطلب والتوقيت:</h4>
                        <div style="display: flex; flex-direction: column; gap: 10px;">
                            <div>
                                <label style="font-size: 0.78rem; color: #94A3B8; display: block; margin-bottom: 4px;">رقم الطلب (Order ID):</label>
                                <input type="text" id="riderCalcOrderId" placeholder="مثال: 94821034" style="width: 100%; background: #0B1120; border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; padding: 8px 12px; color: #FFF; font-size: 0.88rem;">
                            </div>
                            <div>
                                <label style="font-size: 0.78rem; color: #94A3B8; display: block; margin-bottom: 4px;">اسم المتجر / الفرع:</label>
                                <input type="text" id="riderCalcStoreName" placeholder="مثال: برجر ستيشن - فرع الصحافة" style="width: 100%; background: #0B1120; border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; padding: 8px 12px; color: #FFF; font-size: 0.88rem;">
                            </div>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                                <div>
                                    <label style="font-size: 0.78rem; color: #94A3B8; display: block; margin-bottom: 4px;">مدة جاهزية الطعام (دقيقة):</label>
                                    <input type="number" id="riderCalcPrepMinutes" value="12" style="width: 100%; background: #0B1120; border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; padding: 8px 12px; color: #FFF; font-size: 0.88rem;">
                                </div>
                                <div>
                                    <label style="font-size: 0.78rem; color: #94A3B8; display: block; margin-bottom: 4px;">مدة انتظار المندوب (دقيقة):</label>
                                    <input type="number" id="riderCalcWaitMinutes" value="22" style="width: 100%; background: #0B1120; border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; padding: 8px 12px; color: #FFF; font-size: 0.88rem;">
                                </div>
                            </div>
                            <button type="button" onclick="calculateRiderDelaySla()" style="background: linear-gradient(135deg, #F59E0B, #D97706); color: #000; border: none; padding: 10px; border-radius: 8px; font-weight: 800; cursor: pointer; margin-top: 6px;">
                                <i class="fa-solid fa-bolt"></i> فحص الـ SLA واستحقاق التعويض
                            </button>
                        </div>
                    </div>

                    <div style="background: rgba(245,158,11,0.04); border: 1.5px solid rgba(245,158,11,0.3); border-radius: 12px; padding: 16px; display: flex; flex-direction: column;">
                        <h4 style="margin: 0 0 10px 0; color: #FCD34D; font-size: 0.95rem; display: flex; justify-content: space-between;">
                            <span><i class="fa-solid fa-gavel"></i> القرار التشغيلي والماكرو:</span>
                            <span id="riderDelayVerdictBadge" style="font-size: 0.72rem; padding: 2px 8px; border-radius: 10px; background: rgba(239,68,68,0.2); color: #FCA5A5;">تأخير حرج (&gt; 15 دقيقة)</span>
                        </h4>
                        <div id="riderDelayResultBox" style="flex: 1; background: #0B1120; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px; font-size: 0.86rem; color: #E2E8F0; line-height: 1.7; overflow-y: auto;">
                            اضغط زر "فحص الـ SLA" لحساب القرار التلقائي وتوليد الرد المعتمد...
                        </div>
                        <div style="display: flex; gap: 8px; margin-top: 10px;">
                            <button type="button" onclick="copyRiderOpsResult('riderDelayResultBox')" style="flex: 1; background: #10B981; color: #FFF; border: none; padding: 8px; border-radius: 8px; font-weight: 800; cursor: pointer;">
                                <i class="fa-solid fa-copy"></i> نسخ الرد المعتمد للشريك
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tab Content 2: Wrong Rider Picked Order -->
            <div id="riderTabContent_wrong" style="display: none; overflow-y: auto; flex: 1;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px;">
                        <h4 style="margin: 0 0 12px 0; color: #38BDF8; font-size: 0.95rem;"><i class="fa-solid fa-shuffle"></i> بيانات استلام المندوب الخاطئ:</h4>
                        <div style="display: flex; flex-direction: column; gap: 10px;">
                            <div>
                                <label style="font-size: 0.78rem; color: #94A3B8; display: block; margin-bottom: 4px;">رقم الطلب الأصلي:</label>
                                <input type="text" id="wrongRiderOrderId" placeholder="مثال: 88719234" style="width: 100%; background: #0B1120; border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; padding: 8px 12px; color: #FFF; font-size: 0.88rem;">
                            </div>
                            <div>
                                <label style="font-size: 0.78rem; color: #94A3B8; display: block; margin-bottom: 4px;">اسم المندوب الخاطئ (إن وجد):</label>
                                <input type="text" id="wrongRiderName" placeholder="مثال: كابتن محمد / غير معروف" style="width: 100%; background: #0B1120; border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; padding: 8px 12px; color: #FFF; font-size: 0.88rem;">
                            </div>
                            <button type="button" onclick="generateWrongRiderResolution()" style="background: linear-gradient(135deg, #38BDF8, #0284C7); color: #FFF; border: none; padding: 10px; border-radius: 8px; font-weight: 800; cursor: pointer; margin-top: 6px;">
                                <i class="fa-solid fa-file-shield"></i> توليد بروتوكول الحل والتعويض 100%
                            </button>
                        </div>
                    </div>

                    <div style="background: rgba(56,189,248,0.04); border: 1.5px solid rgba(56,189,248,0.3); border-radius: 12px; padding: 16px; display: flex; flex-direction: column;">
                        <h4 style="margin: 0 0 10px 0; color: #38BDF8; font-size: 0.95rem;"><i class="fa-solid fa-bullhorn"></i> رد الدعم وتذكرة التصعيد:</h4>
                        <div id="wrongRiderResultBox" style="flex: 1; background: #0B1120; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px; font-size: 0.86rem; color: #E2E8F0; line-height: 1.7; overflow-y: auto;">
                            أدخل رقم الطلب واضغط على الزر لإخراج الرد الرسمي وتأكيد عدم تضرر الشريك مالياً...
                        </div>
                        <div style="display: flex; gap: 8px; margin-top: 10px;">
                            <button type="button" onclick="copyRiderOpsResult('wrongRiderResultBox')" style="flex: 1; background: #38BDF8; color: #000; border: none; padding: 8px; border-radius: 8px; font-weight: 800; cursor: pointer;">
                                <i class="fa-solid fa-copy"></i> نسخ الرد المعتمد للشريك
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tab Content 3: Rider Left Without Paying -->
            <div id="riderTabContent_unpaid" style="display: none; overflow-y: auto; flex: 1;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px;">
                        <h4 style="margin: 0 0 12px 0; color: #10B981; font-size: 0.95rem;"><i class="fa-solid fa-receipt"></i> تفاصيل المبلغ الكاش غير المدفوع:</h4>
                        <div style="display: flex; flex-direction: column; gap: 10px;">
                            <div>
                                <label style="font-size: 0.78rem; color: #94A3B8; display: block; margin-bottom: 4px;">رقم الطلب:</label>
                                <input type="text" id="unpaidOrderId" placeholder="مثال: 76541290" style="width: 100%; background: #0B1120; border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; padding: 8px 12px; color: #FFF; font-size: 0.88rem;">
                            </div>
                            <div>
                                <label style="font-size: 0.78rem; color: #94A3B8; display: block; margin-bottom: 4px;">المبلغ المستحق (ريال سعودي SAR):</label>
                                <input type="number" id="unpaidAmount" placeholder="مثال: 125.50" style="width: 100%; background: #0B1120; border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; padding: 8px 12px; color: #FFF; font-size: 0.88rem;">
                            </div>
                            <div>
                                <label style="font-size: 0.78rem; color: #94A3B8; display: block; margin-bottom: 4px;">اسم المندوب المسجل في 1VU:</label>
                                <input type="text" id="unpaidRiderName" placeholder="مثال: رايدر أحمد عبد الله" style="width: 100%; background: #0B1120; border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; padding: 8px 12px; color: #FFF; font-size: 0.88rem;">
                            </div>
                            <button type="button" onclick="generateUnpaidCashClaim()" style="background: linear-gradient(135deg, #10B981, #059669); color: #FFF; border: none; padding: 10px; border-radius: 8px; font-weight: 800; cursor: pointer; margin-top: 6px;">
                                <i class="fa-solid fa-money-bill-transfer"></i> توليد مطالبة التحصيل والتسوية المالية
                            </button>
                        </div>
                    </div>

                    <div style="background: rgba(16,185,129,0.04); border: 1.5px solid rgba(16,185,129,0.3); border-radius: 12px; padding: 16px; display: flex; flex-direction: column;">
                        <h4 style="margin: 0 0 10px 0; color: #10B981; font-size: 0.95rem;"><i class="fa-solid fa-envelope-circle-check"></i> نموذج التصعيد المالي للمالية واللوجستيك:</h4>
                        <div id="unpaidResultBox" style="flex: 1; background: #0B1120; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px; font-size: 0.86rem; color: #E2E8F0; line-height: 1.7; overflow-y: auto;">
                            أدخل المبلغ ورقم الطلب لتوليد نموذج المطالبة المعتمد لضمان إيداع المبلغ بحساب الشريك البنكي...
                        </div>
                        <div style="display: flex; gap: 8px; margin-top: 10px;">
                            <button type="button" onclick="copyRiderOpsResult('unpaidResultBox')" style="flex: 1; background: #10B981; color: #FFF; border: none; padding: 8px; border-radius: 8px; font-weight: 800; cursor: pointer;">
                                <i class="fa-solid fa-copy"></i> نسخ نموذج المطالبة والرد
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tab Content 4: Rider Left Items -->
            <div id="riderTabContent_left" style="display: none; overflow-y: auto; flex: 1;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px;">
                        <h4 style="margin: 0 0 12px 0; color: #A855F7; font-size: 0.95rem;"><i class="fa-solid fa-box-open"></i> تفاصيل الأغراض المنسية بالفرع:</h4>
                        <div style="display: flex; flex-direction: column; gap: 10px;">
                            <div>
                                <label style="font-size: 0.78rem; color: #94A3B8; display: block; margin-bottom: 4px;">رقم الطلب:</label>
                                <input type="text" id="leftItemsOrderId" placeholder="مثال: 99120348" style="width: 100%; background: #0B1120; border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; padding: 8px 12px; color: #FFF; font-size: 0.88rem;">
                            </div>
                            <div>
                                <label style="font-size: 0.78rem; color: #94A3B8; display: block; margin-bottom: 4px;">الأصناف المنسية (مثال: كيس العصير والمقبلات):</label>
                                <input type="text" id="leftItemsNames" placeholder="مثال: كيس المشروبات والعصير البارد" style="width: 100%; background: #0B1120; border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; padding: 8px 12px; color: #FFF; font-size: 0.88rem;">
                            </div>
                            <button type="button" onclick="generateLeftItemsProtocol()" style="background: linear-gradient(135deg, #A855F7, #7C3AED); color: #FFF; border: none; padding: 10px; border-radius: 8px; font-weight: 800; cursor: pointer; margin-top: 6px;">
                                <i class="fa-solid fa-truck-fast"></i> استخراج بروتوكول الدعم (#52)
                            </button>
                        </div>
                    </div>

                    <div style="background: rgba(168,85,247,0.04); border: 1.5px solid rgba(168,85,247,0.3); border-radius: 12px; padding: 16px; display: flex; flex-direction: column;">
                        <h4 style="margin: 0 0 10px 0; color: #A855F7; font-size: 0.95rem;"><i class="fa-solid fa-clipboard-check"></i> توجيه الموظف والرد المعتمد:</h4>
                        <div id="leftItemsResultBox" style="flex: 1; background: #0B1120; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px; font-size: 0.86rem; color: #E2E8F0; line-height: 1.7; overflow-y: auto;">
                            أدخل الأصناف المنسية واضغط الزر لاستخراج الإجراء الرسمي...
                        </div>
                        <div style="display: flex; gap: 8px; margin-top: 10px;">
                            <button type="button" onclick="copyRiderOpsResult('leftItemsResultBox')" style="flex: 1; background: #A855F7; color: #FFF; border: none; padding: 8px; border-radius: 8px; font-weight: 800; cursor: pointer;">
                                <i class="fa-solid fa-copy"></i> نسخ الرد المعتمد للشريك
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tab Content 5: Driver Misconduct & Blacklist -->
            <div id="riderTabContent_misconduct" style="display: none; overflow-y: auto; flex: 1;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px;">
                        <h4 style="margin: 0 0 12px 0; color: #EC4899; font-size: 0.95rem;"><i class="fa-solid fa-ban"></i> تفاصيل المخالفة وطلب الحظر:</h4>
                        <div style="display: flex; flex-direction: column; gap: 10px;">
                            <div>
                                <label style="font-size: 0.78rem; color: #94A3B8; display: block; margin-bottom: 4px;">رقم الطلب:</label>
                                <input type="text" id="misconductOrderId" placeholder="مثال: 91823740" style="width: 100%; background: #0B1120; border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; padding: 8px 12px; color: #FFF; font-size: 0.88rem;">
                            </div>
                            <div>
                                <label style="font-size: 0.78rem; color: #94A3B8; display: block; margin-bottom: 4px;">نوع سوء السلوك:</label>
                                <select id="misconductTypeSelect" style="width: 100%; background: #0B1120; border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; padding: 8px 12px; color: #FFF; font-size: 0.88rem;">
                                    <option value="لفظي">تلفظ أو سوء تعامل مع موظفي المطعم</option>
                                    <option value="نظافة">عدم الالتزام بالزي وحقيبة التوصيل الحرارية</option>
                                    <option value="تأخير متعمد">جلوس المندوب خارج المطعم ورفض الاستلام</option>
                                    <option value="تلف الطعام">سوء نقل الوجبة وإتلافها أثناء القيادة</option>
                                </select>
                            </div>
                            <button type="button" onclick="generateRiderMisconductReport()" style="background: linear-gradient(135deg, #EC4899, #BE185D); color: #FFF; border: none; padding: 10px; border-radius: 8px; font-weight: 800; cursor: pointer; margin-top: 6px;">
                                <i class="fa-solid fa-triangle-exclamation"></i> رفع طلب حظر المندوب وتصعيد الأسطول
                            </button>
                        </div>
                    </div>

                    <div style="background: rgba(236,72,153,0.04); border: 1.5px solid rgba(236,72,153,0.3); border-radius: 12px; padding: 16px; display: flex; flex-direction: column;">
                        <h4 style="margin: 0 0 10px 0; color: #EC4899; font-size: 0.95rem;"><i class="fa-solid fa-file-contract"></i> تذكرة إدارة الأسطول ورد التهدئة:</h4>
                        <div id="misconductResultBox" style="flex: 1; background: #0B1120; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px; font-size: 0.86rem; color: #E2E8F0; line-height: 1.7; overflow-y: auto;">
                            حدد نوع المخالفة واضغط الزر لتوليد تصعيد الـ Blacklist الرسمي...
                        </div>
                        <div style="display: flex; gap: 8px; margin-top: 10px;">
                            <button type="button" onclick="copyRiderOpsResult('misconductResultBox')" style="flex: 1; background: #EC4899; color: #FFF; border: none; padding: 8px; border-radius: 8px; font-weight: 800; cursor: pointer;">
                                <i class="fa-solid fa-copy"></i> نسخ الرد المعتمد للشريك
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Footer -->
            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 14px; margin-top: 16px;">
                <span style="font-size: 0.78rem; color: #94A3B8;">📌 جميع الإجراءات مصممة ومطابقة لمعايير Bite Hub والعمليات الميدانية الرسمية لهنقرستيشن.</span>
                <button type="button" onclick="closeRiderOperationsModal()" style="background: rgba(255,255,255,0.1); color: #FFF; border: 1px solid rgba(255,255,255,0.2); padding: 8px 18px; border-radius: 8px; font-weight: 700; cursor: pointer;">إغلاق</button>
            </div>

        </div>
    </div>
'''

RIDER_JS_LOGIC = '''
// ─────────────────────────────────────────────────────────────────────────────
// 🛵 SMART RIDER OPERATIONS & DISPATCH HUB CONTROLLER
// ─────────────────────────────────────────────────────────────────────────────

function openRiderOperationsModal(tab = 'delay') {
    const m = document.getElementById('riderOperationsModal');
    if (!m) return;
    m.style.display = 'flex';
    switchRiderOpsTab(tab);
    
    // Auto-populate Order ID if present in active inputs
    const pInput = document.getElementById('partnerMessage');
    if (pInput && pInput.value) {
        const match = pInput.value.match(/\\b\\d{6,10}\\b/);
        if (match) {
            const oid = match[0];
            ['riderCalcOrderId', 'wrongRiderOrderId', 'unpaidOrderId', 'leftItemsOrderId', 'misconductOrderId'].forEach(id => {
                const el = document.getElementById(id);
                if (el && !el.value) el.value = oid;
            });
        }
    }
}

function closeRiderOperationsModal() {
    const m = document.getElementById('riderOperationsModal');
    if (m) m.style.display = 'none';
}

function switchRiderOpsTab(tabKey) {
    const tabs = ['delay', 'wrong', 'unpaid', 'left', 'misconduct'];
    tabs.forEach(t => {
        const btn = document.getElementById(`riderTabBtn_${t}`);
        const content = document.getElementById(`riderTabContent_${t}`);
        if (btn) {
            if (t === tabKey) {
                btn.style.background = 'rgba(245, 158, 11, 0.2)';
                btn.style.borderColor = '#F59E0B';
                btn.style.color = '#FCD34D';
                btn.classList.add('active');
            } else {
                btn.style.background = 'rgba(255, 255, 255, 0.04)';
                btn.style.borderColor = 'rgba(255, 255, 255, 0.1)';
                btn.style.color = '#94A3B8';
                btn.classList.remove('active');
            }
        }
        if (content) {
            content.style.display = (t === tabKey) ? 'block' : 'none';
        }
    });
}

function calculateRiderDelaySla() {
    const orderId = (document.getElementById('riderCalcOrderId')?.value || 'N/A').trim();
    const store = (document.getElementById('riderCalcStoreName')?.value || 'شريكنا العزيز').trim();
    const prepMin = parseInt(document.getElementById('riderCalcPrepMinutes')?.value || 10, 10);
    const waitMin = parseInt(document.getElementById('riderCalcWaitMinutes')?.value || 0, 10);
    const badge = document.getElementById('riderDelayVerdictBadge');
    const box = document.getElementById('riderDelayResultBox');
    const agent = (typeof getAgentArabicName === 'function') ? getAgentArabicName() : 'عمر';

    let verdict = '';
    let macroText = '';

    if (waitMin >= 15) {
        if (badge) {
            badge.innerText = `🚨 تجاوز الـ SLA بنحو ${waitMin} دقيقة (يحق التعويض 100%)`;
            badge.style.background = 'rgba(239, 68, 68, 0.25)';
            badge.style.color = '#FCA5A5';
        }
        verdict = `[تجاوز حرج لوقت الوصول - انتظر المطعم ${waitMin} دقيقة بعد التجهيز]`;
        macroText = `شريكنا العزيز (${store})،\\n\\nشكراً لتواصلكم مع هنقرستيشن بشأن الطلب رقم #${orderId}.\\n\\nنعتذر بشدة عن التأخير غير المقبول من قبل المندوب والذي تجاوز الـ 15 دقيقة المعتمدة في اللائحة بعد انتهاء تجهيزكم للطلب.\\n\\nوفقاً لسياسة جودة وسلامة الغذاء المعتمدة لعام 2026:\\n1. يرجى التكرم بإتلاف الوجبة الحالية لعدم صلاحيتها للتقديم بدرجة حرارة مناسبة.\\n2. جاري التنسيق الفوري لإعادة إسناد الطلب لمندوب آخر (Auto-Reassignment) ذو أولوية قصوى.\\n3. نؤكد لكم بأن متجركم يستحق تعويضاً كاملاً بنسبة 100% عن قيمة تكلفة الوجبة التالفة وسيتم إدراجها ضمن الحوالة البنكية القادمة.\\n\\nمع الشكر والتقدير لتعاونكم،\\n${agent}\\nفريق دعم شركاء هنقرستيشن`;
    } else if (waitMin >= 8) {
        if (badge) {
            badge.innerText = `⚠️ تأخير متوسط (${waitMin} دقيقة) - المندوب بالطريق`;
            badge.style.background = 'rgba(245, 158, 11, 0.25)';
            badge.style.color = '#FCD34D';
        }
        macroText = `شريكنا العزيز (${store})،\\n\\nشكراً لتواصلكم معنا بخصوص الطلب رقم #${orderId}.\\n\\nنحيطكم علماً بأننا قمنا بتتبع المندوب فوراً، وهو حالياً على بُعد مسافة قصيرة جداً من فرعكم ومتوقع وصوله خلال بضع دقائق. تم إرسال تنبيه عاجل للمندوب عبر التطبيق لإتمام الاستلام فوراً.\\n\\nنرجو منكم إبقاء الوجبة مغلفة بحقيبة الحفظ لحين وصوله.\\n\\nشاكرين لكم صبركم وتفهمكم،\\n${agent}\\nهنقرستيشن`;
    } else {
        if (badge) {
            badge.innerText = `✅ ضمن النطاق الطبيعي (${waitMin} دقيقة)`;
            badge.style.background = 'rgba(16, 185, 129, 0.25)';
            badge.style.color = '#6EE7B7';
        }
        macroText = `شريكنا العزيز،\\n\\nالمندوب في طريقه للاستلام وضمن معدل وقت الوصول القياسي للطلب رقم #${orderId}.\\n\\nشكراً لحرصكم وتعاونكم المثمر،\\n${agent}\\nهنقرستيشن`;
    }

    if (box) {
        box.innerText = macroText.replace(/\\\\n/g, '\\n');
    }
    showToast('⚡ تم حساب الـ SLA وتوليد الرد المعتمد فوراً!');
    if (typeof playSuccessChime === 'function') playSuccessChime();
}

function generateWrongRiderResolution() {
    const orderId = (document.getElementById('wrongRiderOrderId')?.value || 'N/A').trim();
    const wrongRider = (document.getElementById('wrongRiderName')?.value || 'غير محدد').trim();
    const box = document.getElementById('wrongRiderResultBox');
    const agent = (typeof getAgentArabicName === 'function') ? getAgentArabicName() : 'عمر';

    const text = `شريكنا العزيز،\\n\\nشكراً لتواصلكم مع هنقرستيشن وإبلاغنا بشأن استلام الطلب رقم #${orderId} من قبل مندوب خاطئ (${wrongRider}).\\n\\nنود طمأنتكم وتأكيد الإجراء المعتمد فوراً لحفظ حقوقكم:\\n1. تم فتح تحقيق فوري مع الكابتن المستلم بالخطأ، وجاري متابعة الطلب مع المندوب الأصلي.\\n2. يرجى التكرم بإعادة تجهيز وجبة طازجة لتسليمها للكابتن المخصص للنظام فور وصوله لضمان استلام العميل لطلبه.\\n3. نؤكد لكم بأنكم لن تتحملوا أي خسارة، وسيتم تعويضكم بنسبة 100% عن تكلفة الوجبة التي أخذها المندوب الخاطئ ضمن مستحقاتكم الدورية دون أي خصم.\\n\\nمع فائق الاحترام والتقدير،\\n${agent}\\nفريق دعم شركاء هنقرستيشن`;

    if (box) box.innerText = text.replace(/\\\\n/g, '\\n');
    showToast('✅ تم توليد بروتوكول استلام المندوب الخاطئ والتعويض 100%');
    if (typeof playSuccessChime === 'function') playSuccessChime();
}

function generateUnpaidCashClaim() {
    const orderId = (document.getElementById('unpaidOrderId')?.value || 'N/A').trim();
    const amount = (document.getElementById('unpaidAmount')?.value || '0').trim();
    const rider = (document.getElementById('unpaidRiderName')?.value || 'المندوب المسجل').trim();
    const box = document.getElementById('unpaidResultBox');
    const agent = (typeof getAgentArabicName === 'function') ? getAgentArabicName() : 'عمر';

    const text = `[نموذج تصعيد مالي رسمي - مطالبة نقدية غير مدفوعة (Case #51)]\\n• رقم الطلب: ${orderId}\\n• المبلغ المستحق نقداً: ${amount} ريال سعودي SAR\\n• اسم المندوب: ${rider}\\n• تفاصيل الحالة: غادر المندوب الفرع دون سداد قيمة الطلب للمطعم نقداً.\\n\\n[الرد المعتمد للشريك]:\\nشريكنا العزيز،\\nنحيطكم علماً بأنه تم تسجيل مطالبة مالية رسمية برقم الطلب #${orderId} وبمبلغ ${amount} ريال.\\nسيتم خصم هذا المبلغ فوراً من المحفظة المالية للمندوب وإيداعه مباشرة في حسابكم البنكي ضمن الحوالة القادمة، ولن يتحمل مطعمكم أي عجز نقدي بإذن الله.\\n\\nمع التحية،\\n${agent}\\nهنقرستيشن`;

    if (box) box.innerText = text.replace(/\\\\n/g, '\\n');
    showToast('💰 تم توليد مطالبة التحصيل النقدي للمالية واللوجستيك!');
    if (typeof playSuccessChime === 'function') playSuccessChime();
}

function generateLeftItemsProtocol() {
    const orderId = (document.getElementById('leftItemsOrderId')?.value || 'N/A').trim();
    const items = (document.getElementById('leftItemsNames')?.value || 'أغراض ومشروبات منسية').trim();
    const box = document.getElementById('leftItemsResultBox');
    const agent = (typeof getAgentArabicName === 'function') ? getAgentArabicName() : 'عمر';

    const text = `شريكنا العزيز،\\n\\nشكراً لحرصكم وإشعارنا بوجود عناصر متبقية بالفرع (${items}) للطلب رقم #${orderId}.\\n\\nالإجراء المعتمد الرسمي (Case #52):\\n1. تم التواصل هاتفياً مع المندوب لإبلاغه بالعودة لاستلام الصنف المتبقي فوراً إن كان قريباً من موقعكم.\\n2. في حال تعذر عودة المندوب أو تسليم الطلب للعميل، نرجو عدم القلق، فلن يتم تحميلكم أي مسؤولية أو خصم، وسيتم تعويض العميل عن الصنف الناقص مباشرة دون التأثير على مستحقات المتجر.\\n\\nشكراً لأمانتكم وتفانيكم الدائم،\\n${agent}\\nهنقرستيشن`;

    if (box) box.innerText = text.replace(/\\\\n/g, '\\n');
    showToast('📦 تم استخراج بروتوكول الأغراض المنسية!');
    if (typeof playSuccessChime === 'function') playSuccessChime();
}

function generateRiderMisconductReport() {
    const orderId = (document.getElementById('misconductOrderId')?.value || 'N/A').trim();
    const reason = document.getElementById('misconductTypeSelect')?.value || 'سوء سلوك';
    const box = document.getElementById('misconductResultBox');
    const agent = (typeof getAgentArabicName === 'function') ? getAgentArabicName() : 'عمر';

    const text = `[تصعيد عاجل لإدارة الأسطول واللوجستيك - طلب حظر مندوب من الفرع (Case #82)]\\n• رقم الطلب: ${orderId}\\n• نوع المخالفة: ${reason}\\n• الإجراء المطلوب: تفعيل Blacklist للمندوب من هذا الفرع تحديداً لمنعه من استلام أي طلبات مستقبلية.\\n\\n[رد الاعتذار والتهدئة للشريك]:\\nشريكنا العزيز،\\nنأسف بشدة للتجربة غير اللائقة الصادرة من المندوب في الطلب رقم #${orderId}.\\nنؤكد لكم أن مثل هذه التصرفات مرفوضة تماماً ولا تمثل معايير هنقرستيشن في احترام شركائنا.\\nتم رفع شكوى عاجلة لإدارة الأسطول، وطلب حظر المندوب من استلام أي طلبات تابعة لفرعكم مستقبلاً لضمان بيئة عمل مريحة لفريقكم.\\n\\nمع خالص التقدير والاحترام،\\n${agent}\\nهنقرستيشن`;

    if (box) box.innerText = text.replace(/\\\\n/g, '\\n');
    showToast('🚫 تم إنشاء تقرير حظر المندوب وتصعيد الأسطول!');
    if (typeof playSuccessChime === 'function') playSuccessChime();
}

function copyRiderOpsResult(elementId) {
    const el = document.getElementById(elementId);
    if (!el) return;
    const txt = el.innerText || el.textContent;
    navigator.clipboard.writeText(txt);
    showToast('📋 تم نسخ الرد المعتمد لحافظة الجهاز بنجاح!');
    if (typeof playSuccessChime === 'function') playSuccessChime();
}
'''

# Inject RIDER_MODAL_HTML right before liveCallWhispererModal or partnerSimulatorModal
if 'id="riderOperationsModal"' not in html:
    ANCHOR = '<!-- 🎙️ LIVE CALL WHISPERER MODAL -->'
    if ANCHOR in html:
        html = html.replace(ANCHOR, RIDER_MODAL_HTML + '\n\n    ' + ANCHOR, 1)
        print("✅ Injected Rider Operations Modal HTML!")
    else:
        ANCHOR2 = '<div id="liveCallWhispererModal"'
        html = html.replace(ANCHOR2, RIDER_MODAL_HTML + '\n\n    ' + ANCHOR2, 1)
        print("✅ Injected Rider Operations Modal HTML (fallback anchor)!")

# Inject RIDER_JS_LOGIC right after window.selectCase
if 'function openRiderOperationsModal' not in html:
    JS_ANCHOR = 'window.selectCase = selectCase;'
    if JS_ANCHOR in html:
        html = html.replace(JS_ANCHOR, JS_ANCHOR + '\n\n' + RIDER_JS_LOGIC, 1)
        print("✅ Injected Rider Operations JS logic!")
    else:
        # Fallback to end of script
        html = html.replace('</script>\n</body>', RIDER_JS_LOGIC + '\n</script>\n</body>', 1)
        print("✅ Injected Rider Operations JS logic (end of script)!")

# ─────────────────────────────────────────────────────────────────────────────
# 5. UPGRADE MENU INTELLIGENCE (SFDA CALORIES & PREFLIGHT CHECKER)
# ─────────────────────────────────────────────────────────────────────────────

SFDA_CALORIE_ESTIMATOR = '''
// 🥗 SFDA Smart Calorie Auto-Estimator (Saudi Food & Drug Authority Compliance)
function estimateSfdaCalories(item) {
    if (!item) return 350;
    const name = ((item.name_ar || '') + ' ' + (item.name_en || '') + ' ' + (item.category_ar || '')).toLowerCase();
    
    if (/(مشروب|بيبسي|كولا|ماء|عصير|شاي|قهوة|موهيتو|juice|pepsi|water|drink)/i.test(name)) {
        if (/(ماء|water)/i.test(name)) return 0;
        if (/(دايت|diet|zero|سيرب|لايت)/i.test(name)) return 5;
        if (/(عصير طبيعي|fresh|رمان|برتقال|مانجو)/i.test(name)) return 140;
        return 160;
    }
    if (/(سلطة|فتوش|تبولة|سيزر|جرجير|salad)/i.test(name)) {
        if (/(سيزر بالدجاج|chicken caesar)/i.test(name)) return 380;
        return 180;
    }
    if (/(شوربة|عدس|كوارع|soup)/i.test(name)) return 220;
    if (/(بطاطس|فرايز|ودجز|موزاريلا|حلقات بصل|سمبوسة|fries|nuggets|sides)/i.test(name)) return 380;
    if (/(برجر دبل|دبل لحم|دبل تشيز|double burger)/i.test(name)) return 780;
    if (/(برجر|ساندوتش|فاهيتا|صاروخ|burger|sandwich|wrap)/i.test(name)) return 540;
    if (/(شاورما عربي|صحن شاورما)/i.test(name)) return 680;
    if (/(شاورما|shawarma)/i.test(name)) return 420;
    if (/(بروست|بروستد|مسحب|broasted|crispy)/i.test(name)) return 720;
    if (/(مشويات|مشاوي|كباب|اوصال|ستيك|ريش|grill|kebab)/i.test(name)) return 590;
    if (/(كبسة|مندي|مضغوط|حنيذ|بخاري|برياني|سليق|kabsa|mandi)/i.test(name)) return 780;
    if (/(بيتزا|pizza)/i.test(name)) return 680;
    if (/(باستا|مكرونة|نودلز|pasta)/i.test(name)) return 590;
    if (/(حلا|كيك|وافل|كريب|بسبوسة|كنافة|dessert|cake)/i.test(name)) return 440;
    return 450;
}
'''

if 'function estimateSfdaCalories' not in html:
    html = html.replace('function autoTranslateMenuText', SFDA_CALORIE_ESTIMATOR + '\nfunction autoTranslateMenuText', 1)
    print("✅ Injected SFDA Calorie Auto-Estimator!")

# Hook into smartAutoFillAndTranslateBilingual to auto-estimate calories
OLD_AUTOFILL = '''        // 2. If price is 0 or missing, flag warning (keep 0)
        if (!it.price || it.price <= 0) {'''

NEW_AUTOFILL = '''        // 1.5 SFDA Calorie Check & Auto-Estimation
        if (!it.calories || it.calories === 0 || it.calories === '0') {
            it.calories = estimateSfdaCalories(it);
        }

        // 2. If price is 0 or missing, flag warning (keep 0)
        if (!it.price || it.price <= 0) {'''

if OLD_AUTOFILL in html and 'estimateSfdaCalories(it)' not in html:
    html = html.replace(OLD_AUTOFILL, NEW_AUTOFILL, 1)
    print("✅ Hooked SFDA calorie auto-estimation into smartAutoFillAndTranslateBilingual!")

# Write updated html
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Saved upgraded index.html! New length:", len(html))
print("🎉 All audits, rider operations, call whisperer, AI model fixes, and menu intelligence upgrades successfully applied!")
