// Growthryders — opening: the film plays full screen, the camera pulls back to show it inside G R Y,
// then the missing letters arrive and the mark becomes the full name. Drawn on one canvas above the video.
(function () {
  var hero = document.querySelector('.hero-word'), cv = hero && hero.querySelector('.word-veil'); if (!cv) return;
  var D = {"paths":{"G":["M288 260H518V475H55Q0 475 0 420V95Q0 40 55 40H518"],"R":["M0 475V260H393A110 110 0 0 0 393 40H0","M273 262L506 511"],"R2":["M0 475V40H393A110 110 0 0 1 393 260H0","M273 262L506 511"],"O":["M55 40H463Q518 40 518 95V420Q518 475 463 475H55Q0 475 0 420V95Q0 40 55 40Z"],"W":["M0 40V420Q0 475 55 475H545Q600 475 600 420V40","M300 475V150"],"T":["M0 40H470","M235 40V475"],"H":["M0 40V475","M500 40V475","M0 258H500"],"Y":["M0 118L177 268V475","M327 38V88Q327 128 294 158L177 268"],"D":["M0 40H282A217.5 217.5 0 0 1 282 475H0Z"],"E":["M480 40H55Q0 40 0 95V420Q0 475 55 475H480","M0 258H400"],"S":["M500 40H55Q0 40 0 95V203Q0 258 55 258H445Q500 258 500 313V420Q500 475 445 475H0"]},"l1":[["G",35.0],["R",710.0],["O",1380.0],["W",2055.0],["T",2812.0],["H",3439.0]],"l2":[["R2",35.0],["Y",705.0],["D",1189.0],["E",1846.0],["R2",2483.0],["S",3153.0]],"w1":3974,"w2":3688,"gry":[["G",35.0],["R",710.0],["Y",1380.0]],"wg":1742}, ctx = cv.getContext('2d'), reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var INK = '#170e22', GOLD = '#F5B321', LG = 150, P2 = {}, W = 0, H = 0, dpr = 1, k = 1, X0 = 0, Y0 = 0, t0 = 0, done = false, raf = 0;
  Object.keys(D.paths).forEach(function (n) { P2[n] = [new Path2D(D.paths[n].join(' '))]; });
  // each letter: final place (line, x) and, for G R Y, where it sits in the compact logo
  var items = [];
  D.l1.forEach(function (l, i) { items.push({ n: l[0], fx: l[1], fy: 0, i: i }); });
  D.l2.forEach(function (l, i) { items.push({ n: l[0], fx: l[1], fy: 511 + LG, i: 6 + i }); });
  items[0].logo = [D.gry[0][1], 0]; items[1].logo = [D.gry[1][1], 0]; items[7].logo = [D.gry[2][1], 0]; items[7].n0 = 'Y';
  function ease(x) { return x < 0 ? 0 : x > 1 ? 1 : x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
  function fit() {
    var r = hero.getBoundingClientRect(); dpr = Math.min(window.devicePixelRatio || 1, 2); W = r.width; H = r.height;
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    var box = hero.querySelector('.word-slot').getBoundingClientRect();
    k = box.width / D.w1; X0 = box.left - r.left; Y0 = box.top - r.top;
    hero.style.setProperty('--word-h', ((511 * 2 + LG) * k) + 'px');
  }
  function draw(p) { // p: 0 film only -> 1 name complete
    var a = ease(p / .42), b = ease((p - .42) / .58);
    var S1 = Math.min(.62 * W / (D.wg * k), .5 * H / (511 * k)), S0 = S1 * 7, s = b > 0 ? S1 + (1 - S1) * b : S0 + (S1 - S0) * a;
    var fgx = X0 + D.wg * k / 2, fgy = Y0 + 255 * k, px = W / 2, py = H / 2;
    var Fx = fgx + (px - fgx) * b, Fy = fgy + (py - fgy) * b, Cx = W / 2, Cy = H / 2;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.globalCompositeOperation = 'source-over'; ctx.clearRect(0, 0, W, H);
    ctx.globalAlpha = Math.min(1, p / .16); ctx.fillStyle = INK; ctx.fillRect(0, 0, W, H); ctx.globalAlpha = 1;
    var m = [dpr * s * k, 0, 0, dpr * s * k, dpr * (Cx + s * (X0 - Fx)), dpr * (Cy + s * (Y0 - Fy))], dot = null;
    ctx.globalCompositeOperation = 'destination-out'; ctx.lineWidth = 70; ctx.lineJoin = 'miter'; ctx.miterLimit = 6;
    for (var i = 0; i < items.length; i++) {
      var it = items[i], x = it.fx, y = it.fy, al = 1;
      if (it.logo) { x = it.logo[0] + (it.fx - it.logo[0]) * b; y = it.logo[1] + (it.fy - it.logo[1]) * b; }
      else { al = ease((b - .18 - (it.i % 6) * .045) / .5); if (al <= 0) continue; y += (1 - al) * 60; }
      ctx.setTransform(m[0], 0, 0, m[3], m[4] + m[0] * x, m[5] + m[3] * y);
      ctx.save(); ctx.beginPath(); ctx.rect(-60, 0, 800, 511); ctx.clip(); ctx.globalAlpha = al;
      var ps = P2[it.n]; for (var j = 0; j < ps.length; j++) ctx.stroke(ps[j]);
      if (b > 0) { ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = al * .36 * b; ctx.strokeStyle = '#fff'; for (j = 0; j < ps.length; j++) ctx.stroke(ps[j]); ctx.globalCompositeOperation = 'destination-out'; ctx.strokeStyle = '#000'; }
      ctx.restore(); if (i === 1) dot = [m[4] + m[0] * x, m[5] + m[3] * (y + 150), m[0] * 36];
    }
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = Math.min(1, p / .16);
    if (dot) { ctx.fillStyle = GOLD; ctx.beginPath(); ctx.arc(dot[0], dot[1], dot[2], 0, 6.2832); ctx.fill(); } ctx.globalAlpha = 1;
  }
  function finish() { done = true; draw(1); hero.classList.add('settled'); try { sessionStorage.setItem('gry-word', '1'); } catch (e) {} }
  function play(t) { if (!t0) t0 = t; var el = (t - t0) / 1000, p = el < 1.5 ? 0 : (el - 1.5) / 3.3; if (p >= 1) return finish(); draw(p); raf = requestAnimationFrame(play); }
  var seen = false; try { seen = sessionStorage.getItem('gry-word') === '1'; } catch (e) {}
  function start() { fit(); if (reduce || seen) finish(); else { draw(0); raf = requestAnimationFrame(play); } }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(start); else start();
  var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { fit(); if (done) draw(1); }, 120); });
  hero.addEventListener('click', function (e) { if (!done && !e.target.closest('a,button')) { cancelAnimationFrame(raf); finish(); } });
})();
