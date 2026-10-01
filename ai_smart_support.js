/**
 * AI-Driven Support & Smart Triage Engine (v2026)
 * Supports:
 *  1. Debounced real-time input analysis matching knowledge_base.json
 *  2. Interactive instant solution popup ("هل هذه المشكلة تشبه...؟")
 *  3. Automated Smart Triage (Category, Priority, Sentiment, Summary) via Proxy / Cloud AI
 *  4. Seamless integration with GitHub Pages & Zendesk workflows
 */

(function (window) {
    'use strict';

    // 1. In-memory Knowledge Base with embedded fallback for zero-network environments
    const DEFAULT_KB = {
        "faq_database": [
            {
                "id": "ERR_001",
                "category": "Authentication",
                "problem": "نسيت كلمة المرور الخاصة بحساب المورد",
                "solution": "يمكنك استعادة كلمة المرور عبر الضغط على رابط 'هل نسيت كلمة المرور؟' في صفحة تسجيل الدخول، وسيصلك كود التفعيل عبر البريد المسجل.",
                "keywords": ["password", "login", "forgot", "كلمة مرور", "دخول", "حساب", "بوابة الشركاء", "الباسورد"]
            },
            {
                "id": "ERR_002",
                "category": "Payments",
                "problem": "تأخر صرف المستحقات المالية",
                "solution": "يتم صرف المستحقات كل يوم 25 من كل شهر ميلادي. يرجى التأكد من تحديث بيانات الحساب البنكي في لوحة التحكم.",
                "keywords": ["payment", "money", "delay", "فلوس", "دفع", "مستحقات", "حوالة", "فاتورة", "أرباح", "مبيعات"]
            },
            {
                "id": "ERR_003",
                "category": "Technical",
                "problem": "خطأ في تحميل فاتورة الـ PDF",
                "solution": "يرجى التأكد من استخدام متصفح Chrome وتحديثه لآخر إصدار. إذا استمرت المشكلة، جرب مسح الكاش (Cache) أو استخدم وضع التصفح الخفي (Incognito).",
                "keywords": ["pdf", "upload", "error", "فاتورة", "تحميل", "خطأ", "ملف", "كاش", "الفايل"]
            },
            {
                "id": "ERR_004",
                "category": "Technical",
                "problem": "الطابعة اللوحية لا تستقبل الطلبات أو تظهر غير متصلة",
                "solution": "تأكد من اتصال الطابعة بشبكة Wi-Fi مستقرة، أعد تشغيل الجهاز وتأكد من شحن البطارية. إذا استمر العطل تواصل معنا لاستبدال الطابعة (رسوم الاستبدال 500 ريال للأجهزة المفقودة/التالفة).",
                "keywords": ["طابعة", "جهاز", "توصيل", "استقبال", "tablet", "printer", "offline", "عطل", "مسروقة"]
            },
            {
                "id": "ERR_005",
                "category": "Operations",
                "problem": "طلب تعويض عن وجبة تالفة أو تأخر مندوب",
                "solution": "يتم رفع طلب التعويض وإرفاق صورة بون المطبخ الموضح به وقت التجهيز. يحق للمطعم التعويض إذا كان وقت التحضير ضمن الـ SLA وتأخر المندوب أكثر من 15 دقيقة.",
                "keywords": ["تعويض", "مندوب", "ملغي", "تأخر", "بون", "وجبة", "compensation", "rider", "سائق", "سواق"]
            },
            {
                "id": "ERR_006",
                "category": "Operations",
                "problem": "تعديل أوقات العمل أو إيقاف مؤقت للفرع",
                "solution": "يمكن تعديل ساعات العمل مباشرة من خلال بوابة الشركاء قسم الإعدادات. في حالات الطوارئ يمكن تفعيل الإيقاف المؤقت (Busy Mode) من جهاز الطابعة.",
                "keywords": ["ساعات", "مواعيد", "فتح", "إغلاق", "إيقاف", "دوام", "busy", "hours", "schedule", "فطور"]
            }
        ]
    };

    let localKnowledgeBase = DEFAULT_KB;
    let debounceTimer = null;
    let lastSuggestedFaqId = null;

    // Load external knowledge_base.json if available
    async function loadKnowledgeBase() {
        try {
            const res = await fetch('./knowledge_base.json');
            if (res.ok) {
                const data = await res.json();
                if (data && data.faq_database && Array.isArray(data.faq_database)) {
                    localKnowledgeBase = data;
                    console.log('✅ Loaded external knowledge_base.json with', data.faq_database.length, 'entries');
                }
            }
        } catch (e) {
            console.log('ℹ️ Using embedded knowledge_base.json fallback');
        }
    }

    // Arabic normalization helper
    function cleanNormText(text) {
        if (!text) return '';
        return text.toString().toLowerCase()
            .replace(/[أإآ]/g, 'ا')
            .replace(/ة/g, 'ه')
            .replace(/ى/g, 'ي')
            .replace(/[\u064B-\u065F]/g, '') // remove tashkeel
            .trim();
    }

    // Match input text against Knowledge Base
    function findBestFaqMatch(inputText) {
        if (!inputText || inputText.length < 4) return null;
        const normInput = cleanNormText(inputText);
        const tokens = normInput.split(/\s+/).filter(t => t.length > 2);

        let bestMatch = null;
        let highestScore = 0;

        for (const item of localKnowledgeBase.faq_database) {
            let score = 0;
            const normProblem = cleanNormText(item.problem);

            // Exact substring matches
            if (normInput.includes(normProblem) || normProblem.includes(normInput)) {
                score += 50;
            }

            // Keyword matches
            if (item.keywords && Array.isArray(item.keywords)) {
                for (const kw of item.keywords) {
                    const normKw = cleanNormText(kw);
                    if (normInput.includes(normKw)) {
                        score += 20;
                    }
                }
            }

            // Token overlap
            for (const token of tokens) {
                if (normProblem.includes(token)) score += 5;
            }

            if (score > highestScore && score >= 20) {
                highestScore = score;
                bestMatch = { item, score };
            }
        }

        return bestMatch ? bestMatch.item : null;
    }

    // Debounced input handler
    function handleRealtimeInput(e) {
        const text = e.target.value.trim();
        clearTimeout(debounceTimer);

        const card = document.getElementById('aiInstantSuggestionCard');
        if (!card) return;

        if (text.length < 5) {
            card.style.display = 'none';
            lastSuggestedFaqId = null;
            return;
        }

        debounceTimer = setTimeout(() => {
            const match = findBestFaqMatch(text);
            if (match) {
                if (lastSuggestedFaqId === match.id) return;
                lastSuggestedFaqId = match.id;
                renderInstantSuggestion(match);
            } else {
                card.style.display = 'none';
                lastSuggestedFaqId = null;
            }
        }, 320); // 320ms debounce
    }

    // Render the instant popup card
    function renderInstantSuggestion(faq) {
        const card = document.getElementById('aiInstantSuggestionCard');
        if (!card) return;

        card.innerHTML = `
            <div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 12px;">
                <div style="display: flex; align-items: flex-start; gap: 10px;">
                    <div style="width: 38px; height: 38px; border-radius: 10px; background: linear-gradient(135deg, #10B981, #059669); display: flex; align-items: center; justify-content: center; font-size: 1.15rem; color: #FFF; flex-shrink: 0; box-shadow: 0 4px 12px rgba(16,185,129,0.35);">
                        <i class="fa-solid fa-lightbulb"></i>
                    </div>
                    <div>
                        <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                            <span style="font-weight: 800; font-size: 0.88rem; color: #6EE7B7;">
                                هل هذه المشكلة تشبه: "${faq.problem}"؟
                            </span>
                            <span style="background: rgba(16,185,129,0.2); color: #34D399; border: 1px solid rgba(16,185,129,0.35); padding: 1px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: 700;">
                                ${faq.category}
                            </span>
                        </div>
                        <p style="margin: 6px 0 0 0; font-size: 0.82rem; color: #E2E8F0; line-height: 1.5;">
                            ${faq.solution}
                        </p>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 6px; flex-shrink: 0;">
                    <button type="button" onclick="window.applyInstantFaqSolution('${faq.id}')" style="background: linear-gradient(135deg, #10B981, #047857); color: #FFF; border: none; padding: 7px 14px; border-radius: 8px; font-weight: 800; font-size: 0.8rem; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 3px 10px rgba(16,185,129,0.4); transition: transform 0.15s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
                        <i class="fa-solid fa-check"></i> تطبيق الحل فوراً ⚡
                    </button>
                    <button type="button" onclick="window.dismissInstantFaqSuggestion()" style="background: rgba(255,255,255,0.08); color: #94A3B8; border: 1px solid rgba(255,255,255,0.15); padding: 7px 10px; border-radius: 8px; font-size: 0.8rem; cursor: pointer;">
                        ✕
                    </button>
                </div>
            </div>
        `;
        card.style.display = 'block';
    }

    // Dismiss suggestion
    window.dismissInstantFaqSuggestion = function () {
        const card = document.getElementById('aiInstantSuggestionCard');
        if (card) card.style.display = 'none';
    };

    // Apply instant solution
    window.applyInstantFaqSolution = function (faqId) {
        const faq = localKnowledgeBase.faq_database.find(f => f.id === faqId);
        if (!faq) return;

        const agentName = localStorage.getItem('hs_agent_name') || 'فريق الدعم الفني';
        const formattedMacro = `شريكنا العزيز،\nشكراً لتواصلكم مع فريق دعم الموردين.\n\nبخصوص استفساركم حول: "${faq.problem}"\n\n${faq.solution}\n\nتشرفت بمساعدتك اليوم، ويسعدنا دائماً خدمتكم.\n\nتقبل خالص تحياتنا،\n${agentName}\nفريق دعم الشركاء`;

        // Put in cases container or macro display
        const casesCont = document.getElementById('casesContainer');
        if (casesCont) {
            casesCont.innerHTML = `
                <div style="background: rgba(16,185,129,0.08); border: 1.5px solid #10B981; border-radius: 12px; padding: 18px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <span style="font-weight: 800; color: #34D399; font-size: 0.95rem;">
                            <i class="fa-solid fa-circle-check"></i> تم تطبيق الحل الفوري بنجاح من قاعدة المعرفة (${faq.id})
                        </span>
                        <span style="background: rgba(16,185,129,0.25); color: #A7F3D0; padding: 3px 10px; border-radius: 12px; font-size: 0.72rem; font-weight: 800;">
                            ${faq.category}
                        </span>
                    </div>
                    <pre style="white-space: pre-wrap; font-family: inherit; font-size: 0.9rem; color: #FFF; background: rgba(0,0,0,0.3); padding: 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08); line-height: 1.6;">${formattedMacro}</pre>
                    <div style="display: flex; gap: 8px; margin-top: 12px;">
                        <button onclick="navigator.clipboard.writeText(\`${formattedMacro.replace(/`/g, '\\`')}\`); if(typeof showToast==='function') showToast('تم نسخ الحل الفوري المعتمد بنجاح! 📋');" style="flex: 1; background: linear-gradient(135deg, #10B981, #059669); color: #FFF; border: none; padding: 10px; border-radius: 8px; font-weight: 800; font-size: 0.85rem; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px;">
                            <i class="fa-solid fa-copy"></i> نسخ الرد المعتمد للشريك
                        </button>
                    </div>
                </div>
            `;
        }

        // Render Instant Triage Badge for this FAQ
        const triageResult = {
            category: faq.category,
            priority: faq.category === 'Payments' ? 'High' : 'Medium',
            sentiment: 'Neutral',
            summary: faq.problem,
            recommended_action: 'إرسال الإجراء الإرشادي من قاعدة المعرفة'
        };
        renderTriageHud(triageResult);

        window.dismissInstantFaqSuggestion();
        if (typeof showToast === 'function') {
            showToast('⚡ تم توفير وقت الدعم وتطبيق الحل المقترح فورا!');
        }
    };

    // Fast local heuristic triage fallback (Zero-API cost & instant)
    function runLocalHeuristicTriage(text) {
        const norm = cleanNormText(text);

        let category = 'Technical';
        if (norm.match(/دفع|فلوس|مستحقات|حواله|فاتوره|مبيعات|ارباح|خصم|عموله|كاش/)) {
            category = 'Payments';
        } else if (norm.match(/باسورد|دخول|حساب|ايميل|تسجيل|password|login/)) {
            category = 'Authentication';
        } else if (norm.match(/مندوب|سائق|سواق|طلب|اوردر|توصيل|تاخر|الغاء|تعويض|ساعات|فتح|اغلاق/)) {
            category = 'Operations';
        }

        let priority = 'Medium';
        if (norm.match(/عاجل|ضروري|كارثه|طوارئ|متوقف|الان|سرقه|مفقود|urgent|emergency|immediately/)) {
            priority = 'Urgent';
        } else if (norm.match(/تاخير|فلوس|معلق|مشكله|خطا|خصم|مستحقات|delay|lost/)) {
            priority = 'High';
        } else if (norm.match(/استفسار|سؤال|كيف|ممكن|معرفه|hours|question/)) {
            priority = 'Low';
        }

        let sentiment = 'Neutral';
        if (norm.match(/سيء|زفت|حرام|نصابين|غضب|متضايق|كارثه|شكوى|مهزله|worst|angry|scam/)) {
            sentiment = 'Frustrated';
        } else if (norm.match(/شكرا|يعطيكم العافيه|تسلم|تحياتي|ممتاز|thank|great/)) {
            sentiment = 'Positive';
        }

        const summary = text.split(/[.\n،]/)[0].substring(0, 75).trim() || 'استفسار مورد جديد';

        return {
            category,
            priority,
            sentiment,
            summary,
            recommended_action: 'متابعة التذكرة وتوجيهها للقسم المختص'
        };
    }

    // Execute Smart Triage via Proxy or Cloud AI
    async function executeSmartTriage(text) {
        const proxyUrl = localStorage.getItem('hs_triage_proxy_url');
        const customApiKey = localStorage.getItem('hs_openai_api_key');

        // 1. Try Cloudflare Worker / Serverless Proxy if configured
        if (proxyUrl && proxyUrl.trim() !== '') {
            try {
                const res = await fetch(proxyUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: 'triage', text })
                });
                if (res.ok) {
                    const data = await res.json();
                    return data;
                }
            } catch (err) {
                console.warn('⚠️ Proxy failed, falling back to direct AI / local heuristics:', err);
            }
        }

        // 2. Try Direct OpenAI key if provided by user
        if (customApiKey && customApiKey.startsWith('sk-')) {
            try {
                const res = await fetch('https://api.openai.com/v1/chat/completions', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${customApiKey}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        model: 'gpt-4o-mini',
                        response_format: { type: 'json_object' },
                        temperature: 0.2,
                        messages: [
                            {
                                role: 'system',
                                content: `Analyze this vendor support ticket and return strictly valid JSON:
                                {
                                  "category": "Authentication | Payments | Technical | Operations",
                                  "priority": "Low | Medium | High | Urgent",
                                  "sentiment": "Positive | Neutral | Frustrated",
                                  "summary": "ملخص المشكلة في 6 كلمات بالعربية",
                                  "recommended_action": "إجراء فوري مقترح"
                                }`
                            },
                            { role: 'user', content: text }
                        ]
                    })
                });
                if (res.ok) {
                    const json = await res.json();
                    return JSON.parse(json.choices[0].message.content);
                }
            } catch (e) {
                console.warn('⚠️ Direct OpenAI call failed, falling back...');
            }
        }

        // 3. Fallback to Embedded Groq Cloud AI if available
        if (typeof window.getActiveGroqKey === 'function') {
            const groqKey = window.getActiveGroqKey();
            if (groqKey) {
                try {
                    const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${groqKey}`,
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            model: 'llama-3.3-70b-versatile',
                            response_format: { type: 'json_object' },
                            temperature: 0.2,
                            messages: [
                                {
                                    role: 'system',
                                    content: `Analyze this vendor ticket and return strictly JSON:
                                    {
                                      "category": "Authentication | Payments | Technical | Operations",
                                      "priority": "Low | Medium | High | Urgent",
                                      "sentiment": "Positive | Neutral | Frustrated",
                                      "summary": "ملخص المشكلة في 6 كلمات بالعربية",
                                      "recommended_action": "إجراء فوري مقترح"
                                    }`
                                },
                                { role: 'user', content: text }
                            ]
                        })
                    });
                    if (res.ok) {
                        const json = await res.json();
                        return JSON.parse(json.choices[0].message.content);
                    }
                } catch (e) {
                    console.warn('⚠️ Groq triage failed, falling back to local heuristics');
                }
            }
        }

        // 4. Reliable Local Heuristic Triage (Instant & Free)
        return runLocalHeuristicTriage(text);
    }

    // Render Triage HUD in Output panel
    function renderTriageHud(triage) {
        let hud = document.getElementById('aiTriageHud');
        if (!hud) {
            hud = document.createElement('div');
            hud.id = 'aiTriageHud';
            const outputCont = document.getElementById('outputContent');
            if (outputCont && outputCont.parentNode) {
                outputCont.parentNode.insertBefore(hud, outputCont);
            }
        }

        const priorityColors = {
            'Urgent': { bg: 'rgba(239, 68, 68, 0.2)', border: '#EF4444', text: '#FCA5A5', icon: 'fa-bolt' },
            'High': { bg: 'rgba(245, 158, 11, 0.2)', border: '#F59E0B', text: '#FCD34D', icon: 'fa-triangle-exclamation' },
            'Medium': { bg: 'rgba(59, 130, 246, 0.2)', border: '#3B82F6', text: '#93C5FD', icon: 'fa-circle-info' },
            'Low': { bg: 'rgba(16, 185, 129, 0.2)', border: '#10B981', text: '#6EE7B7', icon: 'fa-check' }
        };

        const sentimentBadges = {
            'Frustrated': { emoji: '😡', label: 'مستاء / متضايق', color: '#F87171' },
            'Neutral': { emoji: '😐', label: 'محايد', color: '#CBD5E1' },
            'Positive': { emoji: '😊', label: 'إيجابي / راضٍ', color: '#34D399' }
        };

        const pStyle = priorityColors[triage.priority] || priorityColors['Medium'];
        const sStyle = sentimentBadges[triage.sentiment] || sentimentBadges['Neutral'];

        hud.innerHTML = `
            <div style="background: rgba(15, 23, 42, 0.85); border: 1.5px solid rgba(139, 92, 246, 0.4); border-radius: 12px; padding: 12px 16px; margin-bottom: 12px; backdrop-filter: blur(12px); box-shadow: 0 8px 24px rgba(0,0,0,0.4); animation: fadeIn 0.25s ease;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 8px;">
                    <span style="font-weight: 800; font-size: 0.82rem; color: #DDD6FE; display: flex; align-items: center; gap: 6px;">
                        <i class="fa-solid fa-brain" style="color: #A855F7;"></i> تصنيف التذكرة الذكي (Smart Triage):
                    </span>
                    <button type="button" onclick="window.copyTriageMetadata()" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #CBD5E1; padding: 3px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 5px;">
                        <i class="fa-solid fa-clipboard-list"></i> نسخ بيانات التصنيف
                    </button>
                </div>

                <div style="display: flex; gap: 8px; flex-wrap: wrap; align-items: center; margin-bottom: 8px;">
                    <!-- Category -->
                    <span style="background: rgba(99, 102, 241, 0.2); border: 1px solid rgba(99, 102, 241, 0.4); color: #A5B4FC; padding: 3px 10px; border-radius: 12px; font-size: 0.76rem; font-weight: 800;">
                        📂 ${triage.category}
                    </span>

                    <!-- Priority -->
                    <span style="background: ${pStyle.bg}; border: 1px solid ${pStyle.border}; color: ${pStyle.text}; padding: 3px 10px; border-radius: 12px; font-size: 0.76rem; font-weight: 800;">
                        <i class="fa-solid ${pStyle.icon}"></i> أولوية: ${triage.priority}
                    </span>

                    <!-- Sentiment -->
                    <span style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.15); color: ${sStyle.color}; padding: 3px 10px; border-radius: 12px; font-size: 0.76rem; font-weight: 700;">
                        ${sStyle.emoji} نبرة الشريك: ${sStyle.label}
                    </span>
                </div>

                <div style="font-size: 0.8rem; color: #94A3B8; background: rgba(0,0,0,0.25); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.05);">
                    <strong style="color: #F8FAFC;">📝 ملخص المشكلة:</strong> ${triage.summary || 'تم الفرز والتصنيف بدقة'}
                </div>
            </div>
        `;
        hud.style.display = 'block';

        window.lastTriageMetadata = triage;
    }

    window.copyTriageMetadata = function () {
        if (!window.lastTriageMetadata) return;
        const t = window.lastTriageMetadata;
        const text = `--- AI TICKET TRIAGE ---
Category: ${t.category}
Priority: ${t.priority}
Sentiment: ${t.sentiment}
Summary: ${t.summary}
Recommended Action: ${t.recommended_action || 'N/A'}`;
        navigator.clipboard.writeText(text);
        if (typeof showToast === 'function') {
            showToast('تم نسخ بيانات تصنيف التذكرة للـ Internal Note! 📋');
        }
    };

    // Public API Hook into Generate Response
    window.performSmartTriageOnSubmit = async function (rawText) {
        if (!rawText || rawText.trim().length < 3) return;
        try {
            const triageData = await executeSmartTriage(rawText);
            renderTriageHud(triageData);
            return triageData;
        } catch (e) {
            console.error('Triage error:', e);
        }
    };

    // Initialize listeners when DOM is loaded
    function init() {
        loadKnowledgeBase();

        const inputEl = document.getElementById('partnerMessage');
        if (inputEl) {
            inputEl.addEventListener('input', handleRealtimeInput);
            console.log('✅ Real-time Debounced AI Advisor attached to #partnerMessage');
        }

        // Create the suggestion card slot if not present
        if (!document.getElementById('aiInstantSuggestionCard') && inputEl) {
            const card = document.createElement('div');
            card.id = 'aiInstantSuggestionCard';
            card.style.display = 'none';
            card.style.background = 'rgba(6, 78, 59, 0.45)';
            card.style.border = '1.5px solid #10B981';
            card.style.borderRadius = '12px';
            card.style.padding = '12px 16px';
            card.style.marginTop = '10px';
            card.style.marginBottom = '10px';
            card.style.backdropFilter = 'blur(10px)';
            card.style.boxShadow = '0 8px 24px rgba(16, 185, 129, 0.2)';
            card.style.animation = 'fadeIn 0.2s ease';

            const textareaWrapper = inputEl.closest('.textarea-wrapper') || inputEl.parentNode;
            if (textareaWrapper && textareaWrapper.nextSibling) {
                textareaWrapper.parentNode.insertBefore(card, textareaWrapper.nextSibling);
            } else if (textareaWrapper) {
                textareaWrapper.parentNode.appendChild(card);
            }
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expose
    window.aiSmartSupport = {
        loadKnowledgeBase,
        findBestFaqMatch,
        executeSmartTriage,
        renderTriageHud
    };

})(window);
