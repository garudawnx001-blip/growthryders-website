// Growthryders — behaviours: intro, header, reveals, counters, films, menu, enquiry form
(function () {
  var doc = document.documentElement, body = document.body;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // every page opens from the top (unless it was opened at a section link)
  try { history.scrollRestoration = 'manual'; } catch (e) {}
  if (!location.hash) window.scrollTo(0, 0);

  // ---- intro (home, once per visit)
  var intro = document.getElementById('intro');
  function ready() { body.classList.add('ready'); }
  if (intro && doc.classList.contains('intro-on')) {
    var done = false, logo = intro.querySelector('.intro-logo'), brand = document.querySelector('.site-head .brand');
    // hand-off: the mark travels from the centre of the screen to its place in the header while the page fades up behind it
    var finish = function (fast) {
      if (done) return; done = true;
      try { sessionStorage.setItem('gry-intro', '1'); } catch (e) {}
      var to = brand.querySelector('svg').getBoundingClientRect(), from = logo.getBoundingClientRect();
      intro.classList.add('leaving'); if (fast) intro.classList.add('fast');
      void logo.offsetWidth;
      logo.style.transform = 'translate(' + (to.left - from.left) + 'px,' + (to.top - from.top) + 'px) scale(' + (to.width / from.width) + ')';
      ready();
      setTimeout(function () { doc.classList.remove('intro-on'); brand.classList.add('landed'); intro.remove(); }, fast ? 620 : 1080);
    };
    setTimeout(function () { finish(false); }, 3300);
    intro.querySelector('.intro-skip').addEventListener('click', function () { finish(true); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') finish(true); });
  } else {
    requestAnimationFrame(function () { requestAnimationFrame(ready); });
  }

  // ---- header: solid after the first screen, hides going down, returns going up
  var head = document.querySelector('.site-head'), lastY = window.scrollY, upRun = 0;
  window.addEventListener('scroll', function () {
    var y = window.scrollY, d = y - lastY; lastY = y;
    head.classList.toggle('scrolled', y > 40);
    if (head.classList.contains('menu-open') || y < 120) { head.classList.remove('hide'); upRun = 0; return; }
    if (d > 0) { upRun = 0; if (d > 2) head.classList.add('hide'); }          // going down: out of the way
    else if (d < 0) { upRun -= d; if (upRun > 12) head.classList.remove('hide'); }  // a small scroll up brings it back
  }, { passive: true });
  head.addEventListener('focusin', function () { head.classList.remove('hide'); });

  // ---- brand shots that change (home, "fulcrum" block): only while on screen
  [].forEach.call(document.querySelectorAll('[data-rotor]'), function (el) {
    var s = el.querySelectorAll('.rot-s'), i = 0, tm = 0, vis = false; if (s.length < 2) return;
    [].forEach.call(s, function (f) { var im = f.querySelector('img'); if (im) im.loading = 'eager'; });
    function step() { s[i].classList.remove('on'); i = (i + 1) % s.length; s[i].classList.add('on'); }
    function run() { clearInterval(tm); if (vis && !document.hidden && !matchMedia('(prefers-reduced-motion: reduce)').matches) tm = setInterval(step, 2800); }
    if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { vis = e[0].isIntersecting; run(); }, { threshold: .25 }).observe(el); else { vis = true; run(); }
    document.addEventListener('visibilitychange', run);
  });

  // ---- mobile menu
  var toggle = document.querySelector('.nav-toggle'), nav = document.getElementById('nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      head.classList.toggle('menu-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav.classList.contains('open')) toggle.click(); });
  }

  // ---- scroll reveals (content is visible without JS; with JS it arrives as you reach it)
  var sel = '.sec h2,.sec .lede,.sec p:not(.note):not(.err),.sec .frame,.svc li,.bib,.why > div,.ip,.steps li,.film,.facts,.cols,.contact-list li,.form label,.cta h2,.cta .lede,.cta .btn-row,.sec .btn-row';
  var items = [].slice.call(document.querySelectorAll(sel));
  if ('IntersectionObserver' in window && !reduce) {
    items.forEach(function (el) {
      var sibs = el.parentElement ? [].slice.call(el.parentElement.children) : [el];
      el.style.setProperty('--i', Math.min(sibs.indexOf(el), 4));
      el.setAttribute('data-rv', '');
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); count(en.target); } });
    }, { rootMargin: '0px 0px 6% 0px', threshold: 0 });
    items.forEach(function (el) { io.observe(el); });
  }

  // ---- bib numbers count up when they arrive
  function count(el) {
    var n = el.classList && el.classList.contains('bib') ? el.querySelector('.num') : null;
    if (!n || reduce) return;
    var target = parseInt(n.textContent.replace(/,/g, ''), 10); if (!target) return;
    var t0 = performance.now(), dur = 900;
    (function tick(t) {
      var p = Math.min(1, (t - t0) / dur), v = Math.round(target * (1 - Math.pow(1 - p, 3)));
      n.textContent = v.toLocaleString('en-IN');
      if (p < 1) requestAnimationFrame(tick);
    })(t0);
  }

  // ---- hero video pause
  var video = document.querySelector('.hero video'), pause = document.querySelector('.hero-pause');
  if (video && pause) {
    if (reduce) { video.removeAttribute('autoplay'); video.pause(); pause.textContent = 'Play video'; }
    pause.addEventListener('click', function () {
      if (video.paused) { video.play(); pause.textContent = 'Pause video'; } else { video.pause(); pause.textContent = 'Play video'; }
    });
  }

  // ---- hero video: start as soon as it can, never sit frozen
  if (video && !reduce) {
    var kick = function () { var p = video.play(); if (p && p.catch) p.catch(function () {}); };
    video.muted = true; video.addEventListener('canplay', kick, { once: true }); kick();
    document.addEventListener('visibilitychange', function () { if (!document.hidden && video.paused && pause && pause.textContent === 'Pause video') kick(); });
  }

  // ---- simple opening: the glow leans gently towards the pointer
  var hs = document.querySelector('.hero-simple');
  if (hs && !reduce && window.matchMedia('(hover:hover)').matches) {
    var gl = hs.querySelector('.glow'), tick = false;
    hs.addEventListener('pointermove', function (e) { if (tick) return; tick = true; requestAnimationFrame(function () { var r = hs.getBoundingClientRect(); gl.style.setProperty('--mx', ((e.clientX - r.left) / r.width - .5).toFixed(3)); gl.style.setProperty('--my', ((e.clientY - r.top) / r.height - .5).toFixed(3)); tick = false; }); }, { passive: true });
  }

  // ---- film strip: glides on its own and loops; your swipe or drag always wins, and it carries on once you let go
  var strip = document.querySelector('.strip');
  if (strip && !reduce) {
    var kids = [].slice.call(strip.children), seen = false, x = 0, last = 0, mine = -1, busyUntil = 0, down = false, hover = false;
    for (var rep = 0; rep < 2; rep++) kids.forEach(function (k) { var c = k.cloneNode(true); c.setAttribute('aria-hidden', 'true'); c.removeAttribute('data-rv'); c.classList.add('in'); var ci = c.querySelector('img'); if (ci) ci.loading = 'eager'; c.tabIndex = -1; strip.appendChild(c); });
    var span = function () { return strip.children[kids.length].offsetLeft - strip.children[0].offsetLeft; };
    var settle = function () { var h = span(); if (h <= 0) return; var v = strip.scrollLeft; while (v < h * 0.5) v += h; while (v >= h * 1.5) v -= h; if (v !== strip.scrollLeft) strip.scrollLeft = v; x = v; mine = Math.round(v); };
    var busy = function (ms) { busyUntil = performance.now() + ms; };
    requestAnimationFrame(function () { strip.scrollLeft = span(); settle(); });
    // any scroll we did not cause is the visitor's: step back and let it run, momentum included
    strip.addEventListener('scroll', function () { if (Math.abs(strip.scrollLeft - mine) > 2) busy(1600); }, { passive: true });
    strip.addEventListener('touchstart', function () { down = true; busy(1e7); }, { passive: true });
    var up = function () { down = false; busy(1800); };
    strip.addEventListener('touchend', up, { passive: true }); strip.addEventListener('touchcancel', up, { passive: true });
    strip.addEventListener('wheel', function () { busy(1600); }, { passive: true });
    strip.addEventListener('mouseenter', function () { hover = true; }); strip.addEventListener('mouseleave', function () { hover = false; drag = null; });
    strip.addEventListener('focusin', function () { hover = true; }); strip.addEventListener('focusout', function () { hover = false; });
    // mouse drag on desktop
    var drag = null, moved = false;
    strip.addEventListener('mousedown', function (e) { drag = { x: e.clientX, s: strip.scrollLeft }; moved = false; });
    window.addEventListener('mousemove', function (e) { if (!drag) return; var d = e.clientX - drag.x; if (Math.abs(d) > 4) moved = true; strip.scrollLeft = drag.s - d; busy(1600); });
    window.addEventListener('mouseup', function () { drag = null; });
    strip.addEventListener('click', function (e) { if (moved) { e.stopPropagation(); e.preventDefault(); moved = false; } }, true);
    strip.addEventListener('dragstart', function (e) { e.preventDefault(); });
    // arrows: one film at a time
    var step = function (dir) { var c = strip.children[0], w = c.getBoundingClientRect().width + 16; settle(); busy(2600); strip.scrollTo({ left: strip.scrollLeft + dir * w, behavior: 'smooth' }); };
    var wrapEl = strip.parentElement, pb = wrapEl.querySelector('.strip-btn.prev'), nb = wrapEl.querySelector('.strip-btn.next');
    if (pb) pb.addEventListener('click', function () { step(-1); }); if (nb) nb.addEventListener('click', function () { step(1); });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { seen = e[0].isIntersecting; }, { threshold: 0.15 }).observe(strip); else seen = true;
    var was = true;
    (function glide(t) {
      var dt = Math.min(48, t - last || 16); last = t;
      var dlg = document.getElementById('player'), idle = !down && !drag && !hover && t > busyUntil && !(dlg && dlg.open) && !document.hidden;
      if (idle && !was) settle();           // pick up from wherever the visitor left it
      was = idle;
      if (idle && seen) {
        x += dt * 0.045; var h = span(); if (h > 0 && x >= h * 1.5) x -= h;
        strip.scrollLeft = x; mine = Math.round(strip.scrollLeft);
      }
      requestAnimationFrame(glide);
    })(0);
  }

  // ---- film player
  var player = document.getElementById('player');
  if (player && player.showModal) {
    var pv = player.querySelector('video'), pt = player.querySelector('.player-title');
    document.addEventListener('click', function (e) {
      var b = e.target.closest ? e.target.closest('.film') : null; if (!b) return;
      pv.src = b.dataset.film; pt.textContent = b.dataset.title;
      player.showModal(); pv.play().catch(function () {});
    });
    var close = function () { pv.pause(); pv.removeAttribute('src'); pv.load(); if (player.open) player.close(); };
    player.querySelector('.player-close').addEventListener('click', close);
    player.addEventListener('click', function (e) { if (e.target === player) close(); });
    player.addEventListener('close', function () { pv.pause(); });
  }

  // ---- enquiry form: opens WhatsApp or the email app with the message ready, and files the enquiry in the team's sheet
  function track(name, params) { try { if (window.gtag) gtag('event', name, params || {}); } catch (e) {} }
  var form = document.getElementById('enquiry');
  if (form) {
    var err = form.querySelector('.err'), ENTRY = { name: 'entry.1457202910', company: 'entry.765574579', contact: 'entry.1436458381', need: 'entry.259839848', note: 'entry.1185777336', via: 'entry.1418327185', page: 'entry.885099739', source: 'entry.1439589845' };
    var read = function () {
      var d = new FormData(form), v = { name: (d.get('name') || '').trim(), company: (d.get('company') || '').trim(), contact: (d.get('contact') || '').trim(), need: d.get('need') || '', note: (d.get('note') || '').trim() };
      if (!v.name || !v.note) { err.textContent = 'Add your name and a line about what you are planning.'; return null; }
      if (!/^\+?[0-9][0-9 ()-]{6,}$/.test(v.contact) && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v.contact)) { err.textContent = 'Add a phone number or an email address so we can reply.'; return null; }
      err.textContent = ''; return v;
    };
    var text = function (v) { return 'Hello Growthryders,\n\nName: ' + v.name + (v.company ? '\nCompany: ' + v.company : '') + '\nContact: ' + v.contact + '\nLooking for: ' + v.need + '\n\n' + v.note; };
    var file = function (v, via) {
      try {
        var b = new URLSearchParams(); v.via = via; v.page = location.pathname; v.source = document.referrer ? new URL(document.referrer).hostname : 'Direct';
        Object.keys(ENTRY).forEach(function (k) { b.append(ENTRY[k], v[k] || ''); });
        fetch(form.dataset.sheet, { method: 'POST', mode: 'no-cors', keepalive: true, headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: b.toString() }).catch(function () {});
      } catch (e) {}
      track('generate_lead', { method: via, service: v.need });
    };
    form.querySelector('[data-send="whatsapp"]').addEventListener('click', function () {
      var v = read(); if (!v) return; file(v, 'WhatsApp');
      window.open('https://wa.me/' + form.dataset.wa + '?text=' + encodeURIComponent(text(v)), '_blank', 'noopener');
    });
    form.querySelector('[data-send="email"]').addEventListener('click', function () {
      var v = read(); if (!v) return; file(v, 'Email');
      window.location.href = 'mailto:' + form.dataset.mail + '?subject=' + encodeURIComponent('Enquiry from the Growthryders website') + '&body=' + encodeURIComponent(text(v));
    });
    form.addEventListener('submit', function (e) { e.preventDefault(); form.querySelector('[data-send="whatsapp"]').click(); });
  }
  // ---- count taps on WhatsApp, phone and email links
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]'); if (!a) return; var h = a.getAttribute('href');
    if (h.indexOf('wa.me/') > -1) track('contact_click', { method: 'WhatsApp' });
    else if (h.indexOf('tel:') === 0) track('contact_click', { method: 'Phone' });
    else if (h.indexOf('mailto:') === 0) track('contact_click', { method: 'Email' });
  });

})();

/* v14 photo viewer: tap any photo to open it full screen */
(function(){
  var imgs=[].slice.call(document.querySelectorAll('main .frame:not(.rotor) img')).filter(function(i){return !i.closest('a,button,[data-film]')});
  if(!imgs.length) return;
  var box=document.createElement('div');box.className='lb';box.setAttribute('role','dialog');box.setAttribute('aria-modal','true');box.setAttribute('aria-label','Photo viewer');box.hidden=true;
  box.innerHTML='<figure class="lb-fig"><img class="lb-img" alt=""><figcaption class="lb-cap"></figcaption></figure>'+
    '<button class="lb-btn lb-x" type="button" aria-label="Close">&times;</button>'+
    '<button class="lb-btn lb-prev" type="button" aria-label="Previous photo">&#8249;</button>'+
    '<button class="lb-btn lb-next" type="button" aria-label="Next photo">&#8250;</button>'+
    '<span class="lb-count" aria-live="polite"></span>';
  document.body.appendChild(box);
  var big=box.querySelector('.lb-img'),cap=box.querySelector('.lb-cap'),cnt=box.querySelector('.lb-count'),cur=0,last=null;
  function show(n){cur=(n+imgs.length)%imgs.length;var s=imgs[cur];big.src=s.currentSrc||s.src;big.alt=s.alt;cap.textContent=s.alt;cnt.textContent=(cur+1)+' / '+imgs.length;
    box.querySelector('.lb-prev').hidden=box.querySelector('.lb-next').hidden=imgs.length<2;}
  function open(n){last=document.activeElement;show(n);box.hidden=false;document.documentElement.classList.add('lb-open');box.querySelector('.lb-x').focus();}
  function close(){box.hidden=true;document.documentElement.classList.remove('lb-open');if(last&&last.focus)last.focus();}
  imgs.forEach(function(im,i){var f=im.parentNode;f.classList.add('zoomable');f.tabIndex=0;f.setAttribute('role','button');f.setAttribute('aria-label','Open photo: '+im.alt);
    f.addEventListener('click',function(){open(i)});
    f.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();open(i)}});});
  box.querySelector('.lb-x').onclick=close;
  box.querySelector('.lb-prev').onclick=function(e){e.stopPropagation();show(cur-1)};
  box.querySelector('.lb-next').onclick=function(e){e.stopPropagation();show(cur+1)};
  box.addEventListener('click',function(e){if(e.target===box||e.target.classList.contains('lb-fig'))close()});
  document.addEventListener('keydown',function(e){if(box.hidden)return;if(e.key==='Escape')close();else if(e.key==='ArrowLeft')show(cur-1);else if(e.key==='ArrowRight')show(cur+1);});
  var x0=null;box.addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});
  box.addEventListener('touchend',function(e){if(x0===null)return;var d=e.changedTouches[0].clientX-x0;if(Math.abs(d)>50)show(cur+(d<0?1:-1));x0=null},{passive:true});
})();
