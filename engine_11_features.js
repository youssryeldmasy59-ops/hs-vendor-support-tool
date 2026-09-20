// =========================================================================
// 🚀 ULTIMATE 11-FEATURE ENGINE FOR HUNGERSTATION VENDOR SUPPORT SUITE
// =========================================================================

// ─────────────────────────────────────────────────────────────────────────
// FEATURE 1: PENDING TICKET VAULT & SLA FOLLOW-UP
// ─────────────────────────────────────────────────────────────────────────
let pendingTicketsVault = [];
try {
    pendingTicketsVault = JSON.parse(localStorage.getItem('hs_pending_tickets') || '[]');
} catch(e) { pendingTicketsVault = []; }

function openPendingVaultModal() {
    renderPendingTicketsList();
    const m = document.getElementById('pendingVaultModal');
    if (m) m.style.display = 'flex';
}

function closePendingVaultModal() {
    const m = document.getElementById('pendingVaultModal');
    if (m) m.style.display = 'none';
}

function addNewPendingTicketFromVault() {
    const idInput = document.getElementById('vaultTicketId');
    const vendorInput = document.getElementById('vaultVendorName');
    const catSelect = document.getElementById('vaultCategory');
    const slaSelect = document.getElementById('vaultSlaHours');

    const ticketId = idInput ? idInput.value.trim() : '';
    const vendorName = vendorInput ? vendorInput.value.trim() : 'متجر الشريك';
    const category = catSelect ? catSelect.value : 'أخرى';
    const slaHours = slaSelect ? parseInt(slaSelect.value, 10) : 24;

    if (!ticketId) {
        showToast('⚠️ يرجى كتابة رقم التذكرة أولاً');
        return;
    }

    const now = Date.now();
    const dueAt = now + (slaHours * 3600 * 1000);

    const newTicket = {
        id: 'TICK_' + now,
        ticketId: ticketId,
        vendorName: vendorName,
        category: category,
        slaHours: slaHours,
        createdAt: now,
        dueAt: dueAt,
        status: 'ACTIVE'
    };

    pendingTicketsVault.unshift(newTicket);
    localStorage.setItem('hs_pending_tickets', JSON.stringify(pendingTicketsVault));
    if (idInput) idInput.value = '';
    if (vendorInput) vendorInput.value = '';

    renderPendingTicketsList();
    updatePendingVaultBadge();
    showToast('تمت إضافة التذكرة لحافظة المتابعة بنجاح! ⏳');
}

function promptSaveCurrentTicketToVault() {
    const activeCcr = (typeof currentSelectedCase !== 'undefined' && currentSelectedCase) ? currentSelectedCase.title_arabic : 'تذكرة عامة';
    const tNum = prompt("أدخل رقم التذكرة (Zendesk Ticket ID) لحفظها في قائمة المعلقة:", "");
    if (!tNum) return;
    
    const now = Date.now();
    const dueAt = now + (24 * 3600 * 1000); // Default 24h

    const newTicket = {
        id: 'TICK_' + now,
        ticketId: tNum.trim(),
        vendorName: 'شريك هنقرستيشن',
        category: activeCcr,
        slaHours: 24,
        createdAt: now,
        dueAt: dueAt,
        status: 'ACTIVE'
    };

    pendingTicketsVault.unshift(newTicket);
    localStorage.setItem('hs_pending_tickets', JSON.stringify(pendingTicketsVault));
    updatePendingVaultBadge();
    showToast(`تم حفظ التذكرة #${tNum} في قائمة المعلقة لمتابعة الـ SLA ⏳`);
}

let currentVaultFilter = 'ALL';
function filterVaultTickets(type) {
    currentVaultFilter = type;
    ['ALL', 'ACTIVE', 'WARNING', 'OVERDUE'].forEach(t => {
        const btn = document.getElementById(`vaultTab_${t}`);
        if (btn) {
            if (t === type) btn.classList.add('active');
            else btn.classList.remove('active');
        }
    });
    renderPendingTicketsList();
}

function deletePendingTicket(id) {
    pendingTicketsVault = pendingTicketsVault.filter(t => t.id !== id);
    localStorage.setItem('hs_pending_tickets', JSON.stringify(pendingTicketsVault));
    renderPendingTicketsList();
    updatePendingVaultBadge();
    showToast('تم حذف التذكرة من الحافظة.');
}

function resolvePendingTicket(id) {
    const t = pendingTicketsVault.find(x => x.id === id);
    if (t) {
        if (typeof incrementDailyTicketCount === 'function') incrementDailyTicketCount();
        pendingTicketsVault = pendingTicketsVault.filter(x => x.id !== id);
        localStorage.setItem('hs_pending_tickets', JSON.stringify(pendingTicketsVault));
        renderPendingTicketsList();
        updatePendingVaultBadge();
        showToast(`تم إنجاز وإغلاق التذكرة #${t.ticketId} بنجاح! كفووو 🔥`);
    }
}

function openTicketInWorkspace(ticketId, category) {
    closePendingVaultModal();
    const q = document.getElementById('partnerMessage') || document.getElementById('queryInput');
    if (q) {
        q.value = `متابعة التذكرة #${ticketId} بخصوص ${category}`;
        if (typeof generateResponse === 'function') generateResponse();
    }
}

function renderPendingTicketsList() {
    const list = document.getElementById('pendingTicketsList');
    if (!list) return;

    const now = Date.now();
    let cAll = pendingTicketsVault.length;
    let cActive = 0, cWarn = 0, cOver = 0;

    pendingTicketsVault.forEach(t => {
        const remainingMs = t.dueAt - now;
        if (remainingMs <= 0) cOver++;
        else if (remainingMs <= 12 * 3600 * 1000) cWarn++;
        else cActive++;
    });

    const bAll = document.getElementById('vaultCountAll');
    const bActive = document.getElementById('vaultCountActive');
    const bWarn = document.getElementById('vaultCountWarning');
    const bOver = document.getElementById('vaultCountOverdue');
    if (bAll) bAll.innerText = cAll;
    if (bActive) bActive.innerText = cActive;
    if (bWarn) bWarn.innerText = cWarn;
    if (bOver) bOver.innerText = cOver;

    const filtered = pendingTicketsVault.filter(t => {
        const remainingMs = t.dueAt - now;
        if (currentVaultFilter === 'ACTIVE') return remainingMs > 12 * 3600 * 1000;
        if (currentVaultFilter === 'WARNING') return remainingMs > 0 && remainingMs <= 12 * 3600 * 1000;
        if (currentVaultFilter === 'OVERDUE') return remainingMs <= 0;
        return true;
    });

    if (filtered.length === 0) {
        list.innerHTML = `<div style="text-align: center; color: var(--text-muted); padding: 30px; font-size: 0.85rem;">لا توجد تذاكر معلقة في هذا القسم.</div>`;
        return;
    }

    let html = '';
    filtered.forEach(t => {
        const remainingMs = t.dueAt - now;
        let statusBadge = '';
        let countdownStr = '';

        if (remainingMs <= 0) {
            const overHours = Math.abs(Math.floor(remainingMs / (3600 * 1000)));
            const overMins = Math.abs(Math.floor((remainingMs % (3600 * 1000)) / (60 * 1000)));
            statusBadge = `<span style="background: rgba(239, 68, 68, 0.2); color: #EF4444; border: 1px solid rgba(239,68,68,0.4); padding: 2px 8px; border-radius: 6px; font-size: 0.72rem; font-weight: 800;">🚨 متأخرة عن SLA</span>`;
            countdownStr = `<span style="color: #EF4444; font-weight: 800; font-family: monospace;">متأخرة بـ ${overHours}h ${overMins}m</span>`;
        } else if (remainingMs <= 12 * 3600 * 1000) {
            const remHours = Math.floor(remainingMs / (3600 * 1000));
            const remMins = Math.floor((remainingMs % (3600 * 1000)) / (60 * 1000));
            statusBadge = `<span style="background: rgba(245, 158, 11, 0.2); color: #F59E0B; border: 1px solid rgba(245,158,11,0.4); padding: 2px 8px; border-radius: 6px; font-size: 0.72rem; font-weight: 800;">⚠️ قرب انتهاء SLA</span>`;
            countdownStr = `<span style="color: #F59E0B; font-weight: 800; font-family: monospace;">باقي: ${remHours}h ${remMins}m</span>`;
        } else {
            const remHours = Math.floor(remainingMs / (3600 * 1000));
            const remMins = Math.floor((remainingMs % (3600 * 1000)) / (60 * 1000));
            statusBadge = `<span style="background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16,185,129,0.3); padding: 2px 8px; border-radius: 6px; font-size: 0.72rem; font-weight: 800;">🟢 نشطة ضمن SLA</span>`;
            countdownStr = `<span style="color: #10B981; font-weight: 800; font-family: monospace;">باقي: ${remHours}h ${remMins}m</span>`;
        }

        html += `
            <div class="pending-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <strong style="color: var(--primary); font-size: 0.92rem;">#${t.ticketId}</strong>
                        <span style="font-size: 0.8rem; color: #FFF;">${t.vendorName}</span>
                        <span style="font-size: 0.72rem; background: rgba(255,255,255,0.06); padding: 2px 6px; border-radius: 4px; color: var(--text-muted);">${t.category}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        ${countdownStr}
                        ${statusBadge}
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 6px;">
                    <span style="font-size: 0.7rem; color: var(--text-muted);">مدة الـ SLA الإجمالية: ${t.slaHours} ساعة</span>
                    <div style="display: flex; gap: 6px;">
                        <button type="button" onclick="openTicketInWorkspace('${t.ticketId}', '${t.category}')" style="background: rgba(59, 130, 246, 0.15); color: #60A5FA; border: 1px solid rgba(59,130,246,0.3); padding: 4px 10px; border-radius: 6px; font-size: 0.74rem; cursor: pointer;">
                            <i class="fa-solid fa-comment-dots"></i> فتح في الأداة
                        </button>
                        <button type="button" onclick="resolvePendingTicket('${t.id}')" style="background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16,185,129,0.3); padding: 4px 10px; border-radius: 6px; font-size: 0.74rem; font-weight: 700; cursor: pointer;">
                            <i class="fa-solid fa-check"></i> إنجاز وإغلاق
                        </button>
                        <button type="button" onclick="deletePendingTicket('${t.id}')" style="background: rgba(239, 68, 68, 0.12); color: #EF4444; border: 1px solid rgba(239,68,68,0.3); padding: 4px 8px; border-radius: 6px; font-size: 0.74rem; cursor: pointer;">
                            <i class="fa-solid fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    });

    list.innerHTML = html;
}

function updatePendingVaultBadge() {
    const b = document.getElementById('pendingVaultHeaderBadge');
    if (b) {
        b.innerText = `معلقة (${pendingTicketsVault.length})`;
        if (pendingTicketsVault.length > 0 && b.parentElement) {
            b.parentElement.style.borderColor = 'rgba(245, 158, 11, 0.6)';
        }
    }
}

setInterval(() => {
    const m = document.getElementById('pendingVaultModal');
    if (m && m.style.display === 'flex') {
        renderPendingTicketsList();
    }
}, 30000);


// ─────────────────────────────────────────────────────────────────────────
// FEATURE 2: MENU PRE-FLIGHT SANITY CHECKER (PREVENTS ERROR 422)
// ─────────────────────────────────────────────────────────────────────────
let currentSanityIssues = [];

function openMenuSanityModal() {
    const m = document.getElementById('menuSanityModal');
    if (m) m.style.display = 'flex';
}

function closeMenuSanityModal() {
    const m = document.getElementById('menuSanityModal');
    if (m) m.style.display = 'none';
}

function runMenuPreflightSanityCheck() {
    const data = window.menuBuilderData || { groups: [], items: [], modifiers: [] };
    const items = data.items || [];
    const groups = data.groups || [];
    currentSanityIssues = [];

    if (items.length === 0 && groups.length === 0) {
        showToast('⚠️ لا توجد أصناف في الاستوديو بعد! الصق بيانات المنيو أولاً.');
        return;
    }

    // Check 1: Duplicate Item Names
    const seenNames = new Map();
    items.forEach((it, idx) => {
        const ar = (it.name_ar || '').trim().toLowerCase();
        const en = (it.name_en || '').trim().toLowerCase();
        if (ar) {
            if (seenNames.has(ar)) {
                currentSanityIssues.push({
                    type: 'ERROR',
                    itemIndex: idx,
                    field: 'name_ar',
                    title: `صنف مكرر بالاسم العربي: "${it.name_ar}"`,
                    desc: `تكرار الاسم يسبب رفض السيستم Error 422 لعدم التفريق بين الأصناف.`,
                    fix: 'إضافة تمييز أو رقم للصنف المكرر'
                });
            } else seenNames.set(ar, idx);
        }
        if (en) {
            if (seenNames.has(en)) {
                currentSanityIssues.push({
                    type: 'ERROR',
                    itemIndex: idx,
                    field: 'name_en',
                    title: `Duplicate English Name: "${it.name_en}"`,
                    desc: `System Error 422: duplicate item identity within store catalog.`,
                    fix: 'Append variation or size'
                });
            } else seenNames.set(en, idx);
        }
    });

    // Check 2: Anomalous Prices (0, negative, or NaN)
    items.forEach((it, idx) => {
        const p = parseFloat(it.price);
        if (isNaN(p) || p <= 0) {
            currentSanityIssues.push({
                type: 'ERROR',
                itemIndex: idx,
                field: 'price',
                title: `سعر غير صالح أو 0 للصنف: "${it.name_ar || it.name_en}"`,
                desc: `السعر مسجل كـ (${it.price}). بوابة العمليات ترفض رفع أي صنف بسعر 0.`,
                fix: 'تعيين سعر افتراضي أو تصحيحه'
            });
        } else if (p > 2000) {
            currentSanityIssues.push({
                type: 'WARNING',
                itemIndex: idx,
                field: 'price',
                title: `سعر مرتفع جداً (${p} ريال) للصنف: "${it.name_ar || it.name_en}"`,
                desc: `يرجى مراجعة الصنف للتأكد من عدم وجود صفر إضافي خطأ.`,
                fix: 'تأكيد السعر'
            });
        }
    });

    // Check 3: Fractional or Decimal Calories (Hungerstation expects integers)
    items.forEach((it, idx) => {
        const cal = String(it.calories || '').trim();
        if (cal && cal !== '0' && cal.includes('.')) {
            currentSanityIssues.push({
                type: 'WARNING',
                itemIndex: idx,
                field: 'calories',
                title: `سعرات حرارية بكسور عشرية: (${cal}) للصنف "${it.name_ar || it.name_en}"`,
                desc: `بوابة العمليات تفضل أرقاماً صحيحة للسعرات لتفادي أخطاء التقريب.`,
                fix: 'تقريب السعرات لأقرب رقم صحيح'
            });
        }
    });

    // Check 4: Empty Categories
    groups.forEach((g) => {
        const gItems = items.filter(it => it.group_id == g.id || it.group_name_ar == g.name_ar);
        if (gItems.length === 0) {
            currentSanityIssues.push({
                type: 'WARNING',
                itemIndex: -1,
                field: 'group',
                title: `قسم فارغ بدون أصناف: "${g.name_ar || g.name_en}"`,
                desc: `القسم لا يحتوي على أي صنف. سيظهر فارغاً للعملاء في التطبيق.`,
                fix: 'إزالة القسم الفارغ أو إضافة أصناف داخله'
            });
        }
    });

    renderMenuSanityReport(items.length, groups.length);
    openMenuSanityModal();
}

function renderMenuSanityReport(itemCount, groupCount) {
    const banner = document.getElementById('sanityStatusBanner');
    const list = document.getElementById('sanityIssuesList');
    const fixBtn = document.getElementById('sanityAutoFixBtn');

    const errorsCount = currentSanityIssues.filter(x => x.type === 'ERROR').length;
    const warningsCount = currentSanityIssues.filter(x => x.type === 'WARNING').length;

    if (errorsCount === 0 && warningsCount === 0) {
        if (banner) {
            banner.style.background = 'rgba(16, 185, 129, 0.15)';
            banner.style.border = '1px solid rgba(16, 185, 129, 0.4)';
            banner.innerHTML = `
                <div style="display: flex; align-items: center; gap: 10px;">
                    <i class="fa-solid fa-circle-check" style="color: #10B981; font-size: 1.6rem;"></i>
                    <div>
                        <strong style="color: #10B981; font-size: 0.95rem;">شيت المنيو سليم 100% وجاهز للرفع الفوري!</strong>
                        <div style="font-size: 0.78rem; color: #CBD5E1;">تم فحص ${itemCount} صنف في ${groupCount} قسم، ولا توجد أي أخطاء تسبب Error 422.</div>
                    </div>
                </div>
            `;
        }
        if (list) list.innerHTML = `<div style="text-align: center; color: #10B981; padding: 25px; font-weight: 700;">✅ الفحص ناجح تماماً! يمكنك تنزيل ملف الإكسيل الرسمي الآن بثقة 100%.</div>`;
        if (fixBtn) fixBtn.style.display = 'none';
        return;
    }

    if (fixBtn) fixBtn.style.display = 'inline-flex';
    if (banner) {
        banner.style.background = errorsCount > 0 ? 'rgba(239, 68, 68, 0.15)' : 'rgba(245, 158, 11, 0.15)';
        banner.style.border = errorsCount > 0 ? '1px solid rgba(239, 68, 68, 0.4)' : '1px solid rgba(245, 158, 11, 0.4)';
        banner.innerHTML = `
            <div style="display: flex; align-items: center; gap: 10px;">
                <i class="fa-solid fa-triangle-exclamation" style="color: ${errorsCount > 0 ? '#EF4444' : '#F59E0B'}; font-size: 1.6rem;"></i>
                <div>
                    <strong style="color: ${errorsCount > 0 ? '#EF4444' : '#F59E0B'}; font-size: 0.95rem;">
                        تم كشف ${errorsCount} خطأ جسيم و ${warningsCount} تنبيه قبل الرفع
                    </strong>
                    <div style="font-size: 0.78rem; color: #CBD5E1;">اضغط على "تصحيح الأخطاء تلقائياً" لإصلاح الأسعار والكسور فوراً.</div>
                </div>
            </div>
        `;
    }

    let html = '';
    currentSanityIssues.forEach(iss => {
        const isErr = iss.type === 'ERROR';
        html += `
            <div style="background: ${isErr ? 'rgba(239,68,68,0.08)' : 'rgba(245,158,11,0.08)'}; border: 1px solid ${isErr ? 'rgba(239,68,68,0.3)' : 'rgba(245,158,11,0.3)'}; border-radius: 8px; padding: 10px 14px; display: flex; justify-content: space-between; align-items: center; gap: 10px;">
                <div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="background: ${isErr ? '#EF4444' : '#F59E0B'}; color: #000; padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 800;">${isErr ? 'خطأ جسيم' : 'تنبيه'}</span>
                        <strong style="color: #FFF; font-size: 0.85rem;">${iss.title}</strong>
                    </div>
                    <div style="font-size: 0.74rem; color: #94A3B8; margin-top: 3px;">${iss.desc}</div>
                </div>
                <span style="font-size: 0.72rem; color: #38BDF8; font-weight: 700; white-space: nowrap;">🛠️ الحل: ${iss.fix}</span>
            </div>
        `;
    });
    if (list) list.innerHTML = html;
}

function autoFixMenuSanityIssues() {
    const data = window.menuBuilderData || { groups: [], items: [], modifiers: [] };
    let items = data.items || [];

    // Fix Duplicate names by appending (2), (3)
    const nameCount = {};
    items.forEach(it => {
        const ar = (it.name_ar || '').trim();
        if (ar) {
            if (nameCount[ar]) {
                nameCount[ar]++;
                it.name_ar = `${ar} (${nameCount[ar]})`;
            } else nameCount[ar] = 1;
        }
    });

    // Fix 0 prices to minimum 1.00
    items.forEach(it => {
        let p = parseFloat(it.price);
        if (isNaN(p) || p <= 0) {
            it.price = 1.00;
        }
    });

    // Fix fractional calories
    items.forEach(it => {
        if (it.calories) {
            const num = parseFloat(it.calories);
            if (!isNaN(num)) it.calories = Math.round(num);
        }
    });

    // Re-render studio preview tables
    if (typeof window.renderStudioMenuPreviewTables === 'function') {
        window.renderStudioMenuPreviewTables();
    }

    runMenuPreflightSanityCheck();
    updateMobileMockup();
    showToast('تم تصحيح جميع أخطاء شيت المنيو تلقائياً بنجاح! 🛠️✨');
}


// ─────────────────────────────────────────────────────────────────────────
// FEATURE 3: AGENT QUICK-SNIPPETS BAR
// ─────────────────────────────────────────────────────────────────────────
const DEFAULT_SNIPPETS = [
    { id: 's1', title: '🔗 بوابة الشركاء', text: 'رابط بوابة الشركاء الرسمية: https://partners.hungerstation.com' },
    { id: 's2', title: '🕒 أوقات المالية', text: '(أوقات عمل قسم الحسابات: من الأحد إلى الخميس من 9:00 ص حتى 5:00 م)' },
    { id: 's3', title: '🏦 إيميل المطالبات', text: 'finance@hungerstation.com' },
    { id: 's4', title: '📞 هاتف الدعم', text: 'الرقم الموحد لدعم شركاء هنقرستيشن: 920022200' },
    { id: 's5', title: '⚡ تحويل للعمليات', text: '[تم تحويل الطلب لفريق العمليات التشغيلية لمتابعة حالة الفرع]' }
];

let userSnippets = [];
try {
    userSnippets = JSON.parse(localStorage.getItem('hs_user_snippets') || '[]');
} catch(e) { userSnippets = []; }

function renderQuickSnippetsBar() {
    const cont = document.getElementById('quickSnippetsContainer');
    if (!cont) return;

    const all = [...DEFAULT_SNIPPETS, ...userSnippets];
    let html = '';
    all.forEach(s => {
        const escaped = encodeURIComponent(s.text);
        html += `
            <div class="snippet-pill" onclick="insertSnippetTextDecoded('${escaped}')" title="إدراج في نص الرد">
                ${s.title}
            </div>
        `;
    });
    cont.innerHTML = html;
}

function insertSnippetTextDecoded(enc) {
    const txt = decodeURIComponent(enc);
    const arBox = document.getElementById('arMacroText');
    if (!arBox) {
        showToast('⚠️ يرجى توليد ماكرو أولاً لإدراج القصاصة داخله.');
        return;
    }

    arBox.innerText = arBox.innerText.trim() + '\n\n' + txt;
    if (typeof checkLegalBlacklist === 'function') checkLegalBlacklist();
    showToast('تم إدراج القصاصة بنجاح! ⚡');
}

function openAddSnippetModal() {
    const m = document.getElementById('addSnippetModal');
    if (m) m.style.display = 'flex';
}

function closeAddSnippetModal() {
    const m = document.getElementById('addSnippetModal');
    if (m) m.style.display = 'none';
}

function saveNewCustomSnippet() {
    const tInput = document.getElementById('newSnippetTitle');
    const txtInput = document.getElementById('newSnippetText');
    const title = tInput ? tInput.value.trim() : '';
    const text = txtInput ? txtInput.value.trim() : '';

    if (!title || !text) {
        showToast('⚠️ يرجى كتابة عنوان القصاصة والنص.');
        return;
    }

    userSnippets.push({ id: 'custom_' + Date.now(), title: title, text: text });
    localStorage.setItem('hs_user_snippets', JSON.stringify(userSnippets));
    if (tInput) tInput.value = '';
    if (txtInput) txtInput.value = '';

    closeAddSnippetModal();
    renderQuickSnippetsBar();
    showToast('تم حفظ القصاصة المخصصة الجديدة! 🎉');
}


// ─────────────────────────────────────────────────────────────────────────
// FEATURE 4: POWER-USER GLOBAL HOTKEYS
// ─────────────────────────────────────────────────────────────────────────
function openHotkeysModal() {
    const m = document.getElementById('hotkeysModal');
    if (m) m.style.display = 'flex';
}

function closeHotkeysModal() {
    const m = document.getElementById('hotkeysModal');
    if (m) m.style.display = 'none';
}

window.addEventListener('keydown', (e) => {
    const isMac = (navigator.platform || '').toUpperCase().indexOf('MAC') >= 0;
    const cmdKey = isMac ? e.metaKey : e.ctrlKey;

    // Cmd + K -> Quick Search
    if (cmdKey && (e.key === 'k' || e.key === 'K')) {
        e.preventDefault();
        const hudInput = document.getElementById('hudSearchInput');
        const searchInput = document.getElementById('searchInput');
        if (document.getElementById('floatingGlassHud')?.style.display !== 'none' && hudInput) {
            hudInput.focus();
        } else if (searchInput) {
            searchInput.focus();
            searchInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        showToast('🔍 تم تفعيل البحث السريع');
    }

    // Cmd + Shift + C -> Instant Copy Macro
    if (cmdKey && e.shiftKey && (e.key === 'c' || e.key === 'C')) {
        e.preventDefault();
        const arBox = document.getElementById('arMacroText');
        if (arBox && arBox.innerText.trim()) {
            copyText('arMacroText');
        } else {
            showToast('⚠️ لا يوجد ماكرو جاهز للنسخ بعد');
        }
    }

    // Cmd + Shift + T -> Cycle Tone
    if (cmdKey && e.shiftKey && (e.key === 't' || e.key === 'T')) {
        e.preventDefault();
        cycleToneHotkeys();
    }

    // Cmd + Shift + M -> Toggle Workspace (Tickets <-> Menu)
    if (cmdKey && e.shiftKey && (e.key === 'm' || e.key === 'M')) {
        e.preventDefault();
        const menuWs = document.getElementById('menuStudioWorkspace');
        const isMenu = menuWs && menuWs.style.display !== 'none';
        if (typeof switchMainWorkspace === 'function') {
            switchMainWorkspace(isMenu ? 'TICKETS' : 'MENU_STUDIO');
        }
    }

    // Cmd + Shift + V -> Open Pending Ticket Vault
    if (cmdKey && e.shiftKey && (e.key === 'v' || e.key === 'V')) {
        e.preventDefault();
        openPendingVaultModal();
    }

    // Cmd + / -> Open Hotkeys Modal
    if (cmdKey && e.key === '/') {
        e.preventDefault();
        openHotkeysModal();
    }
});

let currentToneIndex = 0;
const TONES_LIST = ['DE_ESCALATE', 'FIRM_POLICY', 'QUICK_CHAT', 'ORIGINAL'];
function cycleToneHotkeys() {
    currentToneIndex = (currentToneIndex + 1) % TONES_LIST.length;
    const tone = TONES_LIST[currentToneIndex];
    if (typeof applyMacroTone === 'function') {
        applyMacroTone(tone);
    }
}


// ─────────────────────────────────────────────────────────────────────────
// FEATURE 5 & 11: DAILY SHIFT STATS, AHT & GAMIFIED SPEEDRUN (NO SOUND FX)
// ─────────────────────────────────────────────────────────────────────────
let currentTicketStartTime = Date.now();
let liveTicketTimerInterval = null;

function startLiveTicketTimer() {
    currentTicketStartTime = Date.now();
    if (liveTicketTimerInterval) clearInterval(liveTicketTimerInterval);
    liveTicketTimerInterval = setInterval(() => {
        const el = document.getElementById('ticketLiveTimerVal');
        if (el) {
            const diffSec = Math.floor((Date.now() - currentTicketStartTime) / 1000);
            const mm = String(Math.floor(diffSec / 60)).padStart(2, '0');
            const ss = String(diffSec % 60).padStart(2, '0');
            el.innerText = `${mm}:${ss}`;
        }
    }, 1000);
}
startLiveTicketTimer();

function recordTicketResolutionTime(caseTitle) {
    const diffSec = Math.max(5, Math.floor((Date.now() - currentTicketStartTime) / 1000));
    const today = new Date().toISOString().split('T')[0];
    
    // Update AHT data in localStorage
    const ahtKey = `hs_aht_data_${today}`;
    let ahtData = { totalSecs: 0, count: 0 };
    try { ahtData = JSON.parse(localStorage.getItem(ahtKey) || '{"totalSecs":0,"count":0}'); } catch(e){}
    ahtData.totalSecs += diffSec;
    ahtData.count += 1;
    localStorage.setItem(ahtKey, JSON.stringify(ahtData));

    // Update Top Inquiries Category
    const inqKey = `hs_inquiries_${today}`;
    let inqData = {};
    try { inqData = JSON.parse(localStorage.getItem(inqKey) || '{}'); } catch(e){}
    const cat = categorizeCaseForStats(caseTitle);
    inqData[cat] = (inqData[cat] || 0) + 1;
    localStorage.setItem(inqKey, JSON.stringify(inqData));

    // Restart timer for next ticket
    startLiveTicketTimer();
    updateShiftSpeedrunStats();
}

function categorizeCaseForStats(title) {
    if (!title) return 'أخرى';
    if (title.includes('تعويض') || title.includes('إلغاء')) return 'تعويضات';
    if (title.includes('فاتورة') || title.includes('مبيعات') || title.includes('حوالة')) return 'فواتير ومبيعات';
    if (title.includes('جهاز') || title.includes('تابلت') || title.includes('طابعة')) return 'أجهزة وتابلت';
    if (title.includes('آيبان') || title.includes('سجل') || title.includes('بيانات')) return 'تحديث بيانات';
    if (title.includes('منيو') || title.includes('أصناف')) return 'منيو وأسعار';
    return 'أخرى';
}

function updateShiftSpeedrunStats() {
    const today = new Date().toISOString().split('T')[0];
    const count = typeof getDailyTicketCount === 'function' ? getDailyTicketCount() : 0;

    // 1. AHT
    const ahtKey = `hs_aht_data_${today}`;
    let ahtData = { totalSecs: 0, count: 0 };
    try { ahtData = JSON.parse(localStorage.getItem(ahtKey) || '{"totalSecs":0,"count":0}'); } catch(e){}
    const avgSec = ahtData.count > 0 ? Math.round(ahtData.totalSecs / ahtData.count) : 0;
    const ahtEl = document.getElementById('heroAhtVal');
    if (ahtEl) ahtEl.innerText = avgSec;

    // 2. Streak
    const streakEl = document.getElementById('heroStreakVal');
    if (streakEl) streakEl.innerText = count;

    // 3. Top Inquiries
    const inqKey = `hs_inquiries_${today}`;
    let inqData = {};
    try { inqData = JSON.parse(localStorage.getItem(inqKey) || '{}'); } catch(e){}
    const entries = Object.entries(inqData).sort((a,b) => b[1] - a[1]);
    const topEl = document.getElementById('heroTopInquiriesText');
    if (topEl) {
        if (entries.length === 0) {
            topEl.innerText = 'جاري الرصد مع كل تذكرة...';
        } else {
            const total = entries.reduce((acc, curr) => acc + curr[1], 0);
            const str = entries.slice(0, 3).map(([k, v]) => `${Math.round((v/total)*100)}% ${k}`).join(' • ');
            topEl.innerText = str;
        }
    }

    // 4. Dynamic Gamified Ranks (Strictly visual, NO audio)
    const rankEl = document.getElementById('heroAgentRank');
    const avatarEl = document.getElementById('heroAvatarIcon');
    if (rankEl) {
        let rank = "🌱 مبتدئ الشفت (Shift Starter)";
        let avatar = "🌱";
        if (count >= 35) {
            rank = "👑 أسطورة الماكرو (Macro Legend)";
            avatar = "👑";
        } else if (count >= 20) {
            rank = "🥷 خبير الدعم (Support Ninja)";
            avatar = "🥷";
        } else if (count >= 8) {
            rank = "⚡ سريع الاستجابة (Speedy Solver)";
            avatar = "⚡";
        }
        rankEl.innerText = rank;
        if (avatarEl) avatarEl.innerText = avatar;
    }
}

function resetDailyShiftPrompt() {
    if (confirm("هل تريد تصفير إحصائيات وبدء شفت عمل جديد؟")) {
        const today = new Date().toISOString().split('T')[0];
        localStorage.setItem('hs_streak_count', '0');
        localStorage.removeItem(`hs_aht_data_${today}`);
        localStorage.removeItem(`hs_inquiries_${today}`);
        if (typeof updateHeroStats === 'function') updateHeroStats(true);
        updateShiftSpeedrunStats();
        showToast("تم تصفير الشفت بنجاح! شفت مبارك وموفق يا بطل 🚀");
    }
}


// ─────────────────────────────────────────────────────────────────────────
// FEATURE 6: PWA / OFFLINE DESKTOP APP SUPPORT
// ─────────────────────────────────────────────────────────────────────────
let deferredPwaPrompt = null;
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPwaPrompt = e;
    const btn = document.getElementById('pwaInstallBtn');
    if (btn) btn.style.display = 'inline-flex';
});

if (typeof navigator !== 'undefined' && 'serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js')
            .then(() => console.log('✓ Service Worker Registered successfully.'))
            .catch(err => console.log('SW registration error:', err));
    });
}

function installDesktopPwa() {
    if (deferredPwaPrompt) {
        deferredPwaPrompt.prompt();
        deferredPwaPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                showToast('تم تثبيت الأداة كتطبيق مكتبي بنجاح! 🎉');
            }
            deferredPwaPrompt = null;
        });
    } else {
        const m = document.getElementById('pwaInstallModal');
        if (m) m.style.display = 'flex';
    }
}

function closePwaInstallModal() {
    const m = document.getElementById('pwaInstallModal');
    if (m) m.style.display = 'none';
}

function triggerPwaPromptDirect() {
    if (deferredPwaPrompt) {
        deferredPwaPrompt.prompt();
    } else {
        showToast('اضغط على رمز التثبيت بجانب شريط العنوان أو File ➔ Add to Dock');
    }
}


// ─────────────────────────────────────────────────────────────────────────
// FEATURE 7: ZERO-CLICK CLIPBOARD AUTO-SOLVER
// ─────────────────────────────────────────────────────────────────────────
let isZeroClickSolverEnabled = localStorage.getItem('hs_zero_click_solver') === 'true';
let lastProcessedClipboardText = '';

function toggleZeroClickSolver() {
    isZeroClickSolverEnabled = !isZeroClickSolverEnabled;
    localStorage.setItem('hs_zero_click_solver', String(isZeroClickSolverEnabled));
    updateZeroClickUI();
    if (isZeroClickSolverEnabled) {
        showToast('⚡ تم تفعيل الحل التلقائي بنقرة صفر! انسخ أي شكوى من Zendesk وارجع للأداة.');
    } else {
        showToast('تم تعطيل الحل التلقائي.');
    }
}

function updateZeroClickUI() {
    const btn = document.getElementById('zeroClickToggleBtn');
    const txt = document.getElementById('zeroClickBadgeText');
    if (btn && txt) {
        if (isZeroClickSolverEnabled) {
            btn.style.background = 'linear-gradient(135deg, #10B981, #059669)';
            btn.style.color = '#FFF';
            btn.style.borderColor = '#10B981';
            txt.innerText = '⚡ حل تلقائي (نشط)';
        } else {
            btn.style.background = 'rgba(16, 185, 129, 0.12)';
            btn.style.color = '#10B981';
            btn.style.borderColor = 'rgba(16, 185, 129, 0.35)';
            txt.innerText = '⚡ حل تلقائي (معطّل)';
        }
    }
}

window.addEventListener('focus', async () => {
    if (!isZeroClickSolverEnabled) return;
    if (!navigator.clipboard || !navigator.clipboard.readText) return;

    try {
        const clipText = (await navigator.clipboard.readText()).trim();
        if (clipText && clipText.length >= 10 && clipText !== lastProcessedClipboardText) {
            if (!clipText.includes('فريق دعم الشركاء') && !clipText.includes('Hungerstation Vendor Support')) {
                lastProcessedClipboardText = clipText;
                const q = document.getElementById('partnerMessage') || document.getElementById('queryInput');
                if (q) {
                    q.value = clipText;
                    if (typeof generateResponse === 'function') generateResponse();
                    
                    setTimeout(async () => {
                        const arBox = document.getElementById('arMacroText');
                        if (arBox && arBox.innerText.trim()) {
                            await navigator.clipboard.writeText(arBox.innerText.trim());
                            showToast('⚡ [Zero-Click Solver] تم اكتشاف الشكوى وتجهيز الماكرو المعتمد ونسخه في حافظتك فوراً! جاهز للصق في Zendesk 🚀');
                        }
                    }, 400);
                }
            }
        }
    } catch(e) {
        // Clipboard read permission ignored
    }
});


// ─────────────────────────────────────────────────────────────────────────
// FEATURE 8: LIVE MOBILE APP MOCKUP (HUNGERSTATION CUSTOMER VIEW)
// ─────────────────────────────────────────────────────────────────────────
function toggleMobileAppMockup() {
    const wrapper = document.getElementById('studioMobileMockupWrapper');
    if (!wrapper) return;
    if (wrapper.style.display === 'none') {
        wrapper.style.display = 'block';
        updateMobileMockup();
        wrapper.scrollIntoView({ behavior: 'smooth', block: 'start' });
        showToast('📱 تم فتح محاكي تطبيق هنقرستيشن لايف!');
    } else {
        wrapper.style.display = 'none';
    }
}

function updateMobileMockup() {
    const data = window.menuBuilderData || { groups: [], items: [], modifiers: [] };
    const groups = data.groups || [];
    const items = data.items || [];

    // Categories pills
    const catPills = document.getElementById('mockupCategoryPills');
    if (catPills) {
        if (groups.length === 0) {
            catPills.innerHTML = '<div style="background: #FFC400; color: #000; font-weight: 800; font-size: 0.72rem; padding: 4px 10px; border-radius: 12px;">الأكثر طلباً</div>';
        } else {
            catPills.innerHTML = groups.map((g, i) => `
                <div style="background: ${i === 0 ? '#FFC400' : 'rgba(255,255,255,0.08)'}; color: ${i === 0 ? '#000' : '#CBD5E1'}; font-weight: 800; font-size: 0.72rem; padding: 4px 10px; border-radius: 12px; white-space: nowrap;">
                    ${g.name_ar || g.name_en}
                </div>
            `).join('');
        }
    }

    // Items list
    const list = document.getElementById('mockupItemsList');
    if (list) {
        if (items.length === 0) {
            list.innerHTML = '<div style="text-align: center; color: #64748B; padding: 25px; font-size: 0.78rem;">الصق بيانات المنيو لتظهر الأصناف في المحاكي لايف.</div>';
            return;
        }

        list.innerHTML = items.slice(0, 15).map(it => `
            <div class="mobile-item-card">
                <div style="flex: 1;">
                    <div style="font-weight: 800; font-size: 0.8rem; color: #FFF;">${it.name_ar || it.name_en}</div>
                    ${it.name_en && it.name_ar ? `<div style="font-size: 0.68rem; color: #94A3B8;">${it.name_en}</div>` : ''}
                    <div style="font-size: 0.68rem; color: #64748B; margin: 2px 0;">${it.description_ar || it.description_en || 'وجبة طازجة محضرة بأعلى جودة'}</div>
                    <div style="display: flex; align-items: center; gap: 8px; margin-top: 4px;">
                        <span style="font-weight: 800; color: #FFC400; font-size: 0.82rem;">${parseFloat(it.price || 0).toFixed(2)} ر.س</span>
                        ${it.calories ? `<span style="font-size: 0.64rem; color: #F87171;"><i class="fa-solid fa-fire"></i> ${it.calories} kcal</span>` : ''}
                    </div>
                </div>
                <div style="width: 44px; height: 44px; border-radius: 8px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center; justify-content: center; position: relative;">
                    <i class="fa-solid fa-burger" style="color: #FFC400; font-size: 1.2rem;"></i>
                    <div style="position: absolute; bottom: -4px; left: -4px; width: 18px; height: 18px; border-radius: 50%; background: #FFC400; color: #000; display: flex; align-items: center; justify-content: center; font-size: 0.65rem; font-weight: 900;">+</div>
                </div>
            </div>
        `).join('');
    }
}

// Hook updateMobileMockup inside renderStudioMenuPreviewTables
const originalRenderStudioTables = window.renderStudioMenuPreviewTables;
window.renderStudioMenuPreviewTables = function() {
    if (typeof originalRenderStudioTables === 'function') {
        originalRenderStudioTables();
    }
    updateMobileMockup();
};


// ─────────────────────────────────────────────────────────────────────────
// FEATURE 9: VENDOR INVOICE & DEDUCTION DIFF EXPLAINER
// ─────────────────────────────────────────────────────────────────────────
function openInvoiceExplainerModal() {
    calculateInvoiceDiff();
    const m = document.getElementById('invoiceExplainerModal');
    if (m) m.style.display = 'flex';
}

function closeInvoiceExplainerModal() {
    const m = document.getElementById('invoiceExplainerModal');
    if (m) m.style.display = 'none';
}

let lastCalculatedInvoice = {};

function calculateInvoiceDiff() {
    const gross = parseFloat(document.getElementById('invGrossSales')?.value || 0);
    const commPct = parseFloat(document.getElementById('invCommissionPct')?.value || 15);
    const deviceFee = parseFloat(document.getElementById('invDeviceFee')?.value || 0);
    const extraFee = parseFloat(document.getElementById('invExtraFees')?.value || 0);

    const commissionAmount = gross * (commPct / 100);
    const vatOnServices = (commissionAmount + deviceFee + extraFee) * 0.15;
    const totalDeductions = commissionAmount + vatOnServices + deviceFee + extraFee;
    const netPayout = Math.max(0, gross - totalDeductions);

    lastCalculatedInvoice = {
        gross, commPct, commissionAmount, deviceFee, extraFee, vatOnServices, totalDeductions, netPayout
    };
    if (typeof window !== 'undefined') window.lastCalculatedInvoice = lastCalculatedInvoice;

    const box = document.getElementById('invCalcResultsBox');
    if (box) {
        box.innerHTML = `
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 0.8rem; margin-bottom: 10px;">
                <div style="color: #94A3B8;">إجمالي مبيعات المتجر:</div>
                <div style="text-align: left; font-weight: 800; color: #FFF;">${gross.toLocaleString('en-US', {minimumFractionDigits: 2})} ر.س</div>

                <div style="color: #94A3B8;">عمولة هنقرستيشن (${commPct}%):</div>
                <div style="text-align: left; font-weight: 700; color: #F87171;">- ${commissionAmount.toLocaleString('en-US', {minimumFractionDigits: 2})} ر.س</div>

                <div style="color: #94A3B8;">ضريبة القيمة المضافة 15% (VAT):</div>
                <div style="text-align: left; font-weight: 700; color: #F87171;">- ${vatOnServices.toLocaleString('en-US', {minimumFractionDigits: 2})} ر.س</div>

                ${deviceFee > 0 ? `
                    <div style="color: #94A3B8;">رسوم أجهزة وتابلت:</div>
                    <div style="text-align: left; font-weight: 700; color: #F87171;">- ${deviceFee.toLocaleString('en-US', {minimumFractionDigits: 2})} ر.س</div>
                ` : ''}

                ${extraFee > 0 ? `
                    <div style="color: #94A3B8;">رسوم إضافية وتسويق:</div>
                    <div style="text-align: left; font-weight: 700; color: #F87171;">- ${extraFee.toLocaleString('en-US', {minimumFractionDigits: 2})} ر.س</div>
                ` : ''}
            </div>

            <div style="border-top: 1px solid rgba(14,165,233,0.3); padding-top: 8px; display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 800; color: #38BDF8; font-size: 0.9rem;">صافي الحوالة المحولة للبنك:</span>
                <span style="font-weight: 900; color: #10B981; font-size: 1.15rem; font-family: monospace;">${netPayout.toLocaleString('en-US', {minimumFractionDigits: 2})} ر.س</span>
            </div>
        `;
    }
    return lastCalculatedInvoice;
}

function formatInvoiceBreakdownText() {
    const inv = lastCalculatedInvoice;
    let devText = inv.deviceFee > 0 ? `• رسوم جهاز التابلت: -${inv.deviceFee.toLocaleString('en-US', {minimumFractionDigits: 2})} ر.س\n` : '';
    let extText = inv.extraFee > 0 ? `• رسوم تسويق وخدمات: -${inv.extraFee.toLocaleString('en-US', {minimumFractionDigits: 2})} ر.س\n` : '';

    return `شريكنا العزيز،

حرصاً منا على الشفافية التامة والدقة المالية، نوضح لكم تفاصيل الحسبة المالية لمبيعاتكم للفترة الحالية:

• إجمالي مبيعات المتجر: ${inv.gross.toLocaleString('en-US', {minimumFractionDigits: 2})} ر.س
• عمولة هنقرستيشن (${inv.commPct}%): -${inv.commissionAmount.toLocaleString('en-US', {minimumFractionDigits: 2})} ر.س
• ضريبة القيمة المضافة 15% على الخدمات: -${inv.vatOnServices.toLocaleString('en-US', {minimumFractionDigits: 2})} ر.س
${devText}${extText}--------------------------------------------------
= إجمالي الخصومات الرسمية: -${inv.totalDeductions.toLocaleString('en-US', {minimumFractionDigits: 2})} ر.س
= صافي المبلغ المستحق والمحول لحسابكم البنكي: ${inv.netPayout.toLocaleString('en-US', {minimumFractionDigits: 2})} ر.س

شاكرين حسن تعاونكم معنا،
فريق دعم الشركاء | هنقرستيشن`;
}

function insertInvoiceBreakdownIntoMacro() {
    const txt = formatInvoiceBreakdownText();
    const arBox = document.getElementById('arMacroText');
    if (arBox) {
        arBox.innerText = txt;
        closeInvoiceExplainerModal();
        showToast('تم إدراج جدول الشرح المالي في رد التذكرة بنجاح! 🧾');
    } else {
        navigator.clipboard.writeText(txt);
        closeInvoiceExplainerModal();
        showToast('تم نسخ جدول الشرح المالي للحافظة! 📋');
    }
}

function copyInvoiceTextDirect() {
    const txt = formatInvoiceBreakdownText();
    navigator.clipboard.writeText(txt);
    showToast('تم نسخ التقرير المالي للحافظة بنجاح! 📋');
}


// ─────────────────────────────────────────────────────────────────────────
// FEATURE 10: BATCH MULTI-TICKET MODE
// ─────────────────────────────────────────────────────────────────────────
function openBatchTicketsModal() {
    const m = document.getElementById('batchTicketsModal');
    if (m) m.style.display = 'flex';
}

function closeBatchTicketsModal() {
    const m = document.getElementById('batchTicketsModal');
    if (m) m.style.display = 'none';
}

let generatedBatchResponses = [];

function runBatchMultiTicketSolver() {
    const rawInput = document.getElementById('batchOrdersInput')?.value || '';
    const scenario = document.getElementById('batchScenarioSelect')?.value || 'DRIVER_DELAY';
    const agentName = typeof getAgentArabicName === 'function' ? getAgentArabicName() : 'عمر';

    const orderIds = rawInput.split(/[\n,]+/).map(x => x.trim()).filter(x => x.length > 0);
    if (orderIds.length === 0) {
        showToast('⚠️ يرجى إدخال رقم طلب واحد على الأقل.');
        return;
    }

    const templateMap = {
        'DRIVER_DELAY': (ord) => `شريكنا العزيز،

شكراً لتواصلكم مع هنقرستيشن.
بخصوص الطلب رقم (#${ord}) وتأخر وصول السائق لاستلام الوجبة:
تم تصعيد البلاغ فوراً لفريق العمليات الميدانية لإعادة توجيه أقرب سائق بديل لموقع فرعكم بأسرع وقت لتفادي تأثر جودة الطلب.

شاكرين تفهمكم وحسن تعاونكم،
${agentName} | فريق دعم الشركاء`,

        'THURSDAY_PAYOUT': (ord) => `شريكنا العزيز،

شكراً لتواصلكم مع هنقرستيشن بخصوص المبيعات والحوالة البنكية للطلب (#${ord}):
نحيطكم علماً بأن إيداع مستحقات مبيعات الأسبوع يتم كل يوم خميس وتستغرق الحوالة من 24 إلى 48 ساعة عمل كحد أقصى لتظهر في حسابكم البنكي المعتمد.

شاكرين حسن تعاونكم،
${agentName} | فريق دعم الشركاء`,

        'CANCEL_COMP': (ord) => `شريكنا العزيز،

بخصوص الطلب رقم (#${ord}) الذي تم إلغاؤه من قبل العميل بعد استلامه والبدء في تحضيره:
نؤكد لكم أنه وفقاً للائحة التعويضات الرسمية، تم احتساب قيمة الطلب بالكامل لصالح متجركم وسيتم إدراجها ضمن فاتورة الأسبوع القادمة دون أي خصومات.

شاكرين حسن تعاونكم،
${agentName} | فريق دعم الشركاء`,

        'DEVICE_REPLACE': (ord) => `شريكنا العزيز،

بخصوص طلب استبدال جهاز التابلت المرتبط بالفرع (#${ord}):
تم تسجيل طلبكم بنجاح لاستبدال الجهاز، ونفيدكم بأن رسوم استبدال الجهاز هي 500 ريال يتم خصمها تلقائياً من مستحقات المتجر، وسيتم تسليم الجهاز الجديد خلال يومين عمل.

شاكرين حسن تعاونكم،
${agentName} | فريق دعم الشركاء`,

        'MENU_UPDATE': (ord) => `شريكنا العزيز،

شكراً لتواصلكم معنا بخصوص تحديث قائمة الطعام والأسعار للطلب/التذكرة (#${ord}):
تم استلام التعديلات المطلوبة وجاري مراجعتها وتطبيقها على متجركم عبر بوابة العمليات خلال 24 ساعة كحد أقصى.

شاكرين حسن تعاونكم،
${agentName} | فريق دعم الشركاء`
    };

    const builder = templateMap[scenario] || templateMap['DRIVER_DELAY'];
    generatedBatchResponses = orderIds.map(ord => ({
        orderId: ord,
        macroText: builder(ord)
    }));
    if (typeof window !== 'undefined') window.generatedBatchResponses = generatedBatchResponses;

    const cont = document.getElementById('batchResultsContainer');
    const copyAllBtn = document.getElementById('batchCopyAllBtn');

    let html = '';
    generatedBatchResponses.forEach((res, idx) => {
        html += `
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 10px; display: flex; flex-direction: column; gap: 6px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="color: #A855F7; font-size: 0.85rem;"><i class="fa-solid fa-receipt"></i> طلب رقم: #${res.orderId}</strong>
                    <button type="button" onclick="copySingleBatchResponse(${idx})" style="background: rgba(168, 85, 247, 0.2); color: #C084FC; border: 1px solid rgba(168,85,247,0.4); padding: 3px 10px; border-radius: 4px; font-size: 0.74rem; cursor: pointer;">
                        <i class="fa-solid fa-copy"></i> نسخ
                    </button>
                </div>
                <div style="font-size: 0.75rem; color: #CBD5E1; white-space: pre-wrap; font-family: monospace; max-height: 80px; overflow-y: auto; background: rgba(0,0,0,0.3); padding: 6px; border-radius: 4px;">${res.macroText}</div>
            </div>
        `;
    });

    if (cont) cont.innerHTML = html;
    if (copyAllBtn) copyAllBtn.style.display = 'inline-flex';
    showToast(`تم توليد ${generatedBatchResponses.length} رد رسمي مخصص بنجاح! 🚀`);
}

function copySingleBatchResponse(idx) {
    if (generatedBatchResponses[idx]) {
        navigator.clipboard.writeText(generatedBatchResponses[idx].macroText);
        if (typeof incrementDailyTicketCount === 'function') incrementDailyTicketCount();
        showToast(`تم نسخ رد الطلب #${generatedBatchResponses[idx].orderId} 🚀`);
    }
}

function copyAllBatchResponses() {
    if (generatedBatchResponses.length === 0) return;
    const allText = generatedBatchResponses.map(r => `==============================\nطلب #${r.orderId}\n==============================\n${r.macroText}`).join('\n\n');
    navigator.clipboard.writeText(allText);
    showToast(`تم نسخ جميع الـ ${generatedBatchResponses.length} ردود مجمعة للحافظة! 📑`);
}


// ─────────────────────────────────────────────────────────────────────────
// HOOK INTO COPY TEXT FOR STATS & TIMING
// ─────────────────────────────────────────────────────────────────────────
const originalCopyText = window.copyText;
window.copyText = function(id) {
    if (typeof originalCopyText === 'function') {
        originalCopyText(id);
    }
    const activeTitle = (typeof currentSelectedCase !== 'undefined' && currentSelectedCase) ? currentSelectedCase.title_arabic : 'تذكرة عامة';
    recordTicketResolutionTime(activeTitle);
};

// ─────────────────────────────────────────────────────────────────────────
// INITIALIZATION ON PAGE LOAD
// ─────────────────────────────────────────────────────────────────────────
window.addEventListener('DOMContentLoaded', () => {
    updatePendingVaultBadge();
    renderQuickSnippetsBar();
    updateShiftSpeedrunStats();
    updateZeroClickUI();
});
