"""Ergänzt französische Übersetzungen (CFDICT) in zeichendaten.json.gz.

Aufruf:  python3 franzoesisch_ergaenzen.py pfad/zu/cfdict.u8
CFDICT: Chine-Informations.com, CC BY-SA 3.0 (Kopie z. B. unter github.com/aure231/cfdict-fr).
Pro Zeichen werden bis zu 3 kurze Bedeutungen übernommen, bevorzugt die der Hauptaussprache.
Danach die App neu bauen: python3 bauen.py index.html
"""
import gzip
import json
import pathlib
import re
import sys
import unicodedata

here = pathlib.Path(__file__).parent
DATA = here / 'zeichendaten.json.gz'

TONES = {'a': 'āáǎà', 'e': 'ēéěè', 'i': 'īíǐì', 'o': 'ōóǒò', 'u': 'ūúǔù', 'ü': 'ǖǘǚǜ'}


def num2mark(s):
    s = s.lower().replace('u:', 'ü').replace('v', 'ü')
    m = re.match(r'^([a-zü]+)([1-5])$', s)
    if not m:
        return s
    syl, t = m.group(1), int(m.group(2))
    if t == 5:
        return syl
    for v in ('a', 'e'):
        if v in syl:
            return syl.replace(v, TONES[v][t - 1], 1)
    if 'ou' in syl:
        return syl.replace('o', TONES['o'][t - 1], 1)
    for i in range(len(syl) - 1, -1, -1):
        if syl[i] in TONES:
            return syl[:i] + TONES[syl[i]][t - 1] + syl[i + 1:]
    return syl


def parse(path):
    out = {}
    for line in open(path, encoding='utf-8-sig'):
        if line.startswith('#') or not line.strip():
            continue
        m = re.match(r'^(\S+) (\S+) \[([^\]]*)\] /(.*)/\s*$', line)
        if not m:
            continue
        _trad, simp, py, defs = m.groups()
        if len(simp) != 1:
            continue
        out.setdefault(simp, []).append((py, [d for d in defs.split('/') if d]))
    return out


BAD = re.compile(r'(^voir\b|^variante|^var\.|nom de famille|patronyme|^classificateur|^spécificatif|'
                 r'^abr\.|abréviation|^cf\.|^utilisé dans|^radical|^CL:)', re.I)


def clean_fr(s):
    s = re.sub(r'\[[^\]]*\]', '', s)
    s = re.sub(r'\((?:n\.\s?[mf]\.?|n\.|v\.|adj\.|adv\.|prép\.|pron\.|interj\.|conj\.|fam\.|lit\.|arch\.|vx)\)',
               '', s, flags=re.I)
    return re.sub(r'\s+', ' ', s).strip(' ,;')


def split_top(s):
    parts, depth, cur = [], 0, ''
    for ch in s:
        if ch in '([':
            depth += 1
        elif ch in ')]':
            depth = max(0, depth - 1)
        if ch in ';,' and depth == 0:
            if cur.strip():
                parts.append(cur.strip())
            cur = ''
        else:
            cur += ch
    if cur.strip():
        parts.append(cur.strip())
    return parts


def short(entries, main_py, maxlen=42, n=3):
    same = [e for e in entries if num2mark(e[0]) == main_py] if main_py else []
    picked = []
    for _py, senses in (same or entries):
        for s in senses:
            if BAD.search(s):
                continue
            for part in split_top(clean_fr(s)):
                if part.startswith('(') or BAD.search(part) or len(part) > 30 or part in picked:
                    continue
                picked.append(part)
                if len(picked) >= n:
                    break
            if len(picked) >= n:
                break
        if len(picked) >= n:
            break
    out = ''
    for p in picked:
        cand = f'{out}, {p}' if out else p
        if len(cand) > maxlen and out:
            break
        out = cand
    return out


def main():
    cf = parse(sys.argv[1])
    data = json.loads(gzip.decompress(DATA.read_bytes()))
    hits = 0
    for ch, entry in data['d'].items():
        main_py = unicodedata.normalize('NFC', entry.get('p', ''))
        entry['fr'] = short(cf[ch], main_py) if ch in cf else ''
        hits += bool(entry['fr'])
    raw = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    DATA.write_bytes(gzip.compress(raw, 9, mtime=0))
    print(f'{hits} von {len(data["d"])} Zeichen mit französischer Übersetzung; '
          f'{DATA.name}: {DATA.stat().st_size / 1e6:.1f} MB')
    for ch in '爷奶外公婆的人这那电脑笔记本书子我你好学生中国':
        print(ch, data['d'].get(ch, {}).get('p'), '|', data['d'].get(ch, {}).get('fr'))


if __name__ == '__main__':
    main()
