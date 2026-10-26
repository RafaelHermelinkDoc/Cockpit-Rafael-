import http.server, socketserver, threading, os, functools, sys
from playwright.sync_api import sync_playwright
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PORT = int(os.environ.get('PORT', 8801))
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory='.')
class Q(H.func):
    def log_message(self, *a): pass
class T(socketserver.TCPServer): allow_reuse_address = True
srv = T(('127.0.0.1', PORT), functools.partial(Q, directory='.')); threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = 'http://127.0.0.1:%d/' % PORT
ok = fail = 0
def check(c, m):
    global ok, fail
    if c: ok += 1; print('OK  ', m)
    else: fail += 1; print('FAIL', m)
bg = lambda pg: pg.evaluate("getComputedStyle(document.body).backgroundColor")
th = lambda pg: pg.evaluate("document.documentElement.getAttribute('data-theme')")
with sync_playwright() as p:
    b = p.chromium.launch()
    # Rechner, System hell
    c = b.new_context(viewport={'width': 1280, 'height': 900}, color_scheme='light')
    pg = c.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
    pg.goto(BASE + 'test.html'); pg.wait_for_selector('.rows .row'); pg.wait_for_timeout(500)
    light_bg = bg(pg); check(th(pg) is None, 'Start: kein data-theme (Automatisch)')
    pg.click('#bellBtn' if pg.locator('#bellBtn').count() else '[data-act="bell"]'); pg.wait_for_selector('#bellPop .pf-darst')
    check(pg.locator('#bellPop .pf-darst button[aria-pressed="true"]').inner_text() == 'Automatisch', 'Hinweise: Automatisch gewählt')
    pg.click('#bellPop .pf-darst button[data-v="dark"]'); pg.wait_for_timeout(150)
    dark_bg = bg(pg)
    check(th(pg) == 'dark' and dark_bg != light_bg, 'Dunkel gesetzt, Hintergrund wechselt (%s -> %s)' % (light_bg, dark_bg))
    check(pg.locator('#bellPop .pf-darst button[aria-pressed="true"]').inner_text() == 'Dunkel', 'Knopf Dunkel gedrückt')
    pg.screenshot(path='shots/v19-hinweise-dunkel.png')
    pg.reload(); pg.wait_for_selector('.rows .row'); pg.wait_for_timeout(300)
    check(th(pg) == 'dark' and bg(pg) == dark_bg, 'Nach Neuladen bleibt Dunkel')
    pg.click('[data-act="bell"] >> nth=0'); pg.wait_for_selector('#bellPop .pf-darst')
    pg.click('#bellPop .pf-darst button[data-v="auto"]'); pg.wait_for_timeout(150)
    check(th(pg) is None and bg(pg) == light_bg, 'Automatisch: zurück zum System (hell)')
    # Plattform setzt data-theme
    pg.evaluate("document.documentElement.setAttribute('data-theme','dark')"); pg.wait_for_timeout(100)
    check(th(pg) == 'dark' and bg(pg) == dark_bg, 'Automatisch folgt der Plattform (dunkel)')
    pg.click('#bellPop .pf-darst button[data-v="light"]'); pg.wait_for_timeout(150)
    check(th(pg) == 'light' and bg(pg) == light_bg, 'Hell schlägt das Thema der Plattform')
    pg.evaluate("document.documentElement.setAttribute('data-theme','dark')"); pg.wait_for_timeout(100)
    check(th(pg) == 'light', 'Plattform wechselt erneut: Hell bleibt')
    pg.click('#bellPop .pf-darst button[data-v="auto"]'); pg.wait_for_timeout(150)
    check(th(pg) == 'dark', 'Automatisch: wieder Thema der Plattform (dunkel)')
    pg.keyboard.press('Escape')
    # Suche
    pg.evaluate("document.documentElement.removeAttribute('data-theme')"); pg.wait_for_timeout(100)
    pg.click('#searchBtn'); pg.wait_for_selector('#suQ' if pg.locator('#suQ').count() else 'input[type=search]')
    inp = pg.locator('#suQ') if pg.locator('#suQ').count() else pg.locator('input[type=search]').first
    inp.fill('dunkel'); pg.wait_for_timeout(250)
    check(pg.locator('.su-i[data-act="darst"][data-v="dark"]').count() == 1, 'Suche „dunkel“ findet den Befehl')
    pg.click('.su-i[data-act="darst"][data-v="dark"]'); pg.wait_for_timeout(150)
    check(th(pg) == 'dark', 'Befehl aus der Suche setzt Dunkel')
    inp.fill('darstellung'); pg.wait_for_timeout(250)
    check(pg.locator('.su-i[data-act="darst"]').count() == 3, 'Suche „darstellung“ zeigt alle drei')
    pg.screenshot(path='shots/v19-suche.png')
    check(not errs, 'Rechner: keine Konsolenfehler ' + str(errs[:3]))
    c.close()
    # Handy, System dunkel
    c = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, color_scheme='dark', has_touch=True, is_mobile=True)
    pg = c.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
    pg.goto(BASE + 'test.html'); pg.wait_for_selector('.rows .row'); pg.wait_for_timeout(500)
    dk = bg(pg)
    pg.tap('.tbar [data-act="bereiche"]' if pg.locator('.tbar [data-act="bereiche"]').count() else '[data-act="bereiche"] >> nth=0'); pg.wait_for_selector('.br-darst')
    pg.locator('.br-darst').scroll_into_view_if_needed()
    h = pg.locator('.br-darst button').first.bounding_box()['height']
    check(h >= 40, 'Handy: Knöpfe mind. 40 px hoch (%d)' % h)
    pg.tap('.br-darst button[data-v="light"]'); pg.wait_for_timeout(150)
    check(th(pg) == 'light' and bg(pg) != dk, 'Handy: Hell trotz System dunkel')
    pg.screenshot(path='shots/v19-bereiche-390-hell.png')
    sw = pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    check(sw, 'Handy: keine waagerechte Rollleiste')
    check(not errs, 'Handy: keine Konsolenfehler ' + str(errs[:3]))
    b.close()
srv.shutdown()
print('\n%d OK, %d FAIL' % (ok, fail))
