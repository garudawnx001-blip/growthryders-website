// Growthryders — title card. Brand shots flip full screen, the camera pulls back to find them inside G R Y,
// the missing letters arrive one by one, and the name settles in white. One canvas, one image; static once settled.
(function () {
  var hero = document.querySelector('.hero-word'), cv = hero && hero.querySelector('.word-veil'); if (!cv) return;
  var D = {"paths":{"G":"M288 260H518V475H55Q0 475 0 420V95Q0 40 55 40H518","R":"M0 475V260H393A110 110 0 0 0 393 40H0 M273 262L506 511","R2":"M0 475V40H393A110 110 0 0 1 393 260H0 M273 262L506 511","O":"M55 40H463Q518 40 518 95V420Q518 475 463 475H55Q0 475 0 420V95Q0 40 55 40Z","W":"M0 40V420Q0 475 55 475H545Q600 475 600 420V40 M300 475V150","T":"M0 40H470 M235 40V475","H":"M0 40V475 M500 40V475 M0 258H500","Y":"M0 118L177 268V475 M327 38V88Q327 128 294 158L177 268","D":"M0 40H282A217.5 217.5 0 0 1 282 475H0Z","E":"M480 40H55Q0 40 0 95V420Q0 475 55 475H480 M0 258H400","S":"M500 40H55Q0 40 0 95V203Q0 258 55 258H445Q500 258 500 313V420Q500 475 445 475H0"},"full":[["G",35.0,518],["R",710.0,513],["O",1380.0,518],["W",2055.0,600],["T",2812.0,470],["H",3439.0,500],["R2",4096.0,513],["Y",4766.0,327],["D",5250.0,500],["E",5907.0,480],["R2",6544.0,513],["S",7214.0,500]],"wf":7749,"l1":[["G",35.0,518],["R",710.0,513],["O",1380.0,518],["W",2055.0,600],["T",2812.0,470],["H",3439.0,500]],"l2":[["R2",35.0,513],["Y",705.0,327],["D",1189.0,500],["E",1846.0,480],["R2",2483.0,513],["S",3153.0,500]],"w1":3974,"w2":3688,"gry":[["G",35.0,518],["R",710.0,513],["Y",1380.0,327]],"wg":1742}, ctx = cv.getContext('2d'), reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var NAMES = ["TVS Apache", "Royal Enfield", "TVS Apache", "Royal Enfield Guerrilla 450", "Bagmane Tech Park", "TVS Apache", "Royal Enfield", "Axis Bank", "Royal Enfield Continental GT", "Royal Enfield", "Bagmane REIT, Milky Mist, GRY", "Royal Enfield Classic 350"];
  var INK = '#170e22', GOLD = '#F5B321', LG = 150, N = 12, FW = 960, FH = 540, P = {}, img = new Image();
  var W = 0, H = 0, dpr = 1, k = 1, SX = 0, SY = 0, wordW = 0, wordH = 511, items = [], t0 = 0, raf = 0, done = false, started = false;
  Object.keys(D.paths).forEach(function (n) { P[n] = new Path2D(D.paths[n]); });
  var TG = 1.1;
  var layer = document.createElement('canvas'), tmp = document.createElement('canvas'), lx = layer.getContext('2d'), tx = tmp.getContext('2d');
  function ease(x) { return x < 0 ? 0 : x > 1 ? 1 : x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
  function out(x) { return x < 0 ? 0 : x > 1 ? 1 : 1 - Math.pow(1 - x, 3); }
  function layout() {
    var r = hero.getBoundingClientRect(), box = hero.querySelector('.word-slot').getBoundingClientRect(), two = true, order = 0;
    dpr = Math.min(window.devicePixelRatio || 1, 2); W = r.width; H = r.height; cv.width = layer.width = tmp.width = Math.round(W * dpr); cv.height = layer.height = tmp.height = Math.round(H * dpr);
    items = [];
    if (two) { D.l1.forEach(function (l) { items.push({ n: l[0], x: l[1], y: 0, w: l[2] }); }); D.l2.forEach(function (l) { items.push({ n: l[0], x: l[1], y: 511 + LG, w: l[2] }); }); wordW = D.w1; wordH = 511 * 2 + LG; }
    else { D.full.forEach(function (l) { items.push({ n: l[0], x: l[1], y: 0, w: l[2] }); }); wordW = D.wf; wordH = 511; }
    items[0].logo = [D.gry[0][1], 0]; items[1].logo = [D.gry[1][1], 0]; items[7].logo = [D.gry[2][1], 0];
    items.forEach(function (it, i) { it.i = i; if (!it.logo) it.ord = order++; });
    k = box.width / wordW; SX = box.left - r.left; SY = box.top - r.top;
    hero.style.setProperty('--word-h', (wordH * k) + 'px');
    // the settled name: solid letters with a soft pearl-to-lilac sheen, drawn once and kept
    var z = dpr * k; lx.setTransform(1, 0, 0, 1, 0, 0); lx.clearRect(0, 0, layer.width, layer.height); lx.lineWidth = 70; lx.lineJoin = 'miter'; lx.miterLimit = 6;
    var depth = Math.max(3, Math.round(wordH * k * dpr * .028));
    for (var pass = 0; pass < 3; pass++) items.forEach(function (it) {
      var bx0 = dpr * SX + z * it.x, by0 = dpr * SY + z * it.y, g;
      if (pass === 0) { // the block behind the face: a short extrusion down and to the right
        for (var e = depth; e >= 1; e--) { lx.setTransform(z, 0, 0, z, bx0 + e * .55, by0 + e); lx.strokeStyle = e > depth * .6 ? '#241536' : '#3a2459'; lx.stroke(P[it.n]); }
        return;
      }
      lx.setTransform(z, 0, 0, z, bx0, by0); lx.save(); lx.beginPath(); lx.rect(-60, -40, it.w + 120, 560); lx.clip();
      if (pass === 1) { g = lx.createLinearGradient(0, 0, it.w, 511); g.addColorStop(0, '#ffffff'); g.addColorStop(.5, '#b9adcf'); g.addColorStop(1, '#7f7399'); lx.lineWidth = 70; lx.strokeStyle = g; lx.stroke(P[it.n]); }
      else { g = lx.createLinearGradient(0, 0, 0, 511); g.addColorStop(0, '#ffffff'); g.addColorStop(.42, '#f7f4fb'); g.addColorStop(.58, '#e6dff1'); g.addColorStop(1, '#d2c8e4'); lx.lineWidth = 52; lx.strokeStyle = g; lx.stroke(P[it.n]); }
      lx.restore();
    });
    lx.lineWidth = 70;
    lx.setTransform(1, 0, 0, 1, 0, 0); lx.globalCompositeOperation = 'source-over'; var it1 = items[1];
    lx.fillStyle = GOLD; lx.beginPath(); lx.arc(dpr * SX + z * it1.x, dpr * SY + z * (it1.y + 150), z * 36, 0, 6.2832); lx.fill();
  }
  function cover(c, ix, dx, dy, dw, dh) { // draw still number ix to fill a box
    var sw = FW, sh = FH, ar = dw / dh; if (ar > FW / FH) sh = FW / ar; else sw = FH * ar;
    c.drawImage(img, (ix % 4) * FW + (FW - sw) / 2, Math.floor(ix / 4) * FH + (FH - sh) / 2, sw, sh, dx, dy, dw, dh);
  }
  function rrect(c, x, y, w, h, r) { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }
  function settled(g) { // the finished name, with the glint sweeping across when g is between 0 and 1
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 1;
    if (g <= 0 || g >= 1) { ctx.drawImage(layer, 0, 0); return; }
    tx.setTransform(1, 0, 0, 1, 0, 0); tx.globalCompositeOperation = 'source-over'; tx.clearRect(0, 0, tmp.width, tmp.height); tx.drawImage(layer, 0, 0);
    var x0 = dpr * SX, ww = dpr * wordW * k, hh = dpr * wordH * k, bw = Math.max(90 * dpr, ww * .09), xc = x0 - bw * 2 + (ww + bw * 4) * ease(g);
    var gr = tx.createLinearGradient(xc - bw, 0, xc + bw, 0); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(.42, 'rgba(255,240,205,.55)'); gr.addColorStop(.5, 'rgba(255,255,255,1)'); gr.addColorStop(.58, 'rgba(255,240,205,.55)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
    tx.globalCompositeOperation = 'source-atop'; tx.fillStyle = gr; tx.setTransform(1, 0, -.42, 1, .42 * (dpr * SY + hh / 2), 0); tx.fillRect(xc - bw * 3, dpr * SY - 20, bw * 6, hh + 40);
    ctx.drawImage(tmp, 0, 0);
  }
  var TA = 0.95, TB = 0.45, STEP = 0.1, TP = 0.6, TD = 0.4, cue = false;
  function draw(t) {
    var a = (t - TA) / TB, b = ease(a), u = t - TA - TB, uEnd = 9 * STEP + .3, p = ease((u - .1) / (uEnd + TP - .35)), d = ease((u - uEnd - TP * .3) / TD), g = (u - uEnd - TP * .3 - TD * .6) / TG, phone = W < 700;
    cue = p > .92;
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 1; ctx.fillStyle = INK; ctx.fillRect(0, 0, cv.width, cv.height);
    if (d >= 1) { settled(g); return g >= 1; }
    // the screen is never empty: a brand shot sits faintly behind everything
    ctx.globalAlpha = .17 * (1 - d) * Math.min(1, t / .4); cover(ctx, Math.floor(t / .55 + 3) % N, 0, 0, cv.width, cv.height); ctx.globalAlpha = 1;
    // the card of brand shots, large
    var cin = out(t / .45), cw = Math.min(W * (phone ? .92 : .62), 1040) * (.92 + .08 * cin) * (1 + .35 * Math.max(0, Math.min(1, a / .3))), ch = phone ? cw * .82 : cw * 9 / 16, ca = cin * (1 - Math.min(1, Math.max(0, a) / .3)), cyy = H * .47;
    if (ca > 0) {
      ctx.save(); ctx.globalAlpha = ca; rrect(ctx, dpr * (W - cw) / 2, dpr * (cyy - ch / 2), dpr * cw, dpr * ch, dpr * 16); ctx.clip(); cover(ctx, Math.floor(t / .22) % N, dpr * (W - cw) / 2, dpr * (cyy - ch / 2), dpr * cw, dpr * ch); ctx.restore();
      ctx.globalAlpha = ca; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; var fs = Math.round((phone ? 17 : 20) * dpr);
      ctx.font = '600 ' + Math.round(fs * .78) + 'px Archivo, system-ui, sans-serif'; ctx.fillStyle = GOLD; ctx.fillText('Brands we have activated', dpr * W / 2, dpr * (cyy - ch / 2) - fs * 1.5);
      ctx.font = '700 ' + fs + 'px Archivo, system-ui, sans-serif'; ctx.fillStyle = '#fff'; ctx.fillText(NAMES[Math.floor(t / .22) % N], dpr * W / 2, dpr * (cyy + ch / 2) + fs * 1.7); ctx.globalAlpha = 1;
    }
    if (a <= 0) return false;
    // camera. First G R Y fills the screen. Then it stays close and follows each new letter. One pull-back at the end.
    var sG = Math.min((phone ? .9 : .62) * W / (D.wg * k), .42 * H / (511 * k)), sC = Math.max(sG * .8, (phone ? .2 : .34) * H / (511 * k));
    var m = ease(u / .7), fx = D.wg / 2, fy = 255, s = sG * (1.45 - .45 * b), q = u / STEP, j = Math.floor(q), fr = ease(q - j), arr = [], lastT;
    for (var i = 0; i < items.length; i++) if (!items[i].logo) arr[items[i].ord] = items[i];
    var ax = W / 2, ay = cyy;
    if (p > 0) { fx += (wordW / 2 - fx) * p; fy += (wordH / 2 - fy) * p; s += (1 - s) * p; ax += (SX + wordW * k / 2 - ax) * p; ay += (SY + wordH * k / 2 - ay) * p; }
    var z = dpr * s * k, dot = null, la = Math.min(1, a / .3);
    for (i = 0; i < items.length; i++) {
      var it = items[i], x = it.x, y = it.y, al = la, pop = 1;
      if (it.logo) { x = it.logo[0] + (it.x - it.logo[0]) * m; y = it.logo[1] + (it.y - it.logo[1]) * m; }
      else { var qq = (u - it.ord * STEP) / .32; if (qq <= 0) continue; al = Math.min(1, qq * 1.6); pop = .7 + .3 * out(qq); }
      var ox = dpr * ax + z * (x - fx), oy = dpr * ay + z * (y - fy), zz = z * pop, px = ox + z * it.w / 2 * (1 - pop), py = oy + z * 255 * (1 - pop);
      if (px > cv.width + 80 * zz || px + (it.w + 80) * zz < 0 || py > cv.height || py + 520 * zz < 0) { if (i === 1) dot = null; continue; }
      tx.setTransform(1, 0, 0, 1, 0, 0); tx.globalCompositeOperation = 'source-over'; var bx = Math.floor(px - 60 * zz), by = Math.floor(py - 4), bw2 = Math.ceil((it.w + 120) * zz), bh2 = Math.ceil(519 * zz);
      tx.clearRect(bx - 2, by - 2, bw2 + 4, bh2 + 4); tx.save(); tx.beginPath(); tx.rect(bx, py, bw2, 511 * zz); tx.clip();
      tx.setTransform(zz, 0, 0, zz, px, py); tx.lineWidth = 70; tx.lineJoin = 'miter'; tx.miterLimit = 6; tx.strokeStyle = '#fff'; tx.stroke(P[it.n]);
      tx.globalCompositeOperation = 'source-in'; cover(tx, (Math.floor((t + i * .09) / .3) + i * 5) % N, -45, -8, it.w + 90, 527); tx.restore();
      var vx = (dpr * W / 2 - (px + zz * it.w / 2)) * .012, vy = Math.max(2, zz * 9), dn = zz * 511 > 220 * dpr ? 7 : 4;
      ctx.globalAlpha = al * (1 - d); ctx.lineWidth = 70; ctx.lineJoin = 'miter'; ctx.miterLimit = 6;
      for (var e = dn; e >= 1; e--) { ctx.setTransform(zz, 0, 0, zz, px + vx * e, py + vy * e / dn * 1.6); ctx.strokeStyle = e > dn * .5 ? '#22132f' : '#3b2559'; ctx.stroke(P[it.n]); }
      ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(tmp, bx, by, bw2, bh2, bx, by, bw2, bh2);
      if (i === 1) dot = [px, py + zz * 150, zz * 36];
    }
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = la * (1 - d); if (dot) { ctx.fillStyle = GOLD; ctx.beginPath(); ctx.arc(dot[0], dot[1], dot[2], 0, 6.2832); ctx.fill(); }
    if (d > 0) { ctx.globalAlpha = d; ctx.drawImage(layer, 0, 0); } ctx.globalAlpha = 1; return false;
  }
  function finish() { done = true; cancelAnimationFrame(raf); draw(1e3); hero.classList.add('settled'); try { sessionStorage.setItem('gry-word', '1'); } catch (e) {} }
  function tick(now) { if (done) return; if (!t0) t0 = now; var fin = draw((now - t0) / 1000); if (cue && !hero.classList.contains('settled')) hero.classList.add('settled'); if (fin) return finish(); raf = requestAnimationFrame(tick); }
  // a second glint when the pointer comes to the name
  var gl0 = 0; function glint(now) { if (!gl0) gl0 = now; var g = (now - gl0) / (TG * 1000); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; ctx.fillStyle = INK; ctx.fillRect(0, 0, cv.width, cv.height); settled(g); if (g < 1) requestAnimationFrame(glint); else gl0 = 0; }
  hero.querySelector('.word-slot').addEventListener('pointerenter', function () { if (done && !gl0 && !reduce) requestAnimationFrame(glint); });
  var seen = false; try { seen = sessionStorage.getItem('gry-word') === '1'; } catch (e) {}
  function go() { if (started || done) return; started = true; raf = requestAnimationFrame(tick); }
  function boot() {
    layout();
    if (reduce || seen) return finish();
    draw(0);
    // wait for the logo intro (if it is playing) to hand over, then roll
    var body = document.body, introOn = document.documentElement.classList.contains('intro-on');
    if (!introOn) return setTimeout(go, 250);
    var mo = new MutationObserver(function () { if (!document.documentElement.classList.contains('intro-on')) { mo.disconnect(); setTimeout(go, 150); } });
    mo.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] }); setTimeout(go, 6000);
  }
  img.onload = function () { if (document.fonts && document.fonts.ready) document.fonts.ready.then(boot); else boot(); };
  img.onerror = function () { layout(); P && finish(); };
  img.src = cv.getAttribute('data-src');
  var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { if (!img.complete) return; layout(); if (done) draw(1e3); }, 120); });
  hero.addEventListener('click', function (e) { if (started && !done && !e.target.closest('a,button')) finish(); });
  window.addEventListener('scroll', function () { if (started && !done && window.scrollY > 40) finish(); }, { passive: true });
})();
