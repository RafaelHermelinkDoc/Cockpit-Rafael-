#!/bin/sh
# Lädt die fünf Schriften (OFL) aus npm nach tools/fnt/ für lokale Tests (fonts.css verweist darauf).
set -e
cd "$(dirname "$0")"; mkdir -p fnt; cd fnt
for p in cinzel eb-garamond bricolage-grotesque hanken-grotesk ibm-plex-mono; do
  npm pack "@fontsource/$p" >/dev/null && tar xzf fontsource-$p-*.tgz && mv package "$p" && rm fontsource-$p-*.tgz
done
