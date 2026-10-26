# my-weakness.xlsx の1枚目のシートを my-weakness.csv に書き出す（UTF-8・BOM なし・LF 改行）
# 使い方: python3 build-csv.py （xlsx を編集したら実行。標準ライブラリだけで動く）
import csv, os, zipfile
import xml.etree.ElementTree as ET

DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(DIR, 'my-weakness.xlsx')
DST = os.path.join(DIR, 'my-weakness.csv')
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'

def col_index(ref):
    n = 0
    for ch in ref:
        if not ch.isalpha(): break
        n = n * 26 + ord(ch.upper()) - 64
    return n - 1

def text(el):
    return ''.join(t.text or '' for t in el.iter(NS + 't'))

def read_rows(path):
    z = zipfile.ZipFile(path)
    names = z.namelist()
    shared = [text(si) for si in ET.fromstring(z.read('xl/sharedStrings.xml')).iter(NS + 'si')] if 'xl/sharedStrings.xml' in names else []
    sheet = sorted(n for n in names if n.startswith('xl/worksheets/sheet'))[0]
    rows = []
    for r in ET.fromstring(z.read(sheet)).iter(NS + 'row'):
        vals = []
        for c in r.iter(NS + 'c'):
            i = col_index(c.get('r', '')) if c.get('r') else len(vals)
            vals += [''] * (i - len(vals))
            v, t = c.find(NS + 'v'), c.get('t')
            if t == 's': vals.append(shared[int(v.text)])
            elif t == 'inlineStr': vals.append(text(c))
            else: vals.append(v.text if v is not None else '')
        if any(x.strip() for x in vals): rows.append(vals)
    return rows

rows = read_rows(SRC)
with open(DST, 'w', newline='', encoding='utf-8') as f:
    csv.writer(f, lineterminator='\n').writerows(rows)
print(f'my-weakness.csv を書き出しました（{len(rows)} 行）')
