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
    var done = false;
    var finish = function (fast) {
      if (done) return; done = true;
      try { sessionStorage.setItem('gry-intro', '1'); } catch (e) {}
      if (fast) { intro.style.animation = 'introOut .45s cubic-bezier(.7,0,.2,1) forwards'; }
      ready();
      setTimeout(function () { doc.classList.remove('intro-on'); intro.remove(); }, fast ? 500 : 800);
    };
    setTimeout(function () { finish(false); }, 3500);
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
      el.style.setProperty('--i', Math.min(sibs.indexOf(el), 6));
      el.setAttribute('data-rv', '');
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); count(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
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

  // ---- film player
  var player = document.getElementById('player');
  if (player && player.showModal) {
    var pv = player.querySelector('video'), pt = player.querySelector('.player-title');
    document.querySelectorAll('.film').forEach(function (b) {
      b.addEventListener('click', function () {
        pv.src = b.dataset.film; pt.textContent = b.dataset.title;
        player.showModal(); pv.play().catch(function () {});
      });
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
