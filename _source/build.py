#!/usr/bin/env python3
"""Builds the static Growthryders site into ./site (plain HTML, no framework).
Run:  python3 build.py
Content lives in this file so copy edits are one place."""
import os, html, json, datetime

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site')
DOMAIN = 'https://growthryders.in'
PHONE_DISPLAY = '+91 81973 30612'      # WhatsApp Business number, also takes calls
PHONE_E164 = '918197330612'
LINKEDIN = 'https://in.linkedin.com/in/surender-loganathan-65463a15'
IC_CALL = '<svg class="ic" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25c1.12.37 2.33.57 3.6.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>'
IC_CHAT = '<svg class="ic" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M12 3.2a8.8 8.8 0 0 0-7.6 13.3L3.2 20.8l4.4-1.2A8.8 8.8 0 1 0 12 3.2z"/><circle cx="8.4" cy="12" r="1.1" fill="currentColor"/><circle cx="12" cy="12" r="1.1" fill="currentColor"/><circle cx="15.6" cy="12" r="1.1" fill="currentColor"/></svg>'
EMAIL = 'surender@growthryders.in'
YEAR = datetime.date.today().year
FILMS_LIVE = os.environ.get('FILMS_LIVE', '1') == '1'   # set FILMS_LIVE=0 to publish without the film files

LOGO = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="10 0 1590 516" role="img" aria-label="GRY — Growthryders"><defs><clipPath id="lc"><rect x="0" y="0" width="1610" height="511"/></clipPath></defs><g class="ink" clip-path="url(#lc)" fill="none" stroke="#4B2C73" stroke-width="70" stroke-linejoin="miter"><path d="M345 260H575V475H112Q57 475 57 420V95Q57 40 112 40H1125A110 110 0 0 1 1125 260H732V520"/><path d="M1005 262L1245 530"/><path d="M1228 118L1405 268V520"/><path d="M1555 38V88Q1555 128 1522 158L1405 268" stroke-linecap="round"/></g><circle cx="729" cy="150" r="36" fill="#F5B321"/></svg>'''

LOGO_INTRO = '''<svg class="intro-logo" xmlns="http://www.w3.org/2000/svg" viewBox="10 0 1590 516" aria-hidden="true"><g class="rays" fill="none" stroke="#F5B321" stroke-width="5" stroke-linecap="round"><path pathLength="1" d="M-1400 150H729"/><path pathLength="1" d="M3000 150H729"/><path pathLength="1" d="M729 -1300V150"/><path pathLength="1" d="M729 1700V150"/></g><circle class="ring" cx="729" cy="150" r="36" fill="none" stroke="#F5B321" stroke-width="4"/><g fill="none" stroke="#fff" stroke-width="70" stroke-linejoin="miter"><path class="d1" pathLength="1" d="M732 511V260H1125A110 110 0 0 0 1125 40H112Q57 40 57 95V420Q57 475 112 475H575V260H345"/><path class="d2" pathLength="1" d="M1005 262L1238 511"/><path class="d3" pathLength="1" d="M1228 118L1405 268V511"/><path class="d4" pathLength="1" d="M1405 268L1522 158Q1555 128 1555 88V38" stroke-linecap="round"/></g><circle class="rider" cx="729" cy="150" r="36" fill="#F5B321"/></svg>'''
INTRO = f'''<div class="intro" id="intro" aria-hidden="true"><div class="intro-in">{LOGO_INTRO}<p class="intro-word"><span>Growthryders</span></p><p class="intro-tag"><span>Brand activations at the core</span></p></div><button class="intro-skip" type="button">Skip intro</button></div>'''

NAV = [('about.html', 'About'), ('services.html', 'Services'), ('sponsorship-sales.html', 'Sponsorship'), ('work.html', 'Work')] + ([('films.html', 'Films')] if FILMS_LIVE else []) + [('ips.html', 'Our IPs')]

EXTRA_LD = {}
def page(path, title, desc, body, head='light', depth=0, intro=False):
    r = '../' * depth
    cur = path.split('/')[0]
    links = ''.join(f'<a href="{r}{h}"{" aria-current=\"page\"" if h == cur or (cur == "work" and h == "work.html") or (cur == "services" and h == "services.html") else ""}>{t}</a>' for h, t in NAV)
    canonical = DOMAIN + '/' + ('' if path == 'index.html' else path)
    org = {"@type": ["Organization", "ProfessionalService"], "@id": DOMAIN + "/#org", "name": "Growthryders", "alternateName": ["Growth Ryders", "GRY", "Growth Riders", "Growthriders", "GrowthRyders", "Growth Ryders Bengaluru"], "url": DOMAIN,
           "logo": DOMAIN + "/assets/img/gry-logo.svg", "image": DOMAIN + "/assets/img/og.jpg", "email": EMAIL,
           "telephone": "+" + PHONE_E164,
           "contactPoint": [{"@type": "ContactPoint", "telephone": "+" + PHONE_E164, "contactType": "sales", "areaServed": "IN", "availableLanguage": ["en", "hi", "kn"]}],
           "founder": {"@type": "Person", "@id": DOMAIN + "/about.html#founder", "name": "Surender Loganathan", "jobTitle": "Founder", "worksFor": {"@id": DOMAIN + "/#org"}, "sameAs": [LINKEDIN], "image": DOMAIN + "/assets/img/founder.jpg"},
           "address": {"@type": "PostalAddress", "addressLocality": "Bengaluru", "addressRegion": "Karnataka", "addressCountry": "IN"},
           "areaServed": [{"@type": "City", "name": "Bengaluru"}, {"@type": "Country", "name": "India"}],
           "knowsAbout": ["Brand activation", "BTL activation", "Experiential marketing", "Through-the-line marketing", "Corporate park activations", "Tech park activations", "Mall activations", "Roadshows", "Product sampling", "Event management", "Corporate events", "Digital marketing", "Media planning and buying", "Outdoor advertising", "Event film production", "Video production"],
           "description": "Brand activation agency and through-the-line marketing company in Bengaluru (Bangalore), India."}
    site = {"@type": "WebSite", "@id": DOMAIN + "/#site", "url": DOMAIN, "name": "Growthryders", "alternateName": ["Growth Ryders", "GRY"], "publisher": {"@id": DOMAIN + "/#org"}, "inLanguage": "en-IN"}
    graph = [org, site, {"@type": "WebPage", "@id": canonical, "url": canonical, "name": title, "description": desc, "isPartOf": {"@id": DOMAIN + "/#site"}, "about": {"@id": DOMAIN + "/#org"}}]
    if path != 'index.html':
        crumbs = [("Home", DOMAIN + "/")] + ([("Services", DOMAIN + "/services.html")] if path.startswith("services/") else [("Work", DOMAIN + "/work.html")] if depth else []) + [(title.split(' | ')[0], canonical)]
        graph.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]})
    org["hasOfferCatalog"] = {"@type": "OfferCatalog", "name": "Marketing services", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": t, "description": d, "url": DOMAIN + "/" + svc_href(k), "provider": {"@id": DOMAIN + "/#org"}, "areaServed": "IN"}} for k, t, d, cs in SERVICES]}
    graph += EXTRA_LD.get(path, [])
    if path == 'films.html':
        def iso(d): m, sec = d.split(':'); return f'PT{int(m)}M{int(sec)}S'
        for k, t, b, d, o in FILMS:
            graph.append({"@type": "VideoObject", "name": t + " | Growthryders", "description": f"{t}. Brand activation film by Growthryders, Bengaluru. Brands: {b}.", "thumbnailUrl": f"{DOMAIN}/assets/films/{k}.jpg", "contentUrl": f"{DOMAIN}/assets/films/{k}.mp4", "uploadDate": "2026-11-21T00:00:00+05:30", "duration": iso(d), "publisher": {"@id": DOMAIN + "/#org"}})
    if path == 'index.html':
        graph.append({"@type": "FAQPage", "@id": canonical + "#faq", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]})
    ld = {"@context": "https://schema.org", "@graph": graph}
    doc = f'''<!doctype html>
<html lang="en-IN">
<head>
<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-PNP5VGNQ"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());</script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/assets/img/og.jpg">
<meta property="og:site_name" content="Growthryders">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og.jpg">
<meta name="robots" content="index,follow,max-image-preview:large,max-video-preview:-1">
<meta name="geo.region" content="IN-KA">
<meta name="geo.placename" content="Bengaluru">
<meta name="theme-color" content="#170e22">
<link rel="icon" href="/favicon.ico?v=3" sizes="any">
<link rel="shortcut icon" href="/favicon.ico?v=3">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/icon-32.png?v=3">
<link rel="icon" type="image/png" sizes="96x96" href="/assets/img/icon-96.png?v=3">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/img/icon-192.png?v=3">
<link rel="icon" href="{r}assets/img/favicon.svg?v=3" type="image/svg+xml">
<link rel="apple-touch-icon" href="{r}assets/img/icon-180.png?v=3">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/css/site.css?v=36">
<script>document.documentElement.classList.add("js");try{{if({str(intro).lower()}&&!sessionStorage.getItem("gry-intro")&&!matchMedia("(prefers-reduced-motion: reduce)").matches)document.documentElement.classList.add("intro-on")}}catch(e){{}}</script>
<script type="application/ld+json">{json.dumps(ld)}</script>
</head>
<body>
{INTRO if intro else ""}<a class="skip" href="#main">Skip to content</a>
<header class="site-head {head}">
  <div class="wrap">
    <a class="brand" href="{r}index.html" aria-label="Growthryders home">{LOGO}</a>
    <button class="nav-toggle" aria-controls="nav" aria-expanded="false" aria-label="Open menu"><span></span><span></span><span></span></button>
    <nav class="nav" id="nav" aria-label="Main">{links}<a class="btn" href="{r}contact.html">Start a conversation</a></nav>
  </div>
</header>
<main id="main">
{body.replace('{r}', r)}
</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="cols4">
      <div>{LOGO}<p style="margin-top:16px;max-width:34ch">Brand activations at the core. Integrated marketing for growth.</p><p class="aka">Growthryders, also written Growth Ryders (GRY), Bengaluru.</p></div>
      <div><h2>Company</h2><ul><li><a href="{r}about.html">About</a></li><li><a href="{r}services.html">Services</a></li><li><a href="{r}work.html">Work</a></li>{"<li><a href=" + chr(34) + r + "films.html" + chr(34) + ">Films</a></li>" if FILMS_LIVE else ""}<li><a href="{r}ips.html">Our IPs</a></li></ul></div>
      <div><h2>Work</h2><ul><li><a href="{r}work/tu-race-laga.html">TVS Apache: Tu Race Laga</a></li><li><a href="{r}work/tvs-apache-bagmane.html">TVS Apache at Bagmane</a></li><li><a href="{r}work/royal-enfield-bikers-bay.html">Royal Enfield: Bikers Bay</a></li></ul></div>
      <div><h2>Contact</h2><ul><li><a class="wi" href="tel:+{PHONE_E164}">{IC_CALL}{PHONE_DISPLAY}</a></li><li><a class="wi" href="https://wa.me/{PHONE_E164}">{IC_CHAT}WhatsApp us</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>Bengaluru, India</li></ul></div>
    </div>
    <div class="legal"><span>© {YEAR} Growthryders</span><span>Bengaluru, India</span></div>
  </div>
</footer>
<script src="{r}assets/js/site.js?v=14" defer></script>
</body>
</html>
'''
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(doc)

def img(name, alt, cls='ratio-43', w=1280, h=960, eager=False):
    return f'<div class="frame {cls}"><img src="{{r}}assets/img/{name}.jpg" alt="{html.escape(alt)}" width="{w}" height="{h}"{"" if eager else " loading=\"lazy\""}></div>'

def bibs(items, light=False):
    lis = ''.join(f'<li class="bib"><span class="band">{b}</span><span class="num">{n}</span><span class="lbl">{l}</span></li>' for b, n, l in items)
    return f'<ul class="bibs{" on-light" if light else ""}">{lis}</ul>'

CTA = '''<section class="cta"><div class="wrap">
<h2>Let's create something that moves your brand forward.</h2>
<p class="lede" style="margin-top:18px">Have a marketing challenge, a new product or an ambitious brand idea? Tell us about it and we will turn it into an experience.</p>
<div class="btn-row"><a class="btn" href="{r}contact.html">Start a conversation</a><a class="btn ghost wi" href="https://wa.me/''' + PHONE_E164 + '''">''' + IC_CHAT + '''WhatsApp us</a><a class="btn ghost wi" href="tel:+''' + PHONE_E164 + '''">''' + IC_CALL + '''Call us</a></div>
</div></section>'''

def svc_href(k): return 'sponsorship-sales.html' if k == 'sponsorship' else 'services/' + SVC_SLUG[k] + '.html'
SVC_SLUG = {'activations': 'brand-activations', 'digital': 'digital-marketing', 'experiential': 'experiential-marketing', 'media': 'media-solutions', 'events': 'corporate-events', 'technology': 'technology-experiences', 'films': 'film-production'}
SERVICES = [
 ('activations', 'Brand activations and TTL marketing', 'Consumer engagement on the ground, amplified across every channel that reaches the same people.',
  ['Corporate park activations', 'Mall and public space promotions', 'Product sampling', 'Roadshows', 'Campus and residential activations', 'Retail and trade marketing', 'Dealer and channel partner engagement', 'Guerrilla marketing', 'Brand launches']),
 ('digital', 'Digital marketing', 'Search, social, content, websites and performance campaigns that keep the conversation going.',
  ['SEO and GEO', 'Performance marketing', 'Social media management', 'Content strategy and creation', 'Website design and development', 'Lead generation', 'Digital campaign management', 'Marketing analytics and automation']),
 ('experiential', 'Experiential marketing', 'Launches, installations and interactive formats that turn communication into something people remember.',
  ['Product launches', 'Trade shows and exhibitions', 'Immersive brand storytelling', 'Employee and partner engagement']),
 ('media', 'Media solutions', 'Planning and buying across outdoor, transit, print, radio, corporate parks, malls and retail.',
  ['Outdoor and digital outdoor', 'Transit and airport media', 'Print and radio', 'Corporate park media', 'Mall and retail media', 'Retail and point-of-sale branding', 'Innovative and ambient media']),
 ('events', 'Corporate events and engagement', 'Conferences, dealer meets, summits, awards and employee programmes, concept to close.',
  ['Conferences and annual meets', 'Dealer meets', 'Leadership summits', 'Awards', 'Employee engagement programmes', 'Product launches']),
 ('sponsorship', 'Sponsorship Sales & Revenue Management', 'Turning IPs, Events & B2B Platforms into Revenue Opportunities.',
  ['Sponsorship Strategy & Revenue Planning', 'IP and Event Monetisation', 'AI-enabled Brand Identification & Prospecting', 'Industry-wise Sponsor Database Development', 'Decision-maker Mapping & Lead Qualification', 'Personalised Outreach & Sales Engagement', 'Sponsorship Proposal Development', 'Negotiations & Commercial Closure', 'CRM-based Pipeline & Follow-up Management', 'Sponsorship Revenue Tracking & Reporting']),
 ('technology', 'Technology-led experiences', 'Installations, AR and VR, gamification and interactive digital formats built into the activation.',
  ['Technology-led installations', 'Augmented and virtual reality', 'Gamification', 'Interactive digital experiences']),
 ('films', 'Film and content production', 'We shoot and edit the films of the activations and events we run: event films, brand and partner films and vertical cuts for social media.',
  ['Event films', 'Brand and partner films', 'Reels and vertical cuts', 'On-ground shooting', 'Editing']),
]

TRL_BIBS = [('Tu Race Laga', '1,600', 'participants and guests on event day, approximately'), ('Bagmane', '5', 'business park locations'),
            ('Campaign', '40', 'days of engagement before the run'), ('Categories', '3', 'distances: 3K, 5K and 10K')]


FILMS = [
 ('tu-race-laga-event-film', 'Tu Race Laga: the event film', 'TVS Apache, Bagmane REIT and partners', '2:19', 'land'),
 ('tvs-apache-tu-race-laga', 'TVS Apache at Tu Race Laga', 'TVS Apache', '1:20', 'land'),
 ('axis-bank-tu-race-laga', 'Axis Bank at Tu Race Laga', 'Axis Bank', '0:46', 'land'),
 ('milky-mist-tu-race-laga', 'Milky Mist at Tu Race Laga', 'Milky Mist', '0:49', 'land'),
 ('royal-enfield-bagmane-film', 'Royal Enfield across Bagmane parks', 'Royal Enfield, Bagmane REIT', '1:18', 'port'),
 ('royal-enfield-tech-park', 'Royal Enfield at Bagmane Tech Park', 'Royal Enfield', '0:48', 'port'),
 ('royal-enfield-capital', 'Royal Enfield at Bagmane Capital', 'Royal Enfield', '0:50', 'port'),
 ('tvs-apache-reel', 'TVS Apache: the vertical cut', 'TVS Apache', '1:20', 'port'),
]
def film(f, eager=False):
    k, t, b, d, o = f
    w, h = (1280, 720) if o == 'land' else (720, 1280)
    return f'''<button class="film {o}" type="button" data-film="{{r}}assets/films/{k}.mp4" data-title="{html.escape(t)}" data-shape="{o}">
<img src="{{r}}assets/films/{k}.jpg" alt="" width="{w}" height="{h}"{"" if eager else ' loading="lazy"'}>
<span class="play" aria-hidden="true"><svg viewBox="0 0 24 24" width="22" height="22"><path d="M8 5v14l11-7z" fill="currentColor"/></svg></span>
<span class="cap"><strong>{t}</strong><span>{b}, {d}</span></span></button>'''
PLAYER = '''<dialog class="player" id="player" aria-label="Film player"><button class="player-close" type="button" aria-label="Close film">Close</button><div class="player-stage"><video controls playsinline preload="none"></video></div><p class="player-title"></p></dialog>'''
MARQUEE = ['TVS Apache', 'Royal Enfield', 'Bagmane REIT', 'Axis Bank', 'Milky Mist', 'Kauvery Hospital', 'Protein Chef', 'iRaces']
def marquee():
    row = ''.join(f'<span>{m}</span>' for m in MARQUEE)
    return f'<section class="marquee" aria-label="Brands on the ground with us"><div class="track"><div class="row">{row}</div><div class="row" aria-hidden="true">{row}</div></div></section>'

# ---------------------------------------------------------------- HOME
ROTOR = [('bb-tents', 'Bikers Bay', 'Bikers Bay motorcycle expo tents at Bagmane Constellation Business Park, Bengaluru'), ('runcle-duo', 'Runcle', 'A Runcle team pair, one cycling and one running, on the course'), ('apache1', 'TVS Apache', 'TVS Apache motorcycles on display at Bagmane Tech Park, Bengaluru'), ('re1', 'Royal Enfield', 'Royal Enfield motorcycle with a painted tank at a Bagmane business park activation'),
         ('axis-wall', 'Axis Bank', 'Axis Bank banking partner stall at the Tu Race Laga corporate run'), ('sign', 'Bagmane Tech Park', 'Bagmane Tech Park entrance sign, Bengaluru'), ('partners', 'Bagmane REIT and Milky Mist', 'Partner pillar showing Bagmane REIT, Milky Mist and GRY branding')]
def rotor():
    slides = ''.join(f'<figure class="rot-s{" on" if i == 0 else ""}"><img src="{{r}}assets/img/{n}.jpg" alt="{html.escape(a)}" width="1280" height="720" loading="lazy"><figcaption>{b}</figcaption></figure>' for i, (n, b, a) in enumerate(ROTOR))
    return f'<div class="frame ratio-43 rotor" data-rotor>{slides}</div>'

FAQS = [
 ("Is it Growthryders or Growth Ryders?", "Both refer to the same company. Growthryders is the brand name; it is also written Growth Ryders or GRY. Growthryders (Growth Ryders) is a brand activation agency in Bengaluru (Bangalore), Karnataka. The website is growthryders.in."),
 ("What does Growthryders do?", "Growthryders is a brand activation agency and through-the-line marketing company based in Bengaluru (Bangalore). One team plans and runs brand activations, experiential marketing, media, corporate events, digital marketing and technology-led experiences."),
 ("Where is Growthryders based?", "Growthryders is based in Bengaluru (Bangalore), Karnataka, India."),
 ("What kinds of brand activations does Growthryders run?", "Corporate park activations, mall and public space promotions, product sampling, roadshows, campus and residential activations, and brand launches."),
 ("Which services does Growthryders offer?", "; ".join(t for k, t, d, cs in SERVICES) + "."),
 ("Which brands has Growthryders been on the ground with?", ", ".join(MARQUEE[:-1]) + " and " + MARQUEE[-1] + "."),
 ("What are Runcle and Bikers Bay?", "They are platforms Growthryders owns. Runcle is a fitness and wellness platform where running meets cycling, for runners, cyclists and corporate teams. Bikers Bay is a motorcycle community with rides, meets and brand collaborations."),
 ("How do I start a project with Growthryders?", f"Call or WhatsApp {PHONE_DISPLAY}, or email {EMAIL}."),
]
def faq_html():
    items = ''.join(f'<details class="qa"><summary><h3>{html.escape(q)}</h3><span class="qa-x" aria-hidden="true"></span></summary><p>{html.escape(a)}</p></details>' for q, a in FAQS)
    return f'<section class="sec white on-light faq-sec" id="faq"><div class="wrap faq"><div class="sec-head"><h2>Questions people ask us</h2></div><div class="qa-list">{items}</div></div></section>'

home = f'''
<section class="hero h3 on-dark">
<div class="h3-wrap">
  <div class="h3-side h3-left"><a class="h3-ico h3-ico0" style="--n:0" href="{{r}}services/brand-activations.html"><span class="h3-bob"><svg viewBox="-10 -5 640 640" aria-hidden="true" fill="none" stroke-linejoin="miter" stroke-miterlimit="6"><path id="h3-ic0" d="M300 555L128 322A205 205 0 1 1 472 322Z"/><use href="#h3-ic0" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="58"/><use href="#h3-ic0" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="58"/><use href="#h3-ic0" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="58"/><use href="#h3-ic0" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="58"/><use href="#h3-ic0" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic0" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic0" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic0" stroke="url(#h3-f)" stroke-width="58"/><use href="#h3-ic0" stroke="url(#h3-i)" stroke-width="42"/><circle cx="300" cy="215" r="34" fill="#f5b321"/></svg></span><span class="h3-lab"><span class="h3-full">Brand activations</span><span class="h3-short" aria-hidden="true">Activations</span></span></a><a class="h3-ico h3-ico1" style="--n:1" href="{{r}}services/experiential-marketing.html"><span class="h3-bob"><svg viewBox="-10 -5 640 640" aria-hidden="true" fill="none" stroke-linejoin="miter" stroke-miterlimit="6"><path id="h3-ic1" d="M300 40L362 238L560 300L362 362L300 560L238 362L40 300L238 238Z"/><use href="#h3-ic1" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="58"/><use href="#h3-ic1" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="58"/><use href="#h3-ic1" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="58"/><use href="#h3-ic1" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="58"/><use href="#h3-ic1" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic1" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic1" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic1" stroke="url(#h3-f)" stroke-width="58"/><use href="#h3-ic1" stroke="url(#h3-i)" stroke-width="42"/><circle cx="300" cy="300" r="34" fill="#f5b321"/></svg></span><span class="h3-lab"><span class="h3-full">Experiential marketing</span><span class="h3-short" aria-hidden="true">Experiential</span></span></a><a class="h3-ico h3-ico2" style="--n:2" href="{{r}}services/corporate-events.html"><span class="h3-bob"><svg viewBox="-10 -5 640 640" aria-hidden="true" fill="none" stroke-linejoin="miter" stroke-miterlimit="6"><path id="h3-ic2" d="M55 125H545V545H55Z M55 250H545 M180 45V125 M420 45V125"/><use href="#h3-ic2" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="58"/><use href="#h3-ic2" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="58"/><use href="#h3-ic2" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="58"/><use href="#h3-ic2" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="58"/><use href="#h3-ic2" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic2" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic2" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic2" stroke="url(#h3-f)" stroke-width="58"/><use href="#h3-ic2" stroke="url(#h3-i)" stroke-width="42"/><circle cx="300" cy="398" r="34" fill="#f5b321"/></svg></span><span class="h3-lab"><span class="h3-full">Corporate events</span><span class="h3-short" aria-hidden="true">Events</span></span></a><a class="h3-ico h3-ico3" style="--n:3" href="{{r}}sponsorship-sales.html"><span class="h3-bob"><svg viewBox="-10 -5 640 640" aria-hidden="true" fill="none" stroke-linejoin="miter" stroke-miterlimit="6"><path id="h3-ic3" d="M60 300A140 140 0 1 0 340 300A140 140 0 1 0 60 300Z M260 300A140 140 0 1 0 540 300A140 140 0 1 0 260 300Z"/><use href="#h3-ic3" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="58"/><use href="#h3-ic3" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="58"/><use href="#h3-ic3" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="58"/><use href="#h3-ic3" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="58"/><use href="#h3-ic3" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic3" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic3" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic3" stroke="url(#h3-f)" stroke-width="58"/><use href="#h3-ic3" stroke="url(#h3-i)" stroke-width="42"/><circle cx="300" cy="300" r="34" fill="#f5b321"/></svg></span><span class="h3-lab"><span class="h3-full">Sponsorship sales</span><span class="h3-short" aria-hidden="true">Sponsorship</span></span></a></div>
  <div class="h3-mid">
    <h1 class="h3-title"><span class="vh">Growthryders, brand activation and marketing company in Bengaluru</span><svg class="h3-name" viewBox="-45 -5 4075 1245" aria-hidden="true" fill="none" stroke-linejoin="miter" stroke-miterlimit="6">
<defs><path id="h3-G" d="M288 260H518V475H55Q0 475 0 420V95Q0 40 55 40H518"/><path id="h3-R" d="M0 475V260H393A110 110 0 0 0 393 40H0 M273 262L506 511"/><path id="h3-R2" d="M0 475V40H393A110 110 0 0 1 393 260H0 M273 262L506 511"/><path id="h3-O" d="M55 40H463Q518 40 518 95V420Q518 475 463 475H55Q0 475 0 420V95Q0 40 55 40Z"/><path id="h3-W" d="M0 40V420Q0 475 55 475H545Q600 475 600 420V40 M300 475V150"/><path id="h3-T" d="M0 40H470 M235 40V475"/><path id="h3-H" d="M0 40V475 M500 40V475 M0 258H500"/><path id="h3-Y" d="M0 118L177 268V475 M327 38V88Q327 128 294 158L177 268"/><path id="h3-D" d="M0 40H282A217.5 217.5 0 0 1 282 475H0Z"/><path id="h3-E" d="M480 40H55Q0 40 0 95V420Q0 475 55 475H480 M0 258H400"/><path id="h3-S" d="M500 40H55Q0 40 0 95V203Q0 258 55 258H445Q500 258 500 313V420Q500 475 445 475H0"/>
<linearGradient id="h3-f" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="520" y2="511"><stop offset="0" stop-color="#fff"/><stop offset=".5" stop-color="#b9adcf"/><stop offset="1" stop-color="#7f7399"/></linearGradient>
<linearGradient id="h3-i" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="511"><stop offset="0" stop-color="#fff"/><stop offset=".42" stop-color="#f7f4fb"/><stop offset=".58" stop-color="#e6dff1"/><stop offset="1" stop-color="#d2c8e4"/></linearGradient>
<linearGradient id="h3-g" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".42" stop-color="#fff0cd" stop-opacity=".55"/><stop offset=".5" stop-color="#fff"/><stop offset=".58" stop-color="#fff0cd" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="h3-m" maskUnits="userSpaceOnUse" x="-45" y="-5" width="4075" height="1245"><use href="#h3-G" transform="translate(35.0 0)" stroke="#fff" stroke-width="70"/><use href="#h3-R" transform="translate(710.0 0)" stroke="#fff" stroke-width="70"/><use href="#h3-O" transform="translate(1380.0 0)" stroke="#fff" stroke-width="70"/><use href="#h3-W" transform="translate(2055.0 0)" stroke="#fff" stroke-width="70"/><use href="#h3-T" transform="translate(2812.0 0)" stroke="#fff" stroke-width="70"/><use href="#h3-H" transform="translate(3439.0 0)" stroke="#fff" stroke-width="70"/><use href="#h3-R2" transform="translate(35.0 661)" stroke="#fff" stroke-width="70"/><use href="#h3-Y" transform="translate(705.0 661)" stroke="#fff" stroke-width="70"/><use href="#h3-D" transform="translate(1189.0 661)" stroke="#fff" stroke-width="70"/><use href="#h3-E" transform="translate(1846.0 661)" stroke="#fff" stroke-width="70"/><use href="#h3-R2" transform="translate(2483.0 661)" stroke="#fff" stroke-width="70"/><use href="#h3-S" transform="translate(3153.0 661)" stroke="#fff" stroke-width="70"/></mask></defs>
<g transform="translate(35.0 0)"><g class="h3-lt" style="--i:0"><use href="#h3-G" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="70"/><use href="#h3-G" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="70"/><use href="#h3-G" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="70"/><use href="#h3-G" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="70"/><use href="#h3-G" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="70"/><use href="#h3-G" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="70"/><use href="#h3-G" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="70"/><use href="#h3-G" stroke="url(#h3-f)" stroke-width="70"/><use href="#h3-G" stroke="url(#h3-i)" stroke-width="51"/></g></g><g transform="translate(710.0 0)"><g class="h3-lt" style="--i:1"><use href="#h3-R" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="70"/><use href="#h3-R" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="70"/><use href="#h3-R" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="70"/><use href="#h3-R" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="70"/><use href="#h3-R" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="70"/><use href="#h3-R" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="70"/><use href="#h3-R" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="70"/><use href="#h3-R" stroke="url(#h3-f)" stroke-width="70"/><use href="#h3-R" stroke="url(#h3-i)" stroke-width="51"/><circle cx="0" cy="150" r="36" fill="#f5b321"/></g></g><g transform="translate(1380.0 0)"><g class="h3-lt" style="--i:3"><use href="#h3-O" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="70"/><use href="#h3-O" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="70"/><use href="#h3-O" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="70"/><use href="#h3-O" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="70"/><use href="#h3-O" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="70"/><use href="#h3-O" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="70"/><use href="#h3-O" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="70"/><use href="#h3-O" stroke="url(#h3-f)" stroke-width="70"/><use href="#h3-O" stroke="url(#h3-i)" stroke-width="51"/></g></g><g transform="translate(2055.0 0)"><g class="h3-lt" style="--i:4"><use href="#h3-W" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="70"/><use href="#h3-W" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="70"/><use href="#h3-W" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="70"/><use href="#h3-W" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="70"/><use href="#h3-W" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="70"/><use href="#h3-W" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="70"/><use href="#h3-W" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="70"/><use href="#h3-W" stroke="url(#h3-f)" stroke-width="70"/><use href="#h3-W" stroke="url(#h3-i)" stroke-width="51"/></g></g><g transform="translate(2812.0 0)"><g class="h3-lt" style="--i:5"><use href="#h3-T" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="70"/><use href="#h3-T" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="70"/><use href="#h3-T" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="70"/><use href="#h3-T" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="70"/><use href="#h3-T" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="70"/><use href="#h3-T" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="70"/><use href="#h3-T" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="70"/><use href="#h3-T" stroke="url(#h3-f)" stroke-width="70"/><use href="#h3-T" stroke="url(#h3-i)" stroke-width="51"/></g></g><g transform="translate(3439.0 0)"><g class="h3-lt" style="--i:6"><use href="#h3-H" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="70"/><use href="#h3-H" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="70"/><use href="#h3-H" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="70"/><use href="#h3-H" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="70"/><use href="#h3-H" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="70"/><use href="#h3-H" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="70"/><use href="#h3-H" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="70"/><use href="#h3-H" stroke="url(#h3-f)" stroke-width="70"/><use href="#h3-H" stroke="url(#h3-i)" stroke-width="51"/></g></g><g transform="translate(35.0 661)"><g class="h3-lt" style="--i:7"><use href="#h3-R2" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="70"/><use href="#h3-R2" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="70"/><use href="#h3-R2" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="70"/><use href="#h3-R2" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="70"/><use href="#h3-R2" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="70"/><use href="#h3-R2" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="70"/><use href="#h3-R2" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="70"/><use href="#h3-R2" stroke="url(#h3-f)" stroke-width="70"/><use href="#h3-R2" stroke="url(#h3-i)" stroke-width="51"/></g></g><g transform="translate(705.0 661)"><g class="h3-lt" style="--i:2"><use href="#h3-Y" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="70"/><use href="#h3-Y" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="70"/><use href="#h3-Y" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="70"/><use href="#h3-Y" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="70"/><use href="#h3-Y" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="70"/><use href="#h3-Y" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="70"/><use href="#h3-Y" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="70"/><use href="#h3-Y" stroke="url(#h3-f)" stroke-width="70"/><use href="#h3-Y" stroke="url(#h3-i)" stroke-width="51"/></g></g><g transform="translate(1189.0 661)"><g class="h3-lt" style="--i:8"><use href="#h3-D" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="70"/><use href="#h3-D" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="70"/><use href="#h3-D" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="70"/><use href="#h3-D" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="70"/><use href="#h3-D" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="70"/><use href="#h3-D" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="70"/><use href="#h3-D" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="70"/><use href="#h3-D" stroke="url(#h3-f)" stroke-width="70"/><use href="#h3-D" stroke="url(#h3-i)" stroke-width="51"/></g></g><g transform="translate(1846.0 661)"><g class="h3-lt" style="--i:9"><use href="#h3-E" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="70"/><use href="#h3-E" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="70"/><use href="#h3-E" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="70"/><use href="#h3-E" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="70"/><use href="#h3-E" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="70"/><use href="#h3-E" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="70"/><use href="#h3-E" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="70"/><use href="#h3-E" stroke="url(#h3-f)" stroke-width="70"/><use href="#h3-E" stroke="url(#h3-i)" stroke-width="51"/></g></g><g transform="translate(2483.0 661)"><g class="h3-lt" style="--i:10"><use href="#h3-R2" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="70"/><use href="#h3-R2" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="70"/><use href="#h3-R2" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="70"/><use href="#h3-R2" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="70"/><use href="#h3-R2" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="70"/><use href="#h3-R2" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="70"/><use href="#h3-R2" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="70"/><use href="#h3-R2" stroke="url(#h3-f)" stroke-width="70"/><use href="#h3-R2" stroke="url(#h3-i)" stroke-width="51"/></g></g><g transform="translate(3153.0 661)"><g class="h3-lt" style="--i:11"><use href="#h3-S" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="70"/><use href="#h3-S" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="70"/><use href="#h3-S" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="70"/><use href="#h3-S" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="70"/><use href="#h3-S" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="70"/><use href="#h3-S" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="70"/><use href="#h3-S" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="70"/><use href="#h3-S" stroke="url(#h3-f)" stroke-width="70"/><use href="#h3-S" stroke="url(#h3-i)" stroke-width="51"/></g></g><g mask="url(#h3-m)"><rect class="h3-glint" x="-900" y="-60" width="520" height="1360" fill="url(#h3-g)"/></g></svg></h1>
    <div class="h3-copy">
    <p class="hero-kicker">Brand activation and marketing company, Bengaluru</p>
    <p class="hero-line">We take brands to where people are.</p>
    <p class="lede">Activations, events, media and digital, planned and run by one team, so your brand is seen, tried and remembered.</p>
    <div class="btn-row"><a class="btn" href="{{r}}services.html">Our services</a><a class="btn ghost" href="{{r}}work.html">Explore our work</a></div>
    </div>
  </div>
  <div class="h3-side h3-right"><a class="h3-ico h3-ico4" style="--n:4" href="{{r}}services/media-solutions.html"><span class="h3-bob"><svg viewBox="-10 -5 640 640" aria-hidden="true" fill="none" stroke-linejoin="miter" stroke-miterlimit="6"><path id="h3-ic4" d="M55 60H545V345H55Z M190 345V555 M410 345V555"/><use href="#h3-ic4" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="58"/><use href="#h3-ic4" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="58"/><use href="#h3-ic4" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="58"/><use href="#h3-ic4" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="58"/><use href="#h3-ic4" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic4" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic4" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic4" stroke="url(#h3-f)" stroke-width="58"/><use href="#h3-ic4" stroke="url(#h3-i)" stroke-width="42"/><circle cx="300" cy="203" r="34" fill="#f5b321"/></svg></span><span class="h3-lab"><span class="h3-full">Media solutions</span><span class="h3-short" aria-hidden="true">Media</span></span></a><a class="h3-ico h3-ico5" style="--n:5" href="{{r}}services/digital-marketing.html"><span class="h3-bob"><svg viewBox="-10 -5 640 640" aria-hidden="true" fill="none" stroke-linejoin="miter" stroke-miterlimit="6"><path id="h3-ic5" d="M222 45H378Q433 45 433 100V500Q433 555 378 555H222Q167 555 167 500V100Q167 45 222 45Z"/><use href="#h3-ic5" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="58"/><use href="#h3-ic5" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="58"/><use href="#h3-ic5" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="58"/><use href="#h3-ic5" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="58"/><use href="#h3-ic5" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic5" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic5" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic5" stroke="url(#h3-f)" stroke-width="58"/><use href="#h3-ic5" stroke="url(#h3-i)" stroke-width="42"/><circle cx="300" cy="455" r="34" fill="#f5b321"/></svg></span><span class="h3-lab"><span class="h3-full">Digital marketing</span><span class="h3-short" aria-hidden="true">Digital</span></span></a><a class="h3-ico h3-ico6" style="--n:6" href="{{r}}services/technology-experiences.html"><span class="h3-bob"><svg viewBox="-10 -5 640 640" aria-hidden="true" fill="none" stroke-linejoin="miter" stroke-miterlimit="6"><path id="h3-ic6" d="M95 180H505Q560 180 560 235V385Q560 440 505 440H395L300 345L205 440H95Q40 440 40 385V235Q40 180 95 180Z"/><use href="#h3-ic6" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="58"/><use href="#h3-ic6" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="58"/><use href="#h3-ic6" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="58"/><use href="#h3-ic6" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="58"/><use href="#h3-ic6" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic6" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic6" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic6" stroke="url(#h3-f)" stroke-width="58"/><use href="#h3-ic6" stroke="url(#h3-i)" stroke-width="42"/><circle cx="165" cy="300" r="34" fill="#f5b321"/></svg></span><span class="h3-lab"><span class="h3-full">Technology-led experiences</span><span class="h3-short" aria-hidden="true">Technology</span></span></a><a class="h3-ico h3-ico7" style="--n:7" href="{{r}}services/film-production.html"><span class="h3-bob"><svg viewBox="-10 -5 640 640" aria-hidden="true" fill="none" stroke-linejoin="miter" stroke-miterlimit="6"><path id="h3-ic7" d="M50 160H390V440H50Z M390 262L550 175V425L390 338"/><use href="#h3-ic7" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="58"/><use href="#h3-ic7" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="58"/><use href="#h3-ic7" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="58"/><use href="#h3-ic7" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="58"/><use href="#h3-ic7" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic7" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic7" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic7" stroke="url(#h3-f)" stroke-width="58"/><use href="#h3-ic7" stroke="url(#h3-i)" stroke-width="42"/><circle cx="220" cy="300" r="34" fill="#f5b321"/></svg></span><span class="h3-lab"><span class="h3-full">Film and content production</span><span class="h3-short" aria-hidden="true">Films</span></span></a></div>
</div>
</section>
<script src="{{r}}assets/js/hero3d.js?v=1" defer></script>
{marquee()}

<section class="sec white on-light"><div class="wrap split">
  <div>
    <h2>Brand activations are our fulcrum.</h2>
    <p class="lede" style="margin-top:22px">Marketing becomes more powerful when a brand moves beyond communication and creates a real interaction with the people it wants to reach.</p>
    <p>We put the activation at the centre of the plan and build everything else around it: traditional media, digital platforms, outdoor advertising and experiential engagement, working as one through-the-line campaign.</p>
    <div class="btn-row"><a class="btn ghost" href="{{r}}about.html">About Growthryders</a></div>
  </div>
  {rotor()}
</div></section>

<section class="sec on-light"><div class="wrap">
  <div class="sec-head"><p class="kicker">Our services</p><h2>One partner. Multiple marketing capabilities.</h2><p class="lede">Eight services under one roof, so a campaign is planned, built, promoted and run by the same team.</p></div>
  <ul class="svc">
    {''.join(f'<li><a href="{{r}}{svc_href(k)}"><h3>{t}</h3><div><p>{d}</p><ul class="chips">{"".join(f"<li>{c}</li>" for c in cs)}</ul></div><span class="go" aria-hidden="true">View</span></a></li>' for k, t, d, cs in SERVICES)}
  </ul>
</div></section>

<section class="sec dark on-dark"><div class="wrap">
  <div class="sec-head"><h2>Ideas that translate into experiences.</h2><p class="lede">Campaigns we conceptualised and ran on the ground.</p></div>
  <article class="work-row">
    {img('runners1', 'Runners in Tu Race Laga jerseys on the course inside Bagmane Tech Park', 'ratio-169', 1280, 720)}
    <div><p class="tags">Sports marketing, corporate engagement, integrated activation</p>
      <h3>TVS Apache presents Tu Race Laga</h3>
      <p>A 40-day brand engagement campaign across five Bagmane business parks, ending in a corporate run with 3K, 5K and 10K categories.</p>
      {bibs(TRL_BIBS[:2])}
      <p style="margin-top:26px"><a class="more" href="{{r}}work/tu-race-laga.html">Read the case study</a></p></div>
  </article>
  <article class="work-row">
    {img('apache2', 'A TVS Apache motorcycle in the brand display zone', 'ratio-169', 1280, 720)}
    <div><p class="tags">Corporate park activation, product display, consumer engagement</p>
      <h3>TVS Apache at Bagmane</h3>
      <p>Motorcycle display and engagement zones that took the Apache experience straight to a technology-park audience.</p>
      <p style="margin-top:26px"><a class="more" href="{{r}}work/tvs-apache-bagmane.html">Read the case study</a></p></div>
  </article>
  <article class="work-row">
    {img('re1', 'A Royal Enfield motorcycle on display at a Bagmane business park', 'ratio-169', 1280, 720)}
    <div><p class="tags">Community engagement, brand association, motorcycle lifestyle</p>
      <h3>Royal Enfield with Bikers Bay</h3>
      <p>A dedicated Royal Enfield engagement space at Bagmane Constellation Business Park, run through our Bikers Bay rider community.</p>
      <p style="margin-top:26px"><a class="more" href="{{r}}work/royal-enfield-bikers-bay.html">Read the case study</a></p></div>
  </article>
</div></section>


<section class="sec white on-light films-sec"><div class="wrap">
  <div class="sec-head row"><div><h2>Films from the ground.</h2><p class="lede">Every campaign leaves with its own film. Play one.</p></div><a class="btn ghost" href="{{r}}films.html">All films</a></div>
</div>
  <div class="strip-wrap">
    <button class="strip-btn prev" type="button" aria-label="Previous films"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
    <div class="strip" tabindex="0" aria-label="Campaign films">{''.join(film(f) for f in FILMS)}</div>
    <button class="strip-btn next" type="button" aria-label="Next films"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
  </div>
</section>
{PLAYER}
<section class="sec on-light"><div class="wrap">
  <div class="sec-head"><h2>Building communities. Creating brand platforms.</h2><p class="lede">Runcle and Bikers Bay are platforms we own. They give brands a recurring way to meet passionate, engaged communities.</p></div>
  <div class="ips">
    <article class="ip">{img('finish', 'Finishers celebrating with medals after the run', 'ratio-169', 1280, 720)}<div class="body"><h3>Runcle</h3><p style="margin-top:10px">Running meets cycling. A fitness and wellness platform for runners, cyclists and corporate teams.</p><a class="more" style="font-weight:700;color:var(--plum)" href="{{r}}ips.html#runcle">About Runcle</a></div></article>
    <article class="ip">{img('re2', 'Royal Enfield motorcycles lined up at a display', 'ratio-169', 1280, 720)}<div class="body"><h3>Bikers Bay</h3><p style="margin-top:10px">The motorcycle community. Rides, meets and brand collaborations for people who live on two wheels.</p><a class="more" style="font-weight:700;color:var(--plum)" href="{{r}}ips.html#bikers-bay">About Bikers Bay</a></div></article>
  </div>
</div></section>

{faq_html()}
<section class="sec plum on-dark"><div class="wrap">
  <div class="sec-head"><h2>Beyond conventional marketing.</h2></div>
  <dl class="why">
    <div><dt>Activation-led thinking</dt><dd>Meaningful consumer engagement sits at the heart of every plan we write.</dd></div>
    <div><dt>Integrated capabilities</dt><dd>Activations, traditional media, digital and experiential work from one team.</dd></div>
    <div><dt>Creative execution</dt><dd>We turn a marketing objective into a campaign people can walk into.</dd></div>
    <div><dt>Community ecosystems</dt><dd>Our own platforms give brands an audience that comes back.</dd></div>
    <div><dt>End-to-end management</dt><dd>Concept, planning, production and on-ground execution, managed together.</dd></div>
  </dl>
</div></section>
{CTA}
'''
import re
if not FILMS_LIVE: home = re.sub(r'<section class="sec white on-light films-sec">.*?</dialog>\n', '', home, flags=re.S)
page('index.html', 'Growthryders (Growth Ryders) | Brand activation agency in Bengaluru',
     'Growthryders, also written Growth Ryders, is a brand activation agency in Bengaluru (Bangalore): tech park and mall activations, experiential marketing, media, corporate events and digital.', home, 'dark', intro=True)

# ---------------------------------------------------------------- ABOUT
about = f'''
<section class="page-head on-dark"><div class="wrap">
  <h1>Accelerating growth through activations, integrated marketing and experiences.</h1>
  <p class="lede">Growthryders is an integrated marketing and brand activation company that helps brands connect, engage and grow.</p>
</div></section>
<section class="sec white on-light"><div class="wrap split top">
  <div>
    <h2>What we believe</h2>
    <p class="lede" style="margin-top:22px">Successful marketing is built on meaningful consumer interactions and strategic brand partnerships.</p>
    <p>Brand activations sit at the centre of our marketing ecosystem, supported by a mix of traditional media, digital marketing, experiential engagement and new communication platforms.</p>
    <p>We develop Through-the-Line (TTL) solutions that bring strategy, creativity, technology and execution together. Our work spans consumer activations, corporate engagement, media solutions, digital campaigns, experiential marketing and community-driven Intellectual Properties.</p>
    <p>Complementing our marketing capabilities is our <strong>Sponsorship Sales &amp; Revenue Management</strong> vertical, where we help IP owners, event organisers and B2B conference platforms unlock revenue opportunities through structured sponsorship strategies. Leveraging AI-enabled prospecting and a human-led sales approach, we manage the entire sales lifecycle – from sponsor identification and lead generation to engagement, negotiations and commercial closure – building continuous sponsorship pipelines and strategic brand partnerships.</p>
    <p>From bringing a product launch to life and executing large-scale consumer campaigns to monetising an Intellectual Property or building a platform of our own, we bring ideas to life and turn opportunities into growth.</p>
  </div>
  {img('group', 'Participants and organisers under the finish arch at Tu Race Laga')}
</div></section>
<section class="sec on-light founder-sec" id="founder"><div class="wrap founder">
  <div class="frame founder-photo"><img src="{{r}}assets/img/founder.jpg?v=2" alt="Surender Loganathan, founder of Growthryders" width="880" height="1100" loading="lazy"></div>
  <div>
    <p class="kicker">Founder</p>
    <h2>Surender Loganathan</h2>
    <p class="lede" style="margin-top:18px">Surender founded Growthryders and leads its work with brands, from the first conversation to the day of the activation.</p>
    <div class="btn-row"><a class="btn wi" href="{LINKEDIN}" target="_blank" rel="noopener me">View LinkedIn profile</a><a class="btn ghost wi" href="tel:+{PHONE_E164}">{IC_CALL}{PHONE_DISPLAY}</a><a class="btn ghost wi" href="https://wa.me/{PHONE_E164}">{IC_CHAT}WhatsApp</a></div>
  </div>
</div></section>
<section class="sec on-light"><div class="wrap split top">
  <div><h2>Our vision</h2><p class="lede" style="margin-top:18px">To become a trusted growth partner for brands through innovative marketing ecosystems, impactful experiences and sustainable consumer engagement.</p></div>
  <div><h2>Our mission</h2><p class="lede" style="margin-top:18px">To empower brands through integrated marketing, creative activations and community-led platforms that generate visibility, engagement and growth.</p></div>
</div></section>
<section class="sec white on-light"><div class="wrap">
  <div class="sec-head"><h2>How a campaign runs</h2><p class="lede">Every campaign follows the same six steps.</p></div>
  <ol class="steps">
    <li><span>Understand the brand and the marketing objective.</span></li>
    <li><span>Identify the audience and the touchpoints where they can be reached.</span></li>
    <li><span>Develop the activation concept and creative strategy.</span></li>
    <li><span>Plan the media and communication around it.</span></li>
    <li><span>Execute the campaign across the selected locations.</span></li>
    <li><span>Evaluate engagement, participation and outcomes.</span></li>
  </ol>
</div></section>
{CTA}
'''
page('about.html', 'About Growthryders (Growth Ryders) | Brand activation company, Bengaluru',
     'Growthryders (Growth Ryders) builds through-the-line marketing around brand activations: consumer engagement, media, digital, experiential work and community platforms.', about, 'dark')

# ---------------------------------------------------------------- SERVICES
def ul(items): return '<ul class="cols">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
services = f'''
<section class="page-head on-dark"><div class="wrap">
  <h1>Brands should be experienced, not just advertised.</h1>
  <p class="lede">Activations are the centre of what we do. Every other service exists to carry them further.</p>
</div></section>
<section class="sec white on-light" style="padding-top:0"><div class="wrap">
  <div class="service-block" id="activations" style="border-top:0">
    <div><h2>Brand activations and TTL marketing</h2><p style="margin-top:14px"><a class="more" href="{{r}}services/brand-activations.html">More on this service</a></p><p style="margin-top:8px"><a class="more" href="{{r}}services/tech-park-activations.html">Tech park and corporate park activations</a></p></div>
    <div><p class="lede">We conceptualise and run consumer engagement programmes that bring a brand face to face with its audience.</p>
      {ul(['Consumer and product sampling', 'Retail and trade marketing', 'Corporate park activations', 'Mall and public space promotions', 'Roadshows and mobile campaigns', 'Campus and youth engagement', 'Residential community activations', 'Dealer and channel partner engagement', 'Guerrilla marketing', 'Brand launches and promotional campaigns'])}
      <h3 style="margin-top:32px">Integrated around the activation</h3>
      <p style="margin-top:10px">We amplify each activation through the channels that reach the same people, so the message stays consistent across physical and digital touchpoints.</p>
      {ul(['Outdoor advertising, OOH and DOOH', 'Digital and social media campaigns', 'Print and radio advertising', 'Transit and airport media', 'Retail and point-of-sale branding', 'Innovative and ambient media'])}</div>
  </div>
  <div class="service-block" id="digital">
    <div><h2>Digital marketing</h2><p style="margin-top:14px"><a class="more" href="{{r}}services/digital-marketing.html">More on this service</a></p></div>
    <div><p class="lede">We help brands strengthen their digital presence and reach the right audience.</p>
      {ul(['Search engine optimisation (SEO)', 'Generative engine optimisation (GEO)', 'Performance marketing', 'Social media management', 'Content strategy and creation', 'Website design and development', 'Lead generation', 'Digital campaign management', 'Marketing analytics and automation'])}</div>
  </div>
  <div class="service-block" id="experiential">
    <div><h2>Experiential marketing</h2><p style="margin-top:14px"><a class="more" href="{{r}}services/experiential-marketing.html">More on this service</a></p></div>
    <div><p class="lede">Immersive experiences that turn brand communication into something people remember.</p>
      {ul(['Product launches', 'Corporate events and conferences', 'Trade shows and exhibitions', 'Technology-led installations', 'Augmented and virtual reality', 'Interactive digital experiences', 'Gamification', 'Immersive brand storytelling', 'Employee and partner engagement'])}</div>
  </div>
  <div class="service-block" id="media">
    <div><h2>Media solutions</h2><p style="margin-top:14px"><a class="more" href="{{r}}services/media-solutions.html">More on this service</a></p></div>
    <div><p class="lede">Media planning and execution across the formats that surround an activation.</p>
      {ul(['Outdoor and digital outdoor media', 'Transit and airport media', 'Print and radio', 'Corporate park media', 'Mall and retail media', 'Innovative and ambient media platforms'])}</div>
  </div>
  <div class="service-block" id="events">
    <div><h2>Corporate events and engagement</h2><p style="margin-top:14px"><a class="more" href="{{r}}services/corporate-events.html">More on this service</a></p></div>
    <div><p class="lede">Business and corporate engagement platforms, conceptualised and executed end to end.</p>
      {ul(['Conferences and annual meets', 'Dealer meets', 'Leadership summits', 'Awards', 'Employee engagement programmes', 'Product launches'])}</div>
  </div>
  <div class="service-block spons" id="sponsorship">
    <div><p class="kicker">New service</p><h2>Sponsorship Sales &amp; Revenue Management</h2><p style="margin-top:14px"><a class="more" href="{{r}}sponsorship-sales.html">More on this service</a></p></div>
    <div><p class="lede">Turning IPs, Events &amp; B2B Platforms into Revenue Opportunities.</p>
      <p>We help Intellectual Property (IP) owners, event organisers and B2B conference platforms unlock sponsorship opportunities through a structured, technology-enabled sales ecosystem.</p>
      <p>Combining AI-powered research and prospecting with human-led engagement, relationship management and commercial negotiations, we manage the complete sponsorship sales lifecycle.</p>
      <p>Our approach builds a continuous sales pipeline, from identifying potential sponsors and mapping decision-makers to personalised outreach, proposal development, negotiations and closure.</p>
      <h3>Our capabilities include:</h3>
      {ul(['Sponsorship Strategy &amp; Revenue Planning', 'IP and Event Monetisation', 'AI-enabled Brand Identification &amp; Prospecting', 'Industry-wise Sponsor Database Development', 'Decision-maker Mapping &amp; Lead Qualification', 'Personalised Outreach &amp; Sales Engagement', 'Sponsorship Proposal Development', 'Negotiations &amp; Commercial Closure', 'CRM-based Pipeline &amp; Follow-up Management', 'Sponsorship Revenue Tracking &amp; Reporting'])}
      <h3 style="margin-top:28px">Our Operating Model: AI Intelligence + Human Expertise</h3>
      <p>We combine the speed and intelligence of AI with the relationship-building and negotiation capabilities of experienced sales professionals to create a continuous, opportunity-driven sponsorship pipeline.</p>
      <p>From individual events and proprietary IPs to large-scale B2B conclaves, conferences and industry platforms, we operate as an extended sponsorship sales and revenue management partner.</p></div>
    <div class="spons-vis">
      <p class="spons-line">AI-powered prospecting. Human-led engagement. Continuous sales pipeline.</p>
      <div class="pillars">
        <div><h3>AI Intelligence</h3><p>Research, brand identification, prospecting and lead qualification.</p></div>
        <div><h3>Human Expertise</h3><p>Outreach, meetings, relationships and negotiations.</p></div>
        <div><h3>Sales Conversion</h3><p>Proposals, opportunity management and closure.</p></div>
        <div><h3>Revenue Management</h3><p>Pipeline tracking, forecasting and reporting.</p></div>
      </div>
      <ol class="flow" aria-label="Sponsorship sales pipeline"><li>Identify</li><li>Prospect</li><li>Engage</li><li>Propose</li><li>Negotiate</li><li>Close</li></ol>
      <p class="flow-cap">Continuous Sponsorship Sales Pipeline</p>
    </div>
  </div>
  <div class="service-block" id="technology">
    <div><h2>Technology-led experiences</h2><p style="margin-top:14px"><a class="more" href="{{r}}services/technology-experiences.html">More on this service</a></p></div>
    <div><p class="lede">Installations and interactive formats built into the activation.</p>
      {ul(['Technology-led installations', 'Augmented and virtual reality', 'Interactive digital experiences', 'Gamification'])}</div>
  </div>
  <div class="service-block" id="films">
    <div><h2>Film and content production</h2><p style="margin-top:14px"><a class="more" href="{{r}}services/film-production.html">More on this service</a></p></div>
    <div><p class="lede">We shoot and edit the films of the activations and events we run.</p>
      {ul(['Event films', 'Brand and partner films', 'Reels and vertical cuts for social media', 'On-ground shooting', 'Editing'])}
      <div class="btn-row" style="margin-top:22px"><a class="btn ghost" href="{{r}}films.html">Watch our films</a></div></div>
  </div>
</div></section>
{CTA}
'''
page('services.html', 'Services | Brand activations, experiential marketing, media and events in Bengaluru | Growthryders',
     'Brand activations and BTL/TTL marketing, tech park and mall activations, experiential marketing, media, corporate events, digital marketing and event film production in Bengaluru (Bangalore).', services, 'dark')

# ---------------------------------------------------------------- WORK INDEX
work = f'''
<section class="page-head on-dark"><div class="wrap">
  <h1>Ideas into action. Brands into experiences.</h1>
  <p class="lede">The best demonstration of what we can do is the work we have run.</p>
</div></section>
<section class="sec dark on-dark" style="padding-top:0"><div class="wrap">
  <article class="work-row" style="border-top:0">
    {img('flagoff', 'The flag-off at Tu Race Laga, runners leaving the start arch', 'ratio-169', 1280, 720, True)}
    <div><p class="tags">Sports marketing, corporate engagement, integrated activation</p>
      <h3>TVS Apache presents Tu Race Laga</h3>
      <p>A brand-led fitness movement across Bagmane business parks, ending in a corporate run on 31 October 2026.</p>
      {bibs(TRL_BIBS[:2])}
      <p style="margin-top:26px"><a class="more" href="{{r}}work/tu-race-laga.html">Read the case study</a></p></div>
  </article>
  <article class="work-row">
    {img('apache2', 'A TVS Apache motorcycle in the brand display zone', 'ratio-169', 1280, 720)}
    <div><p class="tags">Corporate park activation, product display, consumer engagement</p>
      <h3>TVS Apache at Bagmane</h3>
      <p>Taking the Apache experience to corporate audiences through display and engagement zones inside technology parks.</p>
      <p style="margin-top:26px"><a class="more" href="{{r}}work/tvs-apache-bagmane.html">Read the case study</a></p></div>
  </article>
  <article class="work-row">
    {img('re1', 'A Royal Enfield motorcycle on display at a Bagmane business park', 'ratio-169', 1280, 720)}
    <div><p class="tags">Community engagement, brand association, motorcycle lifestyle</p>
      <h3>Royal Enfield with Bikers Bay</h3>
      <p>Connecting a legendary motorcycle brand with rider communities at Bagmane Constellation Business Park.</p>
      <p style="margin-top:26px"><a class="more" href="{{r}}work/royal-enfield-bikers-bay.html">Read the case study</a></p></div>
  </article>
</div></section>
{CTA}
'''
page('work.html', 'Our work | Campaign case studies | Growthryders',
     'Case studies from Growthryders: TVS Apache Tu Race Laga, TVS Apache activations at Bagmane, and Royal Enfield with Bikers Bay.', work, 'dark')

# ---------------------------------------------------------------- CASE STUDIES
def case(path, title, desc, h1, lede, facts, intro, elements_title, elements, role, gallery, extra='', film_keys=()):
    f = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in facts)
    body = f'''
<section class="page-head on-dark"><div class="wrap">
  <p class="kicker"><a href="{{r}}work.html" style="text-decoration:none">Our work</a></p>
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
</div></section>
<section class="sec white on-light"><div class="wrap split top">
  <div>{intro}</div>
  <div><dl class="facts">{f}</dl>{extra}</div>
</div></section>
<section class="sec on-light" style="padding-top:0;background:#fff"><div class="wrap"><div class="gallery">{gallery}</div></div></section>
{('<section class="sec dark on-dark films-page"><div class="wrap"><div class="sec-head"><h2>Watch the films</h2></div><div class="' + ('grid-port' if FILMS_BY[film_keys[0]][4]=='port' else 'grid-land') + '">' + ''.join(film(FILMS_BY[k]) for k in film_keys) + '</div></div></section>' + PLAYER) if (film_keys and FILMS_LIVE) else ''}
<section class="sec on-light"><div class="wrap split top">
  <div><h2>{elements_title}</h2></div>
  <div><ul style="margin:0;padding-left:1.1em;display:grid;gap:10px">{''.join(f'<li>{e}</li>' for e in elements)}</ul>
  <h3 style="margin-top:36px">Our role</h3><p style="margin-top:10px">{role}</p></div>
</div></section>
{CTA}'''
    page(path, title, desc, body, 'dark', 1)

FILMS_BY = {f[0]: f for f in FILMS}
def g(name, alt, wide=False): return img(name, alt, 'ratio-169' + (' wide' if wide else ''), 1280, 720)

case('work/tu-race-laga.html', 'TVS Apache presents Tu Race Laga | Case study | Growthryders',
     'How Growthryders ran Tu Race Laga for TVS Apache: a 40-day campaign across five Bagmane business parks and a corporate run with about 1,600 participants and guests.',
     'TVS Apache presents Tu Race Laga', 'A brand-led fitness movement across Bagmane tech parks.',
     [('Campaign', 'TVS Apache presents Tu Race Laga'), ('Venue', 'Bagmane Tech Park, Bengaluru'), ('Date', '31 October 2026'), ('Presenting sponsor', 'TVS Apache'), ('In association with', 'Bagmane REIT')],
     '''<h2>Fitness as the meeting point</h2>
     <p class="lede" style="margin-top:22px">We conceptualised and ran an integrated corporate fitness and brand engagement campaign that brought TVS Apache, Bagmane REIT and the workforce of Bengaluru's Bagmane business parks together.</p>
     <p>The campaign used fitness as the platform to connect the Apache brand with a large, active corporate audience, first in the parks where they work and then on the start line.</p>''',
     'What the campaign included',
     ['Campaign visibility across five Bagmane business parks.', 'Apache motorcycle displays and brand engagement zones.', 'Standees and digital registration touchpoints.', 'Apache-themed photo and video experiences.', 'On-ground registration and participant acquisition.', 'A flagship run with 3K, 5K and 10K categories.', 'Brand integration through event branding, stage presence, participant engagement and sampling.'],
     'Campaign conceptualisation, brand integration, activation planning, on-ground execution and event management.',
     g('flagoff', 'Runners leaving the start arch at the flag-off', True) + g('runners2', 'Runners on the course inside the tech park') + g('axis', 'Participants at a partner activity stall') + g('finish', 'Finishers celebrating after the run', True) + g('group', 'Participants and organisers under the finish arch at Tu Race Laga', True) + g('medals', 'Finisher medals laid out for the runners'),
     bibs(TRL_BIBS, True) + '<p style="margin-top:26px"><a class="more" href="{r}work/tu-race-laga-sponsorship-case-study.html">Read the sponsorship case study</a></p>', film_keys=('tu-race-laga-event-film', 'tvs-apache-tu-race-laga', 'axis-bank-tu-race-laga', 'milky-mist-tu-race-laga'))

case('work/tvs-apache-bagmane.html', 'TVS Apache activations at Bagmane | Case study | Growthryders',
     'Growthryders created motorcycle display and engagement zones for TVS Apache inside Bagmane business parks.',
     'TVS Apache at Bagmane', 'Taking the Apache experience to corporate audiences.',
     [('Brand', 'TVS Apache'), ('Where', 'Bagmane business parks, Bengaluru'), ('Format', 'Display and engagement zones')],
     '''<h2>The motorcycle comes to the audience</h2>
     <p class="lede" style="margin-top:22px">We developed on-ground engagement opportunities for TVS Apache across the Bagmane corporate ecosystem.</p>
     <p>Display and engagement zones were positioned inside the technology parks, so people met the motorcycles in the course of their working day.</p>''',
     'What the activation included',
     ['Motorcycle display zones within Bagmane business parks.', 'Dedicated promotional spaces near high-footfall areas.', 'Brand visibility through standees and campaign communication.', 'Apache-themed photo opportunities.', 'QR-based campaign engagement.', 'Direct product discovery and consumer interaction.'],
     'Brand activation strategy, corporate park coordination, display execution and consumer engagement.',
     g('apache1', 'TVS Apache motorcycles on display', True) + g('apache2', 'A TVS Apache motorcycle close up in the display zone') + g('sign', 'The Bagmane Tech Park sign on a green wall') + g('apache3', 'The Tu Race Laga finish arch carrying TVS Apache branding', True), film_keys=('tvs-apache-tu-race-laga',))

case('work/royal-enfield-bikers-bay.html', 'Royal Enfield with Bikers Bay | Case study | Growthryders',
     'Growthryders created a Royal Enfield engagement space at Bagmane Constellation Business Park through its Bikers Bay rider community.',
     'Royal Enfield with Bikers Bay', 'Connecting a legendary motorcycle brand with rider communities.',
     [('Brand', 'Royal Enfield'), ('Platform', 'Bikers Bay'), ('Venue', 'Bagmane Constellation Business Park'), ('Dates', '22 and 23 January 2025'), ('Space', '20 ft by 10 ft branded engagement space')],
     '''<h2>A community, not just a stall</h2>
     <p class="lede" style="margin-top:22px">We created an engagement opportunity for Royal Enfield through our Bikers Bay community platform.</p>
     <p>The initiative placed the Royal Enfield brand alongside a community of motorcycle enthusiasts and in front of the wider corporate audience of the business park.</p>''',
     'What the engagement included',
     ['A dedicated branded activation space.', 'Association with the Bikers Bay community.', 'Visibility with the corporate audience.', 'Motorcycle lifestyle and community-led engagement.', 'Brand presence inside an established rider platform.'],
     'Community platform integration, activation space coordination and brand engagement.',
     g('re1', 'A Royal Enfield motorcycle on display at a Bagmane business park', True) + g('re2', 'Royal Enfield motorcycles lined up at a display') + g('re3', 'Visitors looking at a Royal Enfield motorcycle', True) + g('re4', 'Detail of a Royal Enfield motorcycle') + g('bb-re', 'Visitors trying a Royal Enfield Guerrilla in the Bikers Bay space, January 2025', True) + g('bb-re2', 'Royal Enfield Guerrilla display at Bikers Bay'), film_keys=('royal-enfield-bagmane-film', 'royal-enfield-tech-park', 'royal-enfield-capital'))


# ---------------------------------------------------------------- FILMS
FOLDERS = [
 ('bagmane', 'Bagmane Tech Park', 'Tu Race Laga at Bagmane Tech Park, Bengaluru: the event film, with TVS Apache, Bagmane REIT and partners.', ['tu-race-laga-event-film']),
 ('tvs-apache', 'TVS Apache', 'TVS Apache at Tu Race Laga: motorcycle displays, engagement zones and the corporate run.', ['tvs-apache-tu-race-laga', 'tvs-apache-reel']),
 ('royal-enfield', 'Royal Enfield at Bagmane parks', 'Royal Enfield motorcycle displays across the Bagmane business parks, at Bagmane Tech Park and at Bagmane Capital.', ['royal-enfield-bagmane-film', 'royal-enfield-tech-park', 'royal-enfield-capital']),
 ('partners', 'Axis Bank and Milky Mist', 'Partner brand films from Tu Race Laga: Axis Bank and Milky Mist on the ground with runners.', ['axis-bank-tu-race-laga', 'milky-mist-tu-race-laga']),
]
_FB = {f[0]: f for f in FILMS}
def folder(k, t, d, keys):
    return f'''<section class="fold{" side" if k == "royal-enfield" else ""}{" one" if len(keys) == 1 else ""}" id="{k}"><div class="fold-head"><h2 class="films-h">{t}</h2><p>{d}</p></div><div class="grid-mix">{"".join(film(_FB[x], k == "bagmane") for x in keys)}</div></section>'''
films = f'''
<section class="page-head on-dark"><div class="wrap">
  <h1>Brand activation films from the ground.</h1>
  <p class="lede">Eight films from our brand activations in Bengaluru, filed by brand: TVS Apache, Royal Enfield, Axis Bank and Milky Mist, at Bagmane business parks.</p>
  <nav class="fold-nav" aria-label="Film folders">{"".join(f'<a href="#{k}">{t}</a>' for k, t, d, ks in FOLDERS)}</nav>
</div></section>
<section class="sec dark on-dark films-page" style="padding-top:0"><div class="wrap">
  {"".join(folder(*f) for f in FOLDERS)}
</div></section>
{PLAYER}
{CTA}
'''
if FILMS_LIVE: page('films.html', 'Brand activation films | TVS Apache, Royal Enfield, Bagmane Tech Park | Growthryders',
     'Watch brand activation films by Growthryders, Bengaluru: TVS Apache Tu Race Laga, Royal Enfield at Bagmane Tech Park and Bagmane Capital, Axis Bank and Milky Mist.', films, 'dark')

# ---------------------------------------------------------------- IPS
# ---------------------------------------------------------------- SERVICE PAGES (one page per thing people search for)
WORK_CARDS = {
 'trl': ('work/tu-race-laga.html', 'flagoff', 'The flag-off at Tu Race Laga, runners leaving the start arch', 'TVS Apache presents Tu Race Laga', 'A 40-day campaign across five Bagmane business parks, ending in a corporate run with about 1,600 participants and guests.'),
 'tvs': ('work/tvs-apache-bagmane.html', 'apache1', 'TVS Apache motorcycles on display at Bagmane Tech Park', 'TVS Apache activations at Bagmane', 'Motorcycle display and engagement zones for TVS Apache inside Bagmane business parks.'),
 're':  ('work/royal-enfield-bikers-bay.html', 're1', 'Royal Enfield motorcycle with a painted tank at a Bagmane park', 'Royal Enfield with Bikers Bay', 'A Royal Enfield engagement space at Bagmane Constellation Business Park through the Bikers Bay rider community.'),
}
def work_cards(keys):
    out = ''
    for k in keys:
        href, im, alt, t, d = WORK_CARDS[k]
        out += f'<article class="ip">{img(im, alt, "ratio-169", 1280, 720)}<div class="body"><h3>{t}</h3><p style="margin-top:10px">{d}</p><a class="more" style="margin-top:16px;display:inline-block" href="{{r}}{href}">Read the case study</a></div></article>'
    return f'<div class="ips svc-cards n{len(keys)}">{out}</div>'
SVC_PAGES = [
 dict(slug='brand-activations', sid='activations', title='Brand activation agency in Bengaluru (Bangalore) | Growthryders',
      desc='Growthryders is a brand activation agency in Bengaluru: corporate park and mall activations, product sampling, roadshows, campus and residential activations and brand launches.',
      h1='Brand activation agency in Bengaluru.', lede='We plan and run on-ground brand activations that put a brand face to face with the people it wants to reach.',
      h2='What a brand activation with us includes', intro='Brand activations are the centre of our work. We conceptualise the idea, plan the locations, build the set-up and run it on the ground, then carry it further through media and digital.',
      items=['Consumer and product sampling', 'Retail and trade marketing', 'Corporate park activations', 'Mall and public space promotions', 'Roadshows and mobile campaigns', 'Campus and youth engagement', 'Residential community activations', 'Dealer and channel partner engagement', 'Guerrilla marketing', 'Brand launches and promotional campaigns'],
      h2b='Integrated around the activation', itemsb=['Outdoor advertising, OOH and DOOH', 'Digital and social media campaigns', 'Print and radio advertising', 'Transit and airport media', 'Retail and point-of-sale branding', 'Innovative and ambient media'],
      work=['trl', 'tvs', 're'], films=[],
      faq=[('What is a brand activation?', 'A brand activation is an on-ground campaign where people meet a brand directly: they see the product, try it, take part in an activity or talk to the team, instead of only seeing an advertisement.'),
           ('Where does Growthryders run brand activations in Bengaluru?', 'In corporate and tech parks such as the Bagmane business parks, in malls and public spaces, on campuses, in residential communities and at dealer and retail locations.'),
           ('Which brands has Growthryders run activations for?', 'TVS Apache across five Bagmane business parks and at the Tu Race Laga corporate run, and Royal Enfield at Bagmane Constellation Business Park through the Bikers Bay community.')]),
 dict(slug='tech-park-activations', sid='activations', title='Tech park and corporate park activations in Bengaluru | Growthryders',
      desc='Tech park and corporate park brand activations in Bengaluru by Growthryders: product display zones, employee engagement and campaigns inside business parks such as Bagmane.',
      h1='Tech park and corporate park activations in Bengaluru.', lede='We take brands inside business parks, to the people who work there, with display zones, engagement spaces and campaigns that run across several parks.',
      h2='What we set up inside a business park', intro='A corporate park puts a large working audience in one place every day. We handle the coordination with the park, the display and engagement spaces, the on-ground team and the communication around them.',
      items=['Product display zones inside the park', 'Promotional spaces near high-footfall areas', 'Standees and campaign communication', 'Themed photo and video experiences', 'QR-based campaign engagement', 'On-ground registration and participant acquisition', 'Product discovery and direct consumer interaction', 'Multi-park campaigns'],
      h2b='', itemsb=[], work=['trl', 'tvs', 're'], films=['royal-enfield-bagmane-film', 'royal-enfield-tech-park', 'royal-enfield-capital'],
      faq=[('Which tech parks has Growthryders worked in?', 'Growthryders has run campaigns across five Bagmane business parks in Bengaluru, including Bagmane Tech Park, Bagmane Capital and Bagmane Constellation Business Park.'),
           ('What can a brand do inside a tech park?', 'Product displays, engagement and sampling zones, photo and video experiences, registrations for an event, and standee and digital communication, in the high-footfall areas of the park.'),
           ('How long does a tech park campaign run?', 'It depends on the plan. Tu Race Laga for TVS Apache ran as a 40-day campaign across five Bagmane business parks and ended in a corporate run.')]),
 dict(slug='experiential-marketing', sid='experiential', title='Experiential marketing agency in Bengaluru (Bangalore) | Growthryders',
      desc='Experiential marketing in Bengaluru by Growthryders: product launches, trade shows and exhibitions, immersive brand storytelling and employee and partner engagement.',
      h1='Experiential marketing agency in Bengaluru.', lede='Immersive experiences that turn brand communication into something people take part in and remember.',
      h2='What we create', intro='We design the experience around what the brand wants people to feel and do, then build and run it.',
      items=['Product launches', 'Corporate events and conferences', 'Trade shows and exhibitions', 'Technology-led installations', 'Augmented and virtual reality', 'Interactive digital experiences', 'Gamification', 'Immersive brand storytelling', 'Employee and partner engagement'],
      h2b='', itemsb=[], work=['trl', 're'], films=[],
      faq=[('What is experiential marketing?', 'Experiential marketing lets people take part in a brand experience, such as a launch, an installation, a game or an event, so they remember the brand through what they did.'),
           ('What experiential work has Growthryders done?', 'At Tu Race Laga for TVS Apache, Growthryders built Apache-themed photo and video experiences and brand engagement zones around a corporate run at Bagmane Tech Park.'),
           ('Does Growthryders handle the whole experience?', 'Yes. Concept, planning, production and on-ground execution are handled by the same team.')]),
 dict(slug='corporate-events', sid='events', title='Corporate event management in Bengaluru (Bangalore) | Growthryders',
      desc='Corporate events in Bengaluru by Growthryders: conferences and annual meets, dealer meets, leadership summits, awards, employee engagement programmes and product launches.',
      h1='Corporate event management in Bengaluru.', lede='Business and corporate engagement platforms, conceptualised and run end to end.',
      h2='Events we run', intro='We take a corporate event from the idea to the last guest leaving: the concept, the venue, the production, the brand integration and the people on the ground.',
      items=['Conferences and annual meets', 'Dealer meets', 'Leadership summits', 'Awards', 'Employee engagement programmes', 'Product launches'],
      h2b='', itemsb=[], work=['trl'], films=['tu-race-laga-event-film'],
      faq=[('What corporate events does Growthryders manage?', 'Conferences, annual meets, dealer meets, leadership summits, awards, employee engagement programmes and product launches.'),
           ('Has Growthryders run a large corporate event?', 'Yes. Tu Race Laga at Bagmane Tech Park, Bengaluru, on 31 October 2026 was a corporate run with 3K, 5K and 10K categories and about 1,600 participants and guests.'),
           ('Does Growthryders run employee engagement programmes?', 'Yes. Employee engagement programmes are part of the corporate events and engagement service, including fitness-led formats through the Runcle platform.')]),
 dict(slug='media-solutions', sid='media', title='Outdoor, transit and tech park media in Bengaluru | Growthryders',
      desc='Media planning and buying in Bengaluru by Growthryders: outdoor and digital outdoor, transit and airport media, print and radio, corporate park media and mall and retail media.',
      h1='Media planning and buying in Bengaluru.', lede='Media planning and execution across the formats that surround an activation, so the same people see the brand before and after they meet it.',
      h2='Media we plan and execute', intro='We plan media around the activation and the audience it is meant for, and execute it across the formats below.',
      items=['Outdoor and digital outdoor media', 'Transit and airport media', 'Print and radio', 'Corporate park media', 'Mall and retail media', 'Retail and point-of-sale branding', 'Innovative and ambient media platforms'],
      h2b='', itemsb=[], work=['tvs'], films=[],
      faq=[('Which media does Growthryders plan and buy?', 'Outdoor and digital outdoor, transit and airport media, print and radio, corporate park media, mall and retail media, and innovative and ambient media.'),
           ('Can media be combined with an activation?', 'Yes. Growthryders builds the media plan around the activation so the brand reaches the same people across physical and digital touchpoints.'),
           ('Does Growthryders offer media inside corporate parks?', 'Yes. Corporate park media is one of the formats Growthryders plans and executes.')]),
 dict(slug='digital-marketing', sid='digital', title='Digital marketing services in Bengaluru (Bangalore) | Growthryders',
      desc='Digital marketing in Bengaluru by Growthryders: SEO and GEO, performance marketing, social media management, content, website design and development and lead generation.',
      h1='Digital marketing services in Bengaluru.', lede='Search, social, content, websites and performance campaigns that keep the conversation going after the activation.',
      h2='What we do online', intro='We help brands strengthen their digital presence and reach the right audience, on their own or alongside an on-ground campaign.',
      items=['Search engine optimisation (SEO)', 'Generative engine optimisation (GEO)', 'Performance marketing', 'Social media management', 'Content strategy and creation', 'Website design and development', 'Lead generation', 'Digital campaign management', 'Marketing analytics and automation'],
      h2b='', itemsb=[], work=[], films=[],
      faq=[('Which digital marketing services does Growthryders offer?', 'SEO, generative engine optimisation (GEO), performance marketing, social media management, content strategy and creation, website design and development, lead generation, digital campaign management and marketing analytics and automation.'),
           ('What is generative engine optimisation (GEO)?', 'GEO is preparing a brand\'s content so that AI assistants and answer engines can find it, understand it and quote it when people ask questions.'),
           ('Can digital marketing run together with an activation?', 'Yes. Growthryders plans digital and social media campaigns around the activation so the message stays consistent on the ground and online.')]),
 dict(slug='technology-experiences', sid='technology', title='AR, VR and technology-led brand experiences in Bengaluru | Growthryders',
      desc='Technology-led brand experiences by Growthryders, Bengaluru: installations, augmented and virtual reality, gamification and interactive digital formats built into the activation.',
      h1='Technology-led brand experiences.', lede='Installations, AR and VR, gamification and interactive digital formats built into the activation.',
      h2='Formats we build', intro='Technology gives people something to do with a brand, not just something to look at. We build it into the activation so it works on the ground.',
      items=['Technology-led installations', 'Augmented and virtual reality', 'Interactive digital experiences', 'Gamification', 'QR-based campaign engagement', 'Digital registration touchpoints'],
      h2b='', itemsb=[], work=['tvs', 'trl'], films=[],
      faq=[('What are technology-led brand experiences?', 'They are activations that use technology such as installations, augmented and virtual reality, games and interactive screens so that people take part in the brand experience.'),
           ('Has Growthryders used technology in its campaigns?', 'Yes. The TVS Apache campaigns at Bagmane business parks used QR-based campaign engagement and digital registration touchpoints.'),
           ('Does Growthryders offer AR and VR experiences?', 'Yes. Augmented and virtual reality experiences are part of the technology-led experiences service.')]),
 dict(slug='film-production', sid='films', title='Event film and brand video production in Bengaluru | Growthryders',
      desc='Event films, brand and partner films and vertical reels, shot and edited by Growthryders at its activations and events in Bengaluru.',
      h1='Event film and brand video production in Bengaluru.', lede='We shoot and edit the films of the activations and events we run, so the campaign keeps working after the day is over.',
      h2='What we produce', intro='The crew is on the ground with the activation team, so the film shows the brand, the people and the moments that mattered.',
      items=['Event films', 'Brand and partner films', 'Reels and vertical cuts for social media', 'On-ground shooting', 'Editing'],
      h2b='', itemsb=[], work=[], films=['tu-race-laga-event-film', 'tvs-apache-tu-race-laga', 'axis-bank-tu-race-laga'],
      faq=[('Does Growthryders make event films?', 'Yes. Growthryders shoots and edits event films, brand and partner films and vertical cuts for social media at the activations and events it runs.'),
           ('Which films has Growthryders made?', 'The Tu Race Laga event film at Bagmane Tech Park, brand films for TVS Apache, Axis Bank and Milky Mist, and Royal Enfield films at the Bagmane parks.'),
           ('Where can I watch the films?', 'On the Films page of growthryders.in, filed by brand.')]),
]
SVC_BY_SID = {}
for _p in SVC_PAGES: SVC_BY_SID.setdefault(_p['sid'], _p)
def service_page(sp):
    path = f"services/{sp['slug']}.html"
    qa = ''.join(f'<details class="qa"><summary><h3>{html.escape(q)}</h3><span class="qa-x" aria-hidden="true"></span></summary><p>{html.escape(a)}</p></details>' for q, a in sp['faq'])
    fk = [k for k in sp['films'] if FILMS_LIVE]
    mix = len({_FB[k][4] for k in fk}) > 1 if fk else False
    films_sec = (f'<section class="sec dark on-dark films-page"><div class="wrap"><div class="sec-head"><h2>Watch the films</h2></div><div class="fold"><div class="grid-mix">{"".join(film(_FB[k]) for k in fk)}</div></div><p style="margin-top:22px"><a class="more" href="{{r}}films.html">All films, filed by brand</a></p></div></section>' + PLAYER) if fk else ''
    work_sec = f'<section class="sec on-light"><div class="wrap"><div class="sec-head"><h2>Work that shows it</h2></div>{work_cards(sp["work"])}</div></section>' if sp['work'] else ''
    others = ''.join(f'<a href="{{r}}services/{o["slug"]}.html">{o["h1"].rstrip(".")}</a>' for o in SVC_PAGES if o is not sp)
    body = f'''
<section class="page-head on-dark"><div class="wrap">
  <p class="kicker"><a href="{{r}}services.html" style="text-decoration:none">Our services</a></p>
  <h1>{sp["h1"]}</h1>
  <p class="lede">{sp["lede"]}</p>
  <div class="btn-row"><a class="btn" href="{{r}}contact.html">Start a conversation</a><a class="btn ghost wi" href="https://wa.me/{PHONE_E164}">{IC_CHAT}WhatsApp us</a><a class="btn ghost wi" href="tel:+{PHONE_E164}">{IC_CALL}Call us</a></div>
</div></section>
<section class="sec white on-light"><div class="wrap split top">
  <div><h2>{sp["h2"]}</h2><p class="lede" style="margin-top:20px">{sp["intro"]}</p></div>
  <div>{ul(sp["items"])}{(f'<h3 style="margin-top:32px">{sp["h2b"]}</h3>' + ul(sp["itemsb"])) if sp["itemsb"] else ""}</div>
</div></section>
{work_sec}
{films_sec}
<section class="sec white on-light faq-sec"><div class="wrap faq"><div class="sec-head"><h2>Questions people ask</h2></div><div class="qa-list">{qa}</div></div></section>
<section class="sec on-light svc-more"><div class="wrap"><h2 class="films-h" style="margin-top:0">More from Growthryders</h2><nav class="svc-links" aria-label="Other services">{others}</nav></div></section>
{CTA}'''
    canon = DOMAIN + '/' + path
    EXTRA_LD[path] = [{"@type": "Service", "@id": canon + "#service", "name": sp['h1'].rstrip('.'), "serviceType": sp['h1'].rstrip('.'), "description": sp['desc'], "url": canon, "provider": {"@id": DOMAIN + "/#org"},
                       "areaServed": [{"@type": "City", "name": "Bengaluru"}, {"@type": "Country", "name": "India"}],
                       "hasOfferCatalog": {"@type": "OfferCatalog", "name": sp['h2'], "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": i}} for i in sp['items'] + sp['itemsb']]}},
                      {"@type": "FAQPage", "@id": canon + "#faq", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in sp['faq']]}]
    page(path, sp['title'], sp['desc'], body, 'dark', 1)
for _sp in SVC_PAGES: service_page(_sp)

# ---------------------------------------------------------------- SPONSORSHIP SALES (its own vertical; the client's text, unchanged)

# ---- Sponsorship methodology case study (client text) ----
SC_STAGES = [
 ('Client Requirement', 'Bagmane REIT identified the requirement for a corporate running event.'),
 ('Event Conceptualisation', 'Growthryders developed the event concept around the theme of challenging yourself, with 10K, 5K and 3K running categories.'),
 ('Property Development', 'The event was structured as a corporate running property with opportunities for brand association and sponsorship.'),
 ('Brand Outreach', 'Growthryders approached potential sponsors and explored relevant brand partnerships.'),
 ('Strategic Campaign Identification', "TVS Apache's Tu Race Laga campaign was identified as an appropriate fit for the running event."),
 ('Title Brand Integration', 'The proposed association was accepted, and the event was positioned as TVS Apache Presents &ndash; Tu Race Laga.'),
 ('Multi-Brand Sponsorship Development', 'Additional partners were associated with the event across banking, ticketing, nutrition and protein categories.'),
 ('Event Coordination &amp; Execution', 'Growthryders coordinated the event ecosystem, working with Bagmane REIT and the participating sponsors.'),
]
SC_PARTNERS = [('TVS Apache', 'Presenting / Title Brand'), ('Bagmane REIT', 'Event Association / Venue Ecosystem'), ('Axis Bank', 'Banking Partner'), ('Races', 'Ticketing Partner'), ('Milky Mist', 'Nutrition Partner'), ('Protein Chef', 'Protein Partner')]
SC_URL = 'work/tu-race-laga-sponsorship-case-study.html'
def sc_table(head, rows, cls=''):
    return f'<div class="cs-table-wrap"><table class="cs-table {cls}"><thead><tr><th scope="col">{head[0]}</th><th scope="col">{head[1]}</th></tr></thead><tbody>' + ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in rows) + '</tbody></table></div>'
def ul(items): return '<ul class="cs-list">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


SP_CAPS = [
 ('IP &amp; Sponsorship Monetisation Strategy', ['Understanding the IP, event or conference proposition.', 'Developing sponsorship inventory and partnership opportunities.', 'Structuring sponsorship categories and commercial packages.', 'Identifying monetisation opportunities.', 'Developing industry-specific sponsorship propositions.']),
 ('AI-Enabled Sponsor Identification &amp; Prospecting', ['Identifying relevant brands across industry verticals.', 'Building targeted sponsor databases.', 'Mapping marketing heads, brand managers, corporate decision-makers and business leaders.', 'AI-assisted lead research and qualification.', 'Identifying potential category sponsors and strategic partners.', 'Continuous database enrichment.']),
 ('Human-in-the-Loop Sales Engagement', ['Personalised outreach and communication.', 'Email and telephone engagement.', 'Decision-maker relationship development.', 'Follow-ups and meeting coordination.', 'Understanding sponsor requirements and marketing objectives.', 'Customised sponsorship presentations and proposals.']),
 ('Negotiation &amp; Commercial Closure', ['Sponsorship proposal presentation.', 'Commercial negotiations.', 'Partnership structuring.', 'Deal progression and closure.', 'Documentation and coordination.', 'Client and sponsor relationship management.']),
 ('Continuous Sales Pipeline Management', ['Centralised prospect management.', 'Lead qualification and prioritisation.', 'Sales pipeline tracking.', 'Follow-up scheduling.', 'Opportunity stage management.', 'Conversion and revenue reporting.', 'Continuous pipeline replenishment.']),
]
SP_INDUSTRIES = ['Sports and Fitness IPs', 'Lifestyle and Entertainment Events', 'B2B Conferences and Conclaves', 'Industry Summits and Trade Shows', 'Corporate Events and Business Platforms', 'Education and Institutional Events', 'Exhibitions and Trade Fairs', 'Consumer and Community IPs', 'Festivals and Destination Events']
sponsorship = f'''
<section class="page-head on-dark"><div class="wrap">
  <h1 class="caps-h">SPONSORSHIP SALES &amp; REVENUE MANAGEMENT</h1>
  <p class="lede">Turning Intellectual Properties Into Revenue Opportunities.</p>
  <p class="sp-tag"><strong>A Sponsorship Sales KPO powered by AI intelligence and human expertise.</strong></p>
  <div class="btn-row"><a class="btn" href="{{r}}contact.html">Start a conversation</a><a class="btn ghost wi" href="https://wa.me/{PHONE_E164}">{IC_CHAT}WhatsApp us</a><a class="btn ghost wi" href="tel:+{PHONE_E164}">{IC_CALL}Call us</a></div>
</div></section>
<section class="sec white on-light"><div class="wrap sp-intro">
  <p class="lede">At Growthryders, we recognise that a great Intellectual Property, conference or event is only as valuable as its ability to attract the right brand partnerships and generate sustainable revenue.</p>
  <div>
    <p>We offer specialised Sponsorship Sales and Revenue Management services to IP owners, event organisers, B2B conclave organisers, conference companies and businesses seeking to monetise their properties.</p>
    <p>Our approach combines Artificial Intelligence (AI) with a Human-in-the-Loop sales mechanism to build a continuous, structured and opportunity-driven sponsorship sales pipeline.</p>
    <p>From identifying potential sponsors and mapping decision-makers to prospecting, engagement, proposal development, negotiations and closure, we manage the entire sponsorship sales lifecycle.</p>
    <p>We function as an extended sponsorship sales and business development team for our clients, bringing together technology, market intelligence, sales expertise and relationship management.</p>
  </div>
</div></section>
<section class="sec on-light"><div class="wrap">
  <div class="sec-head"><h2 class="caps-h">OUR SPONSORSHIP SALES CAPABILITIES</h2></div>
  <ol class="sp-caps">{"".join(f'<li><h3>{t}</h3><ul>{"".join(f"<li>{i}</li>" for i in items)}</ul></li>' for t, items in SP_CAPS)}</ol>
</div></section>
<section class="sec dark on-dark"><div class="wrap">
  <div class="sec-head"><h2 class="caps-h">OUR SALES MECHANISM</h2><p class="lede">AI Intelligence + Human Expertise = Continuous Sales Pipeline</p></div>
  <p class="sp-wide">Our operating mechanism combines AI-powered research and prospecting with human-led engagement, relationship building and commercial closure.</p>
  <ol class="flow on-dark-flow" aria-label="Sales mechanism"><li>Discover</li><li>Identify</li><li>Qualify</li><li>Engage</li><li>Propose</li><li>Negotiate</li><li>Close</li></ol>
  <div class="sp-two"><p>Technology improves the speed and scale of prospecting, while human expertise drives conversations, trust, negotiation and business relationships.</p><p>The result is a structured sales engine designed to generate opportunities continuously rather than depending on sporadic sponsor enquiries.</p></div>
</div></section>
<section class="sec white on-light"><div class="wrap">
  <div class="sec-head"><h2 class="caps-h">OUR METHODOLOGY IN PRACTICE</h2><p class="lede">Case study: TVS Apache Presents &ndash; Tu Race Laga, a Bagmane Tech Parks corporate running initiative.</p></div>
  <div class="sp-case">
    <div>
      <p>What began as a corporate running event requirement evolved into a multi-brand sponsorship property through strategic brand integration and sponsorship development by Growthryders.</p>
      <ol class="sp-stages">{"".join(f'<li>{t}</li>' for t, d in SC_STAGES)}</ol>
    </div>
    <div>
      <h3 class="cs-h3" style="margin-top:0">Sponsorship Partner Structure</h3>
      {sc_table(('Partner', 'Sponsorship Category'), SC_PARTNERS)}
      <p style="margin-top:22px"><a class="btn" href="{{r}}work/tu-race-laga-sponsorship-case-study.html">Read the full case study</a></p>
    </div>
  </div>
</div></section>
<section class="sec on-light"><div class="wrap">
  <div class="sec-head"><h2 class="caps-h">INDUSTRIES &amp; PROPERTIES WE SERVE</h2></div>
  <ul class="chips sp-chips">{"".join(f"<li>{i}</li>" for i in SP_INDUSTRIES)}</ul>
</div></section>
<section class="sec on-light"><div class="wrap split top">
  <div><h2 class="caps-h">WHY GROWTHRYDERS?</h2></div>
  <div>
    <p class="lede">We bring together sponsorship strategy, AI-enabled prospecting, industry intelligence, sales execution and relationship management under one integrated KPO model.</p>
    <p>We can operate as an outsourced sponsorship sales partner, an extended business development team or a dedicated revenue management function.</p>
    <p class="sp-commit"><strong>Our commitment is simple: Build the pipeline. Develop the relationships. Drive the closures. Accelerate sponsorship revenue.</strong></p>
  </div>
</div></section>
{CTA}'''
EXTRA_LD['sponsorship-sales.html'] = [{"@type": "Service", "@id": DOMAIN + "/sponsorship-sales.html#service", "name": "Sponsorship Sales & Revenue Management", "serviceType": "Sponsorship sales", "description": "Sponsorship Sales and Revenue Management services for IP owners, event organisers, B2B conclave organisers and conference companies, combining AI-enabled prospecting with human-led sales.", "url": DOMAIN + "/sponsorship-sales.html", "provider": {"@id": DOMAIN + "/#org"}, "areaServed": {"@type": "Country", "name": "India"},
    "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Sponsorship sales capabilities", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": html.unescape(t)}} for t, i in SP_CAPS]}}]
page('sponsorship-sales.html', 'Sponsorship Sales & Revenue Management | Growthryders',
     'Sponsorship sales and revenue management for IP owners, event organisers and B2B conferences: AI-enabled sponsor prospecting with human-led engagement, negotiation and closure.', sponsorship, 'dark')

spcase = f'''
<section class="page-head on-dark"><div class="wrap">
  <p class="kicker"><a href="{{r}}sponsorship-sales.html" style="text-decoration:none">Sponsorship Development &amp; Event Execution Case Study</a></p>
  <h1 class="caps-h">TVS APACHE PRESENTS &ndash; TU RACE LAGA</h1>
  <p class="lede">A Bagmane Tech Parks Corporate Running Initiative</p>
  <p class="sp-tag"><strong>Conceptualisation, Sponsorship Development &amp; Event Execution by Growthryders</strong></p>
</div></section>
<section class="sec white on-light"><div class="wrap split top">
  <div><h2>1. Project Overview</h2></div>
  <div>
    <p class="lede">The Tu Race Laga initiative was conceptualised as a corporate running event for employees and the wider community across Bagmane Tech Parks.</p>
    <p>The objective was to create an engaging fitness-oriented event that encouraged participation, promoted a healthy lifestyle and provided brands with an opportunity to connect with a corporate audience.</p>
    <p>The event featured three running categories:</p>
    {ul(['10K Run', '5K Run', '3K Run'])}
    <p>The central theme of the event was &ldquo;Challenging Yourself.&rdquo;</p>
    <p class="cs-pull">What began as a corporate running event requirement evolved into a multi-brand sponsorship property through strategic brand integration and sponsorship development by Growthryders.</p>
  </div>
</div></section>
<section class="sec on-light"><div class="wrap split top">
  <div><h2>2. Project Initiation &ndash; Bagmane REIT</h2></div>
  <div>
    <p>The initiative originated from Bagmane REIT&rsquo;s requirement to organise a corporate running event across its technology parks.</p>
    <p>The requirement was to create an event that would:</p>
    {ul(['Encourage fitness and physical well-being among employees.', 'Bring together the corporate community through a common activity.', 'Create an engaging and professionally organised running experience.', 'Provide opportunities for brands to associate with the event.'])}
    <p>Growthryders took forward the event conceptualisation, sponsorship development and organisational responsibilities.</p>
  </div>
</div></section>
<section class="sec white on-light"><div class="wrap split top">
  <div><h2>3. Event Conceptualisation &amp; Property Development</h2></div>
  <div>
    <p>Growthryders developed the event around the concept of challenging oneself through running.</p>
    <p>The event was structured into three categories to encourage participation from individuals with different fitness levels.</p>
    <h3 class="cs-h3">Event Categories</h3>
    {sc_table(('Category', 'Purpose'), [('10K Run', 'For experienced and competitive runners'), ('5K Run', 'For regular fitness enthusiasts'), ('3K Run', 'For beginners and recreational participants')])}
    <p>The objective was to position the event as more than just a running activity. It was developed as a corporate community engagement property with potential for brand partnerships and sponsorship opportunities.</p>
  </div>
</div></section>
<section class="sec on-light"><div class="wrap split top">
  <div><h2>4. Sponsorship Strategy &amp; Brand Outreach</h2></div>
  <div>
    <p>Once the event concept and property were established, Growthryders initiated the sponsorship outreach process.</p>
    <p>The strategy was to identify brands that aligned with the event&rsquo;s fitness, lifestyle, performance and corporate audience.</p>
    <p>Rather than approaching brands with generic sponsorship opportunities, the focus was on identifying relevant brand campaigns and integrating them into the event identity.</p>
    <p>This approach created an opportunity to develop a sponsorship structure where different brands could participate through clearly defined partnership categories.</p>
  </div>
</div></section>
<section class="sec dark on-dark"><div class="wrap split top">
  <div><h2>5. Strategic Brand Integration &ndash; TVS Apache</h2></div>
  <div>
    <p>One of the key developments in the sponsorship journey was the integration of TVS Apache&rsquo;s latest campaign, &ldquo;TU RACE LAGA.&rdquo;</p>
    <p>Growthryders identified an opportunity to connect TVS Apache&rsquo;s campaign positioning with the running event.</p>
    <p>The campaign&rsquo;s racing and performance-oriented identity aligned naturally with the event&rsquo;s running concept and its central theme of challenging oneself.</p>
    <p>The proposed integration was accepted by TVS Apache, enabling the event to be presented as:</p>
    <p class="cs-title">TVS APACHE PRESENTS &ndash; TU RACE LAGA</p>
    <p>This integration brought a strong brand identity to the event and created a distinctive association between the automotive brand&rsquo;s campaign and the corporate running property.</p>
    <p>The initiative demonstrated how an existing brand campaign could be strategically integrated into an independently developed event property.</p>
  </div>
</div></section>
<section class="sec white on-light"><div class="wrap split top">
  <div><h2>6. Sponsorship Architecture &amp; Brand Partnerships</h2></div>
  <div>
    <p>Following the title integration, the event was developed into a multi-brand sponsorship ecosystem.</p>
    <p>The participating brands were associated with different sponsorship categories based on their respective roles.</p>
    <h3 class="cs-h3">Sponsorship Partner Structure</h3>
    {sc_table(('Partner', 'Sponsorship Category'), SC_PARTNERS)}
    <p>The sponsorship structure provided multiple brands with opportunities to associate with the event while maintaining a unified event identity.</p>
    <p>Each partner contributed to a different aspect of the overall event ecosystem.</p>
  </div>
</div></section>
<section class="sec on-light"><div class="wrap">
  <div class="sec-head"><h2>7. Sponsorship Flow &ndash; From Requirement to Execution</h2><p class="lede">The overall sponsorship development process followed this sequence:</p></div>
  <ol class="steps cs-stages">{"".join(f'<li><span><strong>Stage {i} &ndash; {t}</strong>{d}</span></li>' for i, (t, d) in enumerate(SC_STAGES, 1))}</ol>
</div></section>
<section class="sec white on-light"><div class="wrap">
  <div class="sec-head"><h2>8. Roles &amp; Responsibilities</h2></div>
  <div class="cs-roles">
    <div><h3>Bagmane REIT</h3>{ul(['Initiated the requirement for the corporate running event.', 'Provided the corporate park ecosystem for the initiative.', "Supported the event&rsquo;s association with the Bagmane community."])}</div>
    <div class="cs-gr"><h3>Growthryders</h3>{ul(['Conceptualised the event property.', 'Developed the event format and positioning.', 'Identified sponsorship opportunities.', 'Approached potential brand partners.', 'Proposed the TVS Apache campaign integration.', 'Developed the multi-brand sponsorship structure.', 'Coordinated event planning and execution with the associated stakeholders.'])}</div>
    <div><h3>TVS Apache</h3>{ul(['Associated with the event through the Tu Race Laga campaign.', 'Became the presenting brand for the running initiative.'])}</div>
    <div><h3>Other Sponsorship Partners</h3>{ul(['Axis Bank &ndash; Banking Partner.', 'Races &ndash; Ticketing Partner.', 'Milky Mist &ndash; Nutrition Partner.', 'Protein Chef &ndash; Protein Partner.'])}</div>
  </div>
</div></section>
<section class="sec dark on-dark"><div class="wrap">
  <div class="sec-head"><h2>9. Growthryders&rsquo; Strategic Contribution</h2><p class="lede">The key contribution of Growthryders was the transformation of a corporate event requirement into a structured sponsorship-led event property.</p></div>
  <p class="sp-wide">The approach involved three important dimensions:</p>
  <div class="cs-dims">
    <div><h3>A. Event Property Development</h3><p>Instead of treating the initiative as only an event-management requirement, Growthryders developed a property that could attract relevant brands and sponsorship opportunities.</p></div>
    <div><h3>B. Campaign-Led Brand Integration</h3><p>The integration of TVS Apache&rsquo;s Tu Race Laga campaign demonstrated the value of connecting an existing brand campaign with a relevant event concept.</p></div>
    <div><h3>C. Multi-Brand Sponsorship Ecosystem</h3><p>The addition of partners across different categories helped establish a broader sponsorship structure around the event.</p></div>
  </div>
</div></section>
<section class="sec white on-light"><div class="wrap split top">
  <div><h2>10. Key Takeaways</h2></div>
  <div>
    <p>The Tu Race Laga initiative demonstrates the importance of strategic event conceptualisation and sponsorship development.</p>
    <p>Key learnings from the initiative include:</p>
    <ol class="steps">{"".join(f'<li><span>{t}</span></li>' for t in ['An event can be transformed into a sponsorship property through the right positioning and conceptualisation.', 'Existing brand campaigns can create meaningful integration opportunities with relevant events.', 'Sponsorship outreach becomes more effective when brands are approached with a clear association opportunity.', 'Multiple brands can participate in one event through distinct sponsorship categories.', 'Strong coordination between the event organiser, client and sponsors is essential for successful execution.'])}</ol>
  </div>
</div></section>
<section class="sec on-light"><div class="wrap split top">
  <div><h2>11. Conclusion</h2></div>
  <div>
    <p class="lede">The TVS Apache Presents &ndash; Tu Race Laga initiative represents a strategic approach to developing a corporate running event into a multi-brand sponsorship property.</p>
    <p>Beginning with Bagmane REIT&rsquo;s requirement for a corporate running initiative, Growthryders developed the event concept, identified relevant sponsorship opportunities and proposed the integration of TVS Apache&rsquo;s Tu Race Laga campaign.</p>
    <p>The successful brand association, along with the participation of Axis Bank, Races, Milky Mist and Protein Chef, helped establish a structured sponsorship ecosystem.</p>
    <p>The initiative reflects Growthryders&rsquo; approach of combining event conceptualisation, brand alignment, sponsorship development and event execution to create meaningful brand and community engagement opportunities.</p>
    <p class="cs-sign"><strong>GROWTHRYDERS</strong><br>From Event Conceptualisation to Strategic Brand Partnerships &amp; Execution.</p>
    <p style="margin-top:26px"><a class="more" href="{{r}}work/tu-race-laga.html">See the event photos and films</a></p>
  </div>
</div></section>
{CTA}'''
EXTRA_LD[SC_URL] = [{"@type": "Article", "@id": DOMAIN + "/" + SC_URL + "#article", "headline": "TVS Apache Presents Tu Race Laga: Sponsorship Development & Event Execution Case Study", "about": "Sponsorship development for a corporate running event at Bagmane Tech Parks, Bengaluru", "author": {"@id": DOMAIN + "/#org"}, "publisher": {"@id": DOMAIN + "/#org"}, "url": DOMAIN + "/" + SC_URL, "inLanguage": "en-IN"}]
page(SC_URL, 'Tu Race Laga sponsorship case study | Sponsorship development | Growthryders',
     'How Growthryders turned a Bagmane REIT corporate run into TVS Apache Presents Tu Race Laga, a multi-brand sponsorship property with Axis Bank, Races, Milky Mist and Protein Chef.', spcase, 'dark', 1)

ips = f'''
<section class="page-head on-dark"><div class="wrap">
  <h1>Building communities. Creating long-term brand platforms.</h1>
  <p class="lede">We develop platforms of our own that bring audiences, communities and brands together again and again.</p>
</div></section>
<section class="sec white on-light"><div class="wrap split top" id="runcle" style="scroll-margin-top:24px">
  <div><h2>Runcle</h2><p class="lede" style="margin-top:18px">Running meets cycling.</p>
    <p>A fitness and wellness platform that brings runners, cyclists and fitness enthusiasts together, and gives brands a way to reach an active-lifestyle audience.</p>
    {ul(['Running and cycling events', 'Corporate wellness programmes', 'Fitness challenges', 'Health awareness initiatives', 'Community engagement', 'Brand partnerships'])}</div>
  {img('runcle-duo', 'A Runcle team on the course: one partner cycling, the other running')}
</div>
<div class="wrap ip-strip">{img('runcle-start', 'Cyclists and runners leaving the Runcle ’24 start arch')}{img('runcle-stage', 'Warm-up session on the Runcle ’24 stage')}{img('runcle-amazon', 'Amazon.in brand boards along the Runcle ’24 venue')}</div>
<p class="wrap ip-note">Runcle '24 was a team duathlon for World Health Day on 6 April 2024: one partner runs while the other cycles, and they finish together.</p>
</section>
<section class="sec on-light"><div class="wrap split top" id="bikers-bay" style="scroll-margin-top:24px">
  {img('bb-tents', 'Bikers Bay brand tents at Bagmane Constellation Business Park')}
  <div><h2>Bikers Bay</h2><p class="lede" style="margin-top:18px">The motorcycle community.</p>
    <p>A community platform that connects motorcycle enthusiasts through rides, experiences, networking and brand associations.</p>
    {ul(['Rider meets and networking', 'Motorcycle experiences', 'Weekend rides and adventures', 'Brand collaborations', 'Lifestyle engagement', 'Digital community initiatives'])}</div>
</div>
<div class="wrap ip-strip">{img('bb-crowd', 'Visitors walking through the Bikers Bay brand tents')}{img('bb-re', 'Visitors trying a Royal Enfield Guerrilla at Bikers Bay')}{img('bb-ktm', 'A rider trying a KTM motorcycle at Bikers Bay')}</div>
<p class="wrap ip-note">Bikers Bay brought motorcycle brands and riders together at Bagmane Constellation Business Park on 22 and 23 January 2025.</p>
</section>
{CTA}
'''
page('ips.html', 'Our IPs | Runcle and Bikers Bay | Growthryders',
     'Runcle, where running meets cycling, and Bikers Bay, the motorcycle community: Growthryders platforms that connect brands with engaged communities.', ips, 'dark')

# ---------------------------------------------------------------- CONTACT
contact = f'''
<section class="page-head on-dark"><div class="wrap">
  <h1>Let's build growth together.</h1>
  <p class="lede">Planning a product launch, a consumer activation, a corporate engagement programme or an integrated campaign? Tell us what you have in mind.</p>
</div></section>
<section class="sec white on-light"><div class="wrap split top">
  <form class="form" id="enquiry" data-wa="{PHONE_E164}" data-mail="{EMAIL}" data-sheet="https://docs.google.com/forms/d/e/1FAIpQLSctMNhN-DjsVpEqyde7s4aB9yuoeaeNzmaksEA9UIUXBEtMMQ/formResponse" novalidate>
    <h2>Send an enquiry</h2>
    <label>Your name<input name="name" autocomplete="name" required></label>
    <label>Company<input name="company" autocomplete="organization"></label>
    <label>Phone or email<input name="contact" autocomplete="tel" inputmode="email" required></label>
    <label>What are you looking for?
      <select name="need"><option>Brand activation</option><option>Integrated TTL campaign</option><option>Digital marketing</option><option>Experiential marketing</option><option>Media solutions</option><option>Corporate event</option><option>Partnering on Runcle or Bikers Bay</option><option>Something else</option></select></label>
    <label>Tell us about it<textarea name="note" required></textarea></label>
    <p class="err" role="alert"></p>
    <div class="btn-row" style="margin-top:0"><button class="btn wi" type="button" data-send="whatsapp">{IC_CHAT}Send on WhatsApp</button><button class="btn ghost" type="button" data-send="email">Send by email</button></div>
    <p class="note">Your message opens in WhatsApp or your email app, ready to send. Your enquiry is also sent to the Growthryders team so they can follow up.</p>
  </form>
  <div>
    <h2>Reach us directly</h2>
    <ul class="contact-list" style="margin-top:24px">
      <li>Phone<br><a class="wi" href="tel:+{PHONE_E164}">{IC_CALL}{PHONE_DISPLAY}</a></li>
      <li>WhatsApp<br><a class="wi" href="https://wa.me/{PHONE_E164}">{IC_CHAT}Message {PHONE_DISPLAY}</a></li>
      <li>Email<br><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li>Location<br><strong>Bengaluru, India</strong></li>
    </ul>
  </div>
</div></section>
'''
page('contact.html', 'Contact Growthryders (Growth Ryders) | Brand activation agency, Bengaluru',
     'Talk to Growthryders about a brand activation, an integrated campaign or a corporate event. Phone, WhatsApp and email.', contact, 'dark')

page('404.html', 'Page not found | Growthryders', 'This page does not exist.',
     '<section class="page-head on-dark"><div class="wrap"><h1>This page is not here.</h1><p class="lede">The link may be old or mistyped.</p><div class="btn-row"><a class="btn" href="/">Go to the home page</a><a class="btn ghost" href="/work.html">See our work</a></div></div></section>', 'dark')

# ---------------------------------------------------------------- static files
pages = ['', 'about.html', 'services.html'] + [f'services/{x["slug"]}.html' for x in SVC_PAGES] + ['sponsorship-sales.html', 'work.html'] + (['films.html'] if FILMS_LIVE else []) + [ 'work/tu-race-laga.html', 'work/tu-race-laga-sponsorship-case-study.html', 'work/tvs-apache-bagmane.html', 'work/royal-enfield-bikers-bay.html', 'ips.html', 'contact.html']
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{DOMAIN}/{p}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod></url>\n' for p in pages) + '</urlset>\n')
INDEXNOW = '78d348323012cbff111fa228a2ef64b3'
open(os.path.join(OUT, INDEXNOW + '.txt'), 'w').write(INDEXNOW)
open(os.path.join(OUT, 'google3cea24fe400a22ae.html'), 'w').write('google-site-verification: google3cea24fe400a22ae.html')   # Search Console ownership file: keep
os.makedirs(os.path.join(OUT, 'admin'), exist_ok=True)
SHEET_URL = 'https://docs.google.com/spreadsheets/d/1eUrwam9PI1eJyy_vO7axUy5-FXNHhSiZd6oVzFnqqLA/edit#gid=1799777081'
open(os.path.join(OUT, 'admin', 'index.html'), 'w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Growthryders admin</title><meta http-equiv="refresh" content="0; url={SHEET_URL}"><style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#170e22;color:#fff;font:600 16px/1.5 system-ui,sans-serif;text-align:center;padding:24px}}a{{color:#f5b321}}</style></head><body><p>Opening the Growthryders enquiries sheet. Sign in with your Google account.<br><a href="{SHEET_URL}">Continue</a></p><script>location.replace("{SHEET_URL}")</script></body></html>''')
BOTS = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'PerplexityBot', 'Google-Extended', 'Applebot-Extended', 'Bingbot']
open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nDisallow: /admin/\n\n' + ''.join(f'User-agent: {b}\nAllow: /\n\n' for b in BOTS) + f'Sitemap: {DOMAIN}/sitemap.xml\n')
open(os.path.join(OUT, 'llms.txt'), 'w').write(f'''# Growthryders

> Growthryders (also written Growth Ryders, or GRY) is a brand activation and through-the-line marketing company based in Bengaluru, Karnataka, India. One team plans and runs activations, experiential marketing, media, corporate events, digital marketing and technology-led experiences.

## Services
''' + ''.join(f'- [{t}]({DOMAIN}/{svc_href(k)}): {d} Includes: {", ".join(cs)}.\n' for k, t, d, cs in SERVICES) + f'- [Tech park and corporate park activations]({DOMAIN}/services/tech-park-activations.html): brand activations inside business parks in Bengaluru, such as the Bagmane parks.\n' + f'''
## Pages
- [Home]({DOMAIN}/): overview, services, work, films and platforms
- [About]({DOMAIN}/about.html): the company
- [Services]({DOMAIN}/services.html): every service in detail
- [Work]({DOMAIN}/work.html): campaign case studies
- [Films]({DOMAIN}/films.html): campaign and event films
- [Our IPs]({DOMAIN}/ips.html): Runcle and Bikers Bay, platforms Growthryders owns
- [Contact]({DOMAIN}/contact.html): start a conversation

## Brands on the ground with Growthryders
{", ".join(MARQUEE)}

## Questions and answers
''' + ''.join(f'- {q} {a}\n' for q, a in FAQS) + f'''
## Contact
- Phone and WhatsApp: {PHONE_DISPLAY}
- Email: {EMAIL}
- Location: Bengaluru, Karnataka, India
''')
open(os.path.join(OUT, 'CNAME'), 'w').write('growthryders.in\n')
open(os.path.join(OUT, '.nojekyll'), 'w').write('')
open(os.path.join(OUT, 'assets/img/gry-logo.svg'), 'w').write(LOGO.replace(' class="ink"', ''))
open(os.path.join(OUT, 'assets/img/gry-logo-white.svg'), 'w').write(LOGO.replace(' class="ink"', '').replace('#4B2C73', '#FFFFFF'))
open(os.path.join(OUT, 'assets/img/favicon.svg'), 'w').write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" rx="112" fill="#4B2C73"/><g transform="translate(66 118) scale(.5)"><path d="M345 260H575V475H112Q57 475 57 420V95Q57 40 112 40H610" fill="none" stroke="#fff" stroke-width="84" stroke-linejoin="miter"/><circle cx="716" cy="150" r="50" fill="#F5B321"/></g></svg>''')

# ---------------------------------------------------------------- CLEAN ADDRESSES
# Every page moves to a folder (about.html -> /about/), every link and file path becomes absolute from the site root,
# and the old .html address stays only as a tiny forwarder, so ".html" never shows in the address bar.
import posixpath, glob as _glob
def clean(path):
    if path in ('index.html', ''): return ''
    if path.endswith('/index.html'): return path[:-len('index.html')]
    return path[:-5] + '/' if path.endswith('.html') else path
def _abs(url, base):
    if not url or url[0] in '#/' or re.match(r'^[a-z][a-z0-9+.-]*:', url): return url
    m = re.match(r'^([^?#]*)(.*)$', url); pth, tail = m.group(1), m.group(2)
    full = posixpath.normpath(posixpath.join(posixpath.dirname(base), pth)) if pth else base
    if full == '.': full = ''
    if full.endswith('.html') and full != '404.html': full = clean(full)
    return '/' + full + tail
_moved = []
for f in sorted(_glob.glob(os.path.join(OUT, '**', '*.html'), recursive=True)):
    rel = os.path.relpath(f, OUT).replace(os.sep, '/')
    if rel.startswith('admin/') or rel.startswith('google') or rel.endswith('/index.html'): continue
    h = open(f).read()
    if 'data-forward' in h[:400]: continue                       # already a forwarder from an earlier build
    h = re.sub(r'\b(href|src|poster|data-film|data-src)="([^"]*)"', lambda m: f'{m.group(1)}="{_abs(m.group(2), rel)}"', h)
    h = re.sub(re.escape(DOMAIN) + r'/([A-Za-z0-9/_-]+)\.html', lambda m: DOMAIN + '/' + clean(m.group(1) + '.html'), h).replace(DOMAIN + '/index.html', DOMAIN + '/')
    if rel in ('index.html', '404.html'):
        open(f, 'w').write(h); continue
    new = clean(rel); os.makedirs(os.path.join(OUT, new), exist_ok=True)
    open(os.path.join(OUT, new, 'index.html'), 'w').write(h)
    open(f, 'w').write(f'<!doctype html><html lang="en" data-forward><head><meta charset="utf-8"><title>Growthryders</title><link rel="canonical" href="{DOMAIN}/{new}"><meta name="robots" content="noindex"><script>location.replace("/{new}" + location.search + location.hash)</script><meta http-equiv="refresh" content="0; url=/{new}"></head><body><a href="/{new}">Continue</a></body></html>')
    _moved.append(rel)
for name in ('sitemap.xml', 'llms.txt'):
    t = open(os.path.join(OUT, name)).read()
    t = re.sub(re.escape(DOMAIN) + r'/([A-Za-z0-9/_-]+)\.html', lambda m: DOMAIN + '/' + clean(m.group(1) + '.html'), t)
    open(os.path.join(OUT, name), 'w').write(t)
print('built', len(pages) + 1, 'pages into', OUT, '| clean addresses:', len(_moved))
