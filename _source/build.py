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
           "knowsAbout": ["Brand activation", "Experiential marketing", "Through-the-line marketing", "Corporate park activations", "Event management", "Digital marketing", "Media planning and buying"],
           "description": "Integrated brand activation and through-the-line marketing company in Bengaluru."}
    site = {"@type": "WebSite", "@id": DOMAIN + "/#site", "url": DOMAIN, "name": "Growthryders", "publisher": {"@id": DOMAIN + "/#org"}, "inLanguage": "en-IN"}
    graph = [org, site, {"@type": "WebPage", "@id": canonical, "url": canonical, "name": title, "description": desc, "isPartOf": {"@id": DOMAIN + "/#site"}, "about": {"@id": DOMAIN + "/#org"}}]
    if path != 'index.html':
        crumbs = [("Home", DOMAIN + "/")] + ([("Work", DOMAIN + "/work.html")] if depth else []) + [(title.split(' | ')[0], canonical)]
        graph.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]})
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
<link rel="stylesheet" href="{r}assets/css/site.css?v=17">
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
<script src="{r}assets/js/site.js?v=11" defer></script>
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
home = f'''
<section class="hero hero-word on-dark">
  <div class="word-stage">
  <canvas class="word-veil" data-src="{{r}}assets/img/flip.jpg?v=2" aria-hidden="true"></canvas>
  <div class="wrap">
    <h1 class="word-slot"><span>Growthryders</span></h1>
    <div class="word-copy">
      <div>
        <p class="hero-kicker">Brand activation and marketing company, Bengaluru</p>
        <p class="hero-line">We take brands to where people are.</p>
      </div>
      <div>
        <p class="lede">Activations, events, media and digital, planned and run by one team, so your brand is seen, tried and remembered.</p>
        <div class="btn-row"><a class="btn" href="{{r}}services.html">Our services</a><a class="btn ghost" href="{{r}}work.html">Explore our work</a></div>
      </div>
    </div>
    <ul class="hero-services">{''.join(f'<li><a href="{{r}}services.html#{k}">{t.split(" and ")[0]}</a></li>' for k, t, d, cs in SERVICES)}</ul>
  </div>
  <a class="scroll-cue" href="#after-hero"><span>Scroll</span><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M12 4v15M6 13l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
  </div>
  <div class="word-run" id="after-hero" aria-hidden="true"></div>
</section>
<script src="{{r}}assets/js/word.js?v=13" defer></script>
{marquee()}

<section class="sec white on-light"><div class="wrap split">
  <div>
    <h2>Brand activations are our fulcrum.</h2>
    <p class="lede" style="margin-top:22px">Marketing becomes more powerful when a brand moves beyond communication and creates a real interaction with the people it wants to reach.</p>
    <p>We put the activation at the centre of the plan and build everything else around it: traditional media, digital platforms, outdoor advertising and experiential engagement, working as one through-the-line campaign.</p>
    <div class="btn-row"><a class="btn ghost" href="{{r}}about.html">About Growthryders</a></div>
  </div>
  {img('apache1', 'TVS Apache motorcycles on display at the Tu Race Laga venue')}
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
page('index.html', 'Growthryders | Brand activations and integrated marketing, Bengaluru',
     'Growthryders is a Bengaluru brand activation and through-the-line marketing company. Activations, digital, experiential, media and corporate events.', home, 'dark', intro=True)

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
page('about.html', 'About Growthryders | Brand activation company in Bengaluru',
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
page('services.html', 'Services | Brand activations, digital, experiential, media and events | Growthryders',
     'Brand activations and TTL marketing, digital marketing, experiential marketing, media solutions and corporate events from Growthryders, Bengaluru.', services, 'dark')

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
land = [f for f in FILMS if f[4] == 'land']; port = [f for f in FILMS if f[4] == 'port']
films = f'''
<section class="page-head on-dark"><div class="wrap">
  <h1>Films from the ground.</h1>
  <p class="lede">Eight films from our activations at Bagmane business parks: the run, the partners and the motorcycles.</p>
</div></section>
<section class="sec dark on-dark films-page" style="padding-top:0"><div class="wrap">
  <div class="feature">{film(land[0], True)}</div>
  <h2 class="films-h">Event and partner films</h2>
  <div class="grid-land">{''.join(film(f) for f in land[1:])}</div>
  <h2 class="films-h">Vertical films</h2>
  <div class="grid-port">{''.join(film(f) for f in port)}</div>
</div></section>
{PLAYER}
{CTA}
'''
if FILMS_LIVE: page('films.html', 'Films | Campaign and event films | Growthryders',
     'Watch films from Growthryders activations: Tu Race Laga with TVS Apache and Bagmane REIT, partner films for Axis Bank and Milky Mist, and Royal Enfield at Bagmane parks.', films, 'dark')

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
page('contact.html', 'Contact Growthryders | Bengaluru',
     'Talk to Growthryders about a brand activation, an integrated campaign or a corporate event. Phone, WhatsApp and email.', contact, 'dark')

page('404.html', 'Page not found | Growthryders', 'This page does not exist.',
     '<section class="page-head on-dark"><div class="wrap"><h1>This page is not here.</h1><p class="lede">The link may be old or mistyped.</p><div class="btn-row"><a class="btn" href="/">Go to the home page</a><a class="btn ghost" href="/work.html">See our work</a></div></div></section>', 'dark')

# ---------------------------------------------------------------- static files
pages = ['', 'about.html', 'services.html', 'work.html'] + (['films.html'] if FILMS_LIVE else []) + [ 'work/tu-race-laga.html', 'work/tvs-apache-bagmane.html', 'work/royal-enfield-bikers-bay.html', 'ips.html', 'contact.html']
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{DOMAIN}/{p}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod></url>\n' for p in pages) + '</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
open(os.path.join(OUT, 'CNAME'), 'w').write('growthryders.in\n')
open(os.path.join(OUT, '.nojekyll'), 'w').write('')
open(os.path.join(OUT, 'assets/img/gry-logo.svg'), 'w').write(LOGO.replace(' class="ink"', ''))
open(os.path.join(OUT, 'assets/img/gry-logo-white.svg'), 'w').write(LOGO.replace(' class="ink"', '').replace('#4B2C73', '#FFFFFF'))
open(os.path.join(OUT, 'assets/img/favicon.svg'), 'w').write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" rx="112" fill="#4B2C73"/><g transform="translate(66 118) scale(.5)"><path d="M345 260H575V475H112Q57 475 57 420V95Q57 40 112 40H610" fill="none" stroke="#fff" stroke-width="84" stroke-linejoin="miter"/><circle cx="716" cy="150" r="50" fill="#F5B321"/></g></svg>''')
print('built', len(pages) + 1, 'pages into', OUT)
