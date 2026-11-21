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
  var head = document.querySelector('.site-head'), lastY = 0;
  window.addEventListener('scroll', function () {
    var y = window.scrollY;
    head.classList.toggle('scrolled', y > 40);
    head.classList.toggle('hide', y > 400 && y > lastY + 4);
    if (y < lastY - 4) head.classList.remove('hide');
    lastY = y;
  }, { passive: true });

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

  // ---- film strip: glides on its own, loops, and waits while you touch, hover or watch a film
  var strip = document.querySelector('.strip');
  if (strip && !reduce) {
    var kids = [].slice.call(strip.children), held = false, seen = false, x = 0, last = 0;
    kids.forEach(function (k) { var c = k.cloneNode(true); c.setAttribute('aria-hidden', 'true'); c.tabIndex = -1; strip.appendChild(c); });
    var half = function () { return strip.children[kids.length].offsetLeft - strip.children[0].offsetLeft; };
    var hold = function (v) { return function () { held = v; if (!v) x = strip.scrollLeft; }; };
    strip.addEventListener('pointerenter', hold(true)); strip.addEventListener('pointerleave', hold(false));
    strip.addEventListener('touchstart', hold(true), { passive: true });
    strip.addEventListener('touchend', function () { setTimeout(hold(false), 2500); }, { passive: true });
    strip.addEventListener('focusin', hold(true)); strip.addEventListener('focusout', hold(false));
    if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { seen = e[0].isIntersecting; }, { threshold: 0.15 }).observe(strip); else seen = true;
    (function glide(t) {
      var dt = Math.min(48, t - last || 16); last = t;
      var open = document.getElementById('player'); open = open && open.open;
      if (seen && !held && !open && !document.hidden) {
        x += dt * 0.045; var h = half(); if (h > 0 && x >= h) x -= h;
        strip.scrollLeft = x;
      } else if (held) { var h2 = half(); if (h2 > 0 && strip.scrollLeft >= h2) strip.scrollLeft -= h2; }
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

  // ---- enquiry form: opens WhatsApp or the email app with the message ready
  var form = document.getElementById('enquiry');
  if (form) {
    var err = form.querySelector('.err');
    var message = function () {
      var d = new FormData(form);
      var name = (d.get('name') || '').trim(), company = (d.get('company') || '').trim();
      var need = d.get('need') || '', note = (d.get('note') || '').trim();
      if (!name || !note) { err.textContent = 'Add your name and a line about what you are planning.'; return null; }
      err.textContent = '';
      return 'Hello Growthryders,\n\nName: ' + name + (company ? '\nCompany: ' + company : '') + '\nLooking for: ' + need + '\n\n' + note;
    };
    form.querySelector('[data-send="whatsapp"]').addEventListener('click', function () {
      var m = message(); if (!m) return;
      window.open('https://wa.me/' + form.dataset.wa + '?text=' + encodeURIComponent(m), '_blank', 'noopener');
    });
    form.querySelector('[data-send="email"]').addEventListener('click', function () {
      var m = message(); if (!m) return;
      window.location.href = 'mailto:' + form.dataset.mail + '?subject=' + encodeURIComponent('Enquiry from the Growthryders website') + '&body=' + encodeURIComponent(m);
    });
    form.addEventListener('submit', function (e) { e.preventDefault(); form.querySelector('[data-send="whatsapp"]').click(); });
  }
})();
