/* Schematic quadrat renderer.
   Parses a Unicode Egyptian hieroglyphic string (joiners, segments, insertion,
   overlay, mirror, rotation selectors, damage marks) into operator trees,
   then lays each tree out in SVG using one glyph per sign from
   Noto Sans Egyptian Hieroglyphs. Noto has no quadrat shaping of its own,
   so the layout here is ours and only approximate. Text is drawn left to right. */
(function () {
  var VJ = 0x13430, HJ = 0x13431, BS = 0x13437, ES = 0x13438, OV = 0x13436, MIR = 0x13440;
  var INS = { 0x13432: 'ts', 0x13433: 'bs', 0x13434: 'te', 0x13435: 'be', 0x13439: 'm', 0x1343A: 't', 0x1343B: 'b' };
  function isSign(c) { return (c >= 0x13000 && c <= 0x1342F) || (c >= 0x13460 && c <= 0x143FF) || (c >= 0x13441 && c <= 0x13446); }
  function parse(str) {
    var s = Array.from(str).map(function (ch) { return ch.codePointAt(0); }), i = 0;
    function peek() { return s[i]; }
    function take(w) { if (w !== undefined && s[i] !== w) throw new Error('bad quadrat at ' + i); return s[i++]; }
    function vgroup() { var a = [hgroup()]; while (peek() === VJ) { take(); a.push(hgroup()); } return a.length === 1 ? a[0] : { op: 'ver', args: a }; }
    function hgroup() { var a = [hsub()]; while (peek() === HJ) { take(); a.push(hsub()); } return a.length === 1 ? a[0] : { op: 'hor', args: a }; }
    function hsub() {
      if (peek() === BS) { take(); var g = vgroup(); take(ES); if (peek() === OV) { take(); g = { op: 'ovl', args: [g, flat()] }; } return ins(g); }
      return ins(core());
    }
    function ins(base) {
      var pos = [], args = [base];
      while (INS[peek()]) { pos.push(INS[take()]); args.push(ingroup()); }
      return pos.length ? { op: 'ins', pos: pos, args: args } : base;
    }
    function ingroup() { if (peek() === BS) { take(); var g = vgroup(); take(ES); return g; } return core(); }
    function core() { var a = lit(); if (peek() === OV) { take(); return { op: 'ovl', args: [a, flat()] }; } return a; }
    function flat() { if (peek() === BS) { take(); var g = vgroup(); take(ES); return g; } return lit(); }
    function lit() {
      var c = peek(); if (c === undefined || !isSign(c)) throw new Error('expected sign at ' + i);
      take(); var leaf = { sign: c };
      if (peek() >= 0xFE00 && peek() <= 0xFE06) leaf.rot = take() - 0xFE00 + 1;
      if (peek() === MIR) { take(); leaf.mirror = true; }
      if (peek() >= 0x13447 && peek() <= 0x13455) leaf.damage = take();
      return leaf;
    }
    var out = []; while (i < s.length) out.push(vgroup()); return out;
  }

  var ctx = document.createElement('canvas').getContext('2d'), cache = {};
  var FONT = '100px "Noto Sans Egyptian Hieroglyphs"';
  function measure(c) {
    if (cache[c]) return cache[c];
    var r;
    if (c >= 0x13460) r = { w: 0.7, h: 0.7, miss: true };          // Extended-A: not in Noto
    else {
      ctx.font = FONT; var m = ctx.measureText(String.fromCodePoint(c));
      var l = m.actualBoundingBoxLeft || 0, rr = m.actualBoundingBoxRight || m.width, a = m.actualBoundingBoxAscent || 80, d = m.actualBoundingBoxDescent || 0;
      r = { w: Math.max((l + rr) / 100, 0.05), h: Math.max((a + d) / 100, 0.05), l: l / 100, a: a / 100 };
    }
    return (cache[c] = r);
  }
  var GAP = 0.06;
  /* Each layout returns {w, h, draw(out, x, y, s)}. */
  function layout(n) {
    if (n.sign !== undefined) {
      var m = measure(n.sign);
      var w = m.w, h = m.h;
      if (n.rot === 1 || n.rot === 3) { w = m.h; h = m.w; }
      return { w: w, h: h, draw: function (o, x, y, s) {
        if (m.miss) {
          o.push('<rect class="miss" x="' + f(x) + '" y="' + f(y) + '" width="' + f(w * s) + '" height="' + f(h * s) + '"/>');
          o.push('<text class="misslabel" x="' + f(x + w * s / 2) + '" y="' + f(y + h * s / 2) + '" font-size="' + f(s * 0.16) + '" text-anchor="middle" dominant-baseline="middle">' + n.sign.toString(16).toUpperCase() + '</text>');
          return;
        }
        var cx = x + w * s / 2, cy = y + h * s / 2, tf = [];
        if (n.mirror) tf.push('translate(' + f(cx) + ' ' + f(cy) + ') scale(-1 1) translate(' + f(-cx) + ' ' + f(-cy) + ')');
        if (n.rot) tf.push('rotate(' + (90 * n.rot) + ' ' + f(cx) + ' ' + f(cy) + ')');
        var gx = cx - m.w * s / 2 + m.l * s, gy = cy - m.h * s / 2 + m.a * s;
        o.push('<text x="' + f(gx) + '" y="' + f(gy) + '" font-size="' + f(s) + '"' + (tf.length ? ' transform="' + tf.join(' ') + '"' : '') + '>' + String.fromCodePoint(n.sign) + '</text>');
      } };
    }
    var kids = n.args.map(layout);
    if (n.op === 'ver') {
      var W = Math.max.apply(null, kids.map(function (k) { return k.w; }));
      var H = kids.reduce(function (t, k) { return t + k.h; }, 0) + GAP * (kids.length - 1);
      return { w: W, h: H, draw: function (o, x, y, s) { var yy = y; kids.forEach(function (k) { k.draw(o, x + (W - k.w) * s / 2, yy, s); yy += (k.h + GAP) * s; }); } };
    }
    if (n.op === 'hor') {
      var H2 = Math.max.apply(null, kids.map(function (k) { return k.h; }));
      var W2 = kids.reduce(function (t, k) { return t + k.w; }, 0) + GAP * (kids.length - 1);
      return { w: W2, h: H2, draw: function (o, x, y, s) { var xx = x; kids.forEach(function (k) { k.draw(o, xx, y + (H2 - k.h) * s / 2, s); xx += (k.w + GAP) * s; }); } };
    }
    if (n.op === 'ovl') {
      var W3 = Math.max(kids[0].w, kids[1].w), H3 = Math.max(kids[0].h, kids[1].h);
      return { w: W3, h: H3, draw: function (o, x, y, s) { kids.forEach(function (k) { k.draw(o, x + (W3 - k.w) * s / 2, y + (H3 - k.h) * s / 2, s); }); } };
    }
    /* insertion: inserted groups shrink to fit about half of the base box */
    var B = kids[0];
    return { w: B.w, h: B.h, draw: function (o, x, y, s) {
      B.draw(o, x, y, s);
      n.pos.forEach(function (p, j) {
        var k = kids[j + 1], sc = Math.min(0.48 * B.w / k.w, 0.48 * B.h / k.h, 1) * s;
        var kw = k.w * sc, kh = k.h * sc, bw = B.w * s, bh = B.h * s;
        var px = p.indexOf('s') >= 0 && p !== 'm' ? x : (p.indexOf('e') >= 0 ? x + bw - kw : x + (bw - kw) / 2);
        var py = p.charAt(0) === 't' ? y : (p.charAt(0) === 'b' ? y + bh - kh : y + (bh - kh) / 2);
        k.draw(o, px, py, sc);
      });
    } };
  }
  function f(v) { return Math.round(v * 100) / 100; }
  function svgFor(tree, em) {
    var L = layout(tree), s = 1 / Math.max(L.w, L.h, 0.9), o = [];  /* floor keeps small single signs at natural size */
    L.draw(o, (1 - L.w * s) / 2 * 100, (1 - L.h * s) / 2 * 100, s * 100);
    return '<svg class="q" viewBox="0 0 100 100" width="' + em + '" height="' + em + '" role="img">' + o.join('') + '</svg>';
  }
  function render(el) {
    var str = el.getAttribute('data-q') || el.textContent.trim(), em = el.getAttribute('data-size') || '3em';
    try {
      var trees = parse(str);
      el.innerHTML = trees.map(function (t) { return svgFor(t, em); }).join('');
      el.setAttribute('aria-label', str);
    } catch (e) { el.textContent = str; }
  }
  window.HOQuadrat = { parse: parse, render: render, svgFor: svgFor };
  function go() { document.querySelectorAll('[data-q]').forEach(render); document.dispatchEvent(new Event('ho-quadrat-ready')); }
  document.addEventListener('DOMContentLoaded', function () {
    if (document.fonts && document.fonts.load) document.fonts.load(FONT, '\u{13000}').then(go, go); else go();
  });
})();
