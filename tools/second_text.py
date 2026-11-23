#!/usr/bin/env python3
"""Second texts: does the share of horizontal joins rise in columns outside EA 581?

Input   HieroJax text pages (M.-J. Nederhof, GPL-3.0) at a fixed commit, fetched once and cached
        in data/second-text-lines.json (sections, line labels, Unicode strings, orientation evidence).
        data/ea581-lines.json for the EA 581 comparison (same counting rule).
Output  data/second-text.json

Orientation is never guessed. A line is a ROW or a COLUMN only when the HieroJax page itself says
so (section heading "rows"/"columns", or a note such as "the rightmost three columns"), or when the
British Museum collection record states the number of rows/lines of that part and it matches the
number of encoded lines. Everything else (scene captions, lunettes, unlabelled registers) is
excluded and listed as excluded.

Counting rule = tools/quadrat_census.py: a node is an operator application of arity >= 2
(vertical joiner, horizontal joiner, insertion, overlay). Enclosures (cartouches, U+1343C/D)
are parsed (HieroJax grammar, "enclosure") but the enclosure itself is not counted as a node;
nodes inside an enclosure are counted separately and left out of the main comparison.

Tests (both one-sided: columns have the larger share of horizontal joins):
  exact line-label permutation: all ways of choosing which lines are columns, keeping the
     number of column lines fixed; statistic = pooled hor share in columns - in rows.
     Lines, not nodes, are the units, because nodes in one line are not independent.
  Fisher's exact test on the 2x2 node table, for comparison only (treats nodes as independent).
A count is not a rule.
"""
from __future__ import annotations
import itertools, json, math, random, re, sys, urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from quadrat_census import Parser, VJ, HJ, BS, ES, OV, INS, MIRROR  # noqa: E402

COMMIT = 'da318801e00b10b4b5c5ec8d9cc6f8fddcc9eb5a'
RAW = 'https://raw.githubusercontent.com/nederhof/hierojax/{c}/docs/texts/{p}.html'
LIVE = 'https://nederhof.github.io/hierojax/texts/{p}.html'
BM = 'https://www.britishmuseum.org/collection/object/Y_EA{n}'

# Orientation evidence, per text: (section, note) -> (orientation, evidence)
TEXTS = [
 {'key': 'ea614', 'page': 'BritishMuseumEA614', 'bm': 614, 'label': 'BM EA 614 (Tjetji)',
  'orient': {('rows', None): ('row', 'HieroJax heading "rows" (14 lines); BM record: "a fourteen-line autobiographical inscription reading from right to left"'),
             ('columns', None): ('col', 'HieroJax heading "columns" (5 lines); BM record: "an elaborate offering prayer written in five vertical rows" / "The vertical columns of the offering prayer"')}},
 {'key': 'ea567', 'page': 'BritishMuseumEA567', 'bm': 567, 'label': 'BM EA 567 (Amenemhat)',
  'orient': {('rows', None): ('row', 'HieroJax heading "rows" (24 lines); the BM record does not state the layout'),
             ('columns', None): ('col', 'HieroJax heading "columns" (4 lines); the BM record does not state the layout')}},
 {'key': 'ea162', 'page': 'BritishMuseumEA162', 'bm': 162, 'label': 'BM EA 162 (Imeny)',
  'orient': {('upper register', None): ('row', 'BM record: "five rows of recessed Hieroglyphic text above two sunk relief figured scenes" (HieroJax upper register: 5 lines)'),
             ('middle register', 'continuation of the text in the rightmost three columns'): ('col', 'HieroJax note: "continuation of the text in the rightmost three columns" (lines 6-8)')}},
 {'key': 'ea562', 'page': 'BritishMuseumEA562', 'bm': 562, 'label': 'BM EA 562 (Intef)',
  'orient': {('main text', None): ('row', 'BM record: "fifteen rows of Hieroglyphic text including the cartouches of Senusret I" (HieroJax main text: 15 lines)')}},
 {'key': 'ea101', 'page': 'BritishMuseumEA101', 'bm': 101, 'label': 'BM EA 101 (Nebipusenusret)',
  'orient': {('central register', 'rightmost columns'): ('col', 'HieroJax note: "rightmost columns" (9 lines); BM record: "columns and rows of Hieroglyphic text"')}},
]

ENC_OPEN = {0x13258, 0x13259, 0x1325A, 0x13379, 0x1342F, 0x13286, 0x13288}
ENC_CLOSE = {0x1325B, 0x1325C, 0x1325D, 0x13282, 0x1337A, 0x1337B, 0x13287, 0x13289}
BE, EE, BWE, EWE = 0x1343C, 0x1343D, 0x1343E, 0x1343F
DAMAGE = set(range(0x13447, 0x13456))


class EncParser(Parser):
    """quadrat_census.Parser plus the HieroJax 'enclosure' production."""
    def at_enclosure(self):
        c = self.peek()
        if c in (BE, BWE): return True
        if c in ENC_OPEN:
            j = self.i + 1
            if j < len(self.s) and self.s[j] in DAMAGE: j += 1
            return j < len(self.s) and self.s[j] in (BE, BWE)
        return False
    def enclosure(self):
        n = {'op': 'enc', 'args': []}
        if self.peek() in ENC_OPEN:
            n['open'] = self.take()
            if self.peek() in DAMAGE: n['openDamage'] = self.take()
        b = self.take(); end = EE if b == BE else EWE
        n['walled'] = b == BWE
        while self.peek() != end:
            if self.peek() is None: raise ValueError('unclosed enclosure')
            n['args'].append(self.vgroup())
        self.take(end)
        if self.peek() in ENC_CLOSE:
            n['close'] = self.take()
            if self.peek() in DAMAGE: n['closeDamage'] = self.take()
        return n
    def basic(self):
        if self.at_enclosure(): return self.enclosure()
        return super().basic()
    def ingroup(self):
        if self.at_enclosure(): return self.enclosure()
        return super().ingroup()


def to_u(n):
    if 'sign' in n:
        s = chr(n['sign'])
        if 'rot' in n: s += chr(0xFE00 + n['rot'] - 1)
        if n.get('mirror'): s += chr(MIRROR)
        if 'damage' in n: s += chr(n['damage'])
        return s
    if n['op'] == 'enc':
        s = ''
        if 'open' in n: s += chr(n['open']) + (chr(n['openDamage']) if 'openDamage' in n else '')
        s += chr(BWE if n['walled'] else BE) + ''.join(to_u(a) for a in n['args']) + chr(EWE if n['walled'] else EE)
        if 'close' in n: s += chr(n['close']) + (chr(n['closeDamage']) if 'closeDamage' in n else '')
        return s
    def br(x, need):
        u = to_u(x)
        return chr(BS) + u + chr(ES) if need else u
    if n['op'] == 'ver':
        return chr(VJ).join(br(a, a.get('op') == 'ver') for a in n['args'])
    if n['op'] == 'hor':
        return chr(HJ).join(br(a, a.get('op') in ('ver', 'hor')) for a in n['args'])
    if n['op'] == 'ovl':
        return br(n['args'][0], 'op' in n['args'][0] and n['args'][0]['op'] != 'enc') + chr(OV) + br(n['args'][1], 'op' in n['args'][1])
    rev = {v: k for k, v in INS.items()}
    s = br(n['args'][0], n['args'][0].get('op') in ('ver', 'hor'))
    for p, a in zip(n['pos'], n['args'][1:]):
        s += chr(rev[p]) + br(a, 'op' in a and a['op'] != 'enc')
    return s


def nodes(n, inside=False, acc=None):
    """(op, insideEnclosure) for each operator node; 'enc' itself is not a node."""
    if acc is None: acc = []
    if 'op' in n:
        if n['op'] == 'enc':
            for a in n['args']: nodes(a, True, acc)
        else:
            acc.append((n['op'], inside))
            for a in n['args']: nodes(a, inside, acc)
    return acc


def count_enc(n):
    if 'op' not in n: return 0
    return (n['op'] == 'enc') + sum(count_enc(a) for a in n['args'])


def fetch_lines():
    out = []
    for T in TEXTS:
        url = RAW.format(c=COMMIT, p=T['page'])
        page = urllib.request.urlopen(url).read().decode('utf8')
        body = page[page.find('<body>'):page.find('<h2>Links')]
        sec = note = lab = None; lines = []
        tok = re.finditer(r'<h3>(.*?)</h3>|(?:^|\n)\((?!\d)([^)\n]*)\)\s*\n|<span class="lineno">\(([^)<]*)\)</span>\s*(?=<span class="hierojax")|<span class="hierojax"[^>]*>(.*?)</span>', body, re.S)
        for m in tok:
            if m.group(1) is not None: sec, note = m.group(1), None; continue
            if m.group(2) is not None: note = m.group(2); continue
            if m.group(3) is not None: lab = m.group(3); continue
            o = T['orient'].get((sec, note))
            lines.append({'n': len(lines) + 1, 'section': sec, 'note': note, 'label': lab,
                          'orientation': o[0] if o else None, 'unicode': m.group(4).strip()})
            lab = None
        title = re.search(r'<h2>(.*?)</h2>', page).group(1)
        out.append({'key': T['key'], 'label': T['label'], 'title': title, 'hierojax': LIVE.format(p=T['page']),
                    'raw': url, 'bm': BM.format(n=T['bm']),
                    'evidence': [{'section': s, 'note': nt, 'orientation': o, 'evidence': e} for (s, nt), (o, e) in T['orient'].items()],
                    'lines': lines})
    data = {'source': {'encoding': f'Mark-Jan Nederhof, HieroJax text pages, repository nederhof/hierojax commit {COMMIT} (GPL-3.0). '
                                   'This file keeps that licence.',
                       'note': 'Encoding of relative positions is the editor\'s; it is not a facsimile. '
                               'orientation: row / col where the evidence field says so, otherwise null (excluded).'},
            'texts': out}
    (ROOT / 'data/second-text-lines.json').write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf8')
    return data


def analyse_lines(lines):
    per_line, fails = [], []
    for ln in lines:
        try:
            frag = EncParser(ln['unicode']).fragment()
        except ValueError as e:
            fails.append({'n': ln['n'], 'error': str(e)}); continue
        assert ''.join(to_u(g) for g in frag) == ln['unicode'], f"round trip failed, line {ln['n']}"
        ns = [x for g in frag for x in nodes(g)]
        main = Counter(op for op, inside in ns if not inside)
        inner = Counter(op for op, inside in ns if inside)
        quads = [g for g in frag if any(not i for _, i in nodes(g))]
        per_line.append({'n': ln['n'], 'label': ln['label'], 'section': ln['section'], 'orientation': ln['orientation'],
                         'groups': len(frag), 'quadrats': len(quads), 'enclosures': sum(count_enc(g) for g in frag),
                         'ops': dict(main), 'opsInsideEnclosure': dict(inner),
                         'nodes': sum(main.values()), 'hor': main.get('hor', 0)})
    return per_line, fails


def summary(pl):
    ops = Counter()
    for l in pl: ops.update(l['ops'])
    n = sum(ops.values())
    return {'lines': len(pl), 'quadrats': sum(l['quadrats'] for l in pl), 'nodes': n, 'ops': dict(ops.most_common()),
            'hor': ops.get('hor', 0), 'horShare': round(ops.get('hor', 0) / n, 4) if n else None}


def exact_perm(rows, cols):
    """One-sided exact permutation over line labels. Returns (p, permutations, at least as extreme)."""
    L = rows + cols; k = len(cols)
    H = sum(l['hor'] for l in L); N = sum(l['nodes'] for l in L)
    def stat(ch, cn):
        rh, rn = H - ch, N - cn
        return (ch / cn if cn else 0) - (rh / rn if rn else 0)
    obs = stat(sum(l['hor'] for l in cols), sum(l['nodes'] for l in cols))
    hs = [l['hor'] for l in L]; ns = [l['nodes'] for l in L]
    tot = ge = 0
    for comb in itertools.combinations(range(len(L)), k):
        ch = sum(hs[i] for i in comb); cn = sum(ns[i] for i in comb)
        tot += 1; ge += stat(ch, cn) >= obs - 1e-12
    return {'p': ge / tot, 'permutations': tot, 'atLeastAsExtreme': ge, 'observedDiff': round(obs, 4)}


def fisher_one_sided(a, b, c, d):
    """2x2 [[a (col hor), b (col other)], [c (row hor), d (row other)]]: P(col hor >= a)."""
    r1, c1, n = a + b, a + c, a + b + c + d
    def pmf(x): return math.comb(c1, x) * math.comb(n - c1, r1 - x) / math.comb(n, r1)
    return sum(pmf(x) for x in range(a, min(r1, c1) + 1))


def stratified_mc(strata, iters=200000, seed=20261123):
    """Permute line labels within each text; statistic = sum over texts of (col share - row share)."""
    rng = random.Random(seed)
    def diff(rows, cols):
        ch = sum(l['hor'] for l in cols); cn = sum(l['nodes'] for l in cols)
        rh = sum(l['hor'] for l in rows); rn = sum(l['nodes'] for l in rows)
        return (ch / cn if cn else 0) - (rh / rn if rn else 0)
    obs = sum(diff(r, c) for r, c in strata)
    ge = 0
    for _ in range(iters):
        s = 0
        for r, c in strata:
            L = r + c; rng.shuffle(L)
            s += diff(L[len(c):], L[:len(c)])
        ge += s >= obs - 1e-12
    return {'p': (ge + 1) / (iters + 1), 'atLeastAsExtreme': ge, 'iterations': iters, 'seed': seed, 'observedSumDiff': round(obs, 4)}


def main():
    cache = ROOT / 'data/second-text-lines.json'
    data = json.load(open(cache, encoding='utf8')) if cache.exists() and '--fetch' not in sys.argv else fetch_lines()
    results, strata = [], []
    # EA 581: same rule, from the pilot file (orientation from the St Andrews RES, see data/ea581-lines.json)
    ea581 = json.load(open(ROOT / 'data/ea581-lines.json', encoding='utf8'))
    l581 = [{'n': l['line'], 'label': str(l['line']), 'section': None, 'unicode': l['unicode'],
             'orientation': {'hrl': 'row', 'vrl': 'col'}[l['direction']]} for l in ea581['lines']]
    for key, label, lines, excluded_note in [('ea581', 'BM EA 581 (Intef son of Senet)', l581, None)] + \
            [(t['key'], t['label'], t['lines'], None) for t in data['texts']]:
        used = [l for l in lines if l['orientation']]
        excl = [l for l in lines if not l['orientation']]
        pl, fails = analyse_lines(used)
        rows = [l for l in pl if l['orientation'] == 'row']; cols = [l for l in pl if l['orientation'] == 'col']
        R, C = summary(rows), summary(cols)
        r = {'key': key, 'label': label, 'rows': R, 'cols': C, 'parseFailures': fails,
             'enclosures': sum(l['enclosures'] for l in pl),
             'nodesInsideEnclosures': sum(sum(l['opsInsideEnclosure'].values()) for l in pl),
             'opsInsideEnclosures': dict(sum((Counter(l['opsInsideEnclosure']) for l in pl), Counter())),
             'excludedLines': [{'n': l['n'], 'section': l['section'], 'note': l.get('note'), 'label': l['label']} for l in excl],
             'lines': pl}
        if rows and cols:
            r['exactPermutation'] = exact_perm(rows, cols)
            r['fisherNodes'] = fisher_one_sided(C['hor'], C['nodes'] - C['hor'], R['hor'], R['nodes'] - R['hor'])
            def withenc(ls):
                h = sum(l['hor'] + l['opsInsideEnclosure'].get('hor', 0) for l in ls); n = sum(l['nodes'] + sum(l['opsInsideEnclosure'].values()) for l in ls)
                return {'nodes': n, 'hor': h, 'horShare': round(h / n, 4)}
            r['withEnclosureNodes'] = {'rows': withenc(rows), 'cols': withenc(cols)}
            if key != 'ea581': strata.append((rows, cols))
        else:
            r['oneSided'] = 'only ' + ('columns' if cols else 'rows') + ' have checked orientation'
        results.append(r)
        print(key, 'rows', R['lines'], R['nodes'], R['hor'], R['horShare'], '| cols', C['lines'], C['nodes'], C['hor'], C['horShare'],
              '| enc', r['enclosures'], r['nodesInsideEnclosures'], '| excl', len(excl), '| fail', len(fails),
              r.get('exactPermutation'), r.get('fisherNodes'))
    pooled_r = summary([l for r in results if r['key'] not in ('ea581',) and r['rows']['lines'] and r['cols']['lines'] for l in r['lines'] if l['orientation'] == 'row'])
    pooled_c = summary([l for r in results if r['key'] not in ('ea581',) and r['rows']['lines'] and r['cols']['lines'] for l in r['lines'] if l['orientation'] == 'col'])
    out = {'source': data['source'] | {'ea581': ea581['source']},
           'rule': __doc__.split('Counting rule = ')[1].split('Tests')[0].strip(),
           'tests': __doc__.split('Tests ')[1].split('A count is')[0].strip(),
           'texts': results,
           'pooledSecondTexts': {'texts': [r['key'] for r in results if r['key'] != 'ea581' and r['rows']['lines'] and r['cols']['lines']],
                                 'rows': pooled_r, 'cols': pooled_c, 'stratifiedPermutation': stratified_mc(strata)}}
    (ROOT / 'data/second-text.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf8')
    print('pooled', pooled_r['nodes'], pooled_r['hor'], pooled_r['horShare'], pooled_c['nodes'], pooled_c['hor'], pooled_c['horShare'], out['pooledSecondTexts']['stratifiedPermutation'])


if __name__ == '__main__':
    main()
