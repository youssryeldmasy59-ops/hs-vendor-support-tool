#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultra-Luxury Omar's Edition UI Upgrade for Hungerstation Vendor Support Suite:
1. Deep Obsidian Velvet Noir background with multi-point radial aurora lighting.
2. Apple-inspired Glassmorphism with 28px blur, saturation boost, and hairline metallic borders.
3. Bespoke glowing dual-tone icon badges and animated shimmer effects.
4. Omar VIP Executive badge with dynamic time-of-day greeting.
5. High-velocity spring micro-interactions on all tabs, cards, and buttons.
"""

import re
import sys

INDEX_PATH = "/Users/usefelbedwehy/Downloads/hs-vendor-support-tool/index.html"
STYLES_PATH = "/Users/usefelbedwehy/Downloads/hs-vendor-support-tool/styles.css"
SW_PATH = "/Users/usefelbedwehy/Downloads/hs-vendor-support-tool/sw.js"

with open(STYLES_PATH, "r", encoding="utf-8") as f:
    css = f.read()

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# ═════════════════════════════════════════════════════════════════════════════
# 1. LUXURY CSS DESIGN SYSTEM INJECTION
# ═════════════════════════════════════════════════════════════════════════════

LUXURY_CSS = '''
/* 👑 ULTRA-LUXURY OMAR'S EDITION DESIGN SYSTEM (v2026) */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root,
[data-theme="dark"] {
    --bg-body: #030712;
    --bg-surface: #070B19;
    --bg-card: rgba(13, 20, 36, 0.72);
    --bg-card-hover: rgba(20, 30, 55, 0.88);
    --primary: #F59E0B;
    --primary-light: #FCD34D;
    --primary-hover: #FBBF24;
    --primary-glow: 0 0 25px rgba(245, 158, 11, 0.45);
    --accent-emerald: #10B981;
    --accent-violet: #8B5CF6;
    --accent-cyan: #06B6D4;
    --accent-rose: #F43F5E;
    --text-main: #F8FAFC;
    --text-muted: #94A3B8;
    --text-dim: #64748B;
    --border: rgba(255, 255, 255, 0.08);
    --border-highlight: rgba(255, 255, 255, 0.16);
    --border-hover: rgba(245, 158, 11, 0.5);
    --radius-xl: 18px;
    --radius-lg: 14px;
    --radius-md: 10px;
    --radius-sm: 8px;
    --spring-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
    --spring-smooth: cubic-bezier(0.16, 1, 0.3, 1);
    --shadow-luxury: 0 20px 50px -10px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(255, 255, 255, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.12);
}

body {
    background-color: var(--bg-body) !important;
    background-image: 
        radial-gradient(circle at 50% -10%, rgba(245, 158, 11, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 90% 15%, rgba(139, 92, 246, 0.1) 0%, transparent 45%),
        radial-gradient(circle at 10% 85%, rgba(16, 185, 129, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(6, 182, 212, 0.06) 0%, transparent 45%) !important;
    background-attachment: fixed !important;
    font-family: 'Cairo', 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif !important;
    letter-spacing: -0.01em;
}

/* Luxury Glassmorphism */
header.main-header,
.workspace-bar,
.panel,
.card,
.modal-content,
.tools-dropdown-menu,
.shift-stats-strip,
.hud-box,
#autonomousSolverHud {
    backdrop-filter: blur(28px) saturate(210%) !important;
    -webkit-backdrop-filter: blur(28px) saturate(210%) !important;
    border: 1px solid var(--border) !important;
    box-shadow: var(--shadow-luxury) !important;
}

/* Header Luxury Elevation */
header.main-header {
    background: rgba(7, 11, 25, 0.8) !important;
    border-radius: 18px !important;
    margin: 12px 20px 8px 20px !important;
    padding: 12px 24px !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
}

.logo-badge {
    background: linear-gradient(135deg, #FFC400 0%, #D97706 100%) !important;
    color: #000 !important;
    font-weight: 900 !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 20px rgba(245, 158, 11, 0.45) !important;
    letter-spacing: 0.5px;
}

.logo-title h1 {
    background: linear-gradient(135deg, #FFF 0%, #FDE68A 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-weight: 900 !important;
    font-size: 1.28rem !important;
}

/* Omar VIP Agent Chip */
.agent-chip {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.25) 100%) !important;
    border: 1.5px solid rgba(245, 158, 11, 0.45) !important;
    color: #FCD34D !important;
    font-weight: 800 !important;
    padding: 6px 16px !important;
    border-radius: 9999px !important;
    box-shadow: 0 2px 14px rgba(245, 158, 11, 0.25) !important;
    transition: all 0.25s var(--spring-bounce) !important;
    cursor: pointer;
}
.agent-chip:hover {
    transform: translateY(-2px) scale(1.03) !important;
    border-color: #FBBF24 !important;
    box-shadow: 0 6px 24px rgba(245, 158, 11, 0.45) !important;
}

/* Workspace Segmented Dock */
.workspace-bar {
    background: rgba(9, 14, 28, 0.85) !important;
    border-radius: 16px !important;
    padding: 6px 8px !important;
    margin: 8px 20px 14px 20px !important;
    display: flex !important;
    gap: 8px !important;
}

.ws-tab-btn {
    border-radius: 12px !important;
    font-weight: 800 !important;
    font-size: 0.86rem !important;
    padding: 10px 18px !important;
    border: 1px solid transparent !important;
    transition: all 0.22s var(--spring-bounce) !important;
    color: #94A3B8 !important;
}

.ws-tab-btn:hover {
    color: #FFF !important;
    background: rgba(255, 255, 255, 0.06) !important;
    transform: translateY(-1px) !important;
}

.ws-tab-btn.active {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.25) 0%, rgba(217, 119, 6, 0.4) 100%) !important;
    border-color: #F59E0B !important;
    color: #FFF !important;
    box-shadow: 0 4px 20px rgba(245, 158, 11, 0.35) !important;
}

.ws-tab-btn.menu-tab.active {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.25) 0%, rgba(5, 150, 105, 0.4) 100%) !important;
    border-color: #10B981 !important;
    box-shadow: 0 4px 20px rgba(16, 185, 129, 0.35) !important;
}

.ws-tab-btn.policy-tab.active {
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.25) 0%, rgba(124, 58, 237, 0.4) 100%) !important;
    border-color: #A855F7 !important;
    box-shadow: 0 4px 20px rgba(168, 85, 247, 0.35) !important;
}

.ws-tab-btn.forensics-tab.active {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.25) 0%, rgba(14, 116, 144, 0.4) 100%) !important;
    border-color: #06B6D4 !important;
    box-shadow: 0 4px 20px rgba(6, 182, 212, 0.35) !important;
}

/* Primary Generate Button (Shimmering Obsidian Gold) */
.btn-generate {
    background: linear-gradient(135deg, #FFC400 0%, #F59E0B 50%, #D97706 100%) !important;
    color: #000 !important;
    font-weight: 900 !important;
    font-size: 1.05rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 24px !important;
    box-shadow: 0 8px 30px rgba(245, 158, 11, 0.45) !important;
    position: relative;
    overflow: hidden;
    transition: all 0.22s var(--spring-bounce) !important;
    cursor: pointer;
}

.btn-generate:hover {
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 12px 40px rgba(245, 158, 11, 0.6) !important;
}

.btn-generate:active {
    transform: scale(0.97) !important;
}

/* Continuous Luxury Shimmer */
@keyframes luxuryShimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

.btn-shimmer {
    background: linear-gradient(90deg, rgba(16, 185, 129, 0.9) 0%, rgba(52, 211, 153, 1) 50%, rgba(16, 185, 129, 0.9) 100%) !important;
    background-size: 200% 100% !important;
    animation: luxuryShimmer 3s infinite linear;
}

/* Textarea Velvet Glow */
#partnerMessage {
    background: rgba(9, 14, 27, 0.85) !important;
    border: 1.5px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 14px !important;
    color: #F8FAFC !important;
    font-size: 0.92rem !important;
    line-height: 1.65 !important;
    padding: 16px !important;
    transition: all 0.2s ease !important;
}

#partnerMessage:focus {
    border-color: #F59E0B !important;
    box-shadow: 0 0 25px rgba(245, 158, 11, 0.25), inset 0 1px 2px rgba(0, 0, 0, 0.5) !important;
    outline: none !important;
}

/* Tool Mini Buttons */
.tool-mini-btn {
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 0.78rem !important;
    padding: 6px 12px !important;
    transition: all 0.18s var(--spring-bounce) !important;
}
.tool-mini-btn:hover {
    transform: translateY(-1px) scale(1.04) !important;
}
.tool-mini-btn:active {
    transform: scale(0.95) !important;
}

/* Pulse indicator animation */
@keyframes pulseDot {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { transform: scale(1.1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

.live-pulse-dot {
    width: 8px;
    height: 8px;
    background: #10B981;
    border-radius: 50%;
    display: inline-block;
    animation: pulseDot 2s infinite;
}
'''

# Append luxury CSS to styles.css
css += "\n\n" + LUXURY_CSS
with open(STYLES_PATH, "w", encoding="utf-8") as f:
    f.write(css)
print("✓ Appended Ultra-Luxury Design System to styles.css")

# ═════════════════════════════════════════════════════════════════════════════
# 2. UPDATE HTML PERSONALIZATION & LUXURY ELEMENTS
# ═════════════════════════════════════════════════════════════════════════════

# Update Omar's chip with star and luxury rank
html = html.replace('<span id="displayAgentName">الموظف: عمر</span>',
                    '<span id="displayAgentName">الموظف: عمر ⭐ (Senior Ops)</span>')

# Inject dynamic time-of-day greeting in script
GREETING_SCRIPT = '''
// ☀️ Dynamic Time-of-Day Personal Greeting for Omar
function updateOmarPersonalGreeting() {
    const greetingEl = document.querySelector('.greeting-text') || document.querySelector('.hero-greeting h2') || document.querySelector('.greeting-header');
    const hour = new Date().getHours();
    let greet = 'صباح الهمة والنشاط، يا عمر! ☀️';
    if (hour >= 12 && hour < 17) {
        greet = 'طاب يومك بكل إنجاز، يا عمر! ☕';
    } else if (hour >= 17 && hour < 23) {
        greet = 'مساء التميز والتألق، يا عمر! 🌙';
    } else if (hour >= 23 || hour < 6) {
        greet = 'شفت الأبطال والتركيز العالي، يا عمر! ⚡';
    }
    
    // Find all elements with greeting
    document.querySelectorAll('*').forEach(el => {
        if (el.children.length === 0 && (el.innerText.includes('صباح الهمة والنشاط، يا عمر') || el.innerText.includes('يا عمر'))) {
            el.innerText = greet;
        }
    });
}

window.addEventListener('DOMContentLoaded', updateOmarPersonalGreeting);
setTimeout(updateOmarPersonalGreeting, 300);
'''

# Bump version to v27 (Ultra-Luxury Omar's Edition)
html = html.replace('Production v26 (Autonomous AI Auto-Pilot)', 'Production v27 (Ultra-Luxury Edition ✨)')
html = html.replace('Production v26', 'Production v27 (Ultra-Luxury Edition ✨)')

# Inject script before </body>
if '</body>' in html:
    html = html.replace('</body>', '<script>' + GREETING_SCRIPT + '</script>\n</body>')
    print("✓ Injected Dynamic Time-of-Day Greeting Script")

# Update sw.js version
html = re.sub(r'sw\.js\?v=\d+', 'sw.js?v=42', html)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

with open(SW_PATH, "r", encoding="utf-8") as f:
    sw = f.read()

sw = re.sub(r"const CACHE_NAME = '[^']+';", "const CACHE_NAME = 'hs-vendor-suite-v42-ultra-luxury';", sw)

with open(SW_PATH, "w", encoding="utf-8") as f:
    f.write(sw)

print("✓ Updated Service Worker to v42")
print("🎉 Ultra-Luxury Omar's Edition applied successfully!")
