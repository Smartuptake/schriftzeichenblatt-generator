import json, re, unicodedata
def parse(path):
    out = {}
    for line in open(path, encoding='utf-8-sig'):
        if line.startswith('#') or not line.strip(): continue
        m = re.match(r'^(\S+) (\S+) \[([^\]]*)\] /(.*)/\s*$', line)
        if not m: continue
        trad, simp, py, defs = m.groups()
        if len(simp) != 1: continue
        out.setdefault(simp, []).append((py, [d for d in defs.split('/') if d]))
    return out
TONES = {'a':'āáǎà','e':'ēéěè','i':'īíǐì','o':'ōóǒò','u':'ūúǔù','ü':'ǖǘǚǜ'}
def num2mark(s):
    s = s.lower().replace('u:','ü').replace('v','ü')
    m = re.match(r'^([a-zü]+)([1-5])$', s)
    if not m: return s
    syl, t = m.group(1), int(m.group(2))
    if t == 5: return syl
    for v in ('a','e'):
        if v in syl: return syl.replace(v, TONES[v][t-1], 1)
    if 'ou' in syl: return syl.replace('o', TONES['o'][t-1], 1)
    for i in range(len(syl)-1, -1, -1):
        if syl[i] in TONES: return syl[:i] + TONES[syl[i]][t-1] + syl[i+1:]
    return syl
def strip_tone(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').replace('ü','ü')
BAD = re.compile(r'(surname|variant of|old variant|^see |used in|^abbr\.|Kurzform|Variante|Familienname|Nachname|Radikal Nr|^\(Substantiv-Suffix\)|^\(Zählwort\)|^Na$|Japanese|Kangxi radical)', re.I)
def clean_en(s):
    s = re.sub(r'\(CL:[^)]*\)', '', s)
    s = re.sub(r'\((bound form|pronoun|specifier|coll\.|literary|classical|dialect|old)\)', '', s, flags=re.I)
    s = re.sub(r'\([^)]*pr\.[^)]*\)', '', s)
    s = re.sub(r'\[[^\]]*\]', '', s)
    s = re.sub(r'\s+', ' ', s).strip(' ,;')
    return s
def clean_de(s):
    s = s.split('; Bsp.:')[0]
    s = re.sub(r'\s*\((S|V|Adj|Adv|Pron|Num|Zähl|Int|Präp|Konj|Part|Art|Eig|Fam|Bio|Gesch|Sprachw|Vorsilbe|[A-Za-zäöü, ]{1,25})\)', '', s)
    s = re.sub(r'\s+', ' ', s).strip(' ,;')
    return s
def split_top(s):
    parts, depth, cur = [], 0, ''
    for ch in s:
        if ch in '([': depth += 1
        elif ch in ')]': depth = max(0, depth - 1)
        if ch in ';,' and depth == 0:
            if cur.strip(): parts.append(cur.strip())
            cur = ''
        else: cur += ch
    if cur.strip(): parts.append(cur.strip())
    return parts
def short(entries, cleaner, maxlen=48, n=3):
    picked = []
    for py, senses in entries:
        for s in senses:
            if BAD.search(s) or s.startswith('CL:'): continue
            s = cleaner(s)
            if not s or BAD.search(s): continue
            for part in split_top(s):
                if part.startswith('CL:') or part.startswith('('): continue
                if part not in picked and len(part) <= 30: picked.append(part)
                if len(picked) >= n: break
            if len(picked) >= n: break
        if len(picked) >= n: break
    out = ''
    for p in picked:
        cand = (out + ', ' + p) if out else p
        if len(cand) > maxlen and out: break
        out = cand
    return out
ce = parse('cedict.txt'); hd = parse('handedict.u8')
dic = {}
for line in open('mmah.txt', encoding='utf-8'):
    d = json.loads(line); c = d['character']
    pys = list(d.get('pinyin') or [])
    if c in ce:
        toned = [num2mark(e[0]) for e in ce[c] if not e[0][:1].isupper()]
        for i, p in enumerate(pys):
            if strip_tone(p) == p:
                for t in toned:
                    if strip_tone(t) == p and t != p:
                        pys[i] = t; break
    main = strip_tone(pys[0]) if pys else ''
    def prefer(entries):
        if not pys: return entries
        same = [e for e in entries if num2mark(e[0]) == pys[0]]
        if not same: same = [e for e in entries if strip_tone(num2mark(e[0])) == main]
        return same if same else entries
    en = short(prefer(ce[c]), clean_en) if c in ce else ''
    if not en and d.get('definition'): en = ', '.join(d['definition'].split(', ')[:3])
    de = short(prefer(hd[c]), clean_de) if c in hd else ''
    dic[c] = {'p': pys[0] if pys else '', 'pa': pys[1:], 'en': en, 'de': de}
PATCH = {
    '的': {'de': 'Attributpartikel (von, -s)'},
    '了': {'de': 'Partikel für Abschluss/Veränderung'},
    '吗': {'de': 'Fragepartikel'},
    '呢': {'de': 'Fragepartikel (und …?)'},
    '吧': {'de': 'Partikel (Vorschlag, Vermutung)'},
}
for k, v in PATCH.items():
    if k in dic: dic[k].update(v)
with open('dict.js','w',encoding='utf-8') as f:
    f.write('// Zeichendaten: makemeahanzi (LGPL), CC-CEDICT (CC-BY-SA 4.0, mdbg.net), HanDeDict (CC-BY-SA 3.0, handedict.zydeo.net)\nwindow.HANZI_DICT=')
    json.dump(dic, f, ensure_ascii=False, separators=(',',':')); f.write(';\n')
print(len(dic), 'chars; DE:', sum(1 for v in dic.values() if v['de']), 'EN:', sum(1 for v in dic.values() if v['en']))
for c in '爷奶外公婆这那的电脑笔记本书子我你好学生中国人':
    print(c, dic.get(c))
