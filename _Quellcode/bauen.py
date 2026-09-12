"""Baut die fertige App aus vorlage.html + zeichendaten.json.gz.

Aufruf:  python3 bauen.py               -> Schriftzeichenblatt.html
         python3 bauen.py index.html    -> index.html (für GitHub Pages)
Die fertige Datei landet einen Ordner höher und enthält alles (Code, Wörterbuch, Strichdaten).
zeichendaten.json.gz = {"d": Wörterbuch (Pinyin/EN/DE), "s": Strichdaten (hanzi-writer-data)}, gzip-komprimiert.
"""
import base64
import pathlib
import sys

here = pathlib.Path(__file__).parent
template = (here / 'vorlage.html').read_text(encoding='utf-8')
data = base64.b64encode((here / 'zeichendaten.json.gz').read_bytes()).decode('ascii')
assert '__ZEICHENDATEN__' in template, 'Platzhalter __ZEICHENDATEN__ fehlt in vorlage.html'
out = here.parent / (sys.argv[1] if len(sys.argv) > 1 else 'Schriftzeichenblatt.html')
out.write_text(template.replace('__ZEICHENDATEN__', data), encoding='utf-8')
print(f'{out.name} geschrieben: {out.stat().st_size / 1e6:.1f} MB')
