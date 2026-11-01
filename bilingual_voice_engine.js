// =========================================================================
// 🎙️ BILINGUAL SPEECH & NEURAL INTELLIGENCE ENGINE (ARABIC + ENGLISH REAL-TIME)
// Hungerstation Vendor Support Suite - Next-Gen Voice Copilot
// =========================================================================

// ── 1. Comprehensive Phonetic & Terminology Auto-Correct Map ───────────
const BILINGUAL_PHONETIC_PAIRS = [
    // Financial & Billing
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:بيلينج|بيلنج|بلينج|بيلينغ)(?![\u0600-\u06FF])/gi, rep: "Billing" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:انفويس|إنفويس|انفويسز|انفوس)(?![\u0600-\u06FF])/gi, rep: "Invoice" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:باي\s*اوت|بي\s*اوت|بايوت|بيوت)(?![\u0600-\u06FF])/gi, rep: "Payout" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:كوميشن|كومشن|عمولة\s*كوميشن)(?![\u0600-\u06FF])/gi, rep: "Commission" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:فات|فاليو\s*ادد\s*تاكس|ضريبة\s*فات)(?![\u0600-\u06FF])/gi, rep: "VAT 15%" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:ستيتمنت|اس\s*او\s*ايه|كشف\s*حساب\s*اس\s*او\s*ايه)(?![\u0600-\u06FF])/gi, rep: "Statement of Account (SOA)" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:آيبان|ايبان|اي\s*بان|اى\s*بان)(?![\u0600-\u06FF])/gi, rep: "IBAN" },

    // Devices & POS
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:ديفايس|ديفيس|بوس\s*ديفايس|ديبايس|جهاز\s*ديفايس)(?![\u0600-\u06FF])/gi, rep: "POS Device" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:بي\s*او\s*اس|بي\s*او\s*إس|بوس)(?![\u0600-\u06FF])/gi, rep: "POS" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:تابلت|تابلت\s*هنقرستيشن|جهاز\s*التابلت)(?![\u0600-\u06FF])/gi, rep: "Tablet" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:برينتر|طابعة\s*برينتر)(?![\u0600-\u06FF])/gi, rep: "Printer" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:سيم\s*كارد|شريحة\s*سيم|سيم\s*كارت)(?![\u0600-\u06FF])/gi, rep: "SIM Card" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:فايف\s*هاندريد(?:\s*ريال)?|خمسمية\s*ريال(?:\s*جهاز)?|رسوم\s*500(?:\s*ريال)?)(?![\u0600-\u06FF])/gi, rep: "500 SAR Fee" },

    // Cancellations & Orders
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:كانسليشن|كنسليشن|كانسل|كنسل|طلب\s*كانسل)(?![\u0600-\u06FF])/gi, rep: "Cancellation" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:كومبينسيشن|كامبينسيشن|كومبنسيشن|تعويض\s*كومبينسيشن)(?![\u0600-\u06FF])/gi, rep: "Compensation" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:درايفر|درايفرز|رايدر|سائق\s*درايفر)(?![\u0600-\u06FF])/gi, rep: "Driver" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:ديليفري|دليفري|توصيل\s*ديليفري)(?![\u0600-\u06FF])/gi, rep: "Delivery" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:ديلاي|تاخير\s*ديلاي)(?![\u0600-\u06FF])/gi, rep: "Delay" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:اوردر|أوردر|اوردرات|اوردارات)(?![\u0600-\u06FF])/gi, rep: "Order" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:ريفاوند|ريفند|استرجاع\s*ريفاوند)(?![\u0600-\u06FF])/gi, rep: "Refund" },

    // Menu Studio & Systems
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:منيو\s*ابلود|منيو\s*شيت|رفع\s*المنيو)(?![\u0600-\u06FF])/gi, rep: "Menu Upload" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:منيو|المنيو)(?![\u0600-\u06FF])/gi, rep: "Menu" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:ايرور\s*(?:422|فور\s*تو\s*تو)|خطأ\s*422)(?![\u0600-\u06FF])/gi, rep: "Error 422" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:اكسيل|اكسل|شيت\s*اكسل)(?![\u0600-\u06FF])/gi, rep: "Excel" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:سيتينجز|سيتنج)(?![\u0600-\u06FF])/gi, rep: "Settings" },

    // Portal & Operations
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:زندسك|زين\s*ديسك|زين\s*دسك)(?![\u0600-\u06FF])/gi, rep: "Zendesk" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:سيلزفورس|سيلز\s*فورس)(?![\u0600-\u06FF])/gi, rep: "Salesforce" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:اوبريشنز|عمليات\s*اوبريشنز)(?![\u0600-\u06FF])/gi, rep: "Operations" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:بارتنر\s*بورتال|بوابة\s*الشركاء)(?![\u0600-\u06FF])/gi, rep: "Partner Portal" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:اكونت\s*مانجر|اريا\s*مانجر)(?![\u0600-\u06FF])/gi, rep: "Account Manager" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:شات|تكت|تيكت)(?![\u0600-\u06FF])/gi, rep: "Ticket" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:ريست\s*باسورد|اعادة\s*تعيين\s*الباسورد)(?![\u0600-\u06FF])/gi, rep: "Reset Password" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:لوجن|لوج\s*ان)(?![\u0600-\u06FF])/gi, rep: "Login" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:اونلاين|أونلاين)(?![\u0600-\u06FF])/gi, rep: "Online" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:اوفلاين|أوفلاين)(?![\u0600-\u06FF])/gi, rep: "Offline" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:اس\s*ال\s*ايه|اس\s*ال\s*إيه)(?![\u0600-\u06FF])/gi, rep: "SLA" },
    { regex: /(?<![\u0600-\u06FF])(?:الـ\s*)?(?:كواليتي|كيو\s*ايه|كيو\s*إيه)(?![\u0600-\u06FF])/gi, rep: "QA" }
];

// English sentence capitalizer & clean-up
function cleanAndFormatBilingualSpeech(text) {
    if (!text) return '';
    let res = text;

    // 1. Replace phonetic Arabized terms with clean English
    BILINGUAL_PHONETIC_PAIRS.forEach(p => {
        res = res.replace(p.regex, p.rep);
    });

    // 2. Normalize English acronyms & common casing
    res = res.replace(/\b(?:pos|p\.o\.s)\b/gi, 'POS')
             .replace(/\b(?:iban|i\.b\.a\.n)\b/gi, 'IBAN')
             .replace(/\b(?:sar|s\.a\.r)\b/gi, 'SAR')
             .replace(/\b(?:ccr)\b/gi, 'CCR')
             .replace(/\b(?:sla)\b/gi, 'SLA')
             .replace(/\b(?:cr)\b/gi, 'CR')
             .replace(/\b(?:eta)\b/gi, 'ETA')
             .replace(/\b(?:hungerstation|hunger\s*station)\b/gi, 'Hungerstation')
             .replace(/\b(?:zendesk)\b/gi, 'Zendesk')
             .replace(/\b(?:salesforce)\b/gi, 'Salesforce');

    // 3. Fix BiDi spacing between Arabic and Latin words
    res = res.replace(/([\u0600-\u06FF])([a-zA-Z0-9])/g, '$1 $2');
    res = res.replace(/([a-zA-Z0-9])([\u0600-\u06FF])/g, '$1 $2');

    // 4. English sentence auto-capitalization (e.g. "the vendor is" -> "The vendor is")
    res = res.replace(/(?:^|[.?!]\s+)([a-z])/g, (m, c) => m.toUpperCase());

    // 5. Clean multi-spaces
    res = res.replace(/\s+/g, ' ').trim();
    return res;
}

// Visual bilingual HTML syntax highlighting (Arabic in white, English in glowing cyan)
function highlightBilingualTokensHtml(text) {
    if (!text) return '';
    const words = text.split(/\s+/);
    return words.map(w => {
        if (/^[a-zA-Z0-9#\-_/.:]+$/.test(w)) {
            return `<span style="color: #38BDF8; font-weight: 800; background: rgba(56, 189, 248, 0.12); padding: 1px 5px; border-radius: 4px; display: inline-block; direction: ltr;">${w}</span>`;
        }
        return `<span>${w}</span>`;
    }).join(' ');
}

// ── 2. Deep Knowledge Intent Matcher for Spoken Inquiries ─────────────
function matchBilingualKnowledgeIntent(spokenText) {
    if (!spokenText || spokenText.trim().length < 2) return null;
    const cleanLower = spokenText.toLowerCase();
    const cases = (typeof allCases !== 'undefined' && allCases && allCases.length > 0) ? allCases :
                  (typeof embeddedKB !== 'undefined' ? embeddedKB : []);

    if (!cases || cases.length === 0) return null;

    // Direct High-Priority Intent Mappings for Spoken Language (Bilingual)
    const directSpokenRules = [
        {
            test: (t) => (t.includes('500') || t.includes('five hundred') || t.includes('خمسمية')) && (t.includes('pos') || t.includes('device') || t.includes('جهاز') || t.includes('تابلت') || t.includes('بديل') || t.includes('استبدال') || t.includes('replacement')),
            caseId: 1
        },
        {
            test: (t) => (t.includes('driver') || t.includes('rider') || t.includes('سائق') || t.includes('مندوب')) && (t.includes('delay') || t.includes('late') || t.includes('تاخر') || t.includes('تأخر') || t.includes('ما وصل') || t.includes('not arrived')),
            caseId: 46
        },
        {
            test: (t) => (t.includes('cancel') || t.includes('الغاء') || t.includes('إلغاء') || t.includes('ملغي')) && (t.includes('comp') || t.includes('تعويض') || t.includes('مستحقات') || t.includes('food ready') || t.includes('جاهز')),
            caseId: 45
        },
        {
            test: (t) => (t.includes('payout') || t.includes('thursday') || t.includes('خميس') || t.includes('حوالة') || t.includes('مبيعات') || t.includes('deposit') || t.includes('تحويل')) && (t.includes('billing') || t.includes('فاتورة') || t.includes('فلوس') || t.includes('money') || t.includes('account')),
            caseId: 54
        },
        {
            test: (t) => (t.includes('iban') || t.includes('آيبان') || t.includes('ايبان') || t.includes('حساب بنكي') || t.includes('bank account')),
            caseId: 13
        },
        {
            test: (t) => (t.includes('error 422') || t.includes('422') || t.includes('menu upload') || t.includes('رفع منيو') || t.includes('شيت منيو') || t.includes('menu excel')),
            caseId: 40
        },
        {
            test: (t) => (t.includes('closed') || t.includes('مغلق') || t.includes('مقفل')) && (t.includes('store') || t.includes('app') || t.includes('تطبيق') || t.includes('فرع') || t.includes('open')),
            caseId: 18
        },
        {
            test: (t) => (t.includes('commission') || t.includes('عمولة') || t.includes('نسبة هنقرستيشن') || t.includes('deduction') || t.includes('خصم')),
            caseId: 50
        }
    ];

    for (const rule of directSpokenRules) {
        if (rule.test(cleanLower)) {
            const found = cases.find(c => c.id === rule.caseId);
            if (found) return found;
        }
    }

    // Secondary: Inbound intent map check if available
    if (typeof inboundIntentMap !== 'undefined' && Array.isArray(inboundIntentMap)) {
        for (const item of inboundIntentMap) {
            if (item.keys.some(k => cleanLower.includes(k.toLowerCase()))) {
                const found = cases.find(c => c.id === item.id);
                if (found) return found;
            }
        }
    }

    // Tertiary: Smart Scoring fallback
    if (typeof smartScore === 'function') {
        let bestCase = null;
        let bestScore = 0;
        cases.forEach(c => {
            const sc = smartScore(c, spokenText);
            if (sc > bestScore) {
                bestScore = sc;
                bestCase = c;
            }
        });
        if (bestCase && bestScore > 20) return bestCase;
    }

    return null;
}

// ── 3. Voice Language Mode State & Switcher ────────────────────────────
var currentVoiceLanguageMode = window.currentVoiceLanguageMode || localStorage.getItem('hs_voice_lang_mode') || 'AUTO_BILINGUAL';

function changeVoiceLanguageMode(mode) {
    currentVoiceLanguageMode = window.currentVoiceLanguageMode = mode;
    localStorage.setItem('hs_voice_lang_mode', mode);
    const badge = document.getElementById('speechDetectedLangBadge');
    if (badge) {
        if (mode === 'AUTO_BILINGUAL') badge.innerText = '🌐 وضع ذكي (AR + EN)';
        else if (mode === 'ar-SA') badge.innerText = '🇸🇦 عربي فقط';
        else if (mode === 'en-US') badge.innerText = '🇬🇧 English Only';
    }
    showToast(`تم تعيين لغة التسجيل الصوتي: ${mode === 'AUTO_BILINGUAL' ? 'عربي + English ذكي' : mode}`);
}

// ── 4. Main Bilingual Voice Recording Controller ──────────────────────
var bilingualSpeechRecognizer = window.bilingualSpeechRecognizer || null;
var isBilingualRecording = window.isBilingualRecording || false;
var bilingualAccumulatedText = window.bilingualAccumulatedText || '';


// ── Safe Lifecycle & Restart Handlers ─────────────────────────────────
function createAndStartSpeechInstance() {
    if (!isBilingualRecording) return;
    try {
        if (bilingualSpeechRecognizer) {
            try {
                bilingualSpeechRecognizer.onend = null;
                bilingualSpeechRecognizer.onerror = null;
                bilingualSpeechRecognizer.onresult = null;
                bilingualSpeechRecognizer.abort();
            } catch(e) {}
            bilingualSpeechRecognizer = null;
        }

        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRec) {
            alert("متصفحك لا يدعم التعرف الصوتي المباشر. يرجى استخدام Google Chrome أو Safari!");
            isBilingualRecording = false;
            return;
        }

        bilingualSpeechRecognizer = new SpeechRec();
        bilingualSpeechRecognizer.continuous = true;
        bilingualSpeechRecognizer.interimResults = true;
        bilingualSpeechRecognizer.maxAlternatives = 1;

        if (typeof currentVoiceLanguageMode !== 'undefined' && currentVoiceLanguageMode === 'en-US') {
            bilingualSpeechRecognizer.lang = 'en-US';
        } else if (typeof currentVoiceLanguageMode !== 'undefined' && currentVoiceLanguageMode === 'ar-EG') {
            bilingualSpeechRecognizer.lang = 'ar-EG';
        } else {
            bilingualSpeechRecognizer.lang = 'ar-SA';
        }

        const btn = document.getElementById('mainMicBtn');
        const btnText = document.getElementById('mainMicText');
        const partnerMsg = document.getElementById('partnerMessage');
        const hud = document.getElementById('liveBilingualSpeechHud');
        const hudLiveText = document.getElementById('liveSpeechLiveText');
        const hudIntentBox = document.getElementById('liveSpeechDetectedIntent');
        const hudIntentText = document.getElementById('liveSpeechIntentText');

        bilingualSpeechRecognizer.onstart = () => {
            if (btn) {
                btn.style.background = '#EF4444';
                btn.style.boxShadow = '0 0 20px rgba(239, 68, 68, 0.9)';
            }
            if (btnText) btnText.innerText = '🔴 جاري الاستماع... اضغط للإنهاء';
            if (hud) hud.style.display = 'block';
            if (hudLiveText) hudLiveText.innerHTML = '<span style="color: #94A3B8;"><i class="fa-solid fa-microphone-lines fa-fade"></i> جاري الاستماع بصوتك الآن... تحدث بالعامية أو الإنجليزية وسيتم التقاطه وتصحيحه فورياً.</span>';
            if (hudIntentBox) hudIntentBox.style.display = 'none';
        };

        bilingualSpeechRecognizer.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript + ' ';
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }

            if (finalTranscript) {
                bilingualAccumulatedText += finalTranscript;
            }

            const rawCombined = bilingualAccumulatedText + interimTranscript;
            let cleanedBilingual = rawCombined;
            try {
                if (typeof cleanAndFormatBilingualSpeech === 'function') {
                    cleanedBilingual = cleanAndFormatBilingualSpeech(rawCombined);
                }
            } catch(e) {
                cleanedBilingual = rawCombined;
            }

            if (partnerMsg) {
                partnerMsg.value = cleanedBilingual || rawCombined;
                partnerMsg.scrollTop = partnerMsg.scrollHeight;
                if (typeof updateInputStats === 'function') updateInputStats();
            }

            if (hudLiveText) {
                hudLiveText.innerHTML = (typeof highlightBilingualTokensHtml === 'function') ? highlightBilingualTokensHtml(cleanedBilingual) : cleanedBilingual;
            }

            try {
                if (typeof matchBilingualKnowledgeIntent === 'function') {
                    const matched = matchBilingualKnowledgeIntent(cleanedBilingual);
                    if (matched && hudIntentBox && hudIntentText) {
                        hudIntentBox.style.display = 'flex';
                        hudIntentText.innerHTML = `تم استيعاب الحالة: <strong style="color: #38BDF8;">#${matched.id} - ${matched.case_title}</strong> (${matched.title_arabic || matched.case_title})`;
                    }
                }
            } catch(e) {}
        };

        bilingualSpeechRecognizer.onerror = (event) => {
            console.warn("Bilingual Speech Notice:", event.error);
            if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
                isBilingualRecording = false;
                if (btn) { btn.style.background = 'linear-gradient(135deg, #EC4899, #8B5CF6)'; }
                if (btnText) btnText.innerText = 'تسجيل صوتي (AR+EN) 🎙️';
                if (hud) hud.style.display = 'none';
                alert('⚠️ المتصفح يمنع استخدام المايك! اضغط على أيقونة الإعدادات أو القفل 🔒 بجانب رابط الموقع في شريط العنوان، واضبط Microphone على السماح (Allow).');
            }
        };

        bilingualSpeechRecognizer.onend = () => {
            if (isBilingualRecording) {
                clearTimeout(window._bilingualRestartTimeout);
                window._bilingualRestartTimeout = setTimeout(() => {
                    if (isBilingualRecording) {
                        createAndStartSpeechInstance();
                    }
                }, 200);
            }
        };

        bilingualSpeechRecognizer.start();
    } catch(err) {
        console.error("Speech instance startup error:", err);
        isBilingualRecording = false;
    }
}

// ── Toggle Speech Function ──────────────────────────────────────────
function toggleMainVoiceRecording() {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRec) {
        alert("متصفحك لا يدعم ميزة التعرف الصوتي المباشر. يرجى استخدام متصفح Google Chrome للحصول على أفضل تجربة صوتية!");
        return;
    }

    const btn = document.getElementById('mainMicBtn');
    const btnText = document.getElementById('mainMicText');
    const partnerMsg = document.getElementById('partnerMessage');
    const hud = document.getElementById('liveBilingualSpeechHud');

    if (isBilingualRecording) {
        // STOP RECORDING
        isBilingualRecording = false;
        if (bilingualSpeechRecognizer) {
            try { bilingualSpeechRecognizer.stop(); } catch(e) {}
        }
        if (btn) {
            btn.style.background = 'linear-gradient(135deg, #EC4899, #8B5CF6)';
            btn.style.boxShadow = '0 4px 12px rgba(236, 72, 153, 0.4)';
        }
        if (btnText) btnText.innerText = 'تسجيل صوتي (AR+EN) 🎙️';
        if (hud) hud.style.display = 'none';
        showToast("🔴 تم إيقاف التسجيل الصوتي وتثبيت النص.");
        return;
    }

    // START RECORDING ENGINE
    isBilingualRecording = true;
    bilingualAccumulatedText = partnerMsg && partnerMsg.value ? partnerMsg.value.trim() + ' ' : '';
    showToast("🎙️ المساعد الصوتي يستمع الآن... اتكلم وهيظهر كلامك على الشاشة!");
    createAndStartSpeechInstance();
}

function stopAndGenerateFromSpeech() {
    if (isBilingualRecording) {
        toggleMainVoiceRecording();
    }
    const partnerMsg = document.getElementById('partnerMessage');
    if (!partnerMsg || !partnerMsg.value.trim()) {
        showToast("⚠️ لم يتم رصد كلمات صوتية بعد.");
        return;
    }

    showToast("⚡ تم تثبيت الكلام وتوليد الماكرو المعتمد فوراً!");
    if (typeof generateResponse === 'function') {
        generateResponse();
    }
}

// Global Exports
if (typeof window !== 'undefined') {
    window.cleanAndFormatBilingualSpeech = cleanAndFormatBilingualSpeech;
    window.matchBilingualKnowledgeIntent = matchBilingualKnowledgeIntent;
    window.toggleMainVoiceRecording = toggleMainVoiceRecording;
    window.changeVoiceLanguageMode = changeVoiceLanguageMode;
    window.stopAndGenerateFromSpeech = stopAndGenerateFromSpeech;
}
