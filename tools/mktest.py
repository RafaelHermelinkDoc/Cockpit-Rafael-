#!/usr/bin/env python3
"""Baut test.html (und test-ruhig.html) aus v17.html: echte Daten aus data/ plus erfundene Testdaten (Bibliothek Politik), Attrappe davor, Google Fonts raus."""
import json, glob, os, pathlib, datetime, copy, sys
W = pathlib.Path(__file__).parent
D = W.parent / 'data'
def load(c):
    out = []
    for f in sorted(glob.glob(str(D / c / '*.json'))):
        d = json.load(open(f, encoding='utf-8')); d['id'] = os.path.basename(f)[:-5]; out.append(d)
    return out
seed = { c: load(c) for c in ['areas', 'projects', 'events', 'moves', 'arbeitsstaende', 'rhythmen'] }
seed['pausen'] = []; seed['personen'] = []; seed['faeden'] = []; seed['gedanken'] = []; seed['meta'] = []
today = datetime.date.today()
# erfundene Testdaten: Bibliothek Politik mit zwei Themen und fuenf Baenden (nur lokal)
seed['felder'] = [
    {'id': 'fe-rente-test', 'areaId': 'politik', 'name': 'Rente', 'order': 10, 'createdAt': '2026-10-01', 'updatedAt': '2026-10-01'},
    {'id': 'fe-energie-test', 'areaId': 'politik', 'name': 'Energie', 'order': 20, 'createdAt': '2026-10-01', 'updatedAt': '2026-10-01'},
]
arts = ['dossier', 'ueberblick', 'vergleich', 'faktencheck', 'analyse']
seed['dokumente'] = []
for i in range(5):
    seed['dokumente'].append({'id': 'd-test-%d' % i, 'areaId': 'politik', 'feldId': 'fe-rente-test' if i < 3 else 'fe-energie-test', 'titel': ['Rentenniveau 48 %: Wer trägt die Lücke?', 'Aktienrente im Vergleich', 'Generationenvertrag: Faktencheck', 'Strompreis und Netzentgelte', 'Wasserstoff: Analyse der Förderung'][i], 'art': arts[i], 'umfang': ['umfangreich', 'mittel', 'kurz', 'mittel', 'umfangreich'][i], 'stand': (today - datetime.timedelta(days=3 + 20 * i)).isoformat(), 'kernaussage': 'Testaussage %d: ein Satz, der die Kernaussage des Dokuments zusammenfasst.' % i, 'link': 'https://example.org/doc%d' % i, 'source': 'claude:chat', 'createdAt': (datetime.datetime.now() - datetime.timedelta(days=40 * i)).isoformat() + 'Z', 'updatedAt': today.isoformat()})
src = (W / (sys.argv[1] if len(sys.argv) > 1 else 'v17.html')).read_text(encoding='utf-8')
mock = (W / 'mock.js').read_text(encoding='utf-8')
# Google Fonts raus (Testumgebung erreicht sie nicht); lokale Schriften, wenn vorhanden
fonts = W / 'fonts.css'
src = src.replace('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..700&family=Hanken+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Cinzel:wght@600;700&family=EB+Garamond:ital,wght@0,400;0,500;1,400&display=swap">',
                  '<link rel="stylesheet" href="fonts.css">' if fonts.exists() else '')
def build(seed, name):
    s = src.replace('<script>\n(function(){', '<script>window.__SEED=' + json.dumps(seed, ensure_ascii=False) + ';</script>\n<script>' + mock + '</script>\n<script>\n(function(){', 1)
    assert s != src
    (W / name).write_text(s, encoding='utf-8')
build(seed, 'test.html')
# ruhige Variante: alles heute bewegt, kein Vorschlag, keine Frage, nichts zu bestaetigen
r = copy.deepcopy(seed)
for p in r['projects']:
    p['lastMove'] = {'date': today.isoformat(), 'text': 'Test'}
    p['planProposal'] = None; p['erreichtFragen'] = []
    for w in p.get('waitingOn', []): w['since'] = today.isoformat()
for e in r['events']:
    e['date'] = (today + datetime.timedelta(days=90)).isoformat(); e['endDate'] = None
build(r, 'test-ruhig.html')
print('ok', len(seed['projects']), 'Projekte', len(seed['dokumente']), 'Testbaende')
