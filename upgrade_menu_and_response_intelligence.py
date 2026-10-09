#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upgrade Menu Studio & Macro Response Intelligence (Fixed escape handling)
hs-vendor-support-tool
"""

import re
import sys

INDEX_PATH = "/Users/usefelbedwehy/Downloads/hs-vendor-support-tool/index.html"
ENGINE_PATH = "/Users/usefelbedwehy/Downloads/hs-vendor-support-tool/engine_11_features.js"

# ==============================================================================
# 1. UPGRADE MENU INTELLIGENCE IN index.html
# ==============================================================================

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Expanded Professional Culinary Dictionary (Multi-word phrases prioritized)
NEW_MENU_DICT_AND_TRANSLATE = r'''// 🌐 Comprehensive Food & Menu Neural Dictionary (Overhauled v2026)
const MENU_DICTIONARY = {
    // Multi-Word Composite Phrases (Longest match first)
    "شاورما دجاج صاروخ": "Jumbo Chicken Shawarma", "شاورما لحم صاروخ": "Jumbo Beef Shawarma",
    "شاورما دجاج عربي": "Arabic Chicken Shawarma Platter", "شاورما لحم عربي": "Arabic Beef Shawarma Platter",
    "صحن شاورما دجاج": "Chicken Shawarma Plate", "صحن شاورما لحم": "Beef Shawarma Plate",
    "برجر لحم دبل": "Double Beef Burger", "برجر دجاج دبل": "Double Chicken Burger",
    "برجر لحم كلاسيك": "Classic Beef Burger", "برجر دجاج كلاسيك": "Classic Chicken Burger",
    "عصير ليمون بالنعناع": "Lemon Mint Juice", "عصير برتقال طازج": "Fresh Orange Juice",
    "عصير رمان طازج": "Fresh Pomegranate Juice", "عصير بطيخ طازج": "Fresh Watermelon Juice",
    "بطاطس بالجبنة": "Cheesy French Fries", "بطاطس ودجز متبلة": "Seasoned Potato Wedges",
    "أصابع جبنة موزاريلا": "Mozzarella Cheese Sticks", "حلقات بصل مقرمشة": "Crispy Onion Rings",
    "سلطة سيزر بالدجاج": "Chicken Caesar Salad", "سلطة يونانية": "Greek Salad",
    "ورق عنب بدبس الرمان": "Stuffed Grape Leaves with Pomegranate Molasses",
    "كبسة دجاج مع الأرز": "Chicken Kabsa with Rice", "مندي لحم بلدي": "Local Meat Mandi",
    "مضغوط دجاج تهامة": "Tihama Chicken Madghoot", "برياني دجاج هندي": "Indian Chicken Biryani",
    "مسحب دجاج مقرمش": "Crispy Chicken Tenders", "بروستد دجاج حار": "Spicy Broasted Chicken",
    "بروستد دجاج عادي": "Regular Broasted Chicken", "تشيز كيك فراولة": "Strawberry Cheesecake",
    "وافل بالنوتيلا والفراولة": "Nutella & Strawberry Waffle", "كريب لوتس مقرمش": "Crispy Lotus Crepe",
    
    // Categories & Sections
    "مشويات": "Grills", "برجر": "Burgers", "ساندوتش": "Sandwiches", "بيتزا": "Pizza",
    "معجنات": "Pastries", "فطائر": "Pies", "شاورما": "Shawarma", "بروستد": "Broasted",
    "مقبلات": "Appetizers", "سلطات": "Salads", "مشروبات": "Beverages", "عصائر": "Fresh Juices",
    "حلويات": "Desserts", "فطور": "Breakfast", "شعبيات": "Traditional Dishes",
    "كبسات": "Rice & Kabsa", "باستا": "Pasta", "أطباق رئيسية": "Main Courses", 
    "شوربة": "Soups", "صوصات": "Sauces & Dips", "إضافات": "Add-ons", "وجبات أطفال": "Kids Meals",
    "وجبات عائلية": "Family Meals", "كومبو": "Combo", "بوكسات": "Boxes",
    
    // Items, Cuts & Ingredients
    "لحم": "Meat", "دجاج": "Chicken", "سمك": "Fish", "جمبري": "Shrimp", "روبيان": "Prawns",
    "فيليه": "Fillet", "كباب": "Kebab", "أوصال": "Meat Skewers", "شيش طاووق": "Shish Tawook",
    "كفتة": "Kofta", "ريش غنم": "Lamb Chops", "ستيك": "Steak", "مسحب": "Chicken Tenders",
    "ناجتس": "Nuggets", "زنجر": "Zinger", "فاهيتا": "Fajita", "تورتيلا": "Tortilla",
    "جبنة": "Cheese", "شيدر": "Cheddar", "موزاريلا": "Mozzarella", "حلوم": "Halloumi",
    "بطاطس": "French Fries", "فرايز": "Fries", "طازج": "Fresh", "حار": "Spicy",
    "عادي": "Regular", "كبير": "Large", "وسط": "Medium", "صغير": "Small",
    "مشوي": "Grilled", "مقلي": "Fried", "مقرمش": "Crispy", "على الفحم": "Charcoal Grilled",
    "ثومية": "Garlic Sauce", "طحينة": "Tahini", "كتشب": "Ketchup", "مايونيز": "Mayonnaise",
    "رانش": "Ranch", "باربيكيو": "BBQ Sauce", "ديناميت": "Dynamite Sauce", "شطة": "Hot Sauce",
    "ماء": "Water", "شاي": "Tea", "قهوة": "Coffee", "بيبسي": "Pepsi", "سفن اب": "7 Up",
    "ميرندا": "Mirinda", "ديو": "Mountain Dew", "كولا": "Coca-Cola", "موهيتو": "Mojito",
    "رمان": "Pomegranate", "مانجو": "Mango", "فراولة": "Strawberry", "ليمون": "Lemon",
    "برتقال": "Orange", "أناناس": "Pineapple", "بطيخ": "Watermelon", "موز": "Banana"
};

function autoTranslateMenuText(text, targetLang = 'EN') {
    if (!text) return '';
    let str = String(text).trim();
    if (targetLang === 'EN') {
        if (/^[a-zA-Z0-9\s.,'%-]+$/.test(str)) return toEnglishProper(str);
        
        // Sort keys by length descending to match composite phrases first
        const sortedEntries = Object.entries(MENU_DICTIONARY).sort((a,b) => b[0].length - a[0].length);
        let result = str;
        for (const [ar, en] of sortedEntries) {
            const regex = new RegExp(ar, 'gi');
            if (regex.test(result)) {
                result = result.replace(regex, ' ' + en + ' ');
            }
        }
        result = result.replace(/\s+/g, ' ').trim();
        return toEnglishProper(result);
    } else {
        if (/[؀-ۿ]/.test(str)) return cleanProperTrim(str);
        const sortedEntries = Object.entries(MENU_DICTIONARY).sort((a,b) => b[1].length - a[1].length);
        let result = str;
        for (const [ar, en] of sortedEntries) {
            const regex = new RegExp('\\b' + en.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b', 'gi');
            if (regex.test(result)) {
                result = result.replace(regex, ' ' + ar + ' ');
            }
        }
        return cleanProperTrim(result.replace(/\s+/g, ' '));
    }
}'''

# Replace old dictionary and autoTranslateMenuText using exact index slicing
start_dict = html.find('const MENU_DICTIONARY = {')
if start_dict != -1:
    end_fn = html.find('// 📊 Bulk Price Adjuster', start_dict)
    if end_fn != -1:
        html = html[:start_dict] + NEW_MENU_DICT_AND_TRANSLATE + "\n\n\n" + html[end_fn:]
        print("✅ Successfully replaced MENU_DICTIONARY & autoTranslateMenuText via slice!")
    else:
        print("⚠️ Could not locate end marker for autoTranslateMenuText")
else:
    print("⚠️ Could not locate const MENU_DICTIONARY marker")

# Comprehensive 14-Category Rules for Saudi & Gulf Restaurants
NEW_CATEGORY_RULES = r'''// 🧠 Comprehensive 14-Category Rule Engine (Saudi & Gulf HungerStation Standards)
const CATEGORY_MAP_RULES = [
    { cat_ar: 'البرجر والساندوتشات', cat_en: 'Burgers and Sandwiches', keywords: ['برجر', 'ساندوتش', 'فاهيتا', 'برگر', 'تورتيلا', 'صاروخ', 'صامولي', 'burger', 'sandwich', 'wrap'] },
    { cat_ar: 'الشاورما والدونر', cat_en: 'Shawarma and Doner', keywords: ['شاورما', 'دونر', 'عربي', 'صحن شاورما', 'shawarma', 'doner'] },
    { cat_ar: 'البروست والمقليات', cat_en: 'Broasted and Fried Chicken', keywords: ['بروست', 'بروستد', 'مسحب', 'تندرز', 'ناجتس', 'زنجر', 'ستريبس', 'broasted', 'tenders', 'nuggets', 'strips', 'crispy'] },
    { cat_ar: 'المشويات والمأكولات الرئيسية', cat_en: 'Grills and Main Dishes', keywords: ['مشاوي', 'مشويات', 'كباب', 'اوصال', 'شيش', 'كفتة', 'ريش', 'ستيك', 'طاووق', 'grill', 'kebab', 'tawook', 'steak'] },
    { cat_ar: 'الشعبيات والكبسات', cat_en: 'Traditional and Rice Dishes', keywords: ['كبسة', 'مندي', 'مضغوط', 'حنيذ', 'بخاري', 'سليق', 'برياني', 'مقلوبة', 'فول', 'تميس', 'معصوب', 'مطبق', 'kabsa', 'mandi', 'biryani'] },
    { cat_ar: 'البيتزا والمعجنات', cat_en: 'Pizza and Pastries', keywords: ['بيتزا', 'فطيرة', 'معجنات', 'منقوشة', 'مناقيش', 'كالزوني', 'pizza', 'pie', 'pastry', 'manakish'] },
    { cat_ar: 'الباستا والمكرونة', cat_en: 'Pasta and Noodles', keywords: ['باستا', 'مكرونة', 'سباغيتي', 'بيني', 'فيتوتشيني', 'نودلز', 'الفريدو', 'pasta', 'spaghetti', 'noodles', 'alfredo'] },
    { cat_ar: 'المأكولات البحرية والأسماك', cat_en: 'Seafood and Fish', keywords: ['سمك', 'جمبري', 'روبيان', 'فيليه', 'سلمون', 'كابوريا', 'كاليماري', 'سي فود', 'fish', 'shrimp', 'prawn', 'seafood', 'salmon'] },
    { cat_ar: 'المقبلات والوجبات الجانبية', cat_en: 'Appetizers and Sides', keywords: ['مقبلات', 'بطاطس', 'ورق عنب', 'حمص', 'متبل', 'سمبوسة', 'فرايز', 'ودجز', 'حلقات بصل', 'fries', 'appetizer', 'hummus', 'sambosa', 'wings', 'wedges'] },
    { cat_ar: 'الشوربات والسلطات', cat_en: 'Soups and Salads', keywords: ['سلطة', 'فتوش', 'تبولة', 'سيزر', 'شوربة', 'عدس', 'كوارع', 'salad', 'soup', 'fattoush', 'caesar'] },
    { cat_ar: 'وجبات الأطفال والكومبو', cat_en: 'Kids Meals and Combos', keywords: ['أطفال', 'اطفال', 'طفل', 'كيدز', 'كومبو', 'بوكس', 'عائلي', 'عائلية', 'وجبة طفل', 'kids', 'combo', 'box', 'family'] },
    { cat_ar: 'المشروبات والعصائر', cat_en: 'Beverages and Juices', keywords: ['عصير', 'بيبسي', 'كولا', 'مشروب', 'ماء', 'موهيتو', 'شاي', 'قهوة', 'ميرندا', 'ديو', 'juice', 'pepsi', 'cola', 'drink', 'water', 'mojito', 'coffee', 'tea'] },
    { cat_ar: 'الحلويات والآيس كريم', cat_en: 'Desserts and Ice Cream', keywords: ['حلا', 'كيك', 'تشيز', 'ايس كريم', 'كريب', 'وافل', 'بسبوسة', 'كنافة', 'لوتس', 'نوتيلا', 'أم علي', 'dessert', 'cake', 'ice cream', 'crepe', 'waffle', 'sweets'] },
    { cat_ar: 'الصوصات والإضافات', cat_en: 'Sauces and Add-ons', keywords: ['صوص', 'ثومية', 'طحينة', 'كتشب', 'مايونيز', 'باربيكيو', 'رانش', 'ديناميت', 'شيدر', 'sauce', 'dip', 'dressing', 'addon'] }
];'''

start_cat = html.find('const CATEGORY_MAP_RULES = [')
if start_cat != -1:
    end_cat = html.find('function smartDetectCategory(itemName) {', start_cat)
    if end_cat != -1:
        html = html[:start_cat] + NEW_CATEGORY_RULES + "\n\n" + html[end_cat:]
        print("✅ Successfully updated CATEGORY_MAP_RULES via slice!")
    else:
        print("⚠️ Could not locate end marker for CATEGORY_MAP_RULES")
else:
    print("⚠️ Could not locate const CATEGORY_MAP_RULES marker")

# Add Offline Appetizing Description Synthesizer
FALLBACK_DESC_SYNTHESIZER = r'''
// 🍳 Smart Sensory Food Description Synthesizer (Instant Offline AI)
function smartSynthesizeFoodDescription(nameAr, catAr, lang = 'AR') {
    const item = String(nameAr || '').toLowerCase();
    const cat = String(catAr || '').toLowerCase();
    
    if (lang === 'AR') {
        if (cat.includes('برجر') || item.includes('برجر')) {
            return "قطعة لحم فاخرة مشوية بعناية مع الخس الطازج، الطماطم، وجبنة الشيدر الذائبة داخل خبز البريوش الطازج.";
        }
        if (cat.includes('شاورما') || item.includes('شاورما')) {
            return "شرائح شاورما طرية متبلة بخلطة التوابل الخاصة، ملفوفة في خبز الصاج الطازج مع صوص الثومية والمخلل.";
        }
        if (cat.includes('مشويات') || item.includes('كباب') || item.includes('أوصال')) {
            return "مشوي على الفحم بتتبيلة مميزة وغنية بالنكهات الأصيلة، يقدم مع صوص الطحينة وخبز التنور الساخن.";
        }
        if (cat.includes('كبسة') || cat.includes('شعبيات') || item.includes('مندي') || item.includes('مضغوط')) {
            return "مطبوخ على الطريقة التقليدية الغنية ببهارات الخليج العطرية مع أرز الحبة الطويلة والمكسرات المقرمشة.";
        }
        if (cat.includes('بيتزا') || item.includes('بيتزا')) {
            return "عجينة إيطالية مخبوزة بالفرن مغطاة بصلصة الطماطم الغنية وجبنة الموزاريلا الفاخرة وأجود الإضافات.";
        }
        if (cat.includes('بروست') || item.includes('مسحب') || item.includes('زنجر')) {
            return "قطع مقرمشة متبلة ومقلية لدرجة الكمال الذهبي، تقدم مع البطاطس المقلية المقرمشة وصوص الثومية الشهي.";
        }
        if (cat.includes('باستا') || item.includes('مكرونة')) {
            return "باستا إيطالية مسلوقة بعناية ومغمورة بالصوص الكريمي الغني والجبنة الفاخرة مع لمسة من الأعشاب العطرية.";
        }
        if (cat.includes('عصائر') || item.includes('عصير') || item.includes('موهيتو')) {
            return "عصير طبيعي منعش محضر من فواكه طازجة مختارة بعناية لإنعاش يومك ومذاق لا يُنسى.";
        }
        if (cat.includes('حلا') || item.includes('كيك') || item.includes('وافل')) {
            return "حلوى فاخرة ولذيذة محضرة بأجود المكونات لتمنحك مذاقاً حالياً وتجربة تدلل حواسك.";
        }
        return "محضر يومياً بأجود المكونات الطازجة لتقديم تجربة طعام استثنائية ومذاق يرضي ذوقك.";
    } else {
        if (cat.includes('burger') || item.includes('burger')) {
            return "Flame-grilled juicy patty served with crisp lettuce, ripe tomatoes, and melted cheddar in a toasted brioche bun.";
        }
        if (cat.includes('shawarma') || item.includes('shawarma')) {
            return "Tender seasoned shawarma strips rolled in fresh saj bread with creamy garlic sauce and crispy pickles.";
        }
        if (cat.includes('grill') || item.includes('kebab')) {
            return "Charcoal-grilled to perfection with authentic aromatic spices, served with tahini dip and fresh tanoor bread.";
        }
        if (cat.includes('rice') || item.includes('mandi') || item.includes('kabsa')) {
            return "Slow-cooked traditional spiced rice dish infused with aromatic Gulf herbs and garnished with roasted nuts.";
        }
        if (cat.includes('pizza')) {
            return "Stone-baked Italian crust topped with slow-simmered tomato sauce, melted mozzarella, and premium toppings.";
        }
        if (cat.includes('broasted') || item.includes('tenders')) {
            return "Crispy golden fried chicken seasoned with special herbs, served with french fries and signature garlic dip.";
        }
        if (cat.includes('pasta')) {
            return "Al dente Italian pasta smothered in a rich savory sauce and finished with freshly grated cheese.";
        }
        if (cat.includes('juice') || item.includes('mojito')) {
            return "Refreshing chilled beverage crafted from premium natural ingredients to revitalise your day.";
        }
        if (cat.includes('dessert') || item.includes('cake')) {
            return "Decadent dessert crafted with finest ingredients for a rich, satisfying sweet indulgence.";
        }
        return "Freshly prepared daily with the finest ingredients to deliver an extraordinary culinary experience.";
    }
}
'''

if 'smartSynthesizeFoodDescription' not in html:
    target_pos = html.find('function smartDetectCategory')
    if target_pos != -1:
        html = html[:target_pos] + FALLBACK_DESC_SYNTHESIZER + '\n' + html[target_pos:]
        print("✅ Injected smartSynthesizeFoodDescription helper!")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("🎉 Saved upgraded index.html!")

# ==============================================================================
# 2. UPGRADE BATCH MACRO ENGINE IN engine_11_features.js
# ==============================================================================

with open(ENGINE_PATH, "r", encoding="utf-8") as f:
    engine = f.read()

NEW_SCENARIOS = '''        'KITCHEN_READY_CANCEL': (ord) => `شريكنا العزيز،

بخصوص الطلب رقم (#${ord}) الذي تم إلغاؤه من قبل العميل بعد استلامه والانتهاء من تجهيزه:
نود إبلاغكم بأنه تم فحص بيانات التذكرة والتأكد من انتهاء التحضير ضمن معيار الـ SLA، وبناءً عليه تم اعتماد التعويض المالي الكامل للمتجر بنسبة 100% وإدراجه في دورة الفواتير القادمة.

شاكرين تعاونكم المستمر معنا،
${agentName} | فريق دعم الشركاء`,

        'QUALITY_DISPUTE': (ord) => `شريكنا العزيز،

شكراً لتواصلكم مع هنقرستيشن بخصوص الاعتراض على شكوى العميل للطلب (#${ord}):
تم تحويل التفاصيل وصور التحضير المرفقة إلى قسم العمليات ومراقبة الجودة لإعادة تدقيق الحالة وإلغاء أي خصم غير مبرر عن متجركم خلال 24 ساعة.

شاكرين حسن تعاونكم،
${agentName} | فريق دعم الشركاء`,

        'VAT_RECONCILIATION': (ord) => `شريكنا العزيز،

بخصوص الاستفسار عن فواتير المبيعات وضريبة القيمة المضافة المرتبطة بالطلب (#${ord}):
نؤكد لكم أن تقرير التسوية الضريبية الأسبوعي متاح للتحميل مباشرة عبر بوابة الشركاء (قسم المالية > تقارير الضريبة)، مع توضيح نسبة الـ 15% وصافي التحويل البنكي بالتفصيل.

شاكرين حسن تعاونكم،
${agentName} | فريق دعم الشركاء`,

        'BRANCH_BUSY_MODE': (ord) => `شريكنا العزيز،

بخصوص طلب تعديل حالة الفرع وتفعيل وضع الانشغال المؤقت (Busy Mode) أو الإيقاف للفرع (#${ord}):
يمكنكم التحكم المباشر بالحالة عبر جهاز التابلت فوراً، كما تم من طرفنا تحديث النظام لحماية تقييم متجركم وتفادي تأخير أي طلبات خلال فترات الضغط.

شاكرين حسن تعاونكم،
${agentName} | فريق دعم الشركاء`'''

if "'KITCHEN_READY_CANCEL'" not in engine:
    marker = "'MENU_UPDATE': (ord) => `"
    end_of_menu_update = engine.find(marker)
    if end_of_menu_update != -1:
        close_brace = engine.find("};", end_of_menu_update)
        if close_brace != -1:
            engine = engine[:close_brace].rstrip() + ",\n\n" + NEW_SCENARIOS + "\n    " + engine[close_brace:]
            print("✅ Successfully added 4 new batch ticket scenarios to engine_11_features.js!")
            with open(ENGINE_PATH, "w", encoding="utf-8") as f:
                f.write(engine)
        else:
            print("⚠️ Could not find closing brace of templateMap")
    else:
        print("⚠️ Could not find MENU_UPDATE marker in templateMap")
else:
    print("ℹ️ Scenarios already present in engine_11_features.js")
