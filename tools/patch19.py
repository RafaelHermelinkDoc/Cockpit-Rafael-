"""Version 18 -> 19: Umschalter Darstellung (Automatisch, Hell, Dunkel), je Gerät."""
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text(encoding='utf-8')
def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, (n, old[:80])
    s = s.replace(old, new)

# CSS
rep('.seg-ctl button[aria-pressed="true"]{background:var(--accent-soft);color:var(--accent);font-weight:600}',
    '.seg-ctl button[aria-pressed="true"]{background:var(--accent-soft);color:var(--accent);font-weight:600}\n'
    '/* Version 19: Darstellung je Gerät */\n'
    '.br-darst{display:flex;flex-wrap:wrap;align-items:center;gap:8px 14px;margin-top:10px;font-size:13px;color:var(--muted)}\n'
    '@media (max-width:700px){ .pf-darst .seg-ctl button,.br-darst .seg-ctl button{min-height:40px;padding:5px 13px;font-size:13.5px} }')

# Logik: direkt nach load/store
rep("function store(k, v){ try { localStorage.setItem('cockpit.' + k, v); } catch(e){} }\n",
    "function store(k, v){ try { localStorage.setItem('cockpit.' + k, v); } catch(e){} }\n"
    "/* Darstellung (Version 19): Automatisch, Hell oder Dunkel, gemerkt je Gerät und Browser (cockpit.darst).\n"
    "   Automatisch lässt gelten, was die Plattform (data-theme) bzw. das System vorgibt; ändert die Plattform ihr Thema, wird es gemerkt. */\n"
    "const DST = { auto: 'Automatisch', light: 'Hell', dark: 'Dunkel' };\n"
    "const DST_HOST = { v: document.documentElement.getAttribute('data-theme'), set: undefined };\n"
    "function darstPref(){ const v = load('darst'); return DST[v] ? v : 'auto'; }\n"
    "function applyDarst(){\n"
    "  const p = darstPref(), el = document.documentElement, want = p === 'auto' ? DST_HOST.v : p;\n"
    "  DST_HOST.set = want || null;\n"
    "  if (el.getAttribute('data-theme') === DST_HOST.set) return;\n"
    "  if (want) el.setAttribute('data-theme', want); else el.removeAttribute('data-theme');\n"
    "}\n"
    "function setDarst(v){\n"
    "  if (!DST[v]) return;\n"
    "  store('darst', v); applyDarst();\n"
    "  document.querySelectorAll('[data-act=\"darst\"][aria-pressed]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.v === v)));\n"
    "}\n"
    "function darstHTML(){ const p = darstPref(); return '<div class=\"seg-ctl\" role=\"group\" aria-label=\"Darstellung\">' + Object.keys(DST).map(k => '<button type=\"button\" data-act=\"darst\" data-v=\"' + k + '\" aria-pressed=\"' + (k === p) + '\">' + DST[k] + '</button>').join('') + '</div>'; }\n"
    "applyDarst();\n"
    "try { new MutationObserver(() => { const cur = document.documentElement.getAttribute('data-theme'); if (cur === DST_HOST.set) return; DST_HOST.v = cur; applyDarst(); }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] }); } catch(e){}\n")

# Hinweise: unten
rep("""    (S.dl ? '<div class="pop-foot pf-export"><span>Sicherung</span><button class="link" type="button" data-act="export">Daten exportieren</button></div>' : '');
  $('#bellPop').innerHTML = html;""",
    """    (S.dl ? '<div class="pop-foot pf-export"><span>Sicherung</span><button class="link" type="button" data-act="export">Daten exportieren</button></div>' : '') +
    '<div class="pop-foot pf-darst"><span>Darstellung</span>' + darstHTML() + '</div>';
  $('#bellPop').innerHTML = html;""")

# Bereiche-Schublade
rep("""(S.dl ? '<button class="link" type="button" data-act="export">Daten exportieren</button>' : '') + '</div>';
}""",
    """(S.dl ? '<button class="link" type="button" data-act="export">Daten exportieren</button>' : '') + '</div>' +
    '<div class="br-darst"><span>Darstellung</span>' + darstHTML() + '</div>';
}""")

# Suche: Befehle
rep("""pen: '<path d="M4 20h4L18.5 9.5a2.12 2.12 0 0 0-3-3L5 17z"/><path d="M13.5 7.5l3 3"/>' };""",
    """pen: '<path d="M4 20h4L18.5 9.5a2.12 2.12 0 0 0-3-3L5 17z"/><path d="M13.5 7.5l3 3"/>', sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>', moon: '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>', half: '<circle cx="12" cy="12" r="8"/><path d="M12 4v16"/>' };""")
rep("""    { act: 'su-tab', v: 'vorne', keys: ['vorne', 'start'], t: 'Vorne', s: 'angepinnte Projekte', c: 'var(--ink)', i: I.front }
  ];""",
    """    { act: 'su-tab', v: 'vorne', keys: ['vorne', 'start'], t: 'Vorne', s: 'angepinnte Projekte', c: 'var(--ink)', i: I.front },
    { act: 'darst', v: 'light', keys: ['hell', 'light', 'darstellung', 'tag'], t: 'Hell', s: 'Darstellung auf diesem Gerät' + (darstPref() === 'light' ? ' · gerade gewählt' : ''), c: 'var(--ink)', i: I.sun },
    { act: 'darst', v: 'dark', keys: ['dunkel', 'dark', 'darstellung', 'nacht'], t: 'Dunkel', s: 'Darstellung auf diesem Gerät' + (darstPref() === 'dark' ? ' · gerade gewählt' : ''), c: 'var(--ink)', i: I.moon },
    { act: 'darst', v: 'auto', keys: ['automatisch', 'system', 'darstellung'], t: 'Automatisch', s: 'Darstellung wie System bzw. claude.ai' + (darstPref() === 'auto' ? ' · gerade gewählt' : ''), c: 'var(--ink)', i: I.half }
  ];""")
rep("Befehle: Pause, Export, Termine, Karte, Leiste, „Notiz: …“.", "Befehle: Pause, Export, Termine, Karte, Leiste, Hell, Dunkel, „Notiz: …“.")

# Aktion
rep("    case 'export': exportData(); break;", "    case 'export': exportData(); break;\n    case 'darst': setDarst(el.dataset.v); break;")

# Export
rep("seite: 18,", "seite: 19,")
p.write_text(s, encoding='utf-8')
print('ok')
