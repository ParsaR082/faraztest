# FRONT.md — نقشه راه بازسازی فرانت فراز بام

> **هدف:** بازسازی کامل UI/UX از صفر — سطح Senior Frontend (۲۰+ سال تجربه)  
> **جهت طراحی:** عکس‌محور (Image-First) · روشن‌تر · شیشه‌ای · صنعتی-مدرن · RTL فارسی  
> **استک:** Django 5 Templates + CSS سفارشی + Vanilla JS + GSAP  
> **این فایل مرجع اصلی agent است** — قبل از هر تسک بخوان، بعد از هر تسک معیار پذیرش را چک کن.

---

## ۰. چرا بازسازی از صفر؟

وضعیت فعلی مشکلات ساختاری دارد که با patch روی `style.css` (~۳۹۰۰ خط) حل نمی‌شود:

| مشکل | علت ریشه‌ای |
|------|-------------|
| بک‌گراند زیر navbar درست نیست | چند رویکرد متضاد (clip-path / top offset / img) روی هم |
| سکشن‌ها شلوغ و بلند | padding ثابت ۱۰۰px + کارت‌های سنگین بدون سیستم فاصله |
| خوانایی ضعیف روی عکس پروضوح | scrim یکنواخت نداریم؛ glass overrideهای پراکنده با `!important` |
| عکس‌محور نیست | blueprint/text-only جایگزین تصویر شده؛ تصویر فقط hero/gallery |
| انیمیشن‌ها ناهماهنگ | GSAP + CSS + inline JS پراکنده |
| CSS غیرقابل نگهداری | یک فایل monolith بدون design tokens منظم |

**راه‌حل:** Design System جدید → CSS modular → HTML section-by-section → JS ماژولار.

---

## ۱. چشم‌انداز طراحی (Design Vision)

### ۱.۱ احساس برند
```
کارخانه واقعی + اجرای حرفه‌ای + اعتماد مهندسی
نه: تمپلیت SaaS · نه: دارک‌مود سنگین · نه: کارت‌های متنی خشک
```

### ۱.۲ اصول طلایی UI
1. **تصویر اول، متن دوم** — هر سکشن حداقل یک نقطه تماس بصری قوی (عکس/ویدیو/تصویر پروژه)
2. **شیشه روی عکس** — متن همیشه روی scrim یا glass panel؛ هرگز مستقیم روی عکس خام
3. **یک سکشن ≈ یک viewport** — کاربر بدون اسکرول زیاد کل سکشن را ببیند
4. **نارنجی = اکشن** — CTA، accent، hover؛ آبی = اعتماد و ساختار
5. **مینیمال ولی پریمیوم** — فضای سفید (negative space) + جزئیات دقیق (border، shadow، typography)

### ۱.۳ مرجع بصری (Mood)
- Industrial editorial: عکس‌های بزرگ full-bleed با overlay گرادیان
- Glass morphism سبک: `blur(16–24px)` + border نیمه‌شفاف
- Magazine layout: asymmetric grid، تصویر ۶۰٪ / متن ۴۰٪
- Progress & trust: آمار با عکس thumbnail + عدد بزرگ

---

## ۲. Design System

### ۲.۱ پالت رنگ (روشن‌تر از قبل)

```css
/* Primary Brand */
--orange:        #ff5722;
--orange-glow:   #ff784e;
--orange-soft:   #ff8d68;
--orange-glass:  rgba(255, 87, 34, 0.22);

/* Trust / Structure */
--blue:          #1a365d;
--blue-light:    #2c5282;
--blue-soft:     #3a6aa3;
--blue-glass:    rgba(26, 54, 93, 0.35);

/* Surfaces — روشن‌تر */
--surface-0:     #2a3f56;          /* body fallback */
--surface-1:     rgba(42, 58, 78, 0.72);   /* card bg */
--surface-2:     rgba(52, 70, 92, 0.82);   /* elevated card */
--surface-glass: rgba(255, 255, 255, 0.10);
--surface-glass-strong: rgba(255, 255, 255, 0.16);

/* Text */
--text-primary:   #f8fafc;
--text-secondary: #e2e8f0;
--text-muted:     #94a3b8;

/* Scrim روی عکس پس‌زمینه */
--scrim-light:    rgba(15, 23, 42, 0.45);
--scrim-medium:   rgba(15, 23, 42, 0.62);
--scrim-heavy:    rgba(15, 23, 42, 0.78);
```

### ۲.۲ تایپوگرافی
| نقش | سایز | وزن |
|-----|------|-----|
| Display (Hero H1) | `clamp(2rem, 5vw, 3.2rem)` | 700 |
| Section Title (H2) | `clamp(1.4rem, 2.8vw, 2rem)` | 700 |
| Card Title (H3) | `clamp(1.05rem, 1.8vw, 1.25rem)` | 600 |
| Body | `0.92rem` | 400 |
| Caption / Label | `0.78–0.84rem` | 500 |
| Stat Number | `clamp(1.8rem, 3.5vw, 2.4rem)` | 700 |

**فونت:** `DigiRastin` (موجود) — fallback: `Vazirmatn` از Google Fonts

### ۲.۳ فاصله‌گذاری (Compact Sections)
```css
--nav-height:     72px;
--section-y:      clamp(48px, 7vh, 72px);    /* قبلاً 100px */
--section-gap:    clamp(16px, 2.5vw, 24px);
--card-pad:       clamp(16px, 2.5vw, 24px);
--container:      1280px;
--radius-sm:      8px;
--radius-md:      14px;
--radius-lg:      20px;
--radius-xl:      28px;
```

### ۲.۴ تصویر — قوانین اجباری
| قانون | جزئیات |
|-------|--------|
| Hero | full-viewport عکس کارخانه + glass panel متن |
| Stats | thumbnail ۷۲×۷۲ یا ۸۰×۸۰ per card (از admin یا static) |
| Products | تصویر ۴۵٪ عرض کارت — `object-fit: cover` |
| About | عکس کارخانه/تیم ۵۰٪ سکشن — magazine split |
| Team | عکس دایره‌ای ۹۶px+ per member |
| Videos | poster thumbnail + player بزرگ |
| Projects | تصویر پروژه ۷۰٪ کارت — overlay gradient + متن |
| Gallery | Bento grid — عکس‌های بزرگ و کوچک |
| CTA | عکس پروژه/کارخانه پس‌زمینه |
| همه img | `loading="lazy"` + `alt` معنادار + WebP |

### ۲.۵ کامپوننت‌های پایه
```
.btn-primary      → نارنجی solid + glow hover
.btn-secondary    → glass outline
.btn-ghost        → متن + آیکون
.glass-panel      → blur + border + scrim
.img-frame        → border radius + hover zoom
.image-card       → عکس بالا + متن پایین
.split-section    → 50/50 image + content
.bento-grid       → gallery asymmetric
.stat-card        → thumb + number + progress bar
.badge            → مستطیل گوشه‌گرد (نه pill)
```

---

## ۳. معماری فایل‌ها (بازسازی)

### ۳.۱ ساختار CSS جدید
```
static/css/
├── tokens.css          ← متغیرها، فونت، reset
├── base.css            ← body, container, typography
├── layout.css          ← section, grid, split
├── components.css      ← buttons, glass, badges, forms
├── nav.css             ← header, mobile menu
├── sections/
│   ├── hero.css
│   ├── stats.css
│   ├── products.css
│   ├── about.css
│   ├── team.css
│   ├── videos.css
│   ├── features.css
│   ├── services.css
│   ├── anatomy.css     ← desktop only
│   ├── process.css
│   ├── projects.css
│   ├── gallery.css
│   ├── faq.css
│   └── contact.css
├── utilities.css       ← reveal, reduced-motion
└── style.css           ← @import همه (entry point)
```

### ۳.۲ ساختار JS جدید
```
static/js/
├── main.js             ← bootstrap
├── nav.js              ← header, mobile menu, scroll spy
├── animations.js       ← GSAP reveals, counters
├── background.js       ← page bg (یک منبع حقیقت)
├── gallery.js          ← lightbox
├── video.js            ← player
├── anatomy.js          ← 3D desktop only
└── process.js          ← timeline + accordion
```

### ۳.۳ Templates
```
templates/
├── base.html           ← head, nav, footer, bg, scripts
└── core/
    └── home.html       ← فقط <section> blocks — بدون inline style/script
```

---

## ۴. بک‌گراند — راه‌حل نهایی (یک‌بار برای همیشه)

### مشکل
عکس `factory_farazbam.webp` پروضوح است؛ اگر full-viewport fixed باشد زیر navbar clip می‌شود یا بخشی دیده نمی‌شود.

### راه‌حل تأییدشده
```html
<!-- base.html -->
<div class="page-bg" aria-hidden="true">
  <img src="factory_farazbam.webp" alt="" />
  <div class="page-bg__scrim"></div>
</div>
```

```css
.page-bg {
  position: fixed;
  inset: 0;
  z-index: -2;
}
.page-bg img {
  width: 100%; height: 100%;
  object-fit: cover;
  object-position: center;
}
.page-bg__scrim {
  position: absolute; inset: 0;
  background: linear-gradient(
    180deg,
    rgba(15,23,42,0.25) 0%,
    rgba(15,23,42,0.12) 40%,
    rgba(15,23,42,0.35) 100%
  );
}
/* navbar شفاف — عکس از پشت دیده می‌شود */
.header-shell {
  background: rgba(255, 87, 34, 0.38);
  backdrop-filter: blur(24px) saturate(1.4);
}
```

**قوانین:**
- هیچ `clip-path` روی background
- هیچ `top: var(--nav-height)` روی background
- `global-background-effects` opacity ≤ 0.12
- هر سکشن scrim خودش را دارد (نه overlay کل صفحه)

---

## ۵. فهرست سکشن‌ها و ترتیب صفحه

| # | ID | عنوان | نقش تصویری |
|---|-----|-------|------------|
| 0 | `hero` | قهرمان | عکس کارخانه full-viewport |
| 1 | `stats` | آمار | ۴ کارت با thumbnail + progress bar |
| 2 | `products` | محصولات | کارت افقی — عکس ۴۵٪ |
| 3 | `about` | درباره | split 50/50 — عکس کارخانه |
| 4 | `team` | تیم | عکس پرسنل دایره‌ای |
| 5 | `videos` | ویدیوها | player + thumbnail strip |
| 6 | `features` | مزایا | آیکون + اختیاری: عکس پس‌زمینه subtle |
| 7 | `services` | خدمات | شماره + متن (بدون عکس اجباری) |
| 8 | `anatomy` | ساختار لایه‌ای | 3D desktop only |
| 9 | `process` | فرآیند همکاری | timeline ۶ مرحله |
| 10 | `projects` | نمونه پروژه‌ها | کارت عکس‌محور — تصویر ۷۰٪ |
| 11 | `gallery` | گالری | Bento grid عکس |
| 12 | `cta` | بنر اقدام | عکس پروژه پس‌زمینه |
| 13 | `faq` | سوالات | متن — glass accordion |
| 14 | `contact` | تماس | فرم + info cards |

---

## ۶. تسک‌ها — فازبندی اجرا

> **قانون Git:** هر تسک → `feat/front-XX-<name>` → commit → push → merge `main`

### فاز ۰ — زیرساخت (اولویت بالا)
| ID | تسک | برنچ | فایل‌ها |
|----|-----|------|---------|
| F00 | Design tokens + CSS architecture | `feat/front-00-tokens` | `tokens.css`, `base.css`, `style.css` imports |
| F01 | Background + Navbar glass | `feat/front-01-bg-nav` | `base.html`, `nav.css`, `background.js` |
| F02 | Layout system (section compact) | `feat/front-02-layout` | `layout.css`, `components.css` |
| F03 | JS modular split | `feat/front-03-js-modules` | `static/js/*.js`, `base.html` scripts |

**معیار پذیرش فاز ۰:**
- [ ] عکس پس‌زمینه کامل زیر navbar دیده می‌شود
- [ ] navbar شیشه‌ای نارنجی — عکس از پشت خوانا
- [ ] `--section-y` ≤ 72px
- [ ] هیچ `!important` glass سراسری روی blueprint cards

---

### فاز ۱ — سکشن‌های کلیدی (عکس‌محور)
| ID | تسک | برنچ | تمرکز تصویری |
|----|-----|------|--------------|
| F10 | Hero redesign | `feat/front-10-hero` | full-bleed factory + glass copy + trust chips |
| F11 | Stats redesign | `feat/front-11-stats` | thumbnail per stat + animated progress + orange glass |
| F12 | Products redesign | `feat/front-12-products` | horizontal image-first cards |
| F13 | About redesign | `feat/front-13-about` | magazine split — factory photo 50% |
| F14 | Projects redesign | `feat/front-14-projects` | image-dominant cards — NO blueprint-only |

**معیار پذیرش فاز ۱:**
- [ ] هر سکشن در ۱ viewport (۱۰۸۰p) جا می‌شود
- [ ] حداقل ۵ نقطه تماس تصویری در ۵ سکشن اول
- [ ] متن روی scrim/glass — WCAG contrast قابل قبول

---

### فاز ۲ — سکشن‌های ثانویه
| ID | تسک | برنچ |
|----|-----|------|
| F20 | Team section | `feat/front-20-team` |
| F21 | Videos section | `feat/front-21-videos` |
| F22 | Gallery bento | `feat/front-22-gallery` |
| F23 | Process timeline | `feat/front-23-process` |
| F24 | Features + Services | `feat/front-24-features-services` |

---

### فاز ۳ — پایان و polish
| ID | تسک | برنچ |
|----|-----|------|
| F30 | FAQ + Contact | `feat/front-30-faq-contact` |
| F31 | CTA banner | `feat/front-31-cta` |
| F32 | Footer polish | `feat/front-32-footer` |
| F33 | Animation polish | `feat/front-33-animations` |
| F34 | Responsive QA (375/768/1280) | `feat/front-34-responsive` |
| F35 | Performance (lazy, preload, WebP) | `feat/front-35-perf` |
| F36 | حذف CSS/JS legacy | `feat/front-36-cleanup` |

---

## ۷. مشخصات تفصیلی هر سکشن

### F10 — Hero
```
Layout: full-viewport (min-height: 92vh)
Background: page-bg visible through hero (no duplicate bg image)
Content: glass panel راست (RTL) — نارنجی شیشه‌ای
Elements:
  - eyebrow badge
  - H1 با gradient span
  - 2 CTA button
  - 3 trust chip با آیکون SVG
  - scroll indicator
Image rule: عکس کارخانه از page-bg — hero خودش عکس جدا ندارد
```

### F11 — Stats
```
Layout: intro چپ + ۴ کارت عمودی راست (یا ۲×۲ در تبلت)
Per card:
  - stat-thumb: 72×72 image (admin cover_image یا static fallback)
  - stat-num: animated counter
  - stat-label
  - progress bar (scroll trigger)
Style: orange glass card — نه blueprint خشک
Height target: کل سکشن ≤ 85vh
```

### F12 — Products
```
Layout: تک ستونه — هر محصول یک ردیف افقی
Per card:
  - product-media: 42% width, min-height 160px
  - product-body: name, desc, feature tags, specs
  - badge «ویژه» روی گوشه عکس
Hover: image scale 1.05 + border glow orange
```

### F13 — About
```
Layout: CSS grid 1fr 1fr — image | content
Image: aspect-ratio 4/5, factory photo, badge overlay (+۱۵ سال)
Content: title, 2 paragraphs, 3 feature mini-cards, CTA link
Background: glass panel کل سکشن
```

### F14 — Projects
```
Layout: masonry یا 2-col grid
Per card:
  - project-image: 65% card height, object-fit cover
  - gradient overlay bottom
  - type badge (rectangular)
  - title + description + meta row
Hover: image zoom + shine sweep
NO: blueprint text-only cards
YES: project.image from admin
```

### F23 — Process
```
Desktop: 6-node horizontal timeline RTL + SVG dashed connector
Mobile: accordion (step 1 open)
Steps: تماس → بازدید → پیشنهاد → قرارداد → اجرا → تحویل
Animation: stroke-dashoffset 1.5s + staggered node activation
```

### F22 — Gallery
```
Bento: 4-col grid, featured 2×2
Click: lightbox fullscreen
Mix: factory + project + production images
```

---

## ۸. انیمیشن‌ها

| انیمیشن | ابزار | مدت |
|---------|-------|-----|
| Section reveal | GSAP ScrollTrigger | 0.45s ease-out |
| Stat counter | GSAP / IntersectionObserver | 1.1s |
| Progress bar | CSS transition + IO | 1s |
| Process timeline | SVG stroke-dashoffset + IO | 1.5s linear |
| Image hover zoom | CSS transform | 0.5s |
| Navbar scroll | CSS class toggle | 0.35s |
| Border draw (optional) | CSS 4-edge | 400ms |

**`prefers-reduced-motion: reduce`** → همه غیرفعال، state نهایی فوری

---

## ۹. ریسپانسیو

| Breakpoint | رفتار |
|------------|-------|
| `< 768px` | تک ستونه، stats 1col، process accordion، anatomy hidden |
| `768–1024px` | ۲ ستونه grids، compact padding |
| `> 1024px` | full layout، anatomy visible، timeline horizontal |

**تست اجباری:** 375px · 768px · 1280px · 1440px

---

## ۱۰. دستور اجرا برای Agent

### قبل از شروع هر تسک
```powershell
cd d:\projects\SepidBam\farazbam
git checkout main
git pull
git checkout -b feat/front-XX-<name>
```

### حین تسک
1. فقط فایل‌های مرتبط با تسک فعلی را تغییر بده
2. از design tokens استفاده کن — hex hardcode ممنوع (جز در tokens.css)
3. هر سکشن باید عکس داشته باشد (جز services/faq)
4. تست visual روی http://127.0.0.1:8002/

### بعد از تسک
```powershell
git add <files>
git commit -m "feat(front): <توضیح کوتاه>"
git push -u origin feat/front-XX-<name>
# merge to main
```

### سرور لوکال
```powershell
cd d:\projects\SepidBam\farazbam
..\venv\Scripts\python.exe manage.py runserver 8002
```

---

## ۱۱. چک‌لیست کیفیت نهایی (Definition of Done)

### بصری
- [ ] سایت روشن‌تر از نسخه فعلی — نه تاریک مطلق
- [ ] پالت نارنجی + آبی حفظ شده
- [ ] ≥ ۱۰ نقطه تماس تصویری در کل صفحه
- [ ] هیچ سکشنی بیش از ~۹۰vh ارتفاع ندارد (جز anatomy)
- [ ] navbar شیشه‌ای — عکس از پشت دیده می‌شود

### فنی
- [ ] CSS modular — style.css فقط imports
- [ ] یک منبع حقیقت برای background
- [ ] بدون inline style در home.html
- [ ] بدون inline script در home.html
- [ ] `loading="lazy"` روی همه img
- [ ] `prefers-reduced-motion` رعایت شده

### دسترسی
- [ ] RTL کامل
- [ ] alt روی تصاویر
- [ ] focus ring روی interactive elements
- [ ] semantic HTML (section, h2, article)

### عملکرد
- [ ] preload فونت + hero image
- [ ] IntersectionObserver (نه scroll listener) برای انیمیشن‌ها
- [ ] anatomy فقط desktop

---

## ۱۲. ترتیب پیشنهادی اجرا

```
F00 → F01 → F02 → F03        (زیرساخت)
  ↓
F10 → F11 → F12 → F13 → F14  (سکشن‌های عکس‌محور اصلی)
  ↓
F20 → F21 → F22 → F23 → F24  (سکشن‌های ثانویه)
  ↓
F30 → F31 → F32 → F33        (پایان)
  ↓
F34 → F35 → F36              (QA + cleanup)
```

**تخمین:** ۱۸–۲۲ تسک · هر تسک ۱ PR جدا

---

## ۱۳. منابع داده (Django Admin)

| مدل | فیلد تصویر | سکشن |
|-----|-----------|------|
| `Stat` | `cover_image` | stats |
| `Product` | `image` | products |
| `TeamMember` | `photo` | team |
| `MediaItem` | `image` | gallery, videos |
| `Project` | `image` | projects |
| `SiteSettings` | — | hero texts, about |

**Placeholder static:** `factory_farazbam.webp`, `stat-*.jpg` در `static/img/`

---

## ۱۴. نکات ممنوع (Anti-Patterns)

❌ clip-path روی page background  
❌ یک فایل CSS ۴۰۰۰ خطی بدون ساختار  
❌ کارت متنی بدون عکس در projects/stats/about  
❌ pill badge (`border-radius: 999px`) برای نوع پروژه  
❌ `!important` glass override سراسری  
❌ padding 100px روی همه section‌ها  
❌ stock photo URL خارجی — فقط static/admin media  
❌ over-engineering (framework جدید، React، Tailwind کامل)  

---

## ۱۵. شروع تسک بعدی

**پیشرفت فعلی:**
- ✅ فاز ۰–۳ کامل (F03 JS modular انجام شد)
- ✅ F32 Footer · F33 Animations · F34 Responsive · F35 Performance · F36 Legacy حذف شد
- 🎉 بازسازی فرانت طبق front.md تکمیل شد

**نگهداری بعدی:** تست visual روی 375/768/1280 · آپلود عکس‌ها از ادمین

---

*آخرین به‌روزرسانی: ۱۴۰۵/۰۳/۲۴ — نسخه ۱.۰*
*نگهدارنده: Agent Frontend — مرجع: farazbam/front.md*
