#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Elevate HungerStation Support Tool to Ultra-Luxury Enterprise Standard
- Strips cheap conflicting rainbow inline styles from header and workspace buttons
- Implements cohesive Obsidian & Brushed Amber design system (Apple / Linear caliber)
- Apple-style segmented glass dock for Workspace Switcher
- Subtle micro-borders, deep Chiaroscuro lighting, and frosted glass panels
- Cleans up tacky emojis from navigation controls
- IMPORTANT: Does NOT deploy to Surge. Only updates local repo & Git.
"""

import re
import sys

INDEX_PATH = "/Users/usefelbedwehy/Downloads/hs-vendor-support-tool/index.html"
STYLES_PATH = "/Users/usefelbedwehy/Downloads/hs-vendor-support-tool/styles.css"

# ==============================================================================
# 1. UPGRADE STYLES.CSS TO ULTRA-LUXURY DESIGN SYSTEM
# ==============================================================================

with open(STYLES_PATH, "r", encoding="utf-8") as f:
    css = f.read()

# Replace root variables with luxury obsidian & brushed amber tokens
LUXURY_ROOT_DARK = """        :root,
        [data-theme="dark"] {
            /* 👑 Obsidian & Brushed Amber Executive Luxury Suite */
            --bg-body: #05070E;
            --bg-card: rgba(11, 16, 29, 0.65);
            --bg-card-hover: rgba(16, 23, 40, 0.85);
            --primary: #F59E0B;
            --primary-hover: #FBBF24;
            --primary-glow: rgba(245, 158, 11, 0.35);
            --text-main: #F8FAFC;
            --text-muted: #8E9BAE;
            --border: rgba(255, 255, 255, 0.07);
            --border-hover: rgba(245, 158, 11, 0.45);
            --radius-xl: 20px;
            --radius-lg: 14px;
            --radius-md: 10px;
            --radius-sm: 6px;
            --radius-pill: 9999px;
            --shadow-panel: 0 24px 60px -12px rgba(0, 0, 0, 0.75), 0 0 0 1px rgba(255, 255, 255, 0.07), inset 0 1px 0 rgba(255, 255, 255, 0.08);
            --header-bg: rgba(5, 7, 14, 0.78);
            --input-bg: rgba(8, 12, 22, 0.7);
            --response-bg: rgba(9, 14, 26, 0.82);
            --response-border: rgba(245, 158, 11, 0.28);
            --response-text: #F8FAFC;
            --kb-filter-bg: rgba(9, 13, 24, 0.7);
            --card-subtle-bg: rgba(245, 158, 11, 0.05);
        }"""

# Update body with ambient Chiaroscuro mesh lighting
LUXURY_BODY = """        body {
            background-color: var(--bg-body);
            background-image: 
                radial-gradient(ellipse 85% 55% at 50% -18%, rgba(245, 158, 11, 0.12) 0%, transparent 60%),
                radial-gradient(ellipse 65% 45% at 90% 12%, rgba(99, 102, 241, 0.05) 0%, transparent 55%),
                radial-gradient(ellipse 50% 50% at 10% 85%, rgba(16, 185, 129, 0.04) 0%, transparent 60%);
            background-attachment: fixed;
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            letter-spacing: -0.01em;
            transition: background-color 0.3s ease, color 0.3s ease;
        }"""

# Luxury Header & Buttons
LUXURY_HEADER_CSS = """        /* Modern Luxury Top Header */
        header.main-header {
            background: var(--header-bg);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border-bottom: 1px solid var(--border);
            padding: 12px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.7);
        }

        .logo-area {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-badge {
            background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
            color: #05070E;
            font-weight: 800;
            padding: 6px 14px;
            border-radius: var(--radius-md);
            font-size: 0.88rem;
            display: flex;
            align-items: center;
            gap: 7px;
            box-shadow: 0 4px 16px rgba(245, 158, 11, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.3);
            letter-spacing: 0.02em;
        }

        .logo-title h1 {
            font-size: 1.05rem;
            font-weight: 800;
            color: var(--text-main);
            line-height: 1.2;
            letter-spacing: -0.02em;
        }

        .logo-title p {
            font-size: 0.73rem;
            color: var(--text-muted);
            margin-top: 1px;
        }

        .version-badge {
            background: rgba(245, 158, 11, 0.1);
            border: 1px solid rgba(245, 158, 11, 0.3);
            color: #FCD34D;
            font-size: 0.7rem;
            font-weight: 700;
            padding: 2px 9px;
            border-radius: var(--radius-pill);
            letter-spacing: 0.02em;
        }

        /* Header Right Utility Cluster */
        .header-controls {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }

        .header-btn {
            background: rgba(255, 255, 255, 0.035) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            color: #E2E8F0 !important;
            padding: 6px 13px !important;
            border-radius: var(--radius-pill) !important;
            font-size: 0.79rem !important;
            font-weight: 600 !important;
            display: inline-flex !important;
            align-items: center !important;
            gap: 6px !important;
            cursor: pointer !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
        }

        .header-btn:hover {
            background: rgba(255, 255, 255, 0.08) !important;
            border-color: rgba(245, 158, 11, 0.4) !important;
            color: #FFF !important;
            transform: translateY(-1.5px) !important;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4), 0 0 16px rgba(245, 158, 11, 0.15) !important;
        }

        .header-btn i {
            font-size: 0.82rem;
            opacity: 0.85;
            transition: opacity 0.2s ease;
        }

        .header-btn:hover i {
            opacity: 1;
            color: #FCD34D;
        }

        /* Specific Highlight for Agent Profile Chip */
        .agent-chip {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.09);
            color: #F8FAFC;
            padding: 6px 13px;
            border-radius: var(--radius-pill);
            font-size: 0.8rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 6px;
            cursor: pointer;
            backdrop-filter: blur(16px);
            transition: all 0.2s ease;
        }

        .agent-chip:hover {
            background: rgba(245, 158, 11, 0.15);
            border-color: rgba(245, 158, 11, 0.45);
            color: #FCD34D;
            transform: translateY(-1px);
        }

        .agent-chip i {
            color: #F59E0B;
        }

        /* ☀️ Theme Toggle Button */
        .theme-toggle-btn {
            background: rgba(255, 255, 255, 0.035);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #CBD5E1;
            padding: 6px 13px;
            border-radius: var(--radius-pill);
            font-size: 0.79rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
            cursor: pointer;
            backdrop-filter: blur(16px);
            transition: all 0.2s ease;
        }

        .theme-toggle-btn:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.18);
            color: #FFF;
            transform: translateY(-1px);
        }"""

# Luxury Segmented Workspace Bar
LUXURY_WORKSPACE_BAR = """        /* 🧭 Executive Segmented Glass Dock (Apple / Linear Caliber) */
        .workspace-bar {
            max-width: 1400px;
            margin: 18px auto 0;
            padding: 6px;
            display: flex;
            gap: 6px;
            align-items: center;
            width: 100%;
            background: rgba(11, 16, 29, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            backdrop-filter: blur(28px);
            -webkit-backdrop-filter: blur(28px);
            box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.06);
        }

        .ws-tab-btn {
            background: transparent !important;
            border: 1px solid transparent !important;
            color: #8E9BAE !important;
            flex: 1;
            padding: 10px 18px !important;
            border-radius: 11px !important;
            font-weight: 600 !important;
            font-size: 0.86rem !important;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
            position: relative;
            overflow: hidden;
            box-shadow: none !important;
        }

        .ws-tab-btn:hover {
            background: rgba(255, 255, 255, 0.04) !important;
            color: #F8FAFC !important;
            border-color: rgba(255, 255, 255, 0.06) !important;
        }

        .ws-tab-btn.active {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.16) 0%, rgba(217, 119, 6, 0.06) 100%) !important;
            border: 1px solid rgba(245, 158, 11, 0.5) !important;
            color: #FCD34D !important;
            font-weight: 800 !important;
            box-shadow: 0 6px 24px -4px rgba(245, 158, 11, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
        }

        .ws-tab-btn.active i {
            color: #F59E0B !important;
        }"""

# Luxury Modal Overhaul
LUXURY_MODALS = """        /* 💎 Luxury Translucent Glass Modals */
        .modal-card {
            background: rgba(11, 16, 29, 0.92) !important;
            backdrop-filter: blur(32px) !important;
            -webkit-backdrop-filter: blur(32px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            box-shadow: 0 40px 100px -20px rgba(0, 0, 0, 0.9), inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
            border-radius: 22px !important;
        }

        .modal-overlay {
            backdrop-filter: blur(14px) !important;
            -webkit-backdrop-filter: blur(14px) !important;
            background: rgba(0, 0, 0, 0.78) !important;
        }

        /* Luxury Panels & Action Buttons */
        .panel {
            background: var(--bg-card) !important;
            backdrop-filter: blur(24px) !important;
            -webkit-backdrop-filter: blur(24px) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-xl) !important;
            box-shadow: var(--shadow-panel) !important;
            transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
        }

        .panel:hover {
            border-color: rgba(255, 255, 255, 0.12) !important;
        }

        .btn-generate {
            background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%) !important;
            color: #05070E !important;
            font-weight: 800 !important;
            border-radius: 12px !important;
            border: none !important;
            box-shadow: 0 8px 24px -4px rgba(245, 158, 11, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }

        .btn-generate:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 12px 32px -4px rgba(245, 158, 11, 0.65), inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
        }"""

# Apply to styles.css
start_root = css.find(':root,')
if start_root != -1:
    end_root = css.find('/* ☀️ Daylight Crisp Mode', start_root)
    if end_root != -1:
        css = css[:start_root] + LUXURY_ROOT_DARK + "\n\n        " + css[end_root:]
        print("✅ Replaced root variables with Luxury Obsidian tokens!")

start_body = css.find('body {')
if start_body != -1:
    end_body = css.find('/* Modern Enterprise Top Header', start_body)
    if end_body != -1:
        css = css[:start_body] + LUXURY_BODY + "\n\n        " + css[end_body:]
        print("✅ Updated body with Chiaroscuro ambient lighting!")

# Append comprehensive luxury rules at the end of styles.css to ensure universal override
css += "\n\n/* ═══════════════════════════════════════════════════════════════ */\n"
css += "/* 👑 ULTRA-LUXURY EXECUTIVE DESIGN SYSTEM OVERRIDES (v2026)      */\n"
css += "/* ═══════════════════════════════════════════════════════════════ */\n"
css += LUXURY_HEADER_CSS + "\n\n"
css += LUXURY_WORKSPACE_BAR + "\n\n"
css += LUXURY_MODALS + "\n"

with open(STYLES_PATH, "w", encoding="utf-8") as f:
    f.write(css)

print("Saved ultra-luxury styles.css!")

# ==============================================================================
# 2. CLEAN UP INDEX.HTML (HEADER BUTTONS & WORKSPACE TABS)
# ==============================================================================

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Luxury Header Buttons Clean Markup (No inline conflicting gradients, clean icons, no tacky emojis)
NEW_HEADER_CONTROLS = '''            <!-- 👤 Agent Profile Chip -->
            <div class="agent-chip" onclick="promptChangeName()" title="تعديل اسم الموظف">
                <i class="fa-solid fa-circle-user"></i>
                <span id="displayAgentName">الموظف: عمر</span>
                <i class="fa-solid fa-pen" style="font-size: 0.65rem; opacity: 0.5;"></i>
            </div>

            <!-- Desktop Ghost PiP -->
            <button type="button" class="header-btn" onclick="toggleDesktopGhostPip()" id="ghostPipHeaderBtn" title="الوضع الشبحي: نافذة ديسكتوب عائمة فوق الشاشات (Always on Top)">
                <i class="fa-solid fa-clone"></i> <span id="ghostPipHeaderLabel">وضع الشبح</span>
            </button>

            <!-- Angry Partner Simulator -->
            <button type="button" class="header-btn" onclick="openPartnerSimulatorModal()" id="partnerSimHeaderBtn" title="محاكي تدريب الشركاء التفاعلي وغرفة تقييم الـ QA">
                <i class="fa-solid fa-gamepad"></i> <span id="partnerSimHeaderLabel">محاكي الشركاء</span>
            </button>

            <!-- Clipboard Sniper -->
            <button type="button" class="header-btn" onclick="toggleClipboardSniper()" id="clipboardSniperBtn" title="رادار الحافظة الذكي: يراقب الحافظة تلقائياً وينسخ الرد فوراً">
                <i class="fa-solid fa-crosshairs"></i> <span id="clipboardSniperLabel">رادار الحافظة</span>
            </button>

            <!-- Smart Rider Operations Hub -->
            <button type="button" class="header-btn" onclick="openRiderOperationsModal()" id="riderOpsHeaderBtn" title="مركز عمليات وحلول الرايدر واللوجستيك (تأخير، استلام خاطئ، هروب دون دفع)">
                <i class="fa-solid fa-motorcycle"></i> <span id="riderOpsHeaderLabel">عمليات الرايدر</span>
            </button>

            <!-- Live Call Whisperer -->
            <button type="button" class="header-btn" onclick="openLiveCallWhispererModal()" id="callWhispererBtn" title="الملقّن الحي لمكالمات الشركاء (يسمع المكالمة لايف ويمليك الرد المعتمد)">
                <i class="fa-solid fa-headset"></i> <span id="whispererBtnLabel">ملقّن المكالمات</span>
            </button>

            <!-- Voice Assistant -->
            <button type="button" class="header-btn" onclick="toggleVoiceAiDrawer()" id="voiceAiTriggerBtn" title="المساعد الصوتي الذكي (AR+EN)">
                <i class="fa-solid fa-microphone"></i> <span id="voiceBadgeText">المساعد الصوتي</span>
            </button>

            <!-- Cloud AI Settings & Model Selector -->
            <button type="button" class="header-btn" onclick="openCloudAiSettingsModal()" id="cloudAiHeaderBtn" title="إعدادات وتشغيل الـ AI السحابي المباشر (علّام / Groq / DeepSeek)">
                <i class="fa-solid fa-brain"></i> <span id="cloudAiHeaderLabel">الذكاء الاصطناعي</span>
            </button>

            <!-- Force Refresh / Cache Purge -->
            <button type="button" class="header-btn" onclick="forcePurgeAndReload()" title="تحديث فوري وحذف الكاش القديم">
                <i class="fa-solid fa-rotate"></i> <span>تحديث</span>
            </button>

            <!-- Theme Switcher -->
            <button type="button" class="theme-toggle-btn" onclick="toggleAppTheme()" id="themeToggleBtn" title="تبديل مظهر الواجهة">
                <i class="fa-solid fa-moon" id="themeToggleIcon"></i>
                <span id="themeToggleText">المظهر</span>
            </button>'''

# Replace header-controls block
start_hc = html.find('<!-- 👤 Agent Profile Chip -->')
if start_hc != -1:
    end_hc = html.find('<!-- ⚡ Consolidated Enterprise Tools Dropdown -->', start_hc)
    if end_hc != -1:
        html = html[:start_hc] + NEW_HEADER_CONTROLS + "\n\n            " + html[end_hc:]
        print("✅ Replaced Header Controls with Luxury Minimalist Glass Pills!")

# Clean up Workspace Tabs Bar (Remove inline 2px neon borders and cluttered emojis)
NEW_WORKSPACE_BAR = '''        <!-- 🧭 Main Workspace View Switcher -->
    <div class="workspace-bar">
        <button id="viewBtnTickets" onclick="switchMainWorkspace('TICKETS')" class="ws-tab-btn active">
            <i class="fa-solid fa-comment-dots"></i>
            <span>مولد الردود وقاعدة المعرفة</span>
        </button>
        <button id="viewBtnPolicies" onclick="switchMainWorkspace('POLICIES')" class="ws-tab-btn policy-tab">
            <i class="fa-solid fa-book-bookmark"></i>
            <span>سياسات الدعم المعتمدة</span>
        </button>
        <button id="viewBtnMenu" onclick="switchMainWorkspace('MENU_STUDIO')" class="ws-tab-btn menu-tab">
            <i class="fa-solid fa-file-excel"></i>
            <span>استوديو المنيو الذكي</span>
        </button>
        <button id="viewBtnForensics" onclick="switchMainWorkspace('FORENSICS')" class="ws-tab-btn forensics-tab">
            <i class="fa-solid fa-scale-balanced"></i>
            <span>المحقق الجنائي للاعتراضات</span>
        </button>
    </div>'''

start_ws = html.find('<!-- 🧭 Main Workspace View Switcher -->')
if start_ws != -1:
    end_ws = html.find('<!-- 🍽️ DEDICATED MENU BUILDER STUDIO WORKSPACE -->', start_ws)
    if end_ws != -1:
        html = html[:start_ws] + NEW_WORKSPACE_BAR + "\n\n    " + html[end_ws:]
        print("✅ Cleaned up Workspace Bar into Apple-style Segmented Glass Dock!")

# Clean up switchMainWorkspace JavaScript function so it only toggles classes without injecting ugly inline styles
REFINED_SWITCH_WORKSPACE = '''        function switchMainWorkspace(mode) {
            const ticketCont = document.querySelector('.app-container');
            const studioCont = document.getElementById('menuStudioWorkspace');
            const policiesCont = document.getElementById('policiesWorkspace');
            const forensicsCont = document.getElementById('forensicsWorkspace');
            
            const btnTicket = document.getElementById('viewBtnTickets');
            const btnMenu = document.getElementById('viewBtnMenu');
            const btnPolicies = document.getElementById('viewBtnPolicies');
            const btnForensics = document.getElementById('viewBtnForensics');

            // Reset all active classes and inline styles
            [btnTicket, btnMenu, btnPolicies, btnForensics].forEach(btn => {
                if (btn) {
                    btn.classList.remove('active');
                    btn.style.background = '';
                    btn.style.borderColor = '';
                    btn.style.color = '';
                    btn.style.boxShadow = '';
                }
            });

            if (mode === 'FORENSICS') {
                if (ticketCont) ticketCont.style.display = 'none';
                if (studioCont) studioCont.style.display = 'none';
                if (policiesCont) policiesCont.style.display = 'none';
                if (forensicsCont) forensicsCont.style.display = 'block';
                if (btnForensics) btnForensics.classList.add('active');
                return;
            } else if (forensicsCont) {
                forensicsCont.style.display = 'none';
            }

            if (mode === 'POLICIES') {
                if (ticketCont) ticketCont.style.display = 'none';
                if (studioCont) studioCont.style.display = 'none';
                if (policiesCont) policiesCont.style.display = 'block';
                if (forensicsCont) forensicsCont.style.display = 'none';
                if (btnPolicies) btnPolicies.classList.add('active');
                if (typeof renderPoliciesCards === 'function') renderPoliciesCards();
                return;
            } else if (policiesCont) {
                policiesCont.style.display = 'none';
            }

            if (mode === 'MENU_STUDIO') {
                if (ticketCont) ticketCont.style.display = 'none';
                if (studioCont) studioCont.style.display = 'block';
                if (policiesCont) policiesCont.style.display = 'none';
                if (forensicsCont) forensicsCont.style.display = 'none';
                if (btnMenu) btnMenu.classList.add('active');
                if (typeof renderStudioMenuPreviewTables === 'function') renderStudioMenuPreviewTables();
                return;
            } else if (studioCont) {
                studioCont.style.display = 'none';
            }

            // Default: TICKETS
            if (ticketCont) ticketCont.style.display = 'grid';
            if (studioCont) studioCont.style.display = 'none';
            if (policiesCont) policiesCont.style.display = 'none';
            if (forensicsCont) forensicsCont.style.display = 'none';
            if (btnTicket) btnTicket.classList.add('active');
        }'''

start_sw = html.find('function switchMainWorkspace(mode) {')
if start_sw != -1:
    end_sw = html.find('window.switchMainWorkspace = switchMainWorkspace;', start_sw)
    if end_sw != -1:
        html = html[:start_sw] + REFINED_SWITCH_WORKSPACE + "\n        " + html[end_sw:]
        print("✅ Cleaned switchMainWorkspace JS logic!")

# Strip 2px neon borders from modal dialogs in HTML
html = html.replace('border: 2px solid #F59E0B;', 'border: 1px solid rgba(245, 158, 11, 0.4);')
html = html.replace('border: 2px solid #10B981;', 'border: 1px solid rgba(16, 185, 129, 0.4);')
html = html.replace('border: 2px solid #EC4899;', 'border: 1px solid rgba(236, 72, 153, 0.4);')
html = html.replace('border: 2px solid #6366F1;', 'border: 1px solid rgba(99, 102, 241, 0.4);')

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Saved luxury index.html! All cheap neon elements eliminated.")
