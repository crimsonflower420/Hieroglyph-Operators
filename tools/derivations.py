#!/usr/bin/env python3
"""Parse, check and render two-layer sub-lexical derivations (SUBLEXICAL-DERIVATIONS-v1).

Source of truth: data/derivations/*.drv (bracket form). This tool
  * parses the bracket lines A: (layout, headless) and B:/B_alt: (typed function, heads _H on determinatives),
  * checks arity, shared leaf ids, heads, walks and reorder labels (exit status 1 on any error),
  * reports where a function constituent does not coincide with layout constituents (MISMATCH),
  * writes data/derivations/<name>.json, and offers SVG renderers used by tools/build_pages.py.
Usage: python3 tools/derivations.py [data/derivations/rahman.drv]
"""
import json, re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- operators
LAYOUT_FIXED = {'⿰': 2, '⿲': 3, '⿱': 2, '⿳': 3, 'OVERLAY': 2, 'CARTOUCHE': 1,
                'INS_ts': 2, 'INS_te': 2, 'INS_bs': 2, 'INS_be': 2, 'INS_m': 2, 'INS_t': 2, 'INS_b': 2}
LAYOUT_FAMILY = {'LINE': (1, 99)}            # LINEk: a row of k quadrats (no Unicode joiner between them)
FUNC_FIXED = {'CLOSE': 2, 'LOGO': 2, 'PL': 2, 'SUFF': 2, 'GEN': 2, 'ATTR': 2, 'COORD': 2, 'ABBR': 1}
FUNC_FAMILY = {'SPELL': (2, 99), 'CMPL': (2, 3), 'INFL': (2, 3), 'NAME': (2, 9), 'PHRASE': (2, 9)}
ROLES = {'PHON1', 'PHON2', 'PHON3', 'LOGO', 'COMPL', 'DET', 'FEM', 'PL', 'INFL', 'STROKE', 'SUFF'}
OP_GLOSS = {  # (ja, en) — what each operator does
    '⿰': ('左右（方形の中）', 'side by side, within a quadrat'), '⿲': ('左中右（方形の中）', 'three side by side, within a quadrat'),
    '⿱': ('上下', 'one above the other'), '⿳': ('上中下', 'three stacked'),
    'INS_te': ('上・終わり側の隅に差し込む', 'insert at top-end corner'), 'INS_ts': ('上・始め側の隅に差し込む', 'insert at top-start corner'),
    'INS_be': ('下・終わり側の隅に差し込む', 'insert at bottom-end corner'), 'INS_bs': ('下・始め側の隅に差し込む', 'insert at bottom-start corner'),
    'INS_m': ('中央に差し込む', 'insert at middle'), 'INS_t': ('上に差し込む', 'insert at top'), 'INS_b': ('下に差し込む', 'insert at bottom'),
    'OVERLAY': ('重ね合わせ', 'overlay'), 'CARTOUCHE': ('カルトゥーシュで囲む', 'enclose in a cartouche'),
    'LINE': ('方形を k 個並べる', 'a row of k quadrats'),
    'SPELL': ('音の単位を k 個つなぐ → WORD', 'join k sound units → WORD'),
    'CMPL': ('多子音記号＋補音 → PHON', 'multiliteral + complement(s) → PHON'),
    'CLOSE': ('WORD＋限定符 → WORD_closed（限定符が主要部）', 'WORD + determinative → WORD_closed (determinative is head)'),
    'LOGO': ('表語＋一本線 → WORD', 'logogram + stroke → WORD'),
    'INFL': ('語幹＋語尾 → WORD', 'stem + ending(s) → WORD'), 'PL': ('複数の印を付ける', 'add a plural marker'),
    'SUFF': ('動詞＋接尾代名詞', 'verb + suffix pronoun'), 'GEN': ('直接属格（所有されるもの＋所有者）', 'direct genitive (possessed + possessor)'),
    'ATTR': ('名詞＋修飾語', 'noun + modifier'), 'COORD': ('並列', 'coordination'),
    'ABBR': ('略記：記号一つで語全体を指す', 'abbreviation: one sign stands for the whole word'),
    'NAME': ('名の文', 'name sentence'), 'PHRASE': ('句', 'phrase'),
}

def op_arity(op, layer):
    fixed, fam = (LAYOUT_FIXED, LAYOUT_FAMILY) if layer == 'A' else (FUNC_FIXED, FUNC_FAMILY)
    if op in fixed: return fixed[op]
    m = re.fullmatch(r'([A-Z]+)(\d+)', op)
    if m and m.group(1) in fam:
        k = int(m.group(2)); lo, hi = fam[m.group(1)]
        if lo <= k <= hi: return k
    return None

def op_base(op):
    m = re.fullmatch(r'([A-Z]+)(\d+)', op)
    return m.group(1) if m and m.group(1) in {**LAYOUT_FAMILY, **FUNC_FAMILY} else op

# ---------------------------------------------------------------- signs
def gardiner_map():
    rev = {}
    for cp in range(0x13000, 0x13430):
        n = unicodedata.name(chr(cp), '')
        m = re.match(r'EGYPTIAN HIEROGLYPH ([A-Z]+?)0*(\d+)([A-Z]*)$', n)
        if m:
            rev[('Aa' if m.group(1) == 'AA' else m.group(1)) + m.group(2) + m.group(3)] = chr(cp)
    return rev
GARD = gardiner_map()

# ---------------------------------------------------------------- bracket parser
TOK = re.compile(r'\[|\]|[^\s\[\]]+')
def parse_bracket(s):
    toks = TOK.findall(s); i = 0
    def node():
        nonlocal i
        t = toks[i]; i += 1
        if t == '[':
            op = toks[i]; i += 1; kids = []
            while toks[i] != ']': kids.append(node())
            i += 1
            return {'op': op, 'kids': kids}
        m = re.fullmatch(r'(n\d+)(?::([A-Z0-9]+?)(_H)?)?', t)
        if not m: raise ValueError(f'bad token {t!r}')
        return {'id': m.group(1), 'role': m.group(2), 'head': bool(m.group(3))}
    tree = node()
    if i != len(toks): raise ValueError('trailing tokens')
    return tree

def leaves(t): return [t] if 'id' in t else [l for k in t['kids'] for l in leaves(k)]
def yield_ids(t): return [l['id'] for l in leaves(t)]
def internal(t): return [] if 'id' in t else [t] + [n for k in t['kids'] for n in internal(k)]
def bracket(t):
    if 'id' in t: return t['id'] + (f":{t['role']}" if t['role'] else '') + ('_H' if t['head'] else '')
    return '[' + ' '.join([t['op']] + [bracket(k) for k in t['kids']]) + ']'
def height(t): return 0 if 'id' in t else 1 + max(height(k) for k in t['kids'])

# ---------------------------------------------------------------- file parser
def parse_file(path):
    out = []; cur = None
    for raw in Path(path).read_text(encoding='utf8').splitlines():
        line = raw.rstrip()
        if not line or line.startswith('#'): continue
        if line.startswith('=== '):
            cur = {'id': line[4:].strip()}; out.append(cur); continue
        k, _, v = line.partition(':'); cur[k.strip()] = v.strip()
    for d in out:
        d['signs_list'] = []
        for part in d['signs'].split('|'):
            sid, code, *val = part.split()
            d['signs_list'].append({'id': sid, 'code': code, 'value': ' '.join(val), 'glyph': GARD.get(code, '')})
        d['A_tree'] = parse_bracket(d['A'])
        d['B_tree'] = None if d['B'] == 'OPEN' else parse_bracket(d['B'])
        d['B_alt_tree'] = parse_bracket(d['B_alt']) if d.get('B_alt') else None
        d['read_list'] = d['read'].split()
        d.setdefault('reorder', '-'); d.setdefault('status', 'HYPOTHESIS')
        d['refs_list'] = [r.strip() for r in d.get('refs', '').split('|') if r.strip()]
    return out

# ---------------------------------------------------------------- checks
def check(d):
    errs = []; ids = [s['id'] for s in d['signs_list']]
    for s in d['signs_list']:
        if s['code'] != '?' and not s['glyph']: errs.append(f"unknown Gardiner code {s['code']}")
    def walk(t, layer):
        if 'id' in t:
            if t['id'] not in ids: errs.append(f'{layer}: leaf {t["id"]} not in signs')
            if layer == 'A' and (t['role'] or t['head']): errs.append(f'A: leaf {t["id"]} has a role/head (layout is headless)')
            if layer != 'A':
                if t['role'] not in ROLES: errs.append(f'{layer}: leaf {t["id"]} role {t["role"]!r} unknown')
                if t['role'] == 'DET' and not t['head']: errs.append(f'{layer}: DET {t["id"]} must be marked _H')
                if t['head'] and t['role'] != 'DET': errs.append(f'{layer}: only DET may be head ({t["id"]})')
            return
        a = op_arity(t['op'], 'A' if layer == 'A' else 'B')
        if a is None: errs.append(f'{layer}: unknown operator {t["op"]}')
        elif a != len(t['kids']): errs.append(f'{layer}: {t["op"]} has {len(t["kids"])} daughters, arity {a}')
        if layer != 'A':
            base = op_base(t['op'])
            if base == 'CMPL':
                ph = [k for k in t['kids'] if 'id' in k and k['role'] in ('PHON2', 'PHON3')]
                co = [k for k in t['kids'] if 'id' in k and k['role'] == 'COMPL']
                if len(ph) != 1 or len(co) != len(t['kids']) - 1: errs.append(f'{layer}: {t["op"]} needs one PHON2/3 and the rest COMPL')
            if base == 'CLOSE':
                last = t['kids'][-1]
                if not ('id' in last and last['role'] == 'DET' and last['head']): errs.append(f'{layer}: CLOSE must end in a DET_H leaf')
        for k in t['kids']: walk(k, layer)
    walk(d['A_tree'], 'A')
    for key, lay in (('B_tree', 'B'), ('B_alt_tree', 'B_alt')):
        if d[key]: walk(d[key], lay)
    ya = yield_ids(d['A_tree'])
    if sorted(ya) != sorted(ids) or len(set(ya)) != len(ya): errs.append('A must use every sign exactly once')
    if sorted(d['read_list']) != sorted(ids): errs.append('read must be a permutation of the signs')
    for key, lay in (('B_tree', 'B'), ('B_alt_tree', 'B_alt')):
        if d[key] and yield_ids(d[key]) != d['read_list']: errs.append(f'{lay} yield must equal WALK_read')
    differs = ya != d['read_list']
    if differs and d['reorder'] == '-': errs.append('WALK_write ≠ WALK_read but no reorder label')
    if not differs and d['reorder'] != '-': errs.append('reorder label but walks coincide')
    if d['reorder'] != '-' and not re.fullmatch(r'TRANSPOSE\((honorific|graphic)\)', d['reorder']): errs.append('bad reorder label')
    if not d['status'].startswith('HYPOTHESIS'): errs.append('every tree carries HYPOTHESIS')
    return errs

def mismatches(A, B):
    """Function nodes whose leaf set is neither a layout node's leaf set nor a contiguous run of one layout node's children."""
    spans = set()
    for n in internal(A) + leaves(A):
        if 'id' in n: spans.add(frozenset([n['id']])); continue
        kid_sets = [frozenset(yield_ids(k)) for k in n['kids']]
        for i in range(len(kid_sets)):
            acc = frozenset()
            for j in range(i, len(kid_sets)):
                acc |= kid_sets[j]; spans.add(acc)
    out = []
    for n in internal(B):
        s = frozenset(yield_ids(n))
        if s not in spans: out.append({'op': n['op'], 'leaves': yield_ids(n)})
    return out

# ---------------------------------------------------------------- Unicode string for the quadrat renderer
VJ, HJ, BS, ES, OV = '\U00013430', '\U00013431', '\U00013437', '\U00013438', '\U00013436'
INSC = {'INS_ts': '\U00013432', 'INS_bs': '\U00013433', 'INS_te': '\U00013434', 'INS_be': '\U00013435',
        'INS_m': '\U00013439', 'INS_t': '\U0001343A', 'INS_b': '\U0001343B'}
def uni(t, g):
    """Return (string, kind) for a quadrat-internal subtree; kind decides when segment brackets are needed."""
    if 'id' in t: return g[t['id']] or '\U00013000', 'leaf'
    parts = [uni(k, g) for k in t['kids']]; op = t['op']
    if op in ('⿱', '⿳'): return VJ.join(s if k != 'ver' else s for s, k in parts), 'ver'
    if op in ('⿰', '⿲'): return HJ.join(BS + s + ES if k == 'ver' else s for s, k in parts), 'hor'
    if op in INSC:
        (b, bk), (c, ck) = parts
        b = b if bk == 'leaf' else BS + b + ES; c = c if ck == 'leaf' else BS + c + ES
        return b + INSC[op] + c, 'ins'
    if op == 'OVERLAY':
        (b, bk), (c, ck) = parts
        return (b if bk == 'leaf' else BS + b + ES) + OV + (c if ck == 'leaf' else BS + c + ES), 'ins'
    raise ValueError(op)
def quadrats(A, g):
    """Split layer A into (cartouche?, [unicode string per quadrat])."""
    cart = False; t = A
    if 'op' in t and t['op'] == 'CARTOUCHE': cart = True; t = t['kids'][0]
    qs = t['kids'] if 'op' in t and op_base(t['op']) == 'LINE' else [t]
    return cart, [uni(q, g)[0] for q in qs]

# ---------------------------------------------------------------- SVG
def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def hue(i, n): return int(360 * i / max(n, 1) + 20) % 360

def svg_tree(t, d, layer):
    sg = {s['id']: s for s in d['signs_list']}; order = [s['id'] for s in d['signs_list']]
    lv = leaves(t); H = height(t); DX, DY, TOP = 58, 54, 22
    pos = {}
    def place(n, depth):
        if 'id' in n:
            x = DX / 2 + DX * lv.index(n); pos[id(n)] = (x, TOP + DY * H); return x
        xs = [place(k, depth + 1) for k in n['kids']]
        x = sum(xs) / len(xs); pos[id(n)] = (x, TOP + DY * depth); return x
    place(t, 0)
    W = DX * len(lv); Ht = TOP + DY * H + 74
    o = [f'<svg class="dtree" viewBox="0 0 {W} {Ht}" width="{W}" height="{Ht}" role="img" aria-label="{esc(bracket(t))}">']
    def draw(n):
        x, y = pos[id(n)]
        if 'id' in n: return
        for k in n['kids']:
            kx, ky = pos[id(k)]
            o.append(f'<line x1="{x:.1f}" y1="{y + 8:.1f}" x2="{kx:.1f}" y2="{ky - 16:.1f}" class="edge"/>')
            draw(k)
        o.append(f'<text x="{x:.1f}" y="{y + 4:.1f}" class="op" text-anchor="middle">{esc(n["op"])}</text>')
    draw(t)
    for n in lv:
        x, y = pos[id(n)]; s = sg[n['id']]; c = hue(order.index(n['id']), len(order))
        o.append(f'<circle cx="{x:.1f}" cy="{y + 6:.1f}" r="22" class="leafbg" style="--h:{c}"/>')
        if s['glyph']: o.append(f'<text x="{x:.1f}" y="{y + 16:.1f}" class="hg" text-anchor="middle">{s["glyph"]}</text>')
        else: o.append(f'<rect x="{x - 11:.1f}" y="{y - 8:.1f}" width="22" height="26" class="miss"/><text x="{x:.1f}" y="{y + 10:.1f}" class="code" text-anchor="middle">?</text>')
        o.append(f'<text x="{x:.1f}" y="{y + 40:.1f}" class="code" text-anchor="middle">{esc(s["code"])}</text>')
        lab = (n['role'] or '') + ('_H' if n['head'] else '') if layer != 'A' else n['id']
        o.append(f'<text x="{x:.1f}" y="{y + 54:.1f}" class="role{" head" if n["head"] else ""}" text-anchor="middle">{esc(lab)}</text>')
    o.append('</svg>')
    return ''.join(o)

def svg_walk(d):
    sg = {s['id']: s for s in d['signs_list']}; order = [s['id'] for s in d['signs_list']]
    w, r = yield_ids(d['A_tree']), d['read_list']; DX = 40; W = DX * len(w) + 150; Ht = 112
    o = [f'<svg class="dwalk" viewBox="0 0 {W} {Ht}" width="{W}" height="{Ht}" role="img" aria-label="WALK_write {" ".join(w)}; WALK_read {" ".join(r)}">']
    o.append(f'<text x="4" y="30" class="wlab">WALK_write</text><text x="4" y="98" class="wlab">WALK_read</text>')
    for i, a in enumerate(w):
        j = r.index(a); x1 = 150 + DX * i + DX / 2; x2 = 150 + DX * j + DX / 2
        moved = i != j
        o.append(f'<line x1="{x1}" y1="40" x2="{x2}" y2="70" class="wl{" moved" if moved else ""}"/>')
    for row, seq, y in (('w', w, 32), ('r', r, 100)):
        for i, a in enumerate(seq):
            x = 150 + DX * i + DX / 2; s = sg[a]; c = hue(order.index(a), len(order))
            o.append(f'<circle cx="{x}" cy="{y - 8}" r="16" class="leafbg" style="--h:{c}"/>')
            o.append(f'<text x="{x}" y="{y}" class="hg sm" text-anchor="middle">{s["glyph"] or "?"}</text>')
    o.append('</svg>')
    return ''.join(o)

# ---------------------------------------------------------------- main
def load(path):
    ds = parse_file(path); report = []
    for d in ds:
        d['errors'] = check(d)
        d['mismatch'] = mismatches(d['A_tree'], d['B_tree']) if d['B_tree'] else []
        d['mismatch_alt'] = mismatches(d['A_tree'], d['B_alt_tree']) if d['B_alt_tree'] else []
        d['walk_write'] = yield_ids(d['A_tree'])
        g = {s['id']: s['glyph'] for s in d['signs_list']}
        d['cartouche'], d['quadrats'] = quadrats(d['A_tree'], g)
    return ds

def export(ds, out):
    keep = ['id', 'title.ja', 'title.en', 'book', 'cat', 'signs_list', 'A', 'B', 'B_alt', 'read_list', 'walk_write', 'reorder',
            'status', 'mismatch', 'mismatch_alt', 'claim.ja', 'claim.en', 'std.ja', 'std.en', 'note.ja', 'note.en', 'refs_list', 'quadrats', 'cartouche']
    data = {'standard': 'SUBLEXICAL-DERIVATIONS-v1', 'generated_by': 'tools/derivations.py',
            'derivations': [{k: d.get(k) for k in keep} for d in ds]}
    Path(out).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf8')

if __name__ == '__main__':
    src = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / 'data/derivations/rahman.drv')
    ds = load(src); bad = 0
    for d in ds:
        flag = 'ok ' if not d['errors'] else 'ERR'
        print(f"{flag} {d['id']:4} {d['cat']:9} A={height(d['A_tree'])} "
              f"{'B=' + str(height(d['B_tree'])) if d['B_tree'] else 'B=OPEN'} reorder={d['reorder']:22} "
              f"mismatch={[m['op'] + ':' + ','.join(m['leaves']) for m in d['mismatch']]}")
        for e in d['errors']: print('     !', e); bad += 1
    export(ds, src.with_suffix('.json'))
    from collections import Counter
    print('by category:', dict(Counter(d['cat'] for d in ds)), 'total', len(ds))
    sys.exit(1 if bad else 0)
