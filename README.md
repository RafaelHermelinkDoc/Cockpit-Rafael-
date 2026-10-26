# Cockpit

Persönliches Cockpit für alle Lebensbereiche: je Projekt ein Füllstand-Balken mit Meilensteinen, dazu Fäden, Ideenbrett, Bibliothek und Takt. Eine einzige HTML-Seite, veröffentlicht als claude.ai-Artifact.

**Stand:** Version 19 (26.10.2026): Umschalter Darstellung (Automatisch, Hell, Dunkel).

## Aufbau
- `page/index.html` – die Seite, genau so veröffentlicht (Inhalt ab `<title>`, ohne Plattform-Gerüst).
- `tools/` – Testumgebung: `mock.js` (Attrappe für `window.claude.use`: db, assets, sample, mcp, downloads, permissions), `mktest.py` (baut `test.html` aus der Seite plus Testdaten), `run18.py` (Playwright-Prüfungen hell/dunkel, 1280/390 px), `fonts.sh` + `fonts.css` (Schriften lokal), `patch18.py` (Beispiel für Änderungen per exakter Ersetzung).

## Daten
Die Daten liegen in der Datenbank der Seite (ArtifactData), nicht hier. Kein Export ins Repository (`.gitignore` sperrt `data/` und `*.json`). Sicherung wöchentlich nach Google Drive.

## Fähigkeiten der Seite
`{db:{}, user:{}, downloads:true, mcp:{servers:[{server:'Google Calendar', tools:['list_events','list_calendars']}]}, assets:{}, sample:{}}` – bei `publish` mit `capabilities` immer alle sechs angeben, sonst weglassen.

## Ändern und veröffentlichen
1. Änderung in `page/index.html`.
2. Testen: `tools/fonts.sh` (einmal), Daten-Export nach `tools/data/` legen, `python3 tools/mktest.py ../page/index.html`, `python3 tools/run18.py`.
3. Veröffentlichen aus einem Claude-Chat mit Artifact `publish` auf dieselbe URL der Seite.
4. Commit, Tag `vNN`.

## Nächste Schritte
Später: Zerlegung in Module (`core/`, `data/`, `ui/`, `styles/`) mit Build zu einer Datei; dann die App.
