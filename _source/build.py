#!/usr/bin/env python3
"""Builds the static Growthryders site into ./site (plain HTML, no framework).
Run:  python3 build.py
Content lives in this file so copy edits are one place."""
import os, html, json, datetime

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site')
DOMAIN = 'https://growthryders.in'
PHONE_DISPLAY = '+91 81973 30612'      # WhatsApp Business number, also takes calls
PHONE_E164 = '918197330612'
PHONE2_DISPLAY = '+91 99005 65911'     # calls only
PHONE2_E164 = '919900565911'
EMAIL = 'surender@growthryders.in'
YEAR = datetime.date.today().year
FILMS_LIVE = os.environ.get('FILMS_LIVE', '1') == '1'   # set FILMS_LIVE=0 to publish without the film files

LOGO = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="10 0 1590 516" role="img" aria-label="GRY — Growthryders"><defs><clipPath id="lc"><rect x="0" y="0" width="1610" height="511"/></clipPath></defs><g class="ink" clip-path="url(#lc)" fill="none" stroke="#4B2C73" stroke-width="70" stroke-linejoin="miter"><path d="M345 260H575V475H112Q57 475 57 420V95Q57 40 112 40H1125A110 110 0 0 1 1125 260H732V520"/><path d="M1005 262L1245 530"/><path d="M1228 118L1405 268V520"/><path d="M1555 38V88Q1555 128 1522 158L1405 268" stroke-linecap="round"/></g><circle cx="729" cy="150" r="36" fill="#F5B321"/></svg>'''

LOGO_INTRO = '''<svg class="intro-logo" xmlns="http://www.w3.org/2000/svg" viewBox="10 0 1590 516" aria-hidden="true"><g class="rays" fill="none" stroke="#F5B321" stroke-width="5" stroke-linecap="round"><path pathLength="1" d="M-1400 150H729"/><path pathLength="1" d="M3000 150H729"/><path pathLength="1" d="M729 -1300V150"/><path pathLength="1" d="M729 1700V150"/></g><circle class="ring" cx="729" cy="150" r="36" fill="none" stroke="#F5B321" stroke-width="4"/><g fill="none" stroke="#fff" stroke-width="70" stroke-linejoin="miter"><path class="d1" pathLength="1" d="M732 511V260H1125A110 110 0 0 0 1125 40H112Q57 40 57 95V420Q57 475 112 475H575V260H345"/><path class="d2" pathLength="1" d="M1005 262L1238 511"/><path class="d3" pathLength="1" d="M1228 118L1405 268V511"/><path class="d4" pathLength="1" d="M1405 268L1522 158Q1555 128 1555 88V38" stroke-linecap="round"/></g><circle class="rider" cx="729" cy="150" r="36" fill="#F5B321"/></svg>'''
INTRO = f'''<div class="intro" id="intro" aria-hidden="true"><div class="intro-in">{LOGO_INTRO}<p class="intro-word"><span>Growthryders</span></p><p class="intro-tag"><span>Brand activations at the core</span></p></div><button class="intro-skip" type="button">Skip intro</button></div>'''

NAV = [('about.html', 'About'), ('services.html', 'Services'), ('work.html', 'Work')] + ([('films.html', 'Films')] if FILMS_LIVE else []) + [('ips.html', 'Our IPs')]

def page(path, title, desc, body, head='light', depth=0, intro=False):
    r = '../' * depth
    cur = path.split('/')[0]
    links = ''.join(f'<a href="{r}{h}"{" aria-current=\"page\"" if h == cur or (cur == "work" and h == "work.html") else ""}>{t}</a>' for h, t in NAV)
    canonical = DOMAIN + '/' + ('' if path == 'index.html' else path)
    org = {"@type": ["Organization", "ProfessionalService"], "@id": DOMAIN + "/#org", "name": "Growthryders", "alternateName": ["GRY", "Growth Ryders"], "url": DOMAIN,
           "logo": DOMAIN + "/assets/img/gry-logo.svg", "image": DOMAIN + "/assets/img/og.jpg", "email": EMAIL,
           "telephone": "+" + PHONE2_E164,
           "contactPoint": [{"@type": "ContactPoint", "telephone": "+" + PHONE2_E164, "contactType": "sales", "areaServed": "IN", "availableLanguage": ["en", "hi", "kn"]},
                            {"@type": "ContactPoint", "telephone": "+" + PHONE_E164, "contactType": "customer service", "areaServed": "IN"}],
           "address": {"@type": "PostalAddress", "addressLocality": "Bengaluru", "addressRegion": "Karnataka", "addressCountry": "IN"},
           "areaServed": [{"@type": "City", "name": "Bengaluru"}, {"@type": "Country", "name": "India"}],
           "knowsAbout": ["Brand activation", "BTL activation", "Experiential marketing", "Through-the-line marketing", "Corporate park activations", "Tech park activations", "Mall activations", "Roadshows", "Product sampling", "Event management", "Corporate events", "Digital marketing", "Media planning and buying", "Outdoor advertising"],
           "description": "Brand activation agency and through-the-line marketing company in Bengaluru (Bangalore), India."}
    site = {"@type": "WebSite", "@id": DOMAIN + "/#site", "url": DOMAIN, "name": "Growthryders", "publisher": {"@id": DOMAIN + "/#org"}, "inLanguage": "en-IN"}
    graph = [org, site, {"@type": "WebPage", "@id": canonical, "url": canonical, "name": title, "description": desc, "isPartOf": {"@id": DOMAIN + "/#site"}, "about": {"@id": DOMAIN + "/#org"}}]
    if path != 'index.html':
        crumbs = [("Home", DOMAIN + "/")] + ([("Work", DOMAIN + "/work.html")] if depth else []) + [(title.split(' | ')[0], canonical)]
        graph.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]})
    org["hasOfferCatalog"] = {"@type": "OfferCatalog", "name": "Marketing services", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": t, "description": d, "url": DOMAIN + "/services.html#" + k, "provider": {"@id": DOMAIN + "/#org"}, "areaServed": "IN"}} for k, t, d, cs in SERVICES]}
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
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="{r}assets/img/favicon.svg?v=2" type="image/svg+xml">
<link rel="apple-touch-icon" href="{r}assets/img/icon-180.png?v=2">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/css/site.css?v=25">
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
      <div>{LOGO}<p style="margin-top:16px;max-width:34ch">Brand activations at the core. Integrated marketing for growth.</p></div>
      <div><h2>Company</h2><ul><li><a href="{r}about.html">About</a></li><li><a href="{r}services.html">Services</a></li><li><a href="{r}work.html">Work</a></li>{"<li><a href=" + chr(34) + r + "films.html" + chr(34) + ">Films</a></li>" if FILMS_LIVE else ""}<li><a href="{r}ips.html">Our IPs</a></li></ul></div>
      <div><h2>Work</h2><ul><li><a href="{r}work/tu-race-laga.html">TVS Apache: Tu Race Laga</a></li><li><a href="{r}work/tvs-apache-bagmane.html">TVS Apache at Bagmane</a></li><li><a href="{r}work/royal-enfield-bikers-bay.html">Royal Enfield: Bikers Bay</a></li></ul></div>
      <div><h2>Contact</h2><ul><li><a href="tel:+{PHONE2_E164}">{PHONE2_DISPLAY}</a></li><li><a href="tel:+{PHONE_E164}">{PHONE_DISPLAY}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="https://wa.me/{PHONE_E164}">WhatsApp us</a></li><li>Bengaluru, India</li></ul></div>
    </div>
    <div class="legal"><span>© {YEAR} Growthryders</span><span>Bengaluru, India</span></div>
  </div>
</footer>
<script src="{r}assets/js/site.js?v=12" defer></script>
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
<div class="btn-row"><a class="btn" href="{r}contact.html">Start a conversation</a><a class="btn ghost" href="https://wa.me/''' + PHONE_E164 + '''">WhatsApp us</a></div>
</div></section>'''

SERVICES = [
 ('activations', 'Brand activations and TTL marketing', 'Consumer engagement on the ground, amplified across every channel that reaches the same people.',
  ['Corporate park activations', 'Mall and public space promotions', 'Product sampling', 'Roadshows', 'Campus and residential activations', 'Brand launches']),
 ('digital', 'Digital marketing', 'Search, social, content, websites and performance campaigns that keep the conversation going.',
  ['SEO and GEO', 'Performance marketing', 'Social media management', 'Content creation', 'Website design and development', 'Lead generation']),
 ('experiential', 'Experiential marketing', 'Launches, installations and interactive formats that turn communication into something people remember.',
  ['Product launches', 'Trade shows and exhibitions', 'Immersive brand storytelling', 'Employee and partner engagement']),
 ('media', 'Media solutions', 'Planning and buying across outdoor, transit, print, radio, corporate parks, malls and retail.',
  ['Outdoor and digital outdoor', 'Transit and airport media', 'Print and radio', 'Corporate park media', 'Mall and retail media']),
 ('events', 'Corporate events and engagement', 'Conferences, dealer meets, summits, awards and employee programmes, concept to close.',
  ['Conferences and annual meets', 'Dealer meets', 'Leadership summits', 'Awards', 'Employee engagement programmes']),
 ('experiential', 'Technology-led experiences', 'Installations, AR and VR, gamification and interactive digital formats built into the activation.',
  ['Technology-led installations', 'Augmented and virtual reality', 'Gamification', 'Interactive digital experiences']),
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
ROTOR = [('apache1', 'TVS Apache', 'TVS Apache motorcycles on display at Bagmane Tech Park, Bengaluru'), ('re1', 'Royal Enfield', 'Royal Enfield motorcycle with a painted tank at a Bagmane business park activation'),
         ('axis-wall', 'Axis Bank', 'Axis Bank banking partner stall at the Tu Race Laga corporate run'), ('sign', 'Bagmane Tech Park', 'Bagmane Tech Park entrance sign, Bengaluru'), ('partners', 'Bagmane REIT and Milky Mist', 'Partner pillar showing Bagmane REIT, Milky Mist and GRY branding')]
def rotor():
    slides = ''.join(f'<figure class="rot-s{" on" if i == 0 else ""}"><img src="{{r}}assets/img/{n}.jpg" alt="{html.escape(a)}" width="1280" height="720" loading="lazy"><figcaption>{b}</figcaption></figure>' for i, (n, b, a) in enumerate(ROTOR))
    return f'<div class="frame ratio-43 rotor" data-rotor>{slides}</div>'

FAQS = [
 ("What does Growthryders do?", "Growthryders is a brand activation agency and through-the-line marketing company based in Bengaluru (Bangalore). One team plans and runs brand activations, experiential marketing, media, corporate events, digital marketing and technology-led experiences."),
 ("Where is Growthryders based?", "Growthryders is based in Bengaluru (Bangalore), Karnataka, India."),
 ("What kinds of brand activations does Growthryders run?", "Corporate park activations, mall and public space promotions, product sampling, roadshows, campus and residential activations, and brand launches."),
 ("Which services does Growthryders offer?", "; ".join(t for k, t, d, cs in SERVICES) + "."),
 ("Which brands has Growthryders been on the ground with?", ", ".join(MARQUEE[:-1]) + " and " + MARQUEE[-1] + "."),
 ("What are Runcle and Bikers Bay?", "They are platforms Growthryders owns. Runcle is a fitness and wellness platform where running meets cycling, for runners, cyclists and corporate teams. Bikers Bay is a motorcycle community with rides, meets and brand collaborations."),
 ("How do I start a project with Growthryders?", f"Call {PHONE2_DISPLAY}, message on WhatsApp at {PHONE_DISPLAY}, or email {EMAIL}."),
]
def faq_html():
    items = ''.join(f'<details class="qa"><summary><h3>{html.escape(q)}</h3><span class="qa-x" aria-hidden="true"></span></summary><p>{html.escape(a)}</p></details>' for q, a in FAQS)
    return f'<section class="sec white on-light faq-sec" id="faq"><div class="wrap faq"><div class="sec-head"><h2>Questions people ask us</h2></div><div class="qa-list">{items}</div></div></section>'

home = f'''
<section class="hero h3 on-dark">
<div class="h3-wrap">
  <div class="h3-side h3-left"><a class="h3-ico h3-ico0" style="--n:0" href="{{r}}services.html#activations"><span class="h3-bob"><svg viewBox="-10 -5 640 640" aria-hidden="true" fill="none" stroke-linejoin="miter" stroke-miterlimit="6"><path id="h3-ic0" d="M300 555L128 322A205 205 0 1 1 472 322Z"/><use href="#h3-ic0" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="58"/><use href="#h3-ic0" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="58"/><use href="#h3-ic0" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="58"/><use href="#h3-ic0" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="58"/><use href="#h3-ic0" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic0" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic0" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic0" stroke="url(#h3-f)" stroke-width="58"/><use href="#h3-ic0" stroke="url(#h3-i)" stroke-width="42"/><circle cx="300" cy="215" r="34" fill="#f5b321"/></svg></span><span class="h3-lab">Brand activations</span></a><a class="h3-ico h3-ico2" style="--n:2" href="{{r}}services.html#experiential"><span class="h3-bob"><svg viewBox="-10 -5 640 640" aria-hidden="true" fill="none" stroke-linejoin="miter" stroke-miterlimit="6"><path id="h3-ic2" d="M300 40L362 238L560 300L362 362L300 560L238 362L40 300L238 238Z"/><use href="#h3-ic2" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="58"/><use href="#h3-ic2" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="58"/><use href="#h3-ic2" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="58"/><use href="#h3-ic2" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="58"/><use href="#h3-ic2" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic2" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic2" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic2" stroke="url(#h3-f)" stroke-width="58"/><use href="#h3-ic2" stroke="url(#h3-i)" stroke-width="42"/><circle cx="300" cy="300" r="34" fill="#f5b321"/></svg></span><span class="h3-lab">Experiential marketing</span></a><a class="h3-ico h3-ico4" style="--n:4" href="{{r}}services.html#events"><span class="h3-bob"><svg viewBox="-10 -5 640 640" aria-hidden="true" fill="none" stroke-linejoin="miter" stroke-miterlimit="6"><path id="h3-ic4" d="M55 125H545V545H55Z M55 250H545 M180 45V125 M420 45V125"/><use href="#h3-ic4" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="58"/><use href="#h3-ic4" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="58"/><use href="#h3-ic4" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="58"/><use href="#h3-ic4" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="58"/><use href="#h3-ic4" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic4" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic4" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic4" stroke="url(#h3-f)" stroke-width="58"/><use href="#h3-ic4" stroke="url(#h3-i)" stroke-width="42"/><circle cx="300" cy="398" r="34" fill="#f5b321"/></svg></span><span class="h3-lab">Corporate events</span></a></div>
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
  <div class="h3-side h3-right"><a class="h3-ico h3-ico3" style="--n:3" href="{{r}}services.html#media"><span class="h3-bob"><svg viewBox="-10 -5 640 640" aria-hidden="true" fill="none" stroke-linejoin="miter" stroke-miterlimit="6"><path id="h3-ic3" d="M55 60H545V345H55Z M190 345V555 M410 345V555"/><use href="#h3-ic3" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="58"/><use href="#h3-ic3" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="58"/><use href="#h3-ic3" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="58"/><use href="#h3-ic3" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="58"/><use href="#h3-ic3" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic3" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic3" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic3" stroke="url(#h3-f)" stroke-width="58"/><use href="#h3-ic3" stroke="url(#h3-i)" stroke-width="42"/><circle cx="300" cy="203" r="34" fill="#f5b321"/></svg></span><span class="h3-lab">Media solutions</span></a><a class="h3-ico h3-ico1" style="--n:1" href="{{r}}services.html#digital"><span class="h3-bob"><svg viewBox="-10 -5 640 640" aria-hidden="true" fill="none" stroke-linejoin="miter" stroke-miterlimit="6"><path id="h3-ic1" d="M222 45H378Q433 45 433 100V500Q433 555 378 555H222Q167 555 167 500V100Q167 45 222 45Z"/><use href="#h3-ic1" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="58"/><use href="#h3-ic1" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="58"/><use href="#h3-ic1" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="58"/><use href="#h3-ic1" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="58"/><use href="#h3-ic1" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic1" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic1" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic1" stroke="url(#h3-f)" stroke-width="58"/><use href="#h3-ic1" stroke="url(#h3-i)" stroke-width="42"/><circle cx="300" cy="455" r="34" fill="#f5b321"/></svg></span><span class="h3-lab">Digital marketing</span></a><a class="h3-ico h3-ico5" style="--n:5" href="{{r}}services.html#experiential"><span class="h3-bob"><svg viewBox="-10 -5 640 640" aria-hidden="true" fill="none" stroke-linejoin="miter" stroke-miterlimit="6"><path id="h3-ic5" d="M95 180H505Q560 180 560 235V385Q560 440 505 440H395L300 345L205 440H95Q40 440 40 385V235Q40 180 95 180Z"/><use href="#h3-ic5" transform="translate(18.2 32.2)" stroke="#241536" stroke-width="58"/><use href="#h3-ic5" transform="translate(15.6 27.6)" stroke="#241536" stroke-width="58"/><use href="#h3-ic5" transform="translate(13.0 23.0)" stroke="#241536" stroke-width="58"/><use href="#h3-ic5" transform="translate(10.4 18.4)" stroke="#241536" stroke-width="58"/><use href="#h3-ic5" transform="translate(7.8 13.8)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic5" transform="translate(5.2 9.2)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic5" transform="translate(2.6 4.6)" stroke="#3a2459" stroke-width="58"/><use href="#h3-ic5" stroke="url(#h3-f)" stroke-width="58"/><use href="#h3-ic5" stroke="url(#h3-i)" stroke-width="42"/><circle cx="165" cy="300" r="34" fill="#f5b321"/></svg></span><span class="h3-lab">Technology-led experiences</span></a></div>
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
  <div class="sec-head"><p class="kicker">Our services</p><h2>One partner. Multiple marketing capabilities.</h2><p class="lede">Six services under one roof, so a campaign is planned, built, promoted and run by the same team.</p></div>
  <ul class="svc">
    {''.join(f'<li><a href="{{r}}services.html#{k}"><h3>{t}</h3><div><p>{d}</p><ul class="chips">{"".join(f"<li>{c}</li>" for c in cs)}</ul></div><span class="go" aria-hidden="true">View</span></a></li>' for k, t, d, cs in SERVICES)}
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
page('index.html', 'Growthryders | Brand activation agency in Bengaluru (Bangalore)',
     'Growthryders is a brand activation agency in Bengaluru (Bangalore): tech park and mall activations, experiential marketing, media, corporate events and digital.', home, 'dark', intro=True)

# ---------------------------------------------------------------- ABOUT
about = f'''
<section class="page-head on-dark"><div class="wrap">
  <h1>Accelerating growth through activations, integrated marketing and experiences.</h1>
  <p class="lede">Growthryders is an integrated marketing and brand activation company that helps brands connect, engage and grow.</p>
</div></section>
<section class="sec white on-light"><div class="wrap split top">
  <div>
    <h2>What we believe</h2>
    <p class="lede" style="margin-top:22px">Successful marketing is built on meaningful consumer interactions.</p>
    <p>Brand activations sit at the centre of our marketing ecosystem, supported by a mix of traditional media, digital marketing, experiential engagement and new communication platforms.</p>
    <p>We develop through-the-line solutions that bring strategy, creativity, technology and execution together. Our work spans consumer activations, corporate engagement, media solutions, digital campaigns, experiential marketing and community-driven intellectual properties.</p>
    <p>From a product launch experience to a large consumer campaign or a platform of our own, we bring ideas to life.</p>
  </div>
  {img('group', 'Participants and organisers under the finish arch at Tu Race Laga')}
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
page('about.html', 'About Growthryders | Brand activation company in Bengaluru (Bangalore)',
     'Growthryders builds through-the-line marketing around brand activations: consumer engagement, media, digital, experiential work and community platforms.', about, 'dark')

# ---------------------------------------------------------------- SERVICES
def ul(items): return '<ul class="cols">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
services = f'''
<section class="page-head on-dark"><div class="wrap">
  <h1>Brands should be experienced, not just advertised.</h1>
  <p class="lede">Activations are the centre of what we do. Every other service exists to carry them further.</p>
</div></section>
<section class="sec white on-light" style="padding-top:0"><div class="wrap">
  <div class="service-block" id="activations" style="border-top:0">
    <div><h2>Brand activations and TTL marketing</h2></div>
    <div><p class="lede">We conceptualise and run consumer engagement programmes that bring a brand face to face with its audience.</p>
      {ul(['Consumer and product sampling', 'Retail and trade marketing', 'Corporate park activations', 'Mall and public space promotions', 'Roadshows and mobile campaigns', 'Campus and youth engagement', 'Residential community activations', 'Dealer and channel partner engagement', 'Guerrilla marketing', 'Brand launches and promotional campaigns'])}
      <h3 style="margin-top:32px">Integrated around the activation</h3>
      <p style="margin-top:10px">We amplify each activation through the channels that reach the same people, so the message stays consistent across physical and digital touchpoints.</p>
      {ul(['Outdoor advertising, OOH and DOOH', 'Digital and social media campaigns', 'Print and radio advertising', 'Transit and airport media', 'Retail and point-of-sale branding', 'Innovative and ambient media'])}</div>
  </div>
  <div class="service-block" id="digital">
    <div><h2>Digital marketing</h2></div>
    <div><p class="lede">We help brands strengthen their digital presence and reach the right audience.</p>
      {ul(['Search engine optimisation (SEO)', 'Generative engine optimisation (GEO)', 'Performance marketing', 'Social media management', 'Content strategy and creation', 'Website design and development', 'Lead generation', 'Digital campaign management', 'Marketing analytics and automation'])}</div>
  </div>
  <div class="service-block" id="experiential">
    <div><h2>Experiential marketing</h2></div>
    <div><p class="lede">Immersive experiences that turn brand communication into something people remember.</p>
      {ul(['Product launches', 'Corporate events and conferences', 'Trade shows and exhibitions', 'Technology-led installations', 'Augmented and virtual reality', 'Interactive digital experiences', 'Gamification', 'Immersive brand storytelling', 'Employee and partner engagement'])}</div>
  </div>
  <div class="service-block" id="media">
    <div><h2>Media solutions</h2></div>
    <div><p class="lede">Media planning and execution across the formats that surround an activation.</p>
      {ul(['Outdoor and digital outdoor media', 'Transit and airport media', 'Print and radio', 'Corporate park media', 'Mall and retail media', 'Innovative and ambient media platforms'])}</div>
  </div>
  <div class="service-block" id="events">
    <div><h2>Corporate events and engagement</h2></div>
    <div><p class="lede">Business and corporate engagement platforms, conceptualised and executed end to end.</p>
      {ul(['Conferences and annual meets', 'Dealer meets', 'Leadership summits', 'Awards', 'Employee engagement programmes', 'Product launches'])}</div>
  </div>
</div></section>
{CTA}
'''
page('services.html', 'Services | Brand activations, experiential marketing, media and events in Bengaluru | Growthryders',
     'Brand activations and BTL/TTL marketing, tech park and mall activations, experiential marketing, media solutions, corporate events and digital marketing in Bengaluru (Bangalore).', services, 'dark')

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
     g('flagoff', 'Runners leaving the start arch at the flag-off', True) + g('runners2', 'Runners on the course inside the tech park') + g('axis', 'Participants at a partner activity stall') + g('medals', 'Finisher medals laid out for the runners') + g('finish', 'Finishers celebrating after the run', True),
     bibs(TRL_BIBS, True), film_keys=('tu-race-laga-event-film', 'tvs-apache-tu-race-laga', 'axis-bank-tu-race-laga', 'milky-mist-tu-race-laga'))

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
     g('re1', 'A Royal Enfield motorcycle on display at a Bagmane business park', True) + g('re2', 'Royal Enfield motorcycles lined up at a display') + g('re3', 'Visitors looking at a Royal Enfield motorcycle', True) + g('re4', 'Detail of a Royal Enfield motorcycle'), film_keys=('royal-enfield-bagmane-film', 'royal-enfield-tech-park', 'royal-enfield-capital'))


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
ips = f'''
<section class="page-head on-dark"><div class="wrap">
  <h1>Building communities. Creating long-term brand platforms.</h1>
  <p class="lede">We develop platforms of our own that bring audiences, communities and brands together again and again.</p>
</div></section>
<section class="sec white on-light"><div class="wrap split top" id="runcle" style="scroll-margin-top:24px">
  <div><h2>Runcle</h2><p class="lede" style="margin-top:18px">Running meets cycling.</p>
    <p>A fitness and wellness platform that brings runners, cyclists and fitness enthusiasts together, and gives brands a way to reach an active-lifestyle audience.</p>
    {ul(['Running and cycling events', 'Corporate wellness programmes', 'Fitness challenges', 'Health awareness initiatives', 'Community engagement', 'Brand partnerships'])}</div>
  {img('runners2', 'Runners on the course inside a Bagmane tech park')}
</div></section>
<section class="sec on-light"><div class="wrap split top" id="bikers-bay" style="scroll-margin-top:24px">
  {img('re3', 'Visitors looking at a Royal Enfield motorcycle')}
  <div><h2>Bikers Bay</h2><p class="lede" style="margin-top:18px">The motorcycle community.</p>
    <p>A community platform that connects motorcycle enthusiasts through rides, experiences, networking and brand associations.</p>
    {ul(['Rider meets and networking', 'Motorcycle experiences', 'Weekend rides and adventures', 'Brand collaborations', 'Lifestyle engagement', 'Digital community initiatives'])}</div>
</div></section>
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
  <form class="form" id="enquiry" data-wa="{PHONE_E164}" data-mail="{EMAIL}" novalidate>
    <h2>Send an enquiry</h2>
    <label>Your name<input name="name" autocomplete="name" required></label>
    <label>Company<input name="company" autocomplete="organization"></label>
    <label>What are you looking for?
      <select name="need"><option>Brand activation</option><option>Integrated TTL campaign</option><option>Digital marketing</option><option>Experiential marketing</option><option>Media solutions</option><option>Corporate event</option><option>Partnering on Runcle or Bikers Bay</option><option>Something else</option></select></label>
    <label>Tell us about it<textarea name="note" required></textarea></label>
    <p class="err" role="alert"></p>
    <div class="btn-row" style="margin-top:0"><button class="btn" type="button" data-send="whatsapp">Send on WhatsApp</button><button class="btn ghost" type="button" data-send="email">Send by email</button></div>
    <p class="note">Your message opens in WhatsApp or your email app, ready to send. Nothing is stored on this site.</p>
  </form>
  <div>
    <h2>Reach us directly</h2>
    <ul class="contact-list" style="margin-top:24px">
      <li>Phone<br><a href="tel:+{PHONE2_E164}">{PHONE2_DISPLAY}</a><br><a href="tel:+{PHONE_E164}">{PHONE_DISPLAY}</a></li>
      <li>WhatsApp<br><a href="https://wa.me/{PHONE_E164}">Message {PHONE_DISPLAY}</a></li>
      <li>Email<br><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li>Location<br><strong>Bengaluru, India</strong></li>
    </ul>
  </div>
</div></section>
'''
page('contact.html', 'Contact Growthryders | Brand activation agency, Bengaluru (Bangalore)',
     'Talk to Growthryders about a brand activation, an integrated campaign or a corporate event. Phone, WhatsApp and email.', contact, 'dark')

page('404.html', 'Page not found | Growthryders', 'This page does not exist.',
     '<section class="page-head on-dark"><div class="wrap"><h1>This page is not here.</h1><p class="lede">The link may be old or mistyped.</p><div class="btn-row"><a class="btn" href="/">Go to the home page</a><a class="btn ghost" href="/work.html">See our work</a></div></div></section>', 'dark')

# ---------------------------------------------------------------- static files
pages = ['', 'about.html', 'services.html', 'work.html'] + (['films.html'] if FILMS_LIVE else []) + [ 'work/tu-race-laga.html', 'work/tvs-apache-bagmane.html', 'work/royal-enfield-bikers-bay.html', 'ips.html', 'contact.html']
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{DOMAIN}/{p}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod></url>\n' for p in pages) + '</urlset>\n')
BOTS = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'PerplexityBot', 'Google-Extended', 'Applebot-Extended', 'Bingbot']
open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\n\n' + ''.join(f'User-agent: {b}\nAllow: /\n\n' for b in BOTS) + f'Sitemap: {DOMAIN}/sitemap.xml\n')
open(os.path.join(OUT, 'llms.txt'), 'w').write(f'''# Growthryders

> Growthryders (GRY) is a brand activation and through-the-line marketing company based in Bengaluru, Karnataka, India. One team plans and runs activations, experiential marketing, media, corporate events, digital marketing and technology-led experiences.

## Services
''' + ''.join(f'- [{t}]({DOMAIN}/services.html#{k}): {d} Includes: {", ".join(cs)}.\n' for k, t, d, cs in SERVICES) + f'''
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
- Phone: {PHONE2_DISPLAY}
- WhatsApp: {PHONE_DISPLAY}
- Email: {EMAIL}
- Location: Bengaluru, Karnataka, India
''')
open(os.path.join(OUT, 'CNAME'), 'w').write('growthryders.in\n')
open(os.path.join(OUT, '.nojekyll'), 'w').write('')
open(os.path.join(OUT, 'assets/img/gry-logo.svg'), 'w').write(LOGO.replace(' class="ink"', ''))
open(os.path.join(OUT, 'assets/img/gry-logo-white.svg'), 'w').write(LOGO.replace(' class="ink"', '').replace('#4B2C73', '#FFFFFF'))
open(os.path.join(OUT, 'assets/img/favicon.svg'), 'w').write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" rx="112" fill="#4B2C73"/><g transform="translate(66 118) scale(.5)"><path d="M345 260H575V475H112Q57 475 57 420V95Q57 40 112 40H610" fill="none" stroke="#fff" stroke-width="84" stroke-linejoin="miter"/><circle cx="716" cy="150" r="50" fill="#F5B321"/></g></svg>''')
print('built', len(pages) + 1, 'pages into', OUT)
