#!/usr/bin/env python3
"""Version 18: Patches auf Version 17 (work/v17.html -> work/v18.html). Jede Ersetzung muss genau einmal treffen."""
import sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text(encoding='utf-8')
out = pathlib.Path(sys.argv[2])

def rep(old, new, count=1):
    global src
    n = src.count(old)
    if n != count:
        raise SystemExit('Treffer %d statt %d fuer: %s' % (n, count, old[:100]))
    src = src.replace(old, new)

def cut(start, end, keep_end=True):
    """entfernt von start (inkl.) bis end (exkl.)"""
    global src
    i = src.index(start); j = src.index(end, i)
    assert src.count(start) == 1
    src = src[:i] + src[j:]

# 1) Versionsnotiz
rep('/* Version 17 (26.10.2026, abends): ',
    '/* Version 18 (26.10.2026, abends): Zusammenhänge beim Darüberfahren weg (zu unruhig); die Karte in zwei Stilen zur Wahl: Rosette nach Llulls Figura A (Messingring, Münzen, Bänder vom Geber zum Nehmer, in der Mitte die Zahl römisch und das Motto „Omnes viae Romam ducunt“) und Arkaden (Säulen in einer Reihe, Bögen darüber), gemerkt in meta/karte; Takt für jeden Bereich: ein Rhythmus gehört zu einem beliebigen Bereich, „Takt heute“ legt neue an, Bereiche ohne Takt-Muster zeigen ihre Rhythmen als Zeile unter dem Inhalt. Version 17 (26.10.2026, abends): ')

# 2) Hover-Zusammenhaenge raus: CSS
cut('/* Zusammenhänge (Version 16): beim Halten oder Darüberfahren leuchten die Projekte, an die eines liefert */\n',
    '.r-main{flex:1;min-width:0;')
# JS: linkSet/applyLinkHi/Hover
cut('/* Zusammenhänge sichtbar machen (Version 16): liefert an → und bekommt von ←; am Rechner beim Darüberfahren, am Handy aus der Projektansicht */\n',
    'function rowHTML(p, t, ctx){')
rep("  const H = S.linkHi, hiL = H && H.from === p.id, hiT = H && H.to.includes(p.id), hiI = H && H.inn.includes(p.id), lo = H && !hiL && !hiT && !hiI;\n  return '<div class=\"row ctx-' + ctx + (dim ? ' dim' : '') + (lo ? ' lo' : '') + (start ? ' start' : '') + (hiL ? ' hi-from' : hiT ? ' hi-to' : hiI ? ' hi-in' : '') + '\" data-pid=\"'",
    "  return '<div class=\"row ctx-' + ctx + (dim ? ' dim' : '') + (start ? ' start' : '') + '\" data-pid=\"'")
rep("  if (S.linkHi && !S.linkHi.hover) setLinkHi(null);\n", "")
rep("  wrOpen: false, linkHi: null, memo: null, karteSel: null\n};", "  wrOpen: false, memo: null, karteSel: null\n};")

# 3) CSS der Karte neu
cut('/* Version 17: Karte der Zusammenhänge (Schublade), Befehle in der Suche, Buchrücken lang drücken */\n',
    '.su-ic{width:28px;height:28px;')
rep('.su-ic{width:28px;height:28px;',
'''/* Version 17/18: Karte der Zusammenhänge (Schublade) in zwei Stilen: Rosette (Ring, Münzen, Bänder) und Arkaden (Säulen, Bögen) */
.km{display:flex;flex-direction:column;gap:12px}
.km svg{display:block;width:100%;height:auto;overflow:visible}
.km-stil{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:8px 12px}
.km-stil .hint{margin:0;flex:1 1 220px}
.km-rb{fill:var(--c);opacity:.3;transition:opacity .15s ease}
.km.sel .km-rb{opacity:.06}
.km.sel .km-rb.on{opacity:.82}
.km-ring{fill:none;stroke:var(--gold-deep);stroke-width:2;opacity:.7}
.km-ring2{fill:none;stroke:var(--gold);stroke-width:.8;opacity:.45}
.km-arc{fill:none;stroke:var(--c);stroke-width:7;stroke-linecap:round;opacity:.45}
.km-num{font-family:var(--font-inscr);font-weight:700;fill:var(--gold-deep);text-anchor:middle}
.km-mot{font-family:var(--font-inscr);font-weight:600;letter-spacing:.16em;fill:var(--gold-deep);paint-order:stroke;stroke:var(--surface);stroke-width:2.5px;stroke-linejoin:round}
.km-n{cursor:pointer;outline:none}
.km-n circle.hit{fill:transparent;stroke:none}
.km-n circle.d{fill:var(--c);stroke:var(--gold);stroke-width:1.6;transition:stroke .15s ease}
.km-n.idle circle.d{fill:var(--surface);stroke:var(--c);stroke-width:1.8}
.km-n.crit circle.d{fill:var(--desat)}
.km-n.goal circle.d{fill:var(--gold);stroke:var(--gold-deep)}
.km-n text{font-family:var(--font-body);font-size:13px;font-weight:600;fill:var(--ink);paint-order:stroke;stroke:var(--surface);stroke-width:3.5px;stroke-linejoin:round}
.km.narrow .km-n text{font-size:15px;stroke-width:4px}
.km-n.lo{opacity:.28}
.km-n.on circle.d{stroke:var(--ink);stroke-width:2.5}
.km-n:hover text,.km-n:focus-visible text{fill:var(--c)}
.km-n:focus-visible circle.d{stroke:var(--accent);stroke-width:3}
/* Arkaden */
.km-col{fill:var(--c);transition:fill .15s ease}
.km-n.crit .km-col{fill:var(--desat)}
.km-n.idle .km-col{fill:var(--surface);stroke:var(--c);stroke-width:1.2}
.km-n.goal .km-col{fill:var(--gold)}
.km-n.on .km-col{stroke:var(--ink);stroke-width:1.5}
.km-n:focus-visible .km-col{stroke:var(--accent);stroke-width:2}
.km-base{fill:none;stroke:var(--line-strong);stroke-width:1.5}
.km-arch{fill:none;stroke:var(--c);stroke-width:2;stroke-linecap:round;opacity:.72;transition:opacity .15s ease}
.km-a{fill:var(--c);opacity:.85;transition:opacity .15s ease}
.km.sel .km-arch,.km.sel .km-a{opacity:.1}
.km.sel .km-arch.on,.km.sel .km-a.on{opacity:1}
.km-n text.rot{font-size:12px;font-weight:500}
.km.narrow .km-n text.rot{font-size:13.5px}
@media (prefers-reduced-motion:reduce){ .km-rb,.km-arch,.km-a,.km-n circle.d,.km-col{transition:none} }
.su-ic{width:28px;height:28px;''')
rep("@media (prefers-reduced-motion:reduce){ .km-e,.km-a,.km-n circle.d{transition:none} }\n", "")

# 4) Karte: Bausteine neu
i = src.index('function karteView(){'); j = src.index('function bereicheView(){')
src = src[:i] + '''/* Stil der Karte (meta/karte): rosette | arkaden; gemerkt auf jedem Gerät gleich */
const KM_STILE = { rosette: 'Rosette', arkaden: 'Arkaden' };
function karteStil(){ const m = (S.meta || []).find(x => x && x.id === 'karte'); return m && KM_STILE[m.stil] ? m.stil : 'rosette'; }
async function saveKarteStil(stil){
  if (!KM_STILE[stil]) return;
  const prev = S.meta;
  S.meta = (S.meta || []).filter(x => x.id !== 'karte').concat([{ id: 'karte', stil }]);
  renderDrawer(true);
  try { await write(() => S.db.doc('meta/karte').set({ stil, updatedAt: today() })); }
  catch(e){ S.meta = prev; renderDrawer(true); }
}
/* Motto in der Mitte der Rosette: belegt als mittelalterliche Sentenz (Alanus ab Insulis, Liber parabolarum, um 1175: „mille viae ducunt homines per saecula Romam“) */
const KM_MOTTO = { caps: 'OMNES · VIAE · ROMAM · DVCVNT', de: 'Alle Wege führen nach Rom.', src: 'nach Alanus ab Insulis, Liber parabolarum, um 1175' };
function karteNodes(links){
  const ids = new Set(); links.forEach(l => { ids.add(l.from); ids.add(l.to); });
  return S.projects.filter(p => ids.has(p.id)).sort((a, b) => { const x = areaOf(a), y = areaOf(b); return ((x ? areaOrd(x) : 1e9) - (y ? areaOrd(y) : 1e9)) || byOrder(a, b); });
}
function karteNodeCls(p, t, sel, links){
  const h = health(p, t), mi = msInfo(p);
  const rel = sel ? (p.id === sel ? 'on' : (links.some(l => (l.from === sel && l.to === p.id) || (l.to === sel && l.from === p.id)) ? '' : 'lo')) : '';
  return 'km-n' + (rel ? ' ' + rel : '') + (isComplete(p, mi) ? ' goal' : p.status === 'idee' ? ' idle' : h.lvl === 'crit' ? ' crit' : '');
}
function karteNodeOpen(p, t, sel, links){
  const h = health(p, t);
  return '<g class="' + karteNodeCls(p, t, sel, links) + '" data-act="karte-pick" data-id="' + esc(p.id) + '" tabindex="0" role="button" aria-label="' + esc(p.name + ', ' + h.label + (sel === p.id ? ', hervorgehoben; noch ein Tipp öffnet das Projekt' : '')) + '" style="--c:' + colorOf(p) + '">';
}
/* Rosette: Ring mit Bereichsbögen, Münzen auf dem Ring, Bänder vom Geber (breit) zum Nehmer (Spitze); am Handy ein hochkant stehendes Oval */
function karteRosette(nodes, links, sel, t, narrow){
  const cx = 230, RX = 150, RY = narrow ? 235 : 150, cy = narrow ? 265 : 200, HT = narrow ? 545 : 395, NR = narrow ? 13 : 10, FS = narrow ? 15 : 13;
  const f = v => v.toFixed(1);
  const ang = new Map(); nodes.forEach((p, i) => ang.set(p.id, -Math.PI / 2 + i * 2 * Math.PI / nodes.length));
  const pt = (a, dr) => ({ x: cx + (RX - (dr || 0)) * Math.cos(a), y: cy + (RY - (dr || 0)) * Math.sin(a) });
  /* Bereichsbögen auf dem Ring */
  let arcs = '';
  let g0 = 0;
  for (let i = 1; i <= nodes.length; i++){
    const same = i < nodes.length && (areaOf(nodes[i]) || {}).id === (areaOf(nodes[g0]) || {}).id;
    if (!same){
      const a = areaOf(nodes[g0]);
      const a0 = ang.get(nodes[g0].id) - 0.09, a1 = ang.get(nodes[i - 1].id) + 0.09, A = pt(a0), B = pt(a1);
      arcs += '<path class="km-arc" style="--c:' + (a && a.color ? cvar(a.color) : 'var(--faint)') + '" d="M' + f(A.x) + ' ' + f(A.y) + 'A' + RX + ' ' + RY + ' 0 ' + (a1 - a0 > Math.PI ? 1 : 0) + ' 1 ' + f(B.x) + ' ' + f(B.y) + '"><title>' + esc(a ? a.name : 'Ohne Bereich') + '</title></path>';
      g0 = i;
    }
  }
  /* Bänder */
  const half = (NR * 0.95) / ((RX + RY) / 2);
  let ribbons = '';
  links.forEach(l => {
    const aA = ang.get(l.from), aB = ang.get(l.to); if (aA == null || aB == null) return;
    const A1 = pt(aA - half, NR), A2 = pt(aA + half, NR), B = pt(aB, NR + 2), A = pt(aA, NR);
    const mx = (A.x + B.x) / 2, my = (A.y + B.y) / 2;
    const dx = B.x - A.x, dy = B.y - A.y, len = Math.hypot(dx, dy) || 1, px = -dy / len, py = dx / len;
    const k = 0.55 + 0.25 * (1 - len / (RX + RY));
    const Cx = mx + (cx - mx) * k + px * 10, Cy = my + (cy - my) * k + py * 10;
    const on = sel && (l.from === sel || l.to === sel);
    const p = projById(l.from);
    ribbons += '<path class="km-rb' + (on ? ' on' : '') + '" style="--c:' + colorOf(p) + '" d="M' + f(A1.x) + ' ' + f(A1.y) + 'Q' + f(Cx) + ' ' + f(Cy) + ' ' + f(B.x) + ' ' + f(B.y) + 'Q' + f(Cx) + ' ' + f(Cy) + ' ' + f(A2.x) + ' ' + f(A2.y) + 'Z"><title>' + esc(p.name + ' → ' + projById(l.to).name + (l.label ? ' · ' + l.label : '')) + '</title></path>';
  });
  /* Münzen und Namen */
  let dots = '', minX = 0, maxX = 460;
  nodes.forEach((p, i) => {
    const a = ang.get(p.id), P = pt(a);
    const above = (i % 2 === 0) !== (Math.cos(a) < -0.2);
    const lx = P.x, ly = above ? P.y - NR - 7 : P.y + NR + 7 + FS * 0.8;
    const w = measure(p.name) * FS / 12.5 * 1.15;
    minX = Math.min(minX, lx - w / 2 - 10); maxX = Math.max(maxX, lx + w / 2 + 10);
    dots += karteNodeOpen(p, t, sel, links) + '<circle class="hit" cx="' + f(P.x) + '" cy="' + f(P.y) + '" r="' + (NR + 12) + '"/><circle class="d" cx="' + f(P.x) + '" cy="' + f(P.y) + '" r="' + NR + '"/><text x="' + f(lx) + '" y="' + f(ly) + '" text-anchor="middle">' + esc(p.name) + '</text></g>';
  });
  /* Zahl in der Mitte, das Motto als Inschrift am unteren Innenrand des Rings (wie auf einer Münze) */
  const M0 = pt(2.705, 17), M1 = pt(0.436, 17);
  const num = '<text class="km-num" x="' + cx + '" y="' + (cy + 10) + '" font-size="' + (narrow ? 34 : 28) + '">' + roman(links.length) + '</text>' +
    '<defs><path id="kmMot" d="M' + f(M0.x) + ' ' + f(M0.y) + 'A' + (RX - 17) + ' ' + (RY - 17) + ' 0 0 0 ' + f(M1.x) + ' ' + f(M1.y) + '"/></defs>' +
    '<text class="km-mot" font-size="' + (narrow ? 10 : 8) + '"><title>' + esc('„' + KM_MOTTO.de + '“ · ' + KM_MOTTO.src) + '</title><textPath href="#kmMot" startOffset="50%" text-anchor="middle">' + esc(KM_MOTTO.caps) + '</textPath></text>';
  const ring = '<ellipse class="km-ring" cx="' + cx + '" cy="' + cy + '" rx="' + RX + '" ry="' + RY + '"/><ellipse class="km-ring2" cx="' + cx + '" cy="' + cy + '" rx="' + (RX - 5) + '" ry="' + (RY - 5) + '"/>';
  return '<svg viewBox="' + f(minX) + ' 10 ' + f(maxX - minX) + ' ' + HT + '" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Rosette: ' + nodes.length + ' Projekte, ' + links.length + ' Verbindungen">' + ring + arcs + ribbons + num + dots + '</svg>';
}
/* Arkaden: Säulen in einer Reihe (nach Bereich), Bögen darüber vom Geber zum Nehmer, Pfeil am Ziel; Hin- und Rückweg mit zwei Bögen */
function karteArkaden(nodes, links, sel, t, narrow){
  const n = nodes.length, x0 = 44, x1 = 416, base = 250, top = base - 30;
  const f = v => v.toFixed(1);
  const xs = new Map(); nodes.forEach((p, i) => xs.set(p.id, n > 1 ? x0 + i * (x1 - x0) / (n - 1) : 230));
  const rev = new Set(links.map(l => l.to + '>' + l.from));
  let arcs = '';
  links.forEach(l => {
    const xa = xs.get(l.from), xb = xs.get(l.to); if (xa == null || xb == null) return;
    const r = Math.abs(xb - xa) / 2, ry = rev.has(l.from + '>' + l.to) && xa > xb ? Math.max(10, r - 8) : r;
    const on = sel && (l.from === sel || l.to === sel);
    const p = projById(l.from);
    const head = 'M' + f(xb) + ' ' + (top - 1) + 'L' + f(xb - 4) + ' ' + (top - 10) + 'L' + f(xb + 4) + ' ' + (top - 10) + 'Z';
    arcs += '<g style="--c:' + colorOf(p) + '"><title>' + esc(p.name + ' → ' + projById(l.to).name + (l.label ? ' · ' + l.label : '')) + '</title><path class="km-arch' + (on ? ' on' : '') + '" d="M' + f(xa) + ' ' + (top - 4) + 'A' + f(r) + ' ' + f(ry) + ' 0 0 ' + (xb > xa ? 1 : 0) + ' ' + f(xb) + ' ' + (top - 4) + '"/><path class="km-a' + (on ? ' on' : '') + '" d="' + head + '"/></g>';
  });
  let cols = '';
  nodes.forEach(p => {
    const x = xs.get(p.id);
    cols += karteNodeOpen(p, t, sel, links) + '<circle class="hit" cx="' + f(x) + '" cy="' + (base - 14) + '" r="22"/>' +
      '<rect class="km-col" x="' + f(x - 7) + '" y="' + (base - 30) + '" width="14" height="4" rx="1"/><rect class="km-col" x="' + f(x - 3.5) + '" y="' + (base - 26) + '" width="7" height="26"/><rect class="km-col" x="' + f(x - 7) + '" y="' + base + '" width="14" height="3.5" rx="1"/>' +
      '<text class="rot" x="' + f(x + 4) + '" y="' + (base + 18) + '" transform="rotate(42 ' + f(x + 4) + ' ' + (base + 18) + ')" text-anchor="start">' + esc(p.name) + '</text></g>';
  });
  const line = '<line class="km-base" x1="20" y1="' + (base + 5) + '" x2="440" y2="' + (base + 5) + '"/>';
  return '<svg viewBox="0 0 460 ' + (narrow ? 430 : 410) + '" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Arkaden: ' + nodes.length + ' Projekte, ' + links.length + ' Verbindungen">' + arcs + line + cols + '</svg>';
}
function karteView(){
  const t = today(), links = karteLinks(), nodes = karteNodes(links), stil = karteStil();
  const top = '<div class="dr-top"><div class="dr-title"><p class="eyebrow">Zusammenhänge</p><h2 id="drTitle" tabindex="-1">' + links.length + (links.length === 1 ? ' Verbindung' : ' Verbindungen') + '</h2></div>' + closeBtn() + '</div>';
  if (!nodes.length) return top + '<p class="none">Noch keine Verbindungen. Über „Bearbeiten“ im Projekt festlegen, an welche Projekte es liefert.</p>';
  const ids = new Set(nodes.map(p => p.id));
  const sel = S.karteSel && ids.has(S.karteSel) ? S.karteSel : null;
  const narrow = !!(window.matchMedia && matchMedia('(max-width:640px)').matches);
  const svg = stil === 'arkaden' ? karteArkaden(nodes, links, sel, t, narrow) : karteRosette(nodes, links, sel, t, narrow);
  const seg = '<div class="seg-ctl" role="group" aria-label="Darstellung">' + Object.keys(KM_STILE).map(k => '<button type="button" data-act="karte-stil" data-v="' + k + '" aria-pressed="' + (k === stil) + '">' + KM_STILE[k] + '</button>').join('') + '</div>';
  const hint = stil === 'arkaden' ? 'Bögen führen vom Geber zum Pfeil am Nehmer. Ein Tipp auf eine Säule hebt ihre Bögen hervor, noch ein Tipp öffnet das Projekt.' : 'Bänder laufen breit vom Geber zur Spitze beim Nehmer. Ein Tipp auf eine Münze hebt ihre Bänder hervor, noch ein Tipp öffnet das Projekt.';
  let below;
  if (sel){
    const p = projById(sel);
    below = '<section class="dr-sec"><h3><span class="ar-h" style="--c:' + colorOf(p) + '"><i class="dot" style="width:9px;height:9px;border-radius:50%;background:var(--c)"></i>' + esc(p.name) + '</span></h3>' + linkGroups(p, t) +
      '<div class="dr-actions"><button class="btn small" type="button" data-act="open" data-id="' + esc(p.id) + '">Projekt öffnen</button><button class="btn small ghost" type="button" data-act="karte-pick">Alle zeigen</button></div></section>';
  } else below = '';
  return top + '<div class="km' + (sel ? ' sel' : '') + (narrow ? ' narrow' : '') + '"><div class="km-stil"><p class="hint">' + hint + '</p>' + seg + '</div>' + svg + '</div>' + below;
}
''' + src[j:]
rep('''    case 'karte-pick': {''', '''    case 'karte-stil': try { await saveKarteStil(el.dataset.v); } catch(e){} break;
    case 'karte-pick': {''')

# 5) Takt fuer jeden Bereich
# Schublade: beim Anlegen den Bereich waehlen; Anfaenge nur im Takt-Bereich
rep('''  } else html += starterHTML(a ? a.id : '', a ? rhythmenIn(a.id) : [], true);
  const soll = r ? rhSoll(r) : 3;''',
'''  } else if (a && patternOf(a) === 'takt') html += starterHTML(a.id, rhythmenIn(a.id), true);
  const soll = r ? rhSoll(r) : 3;''')
rep('''    '<div class="f"><label for="rhName">Name</label><input id="rhName" required maxlength="40" value="' + esc(r ? r.name : '') + '" placeholder="z. B. Ausdauer" autocomplete="off"></div>' +''',
'''    '<div class="f"><label for="rhName">Name</label><input id="rhName" required maxlength="40" value="' + esc(r ? r.name : '') + '" placeholder="z. B. Französisch, MHBA lernen, Lesen" autocomplete="off"></div>' +
    (r ? '' : '<div class="f"><label for="rhArea">Bereich</label><select id="rhArea">' + areaList().map(x => '<option value="' + esc(x.id) + '"' + (a && x.id === a.id ? ' selected' : '') + '>' + esc(x.name) + '</option>').join('') + '</select><p class="hint">Takt gibt es in jedem Bereich: Sport, Lernen, Lesen, MHBA. Ein Tipp am Tag, wenn du es gemacht hast; nichts erinnert, nichts wird gelb.</p></div>') +''')
rep('''  const id = form.dataset.id, aid = form.dataset.area;
  const name = $('#rhName').value.trim(); if (!name){ toast('Bitte einen Namen eingeben.'); return; }''',
'''  const id = form.dataset.id, aid = $('#rhArea') ? $('#rhArea').value : form.dataset.area;
  const name = $('#rhName').value.trim(); if (!name){ toast('Bitte einen Namen eingeben.'); return; }''')
# Takt heute: anlegen
rep('''  const t = today(), rs = rhythmenAll(), ta = areaList().find(a => patternOf(a) === 'takt');
  const go = ta ? '<button class="link" type="button" data-act="go-area" data-v="' + esc(ta.id) + '">Zu ' + esc(ta.name) + '</button>' : '';
  const top = '<div class="dr-top"><div class="dr-title"><p class="eyebrow">Takt</p><h2 id="drTitle" tabindex="-1">Heute</h2></div>' + closeBtn() + '</div>';
  if (!rs.length) return top + '<p class="none">Noch kein Rhythmus. Lege einen im Bereich mit dem Takt an.</p>' + (go ? '<div>' + go + '</div>' : '');
  return top + '<div class="tq col" role="group" aria-label="Takt heute">' + rs.map(r => taktChipHTML(r, t, true)).join('') + '</div>' +
    '<p class="hint">Antippen trägt heute ein oder nimmt es zurück. Vergessene Tage trägst du im Rhythmus nach.</p>' + (go ? '<div>' + go + '</div>' : '');''',
'''  const t = today(), rs = rhythmenAll(), ta = areaList().find(a => patternOf(a) === 'takt');
  const add = '<button class="btn small" type="button" data-act="new-rhythmus" data-area="' + esc(ta ? ta.id : (areaList()[0] ? areaList()[0].id : '')) + '">+ Rhythmus</button>' + (ta ? '<button class="btn small ghost" type="button" data-act="go-area" data-v="' + esc(ta.id) + '">Zu ' + esc(ta.name) + '</button>' : '');
  const top = '<div class="dr-top"><div class="dr-title"><p class="eyebrow">Takt</p><h2 id="drTitle" tabindex="-1">Heute</h2></div>' + closeBtn() + '</div>';
  if (!rs.length) return top + '<p class="none">Noch kein Rhythmus. Wiederkehrendes aus jedem Bereich: Sport, Französisch, MHBA lernen, Lesen.</p><div class="dr-actions">' + add + '</div>';
  return top + '<div class="tq col" role="group" aria-label="Takt heute">' + rs.map(r => taktChipHTML(r, t, true)).join('') + '</div>' +
    '<p class="hint">Antippen trägt heute ein oder nimmt es zurück; vergessene Tage trägst du im Rhythmus nach. Nichts erinnert, nichts wird gelb.</p><div class="dr-actions">' + add + '</div>';''')
# Rhythmen anderer Bereiche als Zeile unter dem Inhalt
rep('''function taktQuickHTML(t){''',
'''/* Rhythmen eines Bereichs ohne Takt-Muster: eine Zeile unter dem Inhalt (Version 18) */
function taktMiniHTML(aid, t){
  if (!S.loaded.rhythmen) return '';
  const rs = rhythmenIn(aid); if (!rs.length) return '';
  return '<section class="fd-sec"><div class="tq" role="group" aria-label="Takt"><p class="k">Takt</p>' + rs.map(r => taktChipHTML(r, t, false)).join('') + '</div></section>';
}
function taktQuickHTML(t){''')
rep('''  if (!ps.length){
    return html + '<div class="empty-in"><p class="big">Hier ist noch nichts.</p><p>Lege ein Projekt an oder sag Claude „neues Projekt“. Ideen altern nicht; erst aktive Projekte bekommen einen Balken.</p></div>';
  }
  return html + projectsBlock(live, ideas, done, t, color);''',
'''  if (!ps.length){
    return html + '<div class="empty-in"><p class="big">Hier ist noch nichts.</p><p>Lege ein Projekt an oder sag Claude „neues Projekt“. Ideen altern nicht; erst aktive Projekte bekommen einen Balken.</p></div>' + taktMiniHTML(aid, t);
  }
  return html + projectsBlock(live, ideas, done, t, color) + taktMiniHTML(aid, t);''')
rep('''  if (ps.length) html += '<section class="fd-sec"><p class="k">Projekte</p>' + projectsBlock(live, ideas, done, t, color) + '</section>';
  return html + '</div>';
}
function circleHTML(x, t){''',
'''  if (ps.length) html += '<section class="fd-sec"><p class="k">Projekte</p>' + projectsBlock(live, ideas, done, t, color) + '</section>';
  return html + taktMiniHTML(a.id, t) + '</div>';
}
function circleHTML(x, t){''')
rep('''  if (ps.length) html += '<section class="fd-sec"><p class="k">Projekte</p>' + projectsBlock(live, ideas, done, t, color) + '</section>';
  return html + '</div>';
}
/* Felder in Leserichtung''',
'''  if (ps.length) html += '<section class="fd-sec"><p class="k">Projekte</p>' + projectsBlock(live, ideas, done, t, color) + '</section>';
  return html + taktMiniHTML(a.id, t) + '</div>';
}
/* Felder in Leserichtung''')
rep('''  if (ps.length) html += '<section class="fd-sec"><p class="k">Projekte</p>' + projectsBlock(live, ideas, done, t, color) + '</section>';
  return html + '</div>';
}
function inscrHTML(a){''',
'''  if (ps.length) html += '<section class="fd-sec"><p class="k">Projekte</p>' + projectsBlock(live, ideas, done, t, color) + '</section>';
  return html + taktMiniHTML(a.id, t) + '</div>';
}
function inscrHTML(a){''')
# Notiz: alle Rhythmen in einer Zeile
rep('''    else if (pat === 'takt') L.push('Takt ' + a.id + ' (' + a.name + '), Rhythmen: ' + (S.rhythmen.filter(r => r.areaId === a.id).map(r => r.id + ' | ' + r.name).join('; ') || 'keine'));
  });''',
'''  });
  if (S.rhythmen && S.rhythmen.length) L.push('Rhythmen für "takt" (ID | Name | Bereich): ' + S.rhythmen.map(r => r.id + ' | ' + r.name + ' | ' + ((areaById(r.areaId) || {}).name || '')).join('; '));''')
# Bereiche-Raster: Rhythmen auch bei anderen Mustern zaehlen
rep('''  const ps = projectsIn(a.id), live = ps.filter(isLive).length, ideas = ps.filter(p => p.status === 'idee').length;
  return [live ? live + ' laufend' : '', ideas ? ideas + (ideas === 1 ? ' Idee' : ' Ideen') : ''].filter(Boolean).join(' · ') || 'noch leer';''',
'''  const ps = projectsIn(a.id), live = ps.filter(isLive).length, ideas = ps.filter(p => p.status === 'idee').length, nr = rhythmenIn(a.id).length;
  return [live ? live + ' laufend' : '', ideas ? ideas + (ideas === 1 ? ' Idee' : ' Ideen') : '', nr ? nr + (nr === 1 ? ' Rhythmus' : ' Rhythmen') : ''].filter(Boolean).join(' · ') || 'noch leer';''')

# 6) Export
rep("seite: 17, meta: S.meta", "seite: 18, meta: S.meta")

out.write_text(src, encoding='utf-8')
print('ok', len(src))
