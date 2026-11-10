#!/usr/bin/env python3
"""Builds the bilingual profile site: index.html (Arabic) and en/index.html (English)."""
import html, os

LINKEDIN = "https://www.linkedin.com/in/mohammed-al-ibrahim-0b7192275/"
GITHUB = "https://github.com/m-alibrahim"
EMAIL = "m.alibrahim.ksa@gmail.com"
WHATSAPP = "https://wa.me/966595521229"
REPO = "https://github.com/m-alibrahim/m-alibrahim.github.io/tree/main/projects/"

C = {
"ar": dict(
  lang="ar", dir="rtl", other_label="English", other_href="en/", self_path="",
  title="محمد البراهيم | مستشار تطوير أعمال",
  desc="ملف أعمال محمد البراهيم، مستشار تطوير أعمال في الرياض: الخدمات القانونية والمهنية، المنافسات الحكومية، الحسابات الرئيسية والشراكات.",
  name="محمد البراهيم", role="مستشار تطوير أعمال", place="الرياض، السعودية",
  statement="أساعد شركات المحاماة والخدمات المهنية على كسب عملاء جدد: من قوائم الاستهداف وحملات التواصل، إلى عروض المنافسات الحكومية والشراكات.",
  cta_contact="راسلني", cta_cv="حمّل السيرة الذاتية", cv_file="assets/cv/Mohammed_Alibrahim_CV_Arabic.pdf",
  nav=[("about","نبذة"),("focus","مجالات التركيز"),("results","نتائج"),("experience","الخبرة"),("work","أعمال"),("now","الآن"),("contact","تواصل")],
  skip="انتقل إلى المحتوى", theme_label="تبديل الوضع الفاتح والداكن", photo_alt="صورة محمد البراهيم",
  about_h="نبذة",
  about=[
    "أعمل في تطوير الأعمال منذ أكثر من ست سنوات، أغلبها في القطاع القانوني والاستشاري في الرياض، مع عملاء من القطاعين الخاص والحكومي.",
    "درست الشريعة، فأفهم ما يقدمه المحامي قبل أن أعرضه على العميل. وأدرس حاليًا ماجستير الذكاء الاصطناعي، وأبني بنفسي الأدوات التي يحتاجها عملي: نظام لمتابعة العملاء، ونماذج استقبال، وحملات مبنية على البحث.",
    "ما يهمني في النهاية نتيجة تُقاس: إيراد، أو عقد موقّع، أو عرض فائز.",
  ],
  focus_h="مجالات التركيز",
  focus=[
    ("تطوير الأعمال للخدمات القانونية والمهنية","تحديد العملاء المناسبين حسب القطاع والحجم، والوصول إليهم بحملات مدروسة، وتحويل الخدمة إلى عرض واضح: باقة سنوية بنطاق محدد وسعر مفهوم."),
    ("المنافسات والعروض","قراءة كراسة الشروط، وإعداد العرض الفني والمالي والتسعير، وتنسيق فريق العرض حتى التقديم على منصة اعتماد."),
    ("إدارة الحسابات الرئيسية","متابعة كبار العملاء، وتوسيع الخدمات التي يستخدمونها، وضبط استهلاك العقد حتى يبقى مجديًا للطرفين."),
    ("الشراكات والتحالفات","تكوين تحالفات بين شركات لمشاريع ومنافسات لا تستطيع جهة واحدة تقديمها منفردة."),
  ],
  results_h="نتائج بالأرقام",
  results=[
    ("63%","نمو في إيرادات شركة محاماة ساهمت فيه أثناء إدارتي لتطوير الأعمال فيها."),
    ("29%","متوسط تجاوز المستهدف الربعي خلال عام 2026."),
    ("27","عرضًا فنيًا وماليًا أعددته لمنافسات حكومية على منصة اعتماد، في ثلاث جهات عمل."),
    ("+35,000","رسالة عبر البريد ولينكدإن والهاتف، تحوّل 4% منها إلى عملاء محتملين مؤهلين."),
    ("40%","زيادة في إيرادات وحدة أعمال بعد إطلاق خدمة استشارية قصيرة المدى."),
    ("المركز الثاني","في برنامج زمالة الابتكار بمركز الابتكار في منشآت، لمشروع كوّنت له تحالفًا من ثلاث شركات."),
  ],
  exp_h="الخبرة",
  exp=[
    ("سبتمبر 2025 – الآن","مدير تطوير أعمال","شركة الزريقي للمحاماة والاستشارات القانونية","أقود فريق تطوير الأعمال: حسابات الشركات، وباقات الرعاية السنوية، وحملات التواصل، وعروض المنافسات، وتقارير الأداء للإدارة.",["باقات سنوية","حملات تواصل","منصة اعتماد","إدارة علاقات العملاء"]),
    ("يناير – سبتمبر 2025","أخصائي أول تطوير أعمال","فيرست أكسس للاستشارات","حلول توظيف للشركات، وعروض لمنافسات حكومية ولعملاء من القطاع الخاص، وتفاوض على عقود طويلة المدى.",["حلول التوظيف","عروض","تفاوض"]),
    ("2023 – 2025","مسؤول تطوير أعمال","مرصد الخبراء","أسست وحدة أعمال جديدة من الصفر لترشيح المستشارين للمنافسات ودعم فرق العروض، بإشراف مباشر من الرئيس التنفيذي.",["تأسيس وحدة أعمال","منافسات","تحالفات"]),
    ("2020 – 2023","محلل عمليات أعمال","شركة الصخور العربية للمقاولات","الجانب المالي لتخطيط المشاريع من مراجعة عروض الأسعار إلى إتمام العقود، مع الإشراف على مبيعات الجملة.",["عقود","مبيعات الجملة","عمليات"]),
    ("2019","متدرب تعاوني","مكتب ابن صالح للمحاماة","متابعة العملاء وتحديث سجلاتهم.",[]),
  ],
  edu_h="التعليم والشهادات",
  edu=[
    "ماجستير الذكاء الاصطناعي، جامعة ميدأوشن (قيد الدراسة، التخرج المتوقع 2028)",
    "بكالوريوس الشريعة، جامعة الإمام محمد بن سعود الإسلامية (2020)",
    "شهادة Legal Engineer من Harvey، ودورات Anthropic Academy في الذكاء الاصطناعي (2026)",
  ],
  work_h="نماذج من أعمالي",
  work_note="نسخ مفتوحة من أدوات بنيتها لعملي. حُذفت منها أسماء العملاء وشعاراتهم وبياناتهم.",
  demo="جرّب النموذج", source="المصدر", view="اعرض",
  work=[
    ("متتبّع مسار المبيعات","نظام خفيف لإدارة علاقات العملاء لفريق تطوير أعمال: حسابات، وفرص حسب المرحلة، ومهام، وعقود، وتحصيل.","projects/bd-pipeline-tracker/","bd-pipeline-tracker"),
    ("استبيان احتياج العميل","استبيان بالعربية والإنجليزية يقدّر احتياج العميل السنوي من الخدمات، وتصل إجاباته بالبريد لتُبنى عليها الباقة المقترحة.","projects/client-needs-questionnaire/","client-needs-questionnaire"),
    ("فحص الأهلية","تقييم ذاتي قصير يخبر الزائر خلال دقيقة إن كان مؤهلًا للخدمة، ثم يحوّل إجاباته للفريق عبر واتساب. بُني لحملة قانونية محددة المدة.","projects/eligibility-checker/","eligibility-checker"),
    ("ضبط نطاق الباقات السنوية","خطة تفاعلية لتحويل الباقات القانونية السنوية من مفتوحة إلى محددة النطاق: مستويات الخدمة، وحدود الاستخدام، وخطة التطبيق.","projects/retainer-scoping/",None),
    ("استقبال العملاء","يحوّل ملاحظات أول مكالمة مع العميل إلى ملف يستكمله العميل بنفسه: ملخص، وأسئلة ناقصة، وقائمة مستندات.","projects/client-intake/","client-intake"),
    ("نظام الاتصال البارد","قائمة اتصال مع موجز لكل عميل محتمل: خلفية صانع القرار، وسبب التواصل، ونقاط الحديث. يُعرض هنا ببيانات افتراضية.","projects/cold-calling-system/","cold-calling-system"),
    ("منصة تقييم المرشحين","أداة توظيف منظمة: تقييمات بدرجات من عدة مقابلين، ومقارنة النتائج، وتصدير تقرير.","projects/candidate-evaluation/","candidate-evaluation"),
    ("حزمة استهداف 100 عميل لشركات التوظيف","سلسلة مهارات ذكاء اصطناعي تحوّل موقع شركة توظيف إلى 100 شركة مستهدفة مع صنّاع القرار ورسائل تواصل مخصصة.",None,"recruitment-dream-100-toolkit"),
    ("مهارات ذكاء اصطناعي للعمل القانوني والعروض","ثلاث مهارات: عروض المنافسات من الكراسة إلى الملف النهائي، وملفات استقبال العملاء، وحجب البيانات الحساسة في الملفات.",None,"claude-skills"),
    ("موقع رواج للورود والهدايا","موقع كامل لمشروع شخصي: المتجر، والمناسبات، والاشتراكات، وقسم هدايا الشركات.","projects/rawaj-website/",None),
  ],
  now_h="الآن", now_updated="آخر تحديث: نوفمبر 2026",
  now=[
    "أدرس ماجستير الذكاء الاصطناعي في جامعة ميدأوشن.",
    "أبني أدوات ذكاء اصطناعي لعمل تطوير الأعمال: كتابة عروض المنافسات، واستقبال العملاء، وبناء قوائم الاستهداف.",
    "منفتح على فرص ومشاريع في تطوير الأعمال، خصوصًا في القطاع القانوني والاستشاري.",
  ],
  contact_h="تواصل",
  contact_p="للتعاون أو الاستفسار، راسلني بالطريقة الأنسب لك. أرد غالبًا خلال يومي عمل.",
  c_email="البريد الإلكتروني", c_wa="واتساب", c_li="لينكدإن", c_gh="جيت هب",
  mail_subject="استفسار عن تطوير الأعمال",
  footer="© 2026 محمد البراهيم",
),
"en": dict(
  lang="en", dir="ltr", other_label="العربية", other_href="../", self_path="en/",
  title="Mohammed Alibrahim | Business Development Consultant",
  desc="Profile of Mohammed Alibrahim, a business development consultant in Riyadh: legal and professional services, government tenders, key accounts and partnerships.",
  name="Mohammed Alibrahim", role="Business Development Consultant", place="Riyadh, Saudi Arabia",
  statement="I help law firms and professional services companies win new clients: target lists and outreach, government tender proposals, and partnerships.",
  cta_contact="Email me", cta_cv="Download CV", cv_file="assets/cv/Mohammed_Alibrahim_CV.pdf",
  nav=[("about","About"),("focus","Focus areas"),("results","Results"),("experience","Experience"),("work","Work"),("now","Now"),("contact","Contact")],
  skip="Skip to content", theme_label="Switch between light and dark mode", photo_alt="Portrait of Mohammed Alibrahim",
  about_h="About",
  about=[
    "I've worked in business development for more than six years, mostly in legal and consulting services in Riyadh, with private and government clients.",
    "I studied Islamic law, so I understand what a lawyer offers before I put it in front of a client. I'm now studying for an MSc in artificial intelligence, and I build the tools my work needs myself: a client pipeline tracker, intake forms, and research-led campaigns.",
    "What I care about is a result you can measure: revenue, a signed contract, or a winning bid.",
  ],
  focus_h="Focus areas",
  focus=[
    ("Business development for legal and professional services","Finding the right clients by sector and size, reaching them with planned campaigns, and turning the service into a clear offer: an annual retainer with a defined scope and a price people understand."),
    ("Tenders and proposals","Reading the RFP, preparing the technical and financial proposal and pricing, and coordinating the bid team through to submission on Etimad."),
    ("Key account management","Looking after major clients, growing the services they use, and keeping retainer usage in line with fees so the contract works for both sides."),
    ("Partnerships and alliances","Bringing companies together for projects and tenders that no single firm could deliver alone."),
  ],
  results_h="Results in numbers",
  results=[
    ("63%","Revenue growth at a law firm, which I contributed to while leading its business development."),
    ("29%","Average amount by which I exceeded quarterly targets in 2026."),
    ("27","Technical and financial proposals prepared for government tenders on Etimad, across three employers."),
    ("35,000+","Messages sent by email, LinkedIn and phone, with 4% turning into qualified leads."),
    ("40%","Increase in a business unit's revenue after launching a short-term consulting service."),
    ("2nd place","In the Innovation Fellowship Program at Monsha'at Innovation Center, for a project I formed a three-company alliance to deliver."),
  ],
  exp_h="Experience",
  exp=[
    ("Sep 2025 – Present","Business Development Manager","Al-Zoriqy Law Firm","I lead the business development team: corporate accounts, annual retainer packages, outreach campaigns, tender proposals, and performance reporting to management.",["Retainer packages","Outreach","Etimad","CRM"]),
    ("Jan – Sep 2025","Senior Business Development Associate","First Access Consulting","Recruitment solutions for companies, proposals for government tenders and private clients, and negotiation of long-term agreements.",["Recruitment solutions","Proposals","Negotiation"]),
    ("2023 – 2025","Business Development Officer","Experts Observatory","Set up a new business unit from scratch for consultant nomination and bid team support, reporting directly to the CEO.",["New business unit","Tenders","Alliances"]),
    ("2020 – 2023","Business Operations Analyst","Arabian Rock Contracting","The financial side of project planning, from reviewing quotations to finalizing contracts, plus oversight of wholesale sales.",["Contracts","Wholesale sales","Operations"]),
    ("2019","Co-op Trainee","Binsaleh Law Firm","Client follow-up and keeping client records up to date.",[]),
  ],
  edu_h="Education and certificates",
  edu=[
    "MSc Artificial Intelligence, Midocean University (in progress, expected 2028)",
    "Bachelor of Islamic Law (Sharia), Imam Mohammad Ibn Saud Islamic University (2020)",
    "Legal Engineer certificate from Harvey, and Anthropic Academy AI courses (2026)",
  ],
  work_h="Selected work",
  work_note="Open versions of tools I built for my work. Client names, logos and data have been removed.",
  demo="Try the demo", source="Source", view="View",
  work=[
    ("BD pipeline tracker","A lightweight CRM for a business development team: accounts, opportunities by stage, tasks, contracts and collections.","projects/bd-pipeline-tracker/","bd-pipeline-tracker"),
    ("Client needs questionnaire","A bilingual questionnaire that estimates a client's annual service needs. Answers arrive by email and feed the proposed retainer.","projects/client-needs-questionnaire/","client-needs-questionnaire"),
    ("Eligibility checker","A short self-assessment that tells a visitor within a minute whether they may qualify, then passes their answers to the team on WhatsApp. Built for a time-limited legal campaign.","projects/eligibility-checker/","eligibility-checker"),
    ("Retainer scoping and usage control","An interactive plan for moving annual legal retainers from open-ended to scoped: service tiers, usage limits and rollout.","projects/retainer-scoping/",None),
    ("Client intake","Turns notes from a first client call into a file the client completes: a summary, open questions and a document checklist.","projects/client-intake/","client-intake"),
    ("Cold-calling system","A calling queue with a brief for each prospect: decision-maker background, reason to call and talking points. Shown here with fictional data.","projects/cold-calling-system/","cold-calling-system"),
    ("Candidate evaluation platform","A structured hiring tool: scored evaluations from several interviewers, side-by-side comparison and a report export.","projects/candidate-evaluation/","candidate-evaluation"),
    ("Dream 100 toolkit for recruitment agencies","A chain of AI skills that turns an agency's website into 100 target companies with decision-makers and tailored outreach.",None,"recruitment-dream-100-toolkit"),
    ("AI skills for legal work and bids","Three skills: tender proposals from RFP to final file, client intake files, and redaction of sensitive data in documents.",None,"claude-skills"),
    ("Rawaj flowers and gifts website","A full website for a personal venture: storefront, occasions, subscriptions and corporate gifting.","projects/rawaj-website/",None),
  ],
  now_h="Now", now_updated="Last updated: November 2026",
  now=[
    "Studying for an MSc in artificial intelligence at Midocean University.",
    "Building AI tools for business development work: tender proposals, client intake and target lists.",
    "Open to business development roles and projects, especially in legal and consulting services.",
  ],
  contact_h="Contact",
  contact_p="For work or questions, reach me whichever way suits you. I usually reply within two working days.",
  c_email="Email", c_wa="WhatsApp", c_li="LinkedIn", c_gh="GitHub",
  mail_subject="Business development enquiry",
  footer="© 2026 Mohammed Alibrahim",
),
}



def e(s): return html.escape(s, quote=True)

def page(c):
    R = "../" if c["lang"] == "en" else ""
    from urllib.parse import quote
    mailto = f"mailto:{EMAIL}?subject={quote(c['mail_subject'])}"
    nav = "".join(f'<li><a href="#{i}"><span class="tick"></span>{e(t)}</a></li>' for i, t in c["nav"])
    about = "".join(f"<p>{e(p)}</p>" for p in c["about"])
    focus = "".join(f"<li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in c["focus"])
    results = "".join(f'<div class="fig"><dt>{e(n)}</dt><dd>{e(d)}</dd></div>' for n, d in c["results"])
    exp = ""
    for when, title, org, d, tags in c["exp"]:
        chips = "".join(f"<li>{e(t)}</li>" for t in tags)
        exp += f'<li class="row"><div class="when">{e(when)}</div><div><h3>{e(title)}<span class="org">{e(org)}</span></h3><p>{e(d)}</p>{"<ul class=chips>"+chips+"</ul>" if chips else ""}</div></li>'
    edu = "".join(f"<li>{e(x)}</li>" for x in c["edu"])
    work = ""
    for title, d, demo, src in c["work"]:
        links = ""
        if demo: links += f'<a href="{R}{demo}">{e(c["demo"] if src else c["view"])}</a>'
        if src: links += f'<a href="{REPO}{src}">{e(c["source"] if demo else c["view"])}</a>'
        work += f'<li class="row work"><div><h3>{e(title)}</h3><p>{e(d)}</p></div><div class="links">{links}</div></li>'
    now = "".join(f"<li>{e(x)}</li>" for x in c["now"])
    font = "IBM Plex Sans Arabic" if c["lang"] == "ar" else "Inter"
    return f'''<!DOCTYPE html>
<html lang="{c["lang"]}" dir="{c["dir"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(c["title"])}</title>
<meta name="description" content="{e(c["desc"])}">
<link rel="canonical" href="https://m-alibrahim.github.io/{c["self_path"]}">
<link rel="alternate" hreflang="ar" href="https://m-alibrahim.github.io/">
<link rel="alternate" hreflang="en" href="https://m-alibrahim.github.io/en/">
<meta property="og:title" content="{e(c["title"])}">
<meta property="og:description" content="{e(c["desc"])}">
<meta property="og:image" content="https://m-alibrahim.github.io/assets/og.jpg">
<meta property="og:type" content="profile">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0d1730">
<script>(function(){{var t=(location.search.match(/theme=(dark|light)/)||[])[1];try{{t=t||localStorage.getItem("theme")}}catch(e){{}}if(!t)t=matchMedia("(prefers-color-scheme: light)").matches?"light":"dark";document.documentElement.dataset.theme=t}})()</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{R}assets/site.css">
<style>body{{font-family:"{font}","IBM Plex Sans Arabic","Inter",system-ui,sans-serif}}</style>
</head>
<body>
<a class="skip" href="#main">{e(c["skip"])}</a>
<div class="glow" aria-hidden="true"></div>
<div class="page">
<header class="intro">
  <div class="intro-top">
    <img class="photo" src="{R}assets/mohammed.jpg" width="112" height="112" alt="{e(c["photo_alt"])}">
    <h1>{e(c["name"])}</h1>
    <p class="role">{e(c["role"])}<span class="place">{e(c["place"])}</span></p>
    <p class="statement">{e(c["statement"])}</p>
    <div class="cta">
      <a class="btn primary" href="{mailto}">{e(c["cta_contact"])}</a>
      <a class="btn" href="{R}{c["cv_file"]}" download>{e(c["cta_cv"])}</a>
    </div>
    <nav aria-label="{e(c["nav"][0][1])}"><ul>{nav}</ul></nav>
  </div>
  <div class="intro-bottom">
    <a href="{LINKEDIN}">{e(c["c_li"])}</a>
    <a href="{GITHUB}">{e(c["c_gh"])}</a>
    <a href="{WHATSAPP}">{e(c["c_wa"])}</a>
    <span class="spacer"></span>
    <a class="lang" href="{c["other_href"]}" lang="{"en" if c["lang"]=="ar" else "ar"}">{e(c["other_label"])}</a>
    <button class="theme" type="button" aria-label="{e(c["theme_label"])}"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M12 3a9 9 0 1 0 0 18V3z"/><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>
  </div>
</header>

<main id="main">
  <section id="about"><h2>{e(c["about_h"])}</h2><div class="prose">{about}</div></section>

  <section id="focus"><h2>{e(c["focus_h"])}</h2><ul class="focus">{focus}</ul></section>

  <section id="results"><h2>{e(c["results_h"])}</h2><dl class="figs">{results}</dl></section>

  <section id="experience"><h2>{e(c["exp_h"])}</h2><ol class="rows">{exp}</ol>
    <h2 class="sub">{e(c["edu_h"])}</h2><ul class="plain">{edu}</ul></section>

  <section id="work"><h2>{e(c["work_h"])}</h2><p class="note">{e(c["work_note"])}</p><ul class="rows">{work}</ul></section>

  <section id="now"><h2>{e(c["now_h"])}</h2><ul class="plain now">{now}</ul><p class="note">{e(c["now_updated"])}</p></section>

  <section id="contact" class="contact">
    <h2>{e(c["contact_h"])}</h2>
    <p>{e(c["contact_p"])}</p>
    <div class="cta">
      <a class="btn primary" href="{mailto}">{e(c["c_email"])}</a>
      <a class="btn" href="{WHATSAPP}">{e(c["c_wa"])}</a>
      <a class="btn" href="{LINKEDIN}">{e(c["c_li"])}</a>
    </div>
  </section>
  <footer>{e(c["footer"])}</footer>
</main>
</div>
<script src="{R}assets/site.js" defer></script>
</body>
</html>
'''

root = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(root, "index.html"), "w", encoding="utf-8").write(page(C["ar"]))
os.makedirs(os.path.join(root, "en"), exist_ok=True)
open(os.path.join(root, "en", "index.html"), "w", encoding="utf-8").write(page(C["en"]))
print("built")
