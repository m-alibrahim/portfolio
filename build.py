#!/usr/bin/env python3
"""Builds the bilingual site: home pages (ar at /, en at /en/) and one page per project under work/."""
import html, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
LINKEDIN = "https://www.linkedin.com/in/mohammed-al-ibrahim-0b7192275/"
GITHUB = "https://github.com/m-alibrahim"
EMAIL = "m.alibrahim.ksa@gmail.com"
WHATSAPP = "https://wa.me/966595521229"
REPO = "https://github.com/m-alibrahim/portfolio/tree/main/projects/"
e = html.escape

# ---------------------------------------------------------------- projects
# kind: demo (opens a working demo), view (opens a page), files (opens source files)
P = [
 dict(slug="eligibility-checker", kind="demo", featured=True, svc=["acq"],
  ar=dict(tag="حملة استقطاب", name="حملة قانونية مع فاحص أهلية",
   line="حملة محددة المدة مبنية على تغيير تنظيمي، يبدأ فيها العميل المحتمل بفحص أهليته بنفسه خلال دقيقة.",
   problem="حين يفتح تغيير تنظيمي بابًا لمطالبة محددة المدة، يتصل كثيرون ليسألوا السؤال نفسه: هل يشملني؟ أغلب هذه المكالمات تنتهي بلا عميل، ووقت المحامي يضيع في الفرز.",
   steps=["يجيب الزائر عن أسئلة قصيرة بلغة بسيطة، دون أي مصطلح قانوني.","تظهر له نتيجة مبدئية فورًا: مؤهل، أو غير مؤهل، أو يحتاج مراجعة.","تنتقل إجاباته جاهزة إلى الفريق عبر واتساب، فيبدأ المحامي من حالة مفروزة."],
   try_="غيّر إجاباتك في تاريخ البيع وصفة البائع، ولاحظ كيف تتغير النتيجة والخطوة التالية.",
   note="النسخة المعروضة قالب عام. اسم الجهة ورقم التواصل محذوفان."),
  en=dict(tag="Acquisition campaign", name="Legal campaign with an eligibility checker",
   line="A time-limited campaign built on a regulatory change, where the prospect checks their own eligibility in about a minute.",
   problem="When a regulatory change opens a time-limited claim, many people call to ask the same thing: does this cover me? Most of those calls never become clients, and lawyers lose hours to screening.",
   steps=["The visitor answers a few short questions in plain language, with no legal terms.","A preliminary result appears straight away: eligible, not eligible, or needs review.","Their answers reach the team on WhatsApp, so the lawyer starts from a screened case."],
   try_="Change your answers for the sale date and the seller type, and watch the result and next step change.",
   note="This is a general template. The firm name and contact number have been removed.")),
 dict(slug="retainer-scoping", kind="view", featured=True, svc=["strategy"],
  ar=dict(tag="استراتيجية وتسعير", name="ضبط نطاق عقود الرعاية السنوية",
   line="خطة تحوّل لعقود الرعاية القانونية السنوية من عقود مفتوحة إلى عقود محددة النطاق تُسعَّر بحسب الاستخدام الفعلي.",
   problem="عقد الرعاية المفتوح يبدو جذابًا عند البيع، ثم يستهلك العميل أضعاف ما دفع. المكتب يخسر، والعميل يفاجأ حين تُطرح مسألة الفواتير الإضافية.",
   steps=["تحليل الاستخدام الفعلي لكل عميل مقابل الأتعاب، خدمةً خدمة.","تصميم مستويات للباقة وحد لكل خدمة، وما يتجاوز الحد يُفوتر بوضوح.","خطة تطبيق على مراحل: العقود الجديدة أولًا، ثم التجديدات."],
   try_="تصفّح أقسام الخطة من القائمة الجانبية، وبدّل اللغة من أعلى الصفحة. الأرقام توضيحية.",
   note="الأرقام في هذه النسخة توضيحية، وأسماء العملاء مستبدلة بحروف."),
  en=dict(tag="Strategy and pricing", name="Retainer scoping and usage control",
   line="A plan for moving annual legal retainers from open-ended contracts to scoped ones priced on what clients actually use.",
   problem="An open retainer is easy to sell, then the client uses several times what they paid for. The firm loses money, and the client is surprised when extra invoices come up.",
   steps=["Compare each client's real usage with their fees, one service line at a time.","Design retainer tiers with a cap per service, and bill clearly for anything above the cap.","Roll it out in waves: new contracts first, then renewals."],
   try_="Browse the plan from the side menu and switch language at the top. The figures are illustrative.",
   note="Figures in this version are illustrative, and client names are replaced with letters.")),
 dict(slug="bd-pipeline-tracker", kind="demo", featured=True, svc=["systems"],
  ar=dict(tag="نظام داخلي", name="نظام متابعة عملاء تطوير الأعمال",
   line="نظام خفيف لفريق تطوير الأعمال: العملاء، والفرص حسب المرحلة، والمهام، والتعاقدات والتحصيل في مكان واحد.",
   problem="الفرص موزعة بين جداول ومحادثات، والمتابعة تعتمد على ذاكرة كل شخص. تبرد فرص جيدة لأن أحدًا لم يتصل، والإدارة لا ترى أين تقف الأمور ولا ما تحصّل فعلًا.",
   steps=["صفحة «اليوم» تعرض ما يحتاج متابعة الآن: مهام متأخرة وفرص تجاوزت موعدها.","لوحة الفرص تنقل كل فرصة بين المراحل بالسحب، من التواصل الأول إلى التعاقد.","بعد التعاقد يتابع النظام الدفعات: ما استُلم، وما تأخر."],
   try_="افتح «الفرص» واسحب بطاقة إلى مرحلة أخرى، ثم افتح «التعاقدات والتحصيل» لترى الدفعة المتأخرة.",
   note="جميع العملاء والمبالغ هنا وهمية. بياناتك تُحفظ في متصفحك فقط."),
  en=dict(tag="Internal system", name="BD pipeline tracker",
   line="A lightweight system for a business development team: accounts, opportunities by stage, tasks, and contracts with collections in one place.",
   problem="Opportunities live in spreadsheets and chats, and follow-up depends on each person's memory. Good leads go cold because nobody called, and management can't see where things stand or what has actually been collected.",
   steps=["The Today page shows what needs attention now: late tasks and overdue follow-ups.","The board moves each opportunity between stages by drag and drop, from first contact to signed.","After signing, it tracks payments: what has come in and what is late."],
   try_="Open the opportunities board and drag a card to another stage, then open contracts and collections to see the late payment. The demo interface is in Arabic.",
   note="All clients and amounts here are fictional. Your changes stay in your browser only.")),
 dict(slug="claude-skills", kind="files", featured=True, svc=["systems","bids"],
  flow_ar=["كراسة الشروط","تحليل المتطلبات","مصفوفة الالتزام","التسعير","ملف العرض والعرض التقديمي"],
  flow_en=["Tender booklet","Requirement analysis","Compliance matrix","Pricing","Proposal file and deck"],
  ar=dict(tag="أتمتة بالذكاء الاصطناعي", name="مهارات ذكاء اصطناعي للعروض والعمل القانوني",
   line="ثلاث مهارات تعمل داخل Claude: عروض المنافسات من الكراسة إلى الملف النهائي، وملف استقبال العميل، وحجب البيانات الحساسة.",
   problem="إعداد عرض لمنافسة يأخذ أيامًا من القراءة والنسخ والتنسيق، وأي بند يفوت قد يُسقط العرض. والأعمال المتكررة الأخرى، مثل تجهيز ملف عميل جديد أو حجب مستند قبل مشاركته، تُنفَّذ كل مرة من الصفر.",
   steps=["مهارة العروض تقرأ الكراسة، وتستخرج المتطلبات ومعايير التقييم، وتبني مصفوفة الالتزام والتسعير.","تُخرج ملف وورد وعرضًا تقديميًا بالعربية وبهوية الجهة المتقدمة.","مهارتان مساندتان: تحويل هوامش أول مكالمة إلى ملف عميل، وحجب نهائي للأسماء والمبالغ في ملفات PDF."],
   try_="افتح الملفات واقرأ ملف التعليمات في كل مهارة. يمكن تثبيتها في Claude وتجربتها على كراسة حقيقية.",
   note="المهارات منشورة بلا أي بيانات جهة أو عميل."),
  en=dict(tag="AI automation", name="AI skills for bids and legal work",
   line="Three skills that run inside Claude: tender proposals from the booklet to the final file, client intake files, and redaction of sensitive data.",
   problem="Preparing a tender proposal takes days of reading, copying and formatting, and one missed requirement can sink the bid. Other repeat jobs, like opening a new client file or redacting a document before sharing it, get done from scratch every time.",
   steps=["The proposal skill reads the booklet, pulls out requirements and scoring criteria, and builds the compliance matrix and pricing.","It produces a Word file and a deck in Arabic, in the bidder's own branding.","Two supporting skills: turning first-call notes into a client file, and permanently redacting names and amounts in PDFs."],
   try_="Open the files and read each skill's instructions. They can be installed in Claude and tried on a real tender booklet.",
   note="The skills are published with no firm or client data.")),
 dict(slug="client-needs-questionnaire", kind="demo", svc=["strategy","acq"],
  ar=dict(tag="أداة للعميل", name="استبيان الاحتياج القانوني السنوي",
   line="استبيان بلغتين يقدّر فيه العميل حاجته السنوية من كل خدمة، وتُبنى عليه الباقة المقترحة.",
   problem="عروض الرعاية السنوية تُسعَّر غالبًا بالتخمين، فيخرج العرض إما غاليًا لا يُقبل أو رخيصًا يخسر فيه المكتب.",
   steps=["يحدد العميل عدد المرات المتوقعة لكل خدمة خلال السنة.","تصل الإجابات إلى الفريق مرتبة بالبريد.","يُبنى العرض على أرقام العميل نفسه، فيسهل شرح السعر."],
   try_="بدّل اللغة من أعلى الصفحة، واملأ الخدمات بأرقام مختلفة ولاحظ شريط التقدم.",
   note="قالب عام باسم جهة افتراضية. الإرسال الفعلي معطّل في النسخة التجريبية."),
  en=dict(tag="Client-facing tool", name="Annual legal needs questionnaire",
   line="A bilingual questionnaire where the client estimates how often they need each service in a year, which then shapes the proposed retainer.",
   problem="Annual retainers are often priced by guesswork, so the offer comes out either too expensive to accept or too cheap for the firm.",
   steps=["The client sets the expected volume for each service over the year.","The answers reach the team by email, already organised.","The proposal is built on the client's own numbers, which makes the price easy to explain."],
   try_="Switch language at the top, fill in different volumes and watch the progress bar.",
   note="A general template under a placeholder firm name. Sending is switched off in the demo.")),
 dict(slug="client-intake", kind="demo", svc=["systems"],
  ar=dict(tag="أتمتة", name="ملف استقبال العميل",
   line="يحوّل هوامش أول مكالمة مع العميل إلى ملف مرتب يكمله العميل بنفسه: ملخص، وأسئلة ناقصة، وقائمة مستندات.",
   problem="بعد المكالمة الأولى يبقى المحامي يطارد العميل أيامًا ليستكمل التفاصيل والمستندات، وكل طلب يأتي في رسالة منفصلة.",
   steps=["يلصق المحامي هوامشه كما كتبها، دون ترتيب.","يجهّز النظام ملخصًا يصححه العميل، وأسئلة محددة، وقائمة مستندات.","يخرج معه نص رسالة واتساب جاهز للإرسال."],
   try_="اضغط «عرض المثال الجاهز» لترى ملفًا كاملًا مبنيًا على مكالمة افتراضية.",
   note="المثال المعروض لقضية وأسماء افتراضية."),
  en=dict(tag="Automation", name="Client intake file",
   line="Turns notes from a first client call into an organised file the client completes: a summary, open questions and a document checklist.",
   problem="After the first call, the lawyer spends days chasing the client for missing details and documents, one message at a time.",
   steps=["The lawyer pastes the call notes as written, unsorted.","The tool prepares a summary for the client to correct, specific questions and a document list.","It also drafts the WhatsApp message to send with it."],
   try_="Press the ready-made example button to see a full file built from a fictional call. The demo interface is in Arabic.",
   note="The example uses a fictional case and names.")),
 dict(slug="cold-calling-system", kind="demo", svc=["acq"],
  ar=dict(tag="استقطاب عملاء", name="نظام الاتصال البارد",
   line="قائمة اتصال لمندوب المبيعات، ومع كل اسم موجز يجهزه للمكالمة: من هو، ولماذا نتصل به، وماذا نقول.",
   problem="المندوب يتصل بقائمة أسماء لا يعرف عنها شيئًا، فيبدأ كل مكالمة بالجملة نفسها ويُغلق الخط في وجهه.",
   steps=["بحث مسبق عن كل شركة وصانع القرار فيها.","بطاقة لكل مكالمة: خلفية، وسبب للتواصل، ونصائح للحديث.","تسجيل نتيجة كل مكالمة ومتابعة ما تبقى."],
   try_="افتح أي اسم في القائمة لترى بطاقة المكالمة، ثم سجّل نتيجتها.",
   note="الأسماء والشركات كلها افتراضية لأغراض العرض."),
  en=dict(tag="Client acquisition", name="Cold-calling system",
   line="A calling list for a sales rep, with a brief for every name: who they are, why we are calling, and what to say.",
   problem="Reps call a list of names they know nothing about, open every call with the same line, and get hung up on.",
   steps=["Research on each company and its decision-maker before any call.","A card per call: background, a reason to get in touch, and talking points.","Log each outcome and keep track of who is left."],
   try_="Open any name on the list to see its call card, then log an outcome. The demo interface is in Arabic.",
   note="All names and companies are fictional.")),
 dict(slug="candidate-evaluation", kind="demo", svc=["systems"],
  ar=dict(tag="نظام داخلي", name="منصة تقييم المرشحين",
   line="أداة توظيف منظمة: عدة مقيّمين يقيّمون المرشح على معايير موحدة، ثم تُقارن النتائج ويُصدَّر تقرير.",
   problem="بعد المقابلات يبقى القرار انطباعات متفرقة، وكل مقيّم يتذكر شيئًا مختلفًا، ولا توجد مقارنة عادلة بين المرشحين.",
   steps=["معايير عامة وأخرى خاصة بالوظيفة، ولكل منهما وزن.","كل مقيّم يدخل تقييمه مستقلًا، مع نقاط القوة والضعف.","صفحة تحليل تقارن المرشحين وتُصدّر تقريرًا."],
   try_="افتح «التحليل» واختر مرشحًا لترى تقييمات المقيّمين الثلاثة، أو أضف تقييمًا جديدًا من «التقييم».",
   note="المرشحون والتقييمات بيانات تجريبية، وتُحفظ تعديلاتك في متصفحك فقط."),
  en=dict(tag="Internal system", name="Candidate evaluation platform",
   line="A structured hiring tool: several interviewers score a candidate on shared criteria, then results are compared and exported as a report.",
   problem="After interviews, the decision rests on scattered impressions. Each interviewer remembers something different, and candidates are never compared fairly.",
   steps=["General criteria and role-specific ones, each with its own weight.","Every interviewer scores independently and notes strengths and weaknesses.","An analysis page compares candidates and exports a report."],
   try_="Open the analysis tab and pick a candidate to see three interviewers' scores, or add a new evaluation. The demo interface is in Arabic.",
   note="Candidates and scores are sample data, and your changes stay in your browser only.")),
 dict(slug="recruitment-dream-100-toolkit", kind="files", svc=["acq","systems"],
  flow_ar=["موقع شركة التوظيف","100 شركة مستهدفة","300 صانع قرار","رسائل مخصصة لكل عميل"],
  flow_en=["Agency website","100 target companies","300 decision-makers","Tailored outreach per prospect"],
  ar=dict(tag="أتمتة بالذكاء الاصطناعي", name="حزمة استهداف 100 عميل لشركات التوظيف",
   line="سلسلة مهارات ذكاء اصطناعي تبدأ من موقع شركة التوظيف وتنتهي بمئة شركة مستهدفة وصنّاع قرارها ورسائل مخصصة لكل واحدة.",
   problem="شركات التوظيف تراسل قوائم عامة برسالة واحدة، فتضيع بين مئات الرسائل المشابهة. بناء قائمة دقيقة يدويًا يأخذ أسابيع.",
   steps=["مقابلة قصيرة تحدد العميل المثالي للشركة.","بحث يُخرج مئة شركة لديها إشارات توظيف، وثلاثة صنّاع قرار لكل شركة.","رسائل متعددة القنوات مكتوبة لكل عميل على حدة."],
   try_="افتح الملفات واقرأ تسلسل المهارات الأربع وأمثلة الأوامر.",
   note="منشورة كمنهجية وأدوات، دون أي قوائم عملاء حقيقية."),
  en=dict(tag="AI automation", name="Dream 100 toolkit for recruitment agencies",
   line="A chain of AI skills that starts from an agency's website and ends with 100 target companies, their decision-makers, and outreach written for each one.",
   problem="Recruitment agencies send one message to generic lists and disappear among hundreds like it. Building a precise list by hand takes weeks.",
   steps=["A short interview defines the agency's ideal client.","Research returns 100 companies with hiring signals and three decision-makers at each.","Multichannel outreach is written for each prospect individually."],
   try_="Open the files and read how the four skills chain together, with example prompts.",
   note="Published as a method and tools, with no real client lists.")),
 dict(slug="rawaj-website", kind="view", svc=["systems"],
  ar=dict(tag="مشروع شخصي", name="موقع رواج للورود والهدايا",
   line="موقع كامل لمشروع تجاري شخصي: المتجر، والمناسبات، والاشتراكات، وقسم لهدايا الشركات.",
   problem="متجر ورود وهدايا يبيع عبر تطبيقات التوصيل فقط، بلا واجهة خاصة تعرض هويته ولا قناة لطلبات الشركات.",
   steps=["هوية بصرية موحدة وصور منتجات بخلفية واحدة.","أقسام للمناسبات والاشتراكات الدورية.","قسم «رواج للأعمال» لطلبات وهدايا الشركات."],
   try_="تصفّح الأقسام من القائمة العلوية وانتقل إلى «رواج للأعمال».",
   note="مشروع شخصي يُعرض كاملًا."),
  en=dict(tag="Personal venture", name="Rawaj flowers and gifts website",
   line="A full website for a personal business: storefront, occasions, subscriptions and a corporate gifting section.",
   problem="A flowers and gifts shop that sold only through delivery apps, with no storefront of its own and no channel for corporate orders.",
   steps=["One visual identity and product photos on a single background.","Sections for occasions and recurring subscriptions.","A business section for corporate orders and gifts."],
   try_="Browse the sections from the top menu and open the business page. The site is in Arabic.",
   note="A personal venture, shown in full.")),
]
BY = {p["slug"]: p for p in P}

T = dict(
 ar=dict(lang="ar", dir="rtl", other="English",
  title="محمد البراهيم | مستشار تطوير أعمال",
  desc="محمد البراهيم، مستشار تطوير أعمال في الرياض: استراتيجية وتسعير الخدمات، استقطاب العملاء، العروض والمنافسات، وبناء الأنظمة والأتمتة.",
  name="محمد البراهيم", role="مستشار تطوير أعمال", place="الرياض، السعودية",
  statement="أساعد شركات الخدمات المهنية على النمو بطريقة منظمة: استراتيجية واضحة، وعملاء جدد، وأنظمة تُبقي العمل مستمرًا بعد أن أغادر.",
  cta_contact="راسلني", cta_cv="حمّل السيرة الذاتية", cv="assets/cv/Mohammed_Alibrahim_CV_Arabic.pdf",
  nav=[("services","ما أقدمه"),("work","الأعمال"),("method","طريقة عملي"),("results","بالأرقام"),("about","عني"),("now","الآن"),("contact","تواصل")],
  skip="انتقل إلى المحتوى", theme="تبديل الوضع الفاتح والداكن", photo_alt="صورة محمد البراهيم",
  services_h="ما أقدمه",
  services=[
   ("strategy","استراتيجية تطوير الأعمال","أين تنمو الشركة، ومع من، وبأي عرض. أحوّل الخدمة إلى باقة محددة النطاق والسعر، وأضع خطة يمكن قياسها كل ربع."),
   ("acq","استقطاب العملاء","قوائم استهداف مبنية على بحث، وحملات تواصل عبر البريد ولينكدإن والهاتف، وأدوات تجعل العميل المحتمل يبدأ الخطوة الأولى بنفسه."),
   ("bids","العروض والمنافسات","من قراءة كراسة الشروط إلى العرض الفني والمالي والتسعير، وتكوين التحالفات حين لا تكفي جهة واحدة."),
   ("systems","الأنظمة والأتمتة","أنظمة متابعة العملاء، ونماذج الاستقبال، وأدوات ذكاء اصطناعي تختصر العمل المتكرر. أبنيها بنفسي على مقاس الفريق."),
  ],
  see="من الأعمال:",
  work_h="الأعمال", work_note="نسخ مفتوحة من أعمال نفذتها فعلًا. حُذفت أسماء العملاء وشعاراتهم، وكل البيانات المعروضة وهمية.",
  more_h="أعمال أخرى",
  read="عن المشروع", demo="جرّب النسخة التجريبية", view="افتح المشروع", files="اعرض الملفات",
  method_h="طريقة عملي",
  method=[("أفهم السوق أولًا","من يشتري هذه الخدمة، وماذا يدفع اليوم، ومن ينافس عليها. بحث وأرقام قبل أي حملة."),
          ("أحدد من نستهدف","قائمة قصيرة ودقيقة حسب القطاع والحجم، بدل قائمة طويلة عامة."),
          ("أصوغ العرض","خدمة بنطاق واضح وسعر يفهمه العميل، ورسالة مكتوبة له هو."),
          ("أبني ما يُبقيه مستمرًا","نظام متابعة وتقارير وأتمتة، حتى لا يتوقف العمل على شخص واحد.")],
  results_h="بالأرقام",
  results=[("63%","نمو في إيرادات شركة محاماة ساهمت فيه أثناء إدارتي لتطوير الأعمال فيها."),
           ("29%","متوسط تجاوز المستهدف الربعي خلال عام 2026."),
           ("27","عرضًا فنيًا وماليًا لمنافسات حكومية على منصة اعتماد."),
           ("+35,000","رسالة تواصل عبر البريد ولينكدإن والهاتف، تحوّل 4% منها إلى عملاء محتملين مؤهلين."),
           ("40%","زيادة في إيرادات وحدة أعمال بعد إطلاق خدمة استشارية قصيرة المدى."),
           ("المركز الثاني","في برنامج زمالة الابتكار بمركز ابتكار منشآت، لمشروع جمعت له تحالفًا من ثلاث شركات.")],
  about_h="عني",
  about=["أعمل في تطوير الأعمال منذ أكثر من ست سنوات، أغلبها مع شركات المحاماة والاستشارات في الرياض، ومع عملاء من القطاعين الخاص والحكومي.",
         "درست الشريعة، فأفهم ما يقدمه المحامي قبل أن أعرضه على العميل. وأدرس حاليًا ماجستير الذكاء الاصطناعي، ولهذا لا أكتفي بالتوصية: أبني الأداة التي تنفذها.",
         "عملت في تطوير الأعمال داخل شركة محاماة، وشركة استشارات توظيف، ومنصة خبراء واستشاريين بنيت فيها وحدة أعمال جديدة من الصفر."],
  creds=["ماجستير الذكاء الاصطناعي، جامعة ميدأوشن (قيد الدراسة)","بكالوريوس الشريعة، جامعة الإمام محمد بن سعود الإسلامية","شهادة المهندس القانوني من هارفي، ودورات أكاديمية أنثروبيك"],
  now_h="الآن", now_upd="آخر تحديث: نوفمبر 2026",
  now=["أدرس ماجستير الذكاء الاصطناعي.","أبني أدوات ذكاء اصطناعي لعمل تطوير الأعمال: عروض المنافسات، واستقبال العملاء، وقوائم الاستهداف.","منفتح على مشاريع واستشارات في تطوير الأعمال، خصوصًا في الخدمات القانونية والمهنية."],
  contact_h="تواصل", contact_p="إن كان عندك مشروع أو سؤال، راسلني بالطريقة الأنسب لك. أرد غالبًا خلال يومي عمل.",
  c_email="البريد", c_wa="واتساب", c_li="لينكدإن", c_gh="جيت هب", subject="استفسار عن تطوير الأعمال",
  footer="© 2026 محمد البراهيم",
  back="كل الأعمال", h_problem="المشكلة", h_how="كيف يعمل", h_try="جرّب بنفسك", next="المشروع التالي",
  shot_alt="لقطة من ", flow_alt="مراحل العمل"),
 en=dict(lang="en", dir="ltr", other="العربية",
  title="Mohammed Alibrahim | Business Development Consultant",
  desc="Mohammed Alibrahim, a business development consultant in Riyadh: strategy and service pricing, client acquisition, bids and tenders, and systems and automation.",
  name="Mohammed Alibrahim", role="Business Development Consultant", place="Riyadh, Saudi Arabia",
  statement="I help professional services firms grow in an organised way: a clear strategy, new clients, and systems that keep the work running after I leave.",
  cta_contact="Email me", cta_cv="Download CV", cv="assets/cv/Mohammed_Alibrahim_CV.pdf",
  nav=[("services","What I do"),("work","Work"),("method","How I work"),("results","In numbers"),("about","About"),("now","Now"),("contact","Contact")],
  skip="Skip to content", theme="Switch between light and dark mode", photo_alt="Portrait of Mohammed Alibrahim",
  services_h="What I do",
  services=[
   ("strategy","Business development strategy","Where the firm should grow, with whom, and with what offer. I turn a service into a package with a defined scope and price, and set a plan you can measure each quarter."),
   ("acq","Client acquisition","Research-based target lists, outreach by email, LinkedIn and phone, and tools that let a prospect take the first step on their own."),
   ("bids","Bids and tenders","From reading the tender booklet to the technical and financial proposal and pricing, and forming alliances when one firm is not enough."),
   ("systems","Systems and automation","Pipeline trackers, intake forms and AI tools that cut repeat work. I build them myself, to fit the team."),
  ],
  see="From the work:",
  work_h="Work", work_note="Open versions of work I have actually delivered. Client names and logos are removed, and all data shown is fictional.",
  more_h="More work",
  read="About the project", demo="Try the demo", view="Open the project", files="View the files",
  method_h="How I work",
  method=[("Understand the market first","Who buys this service, what they pay today, and who competes for it. Research and numbers before any campaign."),
          ("Decide who to target","A short, precise list by sector and size, not a long generic one."),
          ("Shape the offer","A service with a clear scope and a price the client understands, and a message written for them."),
          ("Build what keeps it running","Tracking, reporting and automation, so the work does not depend on one person.")],
  results_h="In numbers",
  results=[("63%","Revenue growth at a law firm, which I contributed to while leading its business development."),
           ("29%","Average amount by which I exceeded quarterly targets in 2026."),
           ("27","Technical and financial proposals for government tenders on Etimad."),
           ("35,000+","Outreach messages by email, LinkedIn and phone, with 4% turning into qualified leads."),
           ("40%","Increase in a business unit's revenue after launching a short-term consulting service."),
           ("2nd place","In the Innovation Fellowship Program at Monsha'at Innovation Center, for a project I formed a three-company alliance to deliver.")],
  about_h="About",
  about=["I have worked in business development for more than six years, mostly with law firms and consultancies in Riyadh, for private and government clients.",
         "I studied Islamic law, so I understand what a lawyer offers before I put it in front of a client. I am now studying for an MSc in artificial intelligence, which is why I don't stop at the recommendation: I build the tool that carries it out.",
         "I have led business development inside a law firm, a recruitment consultancy, and an experts and consultants platform where I set up a new business unit from scratch."],
  creds=["MSc Artificial Intelligence, Midocean University (in progress)","Bachelor of Islamic Law (Sharia), Imam Mohammad Ibn Saud Islamic University","Legal Engineer certificate from Harvey, and Anthropic Academy courses"],
  now_h="Now", now_upd="Last updated: November 2026",
  now=["Studying for an MSc in artificial intelligence.","Building AI tools for business development work: tender proposals, client intake and target lists.","Open to business development projects and advisory work, especially in legal and professional services."],
  contact_h="Contact", contact_p="If you have a project or a question, reach me whichever way suits you. I usually reply within two working days.",
  c_email="Email", c_wa="WhatsApp", c_li="LinkedIn", c_gh="GitHub", subject="Business development enquiry",
  footer="© 2026 Mohammed Alibrahim",
  back="All work", h_problem="The problem", h_how="How it works", h_try="Try it yourself", next="Next project",
  shot_alt="Screenshot of ", flow_alt="Stages of the work"),
)

THEME_JS = '<script>(function(){var t;try{t=localStorage.getItem("theme")}catch(e){}if(!t)t=matchMedia("(prefers-color-scheme: light)").matches?"light":"dark";document.documentElement.dataset.theme=t})()</script>'
THEME_BTN = '<button class="theme" type="button" aria-label="{}"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M12 3a9 9 0 1 0 0 18V3z"/><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>'

def head(t, title, desc, root):
    font = '"IBM Plex Sans Arabic","Inter",system-ui,sans-serif' if t["lang"] == "ar" else '"Inter","IBM Plex Sans Arabic",system-ui,sans-serif'
    return f'''<!DOCTYPE html>
<html lang="{t["lang"]}" dir="{t["dir"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="profile">
<meta name="theme-color" content="#0d1730">
{THEME_JS}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/site.css">
<style>body{{font-family:{font}}}</style>
</head>
<body>
<a class="skip" href="#main">{e(t["skip"])}</a>
'''

def action(p, t, root, primary=False):
    label = {"demo": t["demo"], "view": t["view"], "files": t["files"]}[p["kind"]]
    href = (REPO + p["slug"]) if p["kind"] == "files" else f'{root}projects/{p["slug"]}/'
    cls = "btn primary" if primary else "link"
    return f'<a class="{cls}" href="{href}">{e(label)}</a>'

def visual(p, t, root, lang):
    if p["kind"] == "files":
        steps = p["flow_" + lang]
        lis = "".join(f"<li>{e(s)}</li>" for s in steps)
        return f'<div class="frame flow" role="img" aria-label="{e(t["flow_alt"])}"><ol>{lis}</ol></div>'
    return (f'<div class="frame"><div class="bar" aria-hidden="true"><i></i><i></i><i></i></div>'
            f'<img src="{root}assets/shots/{p["slug"]}.jpg" width="1200" height="750" loading="lazy" alt="{e(t["shot_alt"] + p[lang]["name"])}"></div>')

def card(p, t, root, lang, big):
    d = p[lang]; url = f'{root if lang=="ar" else root+"en/"}work/{p["slug"]}/'
    return (f'<li class="plate{" big" if big else ""}"><a class="shot" href="{url}" tabindex="-1" aria-hidden="true">{visual(p,t,root,lang)}</a>'
            f'<div class="meta"><span class="tag">{e(d["tag"])}</span><h3><a href="{url}">{e(d["name"])}</a></h3><p>{e(d["line"])}</p>'
            f'<div class="links"><a class="link" href="{url}">{e(t["read"])}</a>{action(p,t,root)}</div></div></li>')

def home(lang):
    t = T[lang]; root = "" if lang == "ar" else "../"
    here = "" if lang == "ar" else "en/"
    other = "en/" if lang == "ar" else "../"
    wk = lambda s: f'{root}{here}work/{s}/'
    nav = "".join(f'<li><a href="#{i}"><span class="tick"></span>{e(l)}</a></li>' for i, l in t["nav"])
    svc = ""
    for key, name, body in t["services"]:
        rel = [p for p in P if key in p["svc"]][:3]
        links = "".join(f'<a href="{wk(p["slug"])}">{e(p[lang]["name"])}</a>' for p in rel)
        svc += f'<li><h3>{e(name)}</h3><p>{e(body)}</p><p class="rel"><span>{e(t["see"])}</span>{links}</p></li>'
    feat = "".join(card(p, t, root, lang, True) for p in P if p.get("featured"))
    rest = "".join(card(p, t, root, lang, False) for p in P if not p.get("featured"))
    method = "".join(f'<li><h3>{e(a)}</h3><p>{e(b)}</p></li>' for a, b in t["method"])
    figs = "".join(f'<div class="fig"><dt>{e(a)}</dt><dd>{e(b)}</dd></div>' for a, b in t["results"])
    about = "".join(f"<p>{e(x)}</p>" for x in t["about"])
    creds = "".join(f"<li>{e(x)}</li>" for x in t["creds"])
    now = "".join(f"<li>{e(x)}</li>" for x in t["now"])
    mail = f'mailto:{EMAIL}?subject={t["subject"].replace(" ", "%20")}'
    s = head(t, t["title"], t["desc"], root) + f'''<div class="glow" aria-hidden="true"></div>
<div class="page">
<header class="intro">
<div class="intro-top">
<img class="photo" src="{root}assets/mohammed.jpg" width="112" height="112" alt="{e(t["photo_alt"])}">
<h1>{e(t["name"])}</h1>
<p class="role">{e(t["role"])}<span class="place">{e(t["place"])}</span></p>
<p class="statement">{e(t["statement"])}</p>
<div class="cta"><a class="btn primary" href="{mail}">{e(t["cta_contact"])}</a><a class="btn" href="{root}{t["cv"]}" download>{e(t["cta_cv"])}</a></div>
<nav aria-label="{e(t["name"])}"><ul>{nav}</ul></nav>
</div>
<div class="intro-bottom">
<a href="{LINKEDIN}">{e(t["c_li"])}</a><a href="{GITHUB}">{e(t["c_gh"])}</a><a href="{WHATSAPP}">{e(t["c_wa"])}</a>
<span class="spacer"></span>
<a class="lang" href="{other}" lang="{"en" if lang=="ar" else "ar"}">{e(t["other"])}</a>
{THEME_BTN.format(e(t["theme"]))}
</div>
</header>

<main id="main">
<section id="services"><h2>{e(t["services_h"])}</h2><ul class="services">{svc}</ul></section>
<section id="work"><h2>{e(t["work_h"])}</h2><p class="note">{e(t["work_note"])}</p><ul class="plates">{feat}</ul>
<h2 class="sub">{e(t["more_h"])}</h2><ul class="plates grid">{rest}</ul></section>
<section id="method"><h2>{e(t["method_h"])}</h2><ol class="method">{method}</ol></section>
<section id="results"><h2>{e(t["results_h"])}</h2><dl class="figs">{figs}</dl></section>
<section id="about"><h2>{e(t["about_h"])}</h2><div class="prose">{about}</div><ul class="plain creds">{creds}</ul></section>
<section id="now"><h2>{e(t["now_h"])}</h2><ul class="plain now">{now}</ul><p class="note">{e(t["now_upd"])}</p></section>
<section id="contact" class="contact"><h2>{e(t["contact_h"])}</h2><p>{e(t["contact_p"])}</p>
<div class="cta"><a class="btn primary" href="{mail}">{e(t["c_email"])}</a><a class="btn" href="{WHATSAPP}">{e(t["c_wa"])}</a><a class="btn" href="{LINKEDIN}">{e(t["c_li"])}</a></div>
<p class="addr">{EMAIL}</p></section>
<footer>{e(t["footer"])}</footer>
</main>
</div>
<script src="{root}assets/site.js" defer></script>
</body>
</html>
'''
    return s

def project(p, lang):
    t = T[lang]; d = p[lang]
    root = "../../" if lang == "ar" else "../../../"
    homeurl = "../../" + "#work"
    other = f'../../en/work/{p["slug"]}/' if lang == "ar" else f'../../../work/{p["slug"]}/'
    i = P.index(p); nx = P[(i + 1) % len(P)]
    steps = "".join(f"<li>{e(x)}</li>" for x in d["steps"])
    s = head(t, f'{d["name"]} | {t["name"]}', d["line"], root) + f'''<div class="page solo">
<header class="top"><a class="backlink" href="{homeurl}">{e(t["back"])}</a><span class="spacer"></span><a class="who" href="../../">{e(t["name"])}</a>
<a class="lang" href="{other}" lang="{"en" if lang=="ar" else "ar"}">{e(t["other"])}</a>{THEME_BTN.format(e(t["theme"]))}</header>
<main id="main" class="case">
<span class="tag">{e(d["tag"])}</span>
<h1>{e(d["name"])}</h1>
<p class="lead">{e(d["line"])}</p>
<div class="cta">{action(p,t,root,True)}</div>
{visual(p,t,root,lang)}
<div class="cols">
<section><h2>{e(t["h_problem"])}</h2><p>{e(d["problem"])}</p></section>
<section><h2>{e(t["h_how"])}</h2><ol class="steps">{steps}</ol></section>
</div>
<section class="tryit"><h2>{e(t["h_try"])}</h2><p>{e(d["try_"])}</p><p class="note">{e(d["note"])}</p><div class="cta">{action(p,t,root,True)}</div></section>
<a class="nextp" href="../{nx["slug"]}/"><span>{e(t["next"])}</span><strong>{e(nx[lang]["name"])}</strong></a>
<footer>{e(t["footer"])}</footer>
</main>
</div>
<script src="{root}assets/site.js" defer></script>
</body>
</html>
'''
    return s

def write(path, s):
    full = os.path.join(ROOT, path); os.makedirs(os.path.dirname(full) or ROOT, exist_ok=True)
    open(full, "w", encoding="utf-8").write(s)

PILL = '<a id="pf-pill" href="{href}" style="position:fixed;bottom:14px;left:14px;z-index:99999;background:#0d1730;color:#fff;font:600 13px/1.4 \'IBM Plex Sans Arabic\',system-ui,sans-serif;padding:9px 14px;border-radius:999px;text-decoration:none;box-shadow:0 6px 20px rgba(13,23,48,.3);border:1px solid #d39c6e;direction:rtl">{txt}</a>'
def pills():
    for p in P:
        f = os.path.join(ROOT, "projects", p["slug"], "index.html")
        if not os.path.exists(f): continue
        s = open(f, encoding="utf-8").read()
        s = re.sub(r'<a id="pf-pill".*?</a>\n?', "", s, flags=re.S)
        txt = "مشروع شخصي، عن المشروع" if p["slug"] == "rawaj-website" else "نسخة تجريبية ببيانات وهمية، عن المشروع"
        tag = PILL.format(href=f'../../work/{p["slug"]}/', txt=txt) + "\n"
        k = s.rfind("</body>")
        s = s[:k] + tag + s[k:] if k >= 0 else s + tag
        open(f, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    write("index.html", home("ar")); write("en/index.html", home("en"))
    for p in P:
        write(f'work/{p["slug"]}/index.html', project(p, "ar"))
        write(f'en/work/{p["slug"]}/index.html', project(p, "en"))
    pills()
    print("built", 2 + 2 * len(P), "pages")
