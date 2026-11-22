#!/usr/bin/env python3
"""Quadrat boundaries against word boundaries (backlog #2): BM EA 581, then BM EA 162.

Inputs (per text)
  data/<key>-lines.json      Nederhof's Unicode quadrat encoding (HieroJax, GPL-3.0), one string per line.
                             ea581 is the pilot file; ea162 is made by `--fetch` from the HieroJax repo.
  data/<key>-tla-words.json  The TLA word division of the same text, as published in AES
                             (S. D. Schweitzer, github.com/simondschweitzer/aes, CC BY-SA 4.0). Made by `--fetch`.
Output
  data/quadrat-word.json     counts, per-quadrat and per-word tables (page `boundaries`).

Line mapping: the k-th TLA line label (in order of first appearance) is taken to be the k-th HieroJax
line; the script stops if the counts differ, and reports for each TLA line whether the HieroJax line
with the lowest alignment cost is the same one (a check, not an assumption).

Method
  1. Each TLA sentence element ("token") carries its line (lineCount) and, where the editors
     encoded it, its signs: Unicode (hiero_unicode) or Gardiner codes (hiero). Codes without a
     Unicode sign (TLA/JSesh extensions such as US248Y1VARB) become a wildcard sign.
  2. Line by line, the token signs are aligned to the signs of Nederhof's quadrats by edit distance
     (match 0, wildcard 0.5, substitution 1, gap 1). Every Nederhof sign receives the token whose
     sign it matched or replaced. A Nederhof sign left over between two signs of the same token is
     given to that token; any other leftover sign stays unassigned (OPEN).
  3. A quadrat (a group with an operator node) is INSIDE if all its signs belong to one token,
     ACROSS if they belong to two or more, OPEN if any sign is unassigned and the rest do not
     already show two tokens. Lone signs are counted separately.
  4. The same counts are repeated with "words" = a token plus any following suffix pronoun
     (tokens whose transliteration begins with "="), because the TLA writes suffix pronouns as
     separate elements.
A count is not a rule, and the alignment is not an edition: where the two encodings differ,
the difference is listed, not resolved.
"""
from __future__ import annotations
import argparse, hashlib, html, json, re, sys, unicodedata, urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from quadrat_census import Parser, leaves, walk, to_unicode  # noqa: E402

HIEROJAX_COMMIT = 'da318801e00b10b4b5c5ec8d9cc6f8fddcc9eb5a'
TEXTS = [
    {'key': 'ea581', 'tla': '5D5ST6HPRRG4FEQKZZEWHNX36E', 'hierojax': 'BritishMuseumEA581', 'label': 'BM EA 581 (Intef son of Senet)'},
    {'key': 'ea162', 'tla': 'RGI3F7G3OFDJ5A44XJ7DOFL55U', 'hierojax': 'BritishMuseumEA162', 'label': 'BM EA 162 (Imeny)'},
]
AES_COMMIT = '35276d2527cca1a055e31ed5f6683e777717170f'
AES_URL = f'https://raw.githubusercontent.com/simondschweitzer/aes/{AES_COMMIT}/files/aes/_aes_sawlit.json'
WILD = '?'

def fetch_lines(T):
    """HieroJax text page -> data/<key>-lines.json (only for texts other than the pilot file)."""
    url = f'https://raw.githubusercontent.com/nederhof/hierojax/{HIEROJAX_COMMIT}/docs/texts/{T["hierojax"]}.html'
    page = urllib.request.urlopen(url).read().decode('utf8')
    sections, lines, cur = [], [], None
    for m in re.finditer(r'<h3>(.*?)</h3>|<span class="lineno">\((.*?)\)</span>\s*<span class="hierojax"[^>]*>(.*?)</span>', page, re.S):
        if m.group(1) is not None: cur = m.group(1); continue
        lines.append({'line': len(lines) + 1, 'section': cur, 'label': m.group(2), 'direction': None, 'unicode': m.group(3).strip()})
    title = re.search(r'<h2>(.*?)</h2>', page).group(1)
    out = {'source': {'object': f'{T["label"]}: HieroJax heading "{title}"',
                      'encoding': f'Mark-Jan Nederhof, HieroJax text page {T["hierojax"]}, {url} (commit {HIEROJAX_COMMIT}); HieroJax repository is GPL-3.0',
                      'direction': 'Not recorded here (OPEN); not needed for the boundary counts.',
                      'note': 'Encoding of relative positions is the editor\'s; it is not a facsimile.'},
           'lines': lines}
    (ROOT / f'data/{T["key"]}-lines.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf8')
    print(f'wrote data/{T["key"]}-lines.json:', len(lines), 'lines')

def fetch(cache: Path, T):
    TLA_TEXT = T['tla']
    if not cache.exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(AES_URL, cache)
    raw = cache.read_bytes()
    d = json.loads(raw)
    sents = [{'id': k, 'sentence_translation': v.get('sentence_translation'), 'token': v['token']}
             for k, v in d.items() if v['text'] == TLA_TEXT]
    meta = next(v for v in d.values() if v['text'] == TLA_TEXT)
    out = {
        'source': {
            'text': f'Thesaurus Linguae Aegyptiae text {TLA_TEXT} ({T["label"]}); TLA editor field (owner): "{meta["owner"]}"; '
                    f'corpus "{meta["corpus"]}"; date "{meta.get("date")}".',
            'tla': f'https://tla.digital/text/{TLA_TEXT}',
            'via': 'AES - Ancient Egyptian Sentences, S. D. Schweitzer, converted from the TLA database excerpt of January 2018 '
                   '(urn:nbn:de:kobv:b4-opus4-29190).',
            'file': AES_URL, 'sha256': hashlib.sha256(raw).hexdigest(),
            'licence': 'CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/). This extract keeps that licence.',
        },
        'sentences': sents,
    }
    (ROOT / f'data/{T["key"]}-tla-words.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf8')
    print(f'wrote data/{T["key"]}-tla-words.json:', len(sents), 'sentences,', sum(len(s['token']) for s in sents), 'tokens')

def gardiner_to_char(code):
    m = re.fullmatch(r'([A-Z][a-z]?)(\d+)([A-Z]?)', code)
    if not m:
        return None
    cat, num, suf = m.groups()
    try:
        return unicodedata.lookup(f'EGYPTIAN HIEROGLYPH {cat.upper()}{int(num):03d}{suf}')
    except KeyError:
        return None

def is_sign(ch):
    c = ord(ch)
    return 0x13000 <= c <= 0x1342F or 0x13460 <= c <= 0x143FF

def token_signs(t):
    """Return (signs, how). signs: list of chars, WILD for an unencodable sign."""
    u = html.unescape(t.get('hiero_unicode') or '')
    if u:
        return [c for c in u if is_sign(c)], 'unicode'
    if t.get('hiero'):
        codes = [c for c in re.split(r'[-:*&\s()]+', t['hiero']) if c]
        return [gardiner_to_char(c) or WILD for c in codes], 'gardiner'
    if t.get('hiero_inventar'):   # sign inventory only, order unknown
        return [WILD] * len(t['hiero_inventar'].split(';')), 'inventory'
    return [], 'none'

def align(A, B):
    """A: Nederhof signs; B: list of (sign, token). Return per-A token index or None, and ops."""
    n, m = len(A), len(B)
    INF = float('inf')
    D = [[INF] * (m + 1) for _ in range(n + 1)]
    P = [[None] * (m + 1) for _ in range(n + 1)]
    D[0][0] = 0
    for i in range(n + 1):
        for j in range(m + 1):
            if i == j == 0: continue
            best, bp = INF, None
            if i and j:
                s = B[j - 1][0]
                c = 0 if s == A[i - 1] else (0.5 if s == WILD else 1)
                if D[i - 1][j - 1] + c < best: best, bp = D[i - 1][j - 1] + c, 'M'
            if i and D[i - 1][j] + 1 < best: best, bp = D[i - 1][j] + 1, 'I'   # Nederhof sign not in TLA
            if j and D[i][j - 1] + 1 < best: best, bp = D[i][j - 1] + 1, 'D'   # TLA sign not in Nederhof
            D[i][j], P[i][j] = best, bp
    i, j, ops = n, m, []
    while i or j:
        op = P[i][j]
        if op == 'M': ops.append(('M', i - 1, j - 1)); i -= 1; j -= 1
        elif op == 'I': ops.append(('I', i - 1, None)); i -= 1
        else: ops.append(('D', None, j - 1)); j -= 1
    ops.reverse()
    lab, ex = [None] * n, [False] * n
    for op, a, b in ops:
        if op == 'M': lab[a] = B[b][1]; ex[a] = B[b][0] == A[a]
    # a token none of whose signs matched in place, but whose signs stand as one unmatched run
    # elsewhere in the line: the two encodings put it in a different order. Give it that run.
    moved = []
    placed = {B[b][1] for op, a, b in ops if op == 'M'}
    for t in dict.fromkeys(tk for _, tk in B):
        if t in placed: continue
        seq = [c for c, tk in B if tk == t]
        for k in range(n - len(seq) + 1):
            if A[k:k + len(seq)] == seq and all(lab[x] is None for x in range(k, k + len(seq))):
                for x in range(k, k + len(seq)): lab[x] = t; ex[x] = True
                moved.append(t); break
    # leftover Nederhof signs between two signs of the same token go to that token
    for k in range(n):
        if lab[k] is None:
            l = next((lab[x] for x in range(k - 1, -1, -1) if lab[x] is not None), None)
            r = next((lab[x] for x in range(k + 1, n) if lab[x] is not None), None)
            if l is not None and l == r: lab[k] = l
    return lab, ex, ops, D[n][m], moved

def classify(labels):
    known = {x for x in labels if x is not None}
    if len(known) >= 2: return 'across'
    if None in labels: return 'open'
    return 'inside'

def analyse(T):
    W = json.load(open(ROOT / f'data/{T["key"]}-tla-words.json', encoding='utf8'))
    E = json.load(open(ROOT / f'data/{T["key"]}-lines.json', encoding='utf8'))
    labels = list(dict.fromkeys(t['lineCount'] for s in W['sentences'] for t in s['token']))
    if len(labels) != len(E['lines']):
        raise SystemExit(f'{T["key"]}: {len(labels)} TLA lines vs {len(E["lines"])} HieroJax lines')
    line_of = {lab: E['lines'][k]['line'] for k, lab in enumerate(labels)}

    toks = []
    for s in W['sentences']:
        for t in s['token']:
            sig, how = token_signs(t)
            toks.append({'i': len(toks), 'sent': s['id'], 'line': line_of[t['lineCount']], 'tlaLine': t['lineCount'], 'tr': t['written_form'],
                         'pos': t.get('pos'), 'gloss': t.get('cotext_translation'), 'signs': sig, 'how': how})
    # word = token + following suffix pronouns
    word_of, wid = [], -1
    for t in toks:
        if not (t['tr'].startswith('=') and wid >= 0 and toks[t['i'] - 1]['sent'] == t['sent']): wid += 1
        word_of.append(wid)

    groups, per_line = [], []
    for ln in E['lines']:
        L = ln['line']
        frag = Parser(ln['unicode']).fragment()
        A, gidx = [], []
        for k, g in enumerate(frag, 1):
            gl = [chr(x['sign']) for x in leaves(g)]
            groups.append({'line': L, 'pos': k, 'quadrat': bool(walk(g)), 'signs': gl, 'labels': None, 'enc': to_unicode(g)})
            for c in gl: A.append(c); gidx.append(len(groups) - 1)
        B = [(c, t['i']) for t in toks if t['line'] == L for c in t['signs']]
        lab, ex, ops, cost, moved = align(A, B)
        start = len(groups) - len(frag)
        for g in range(start, len(groups)):
            groups[g]['labels'] = [lab[x] for x in range(len(A)) if gidx[x] == g]
            groups[g]['exact'] = [ex[x] for x in range(len(A)) if gidx[x] == g]
        diffs = []
        for op, ai, bj in ops:
            if op == 'M' and B[bj][0] != A[ai] and B[bj][0] != WILD:
                diffs.append({'kind': 'sub', 'nederhof': A[ai], 'tla': B[bj][0], 'token': toks[B[bj][1]]['tr']})
            elif op == 'I':
                diffs.append({'kind': 'nederhof-only', 'nederhof': A[ai], 'assigned': lab[ai] is not None})
            elif op == 'D':
                diffs.append({'kind': 'tla-only', 'tla': B[bj][0], 'token': toks[B[bj][1]]['tr']})
        exact = sum(1 for op, ai, bj in ops if op == 'M' and B[bj][0] == A[ai])
        wild = sum(1 for op, ai, bj in ops if op == 'M' and B[bj][0] == WILD)
        # check: is the HieroJax line with the lowest cost for this TLA line the mapped one?
        best = min(E['lines'], key=lambda o: align([chr(x['sign']) for g in Parser(o['unicode']).fragment() for x in leaves(g)], B)[3] / max(1, len(B)))
        per_line.append({'line': L, 'tlaLine': labels[[line_of[l] for l in labels].index(L)], 'bestMatch': best['line'] == L,
                         'dir': ln.get('direction'), 'orderDiffers': [toks[t]['tr'] for t in moved], 'nederhofSigns': len(A), 'tlaSigns': len(B),
                         'exact': exact, 'wildcard': wild, 'cost': cost, 'diffs': diffs})

    def census(key):
        """key maps token index -> unit id (token itself, or word)."""
        res = {'quadrats': Counter(), 'lone': Counter()}
        rows = []
        for g in groups:
            labs = [None if x is None else key(x) for x in g['labels']]
            c = classify(labs)
            res['quadrats' if g['quadrat'] else 'lone'][c] += 1
            exact_units = {u for u, e in zip(labs, g['exact']) if e and u is not None}
            if g['quadrat'] and c == 'across' and len(exact_units) >= 2: res['quadrats']['acrossExact'] = res['quadrats'].get('acrossExact', 0) + 1
            if g['quadrat'] and c == 'inside' and all(g['exact']): res['quadrats']['insideExact'] = res['quadrats'].get('insideExact', 0) + 1
            if g['quadrat']:
                rows.append({'line': g['line'], 'pos': g['pos'], 'u': g['enc'], 'class': c,
                             'units': sorted({x for x in labs if x is not None}), 'open': labs.count(None)})
        # units: how many groups does each unit touch, and does it share a group?
        span, share = Counter(), set()
        for g in groups:
            labs = {key(x) for x in g['labels'] if x is not None}
            for u in labs: span[u] += 1
            if len(labs) >= 2: share |= labs
        units = sorted({key(t['i']) for t in toks})
        written = [u for u in units if span[u]]
        open_units = set()
        for g in groups:
            if None in g['labels']:
                for x in g['labels']:
                    if x is not None: open_units.add(key(x))
        dist = Counter()
        for u in written:
            if u in open_units: dist['open'] += 1
            elif span[u] == 1 and u not in share: dist['oneGroupAlone'] += 1
            elif span[u] == 1: dist['oneGroupShared'] += 1
            else: dist['multiGroup'] += 1
        res['units'] = {'total': len(units), 'written': len(written), 'noSigns': len(units) - len(written),
                        'dist': dict(dist), 'groupsTouched': dict(sorted(Counter(span[u] for u in written).items()))}
        res['quadrats'] = dict(res['quadrats']); res['lone'] = dict(res['lone'])
        gi, k = {}, 0
        for g in groups:                      # sign positions in stream order
            for x in g['labels']:
                if x is not None: gi.setdefault(key(x), set()).add(k)
                k += 1
        res['discontinuous'] = [' '.join(toks[t]['tr'] for t in range(len(toks)) if key(t) == u)
                                for u, ks in gi.items() if max(ks) - min(ks) + 1 != len(ks)]  # signs of another unit (or unassigned) in between
        dirs = {ln['line']: ln.get('direction') for ln in E['lines']}
        if all(dirs.values()):
            res['quadratsByDirection'] = {d: dict(Counter(r['class'] for r in rows if dirs[r['line']] == d))
                                          for d in dict.fromkeys(dirs.values())}
        res['unplaced'] = [toks[i]['tr'] if key is not None else None for i in range(len(toks))
                           if toks[i]['signs'] and not any(key(x) == key(i) for g in groups for x in g['labels'] if x is not None)]
        return res, rows

    tok_c, tok_rows = census(lambda i: i)
    word_c, word_rows = census(lambda i: word_of[i])

    # what kinds of token pair share an ACROSS quadrat (by TLA pos of the members)
    pair = Counter()
    for r in tok_rows:
        if r['class'] == 'across':
            pair[' + '.join(toks[i]['pos'] or '?' for i in r['units'])] += 1
    # tokens whose TLA signs are absent from the alignment
    no_sign_tokens = [t['tr'] for t in toks if not t['signs']]
    how = Counter(t['how'] for t in toks)

    tot_n = sum(p['nederhofSigns'] for p in per_line)
    out = {
        'key': T['key'], 'label': T['label'],
        'sources': {'quadrats': E['source'], 'words': W['source']},
        'coverage': {
            'linesMappedAndBestMatch': sum(p['bestMatch'] for p in per_line), 'lines': len(per_line),
            'tlaSentences': len(W['sentences']), 'tlaTokens': len(toks), 'words': len(set(word_of)),
            'tokenSignSource': dict(how), 'tokensWithoutSigns': no_sign_tokens,
            'nederhofSigns': tot_n, 'tlaSigns': sum(p['tlaSigns'] for p in per_line),
            'exact': sum(p['exact'] for p in per_line), 'wildcard': sum(p['wildcard'] for p in per_line),
            'substituted': sum(1 for p in per_line for d in p['diffs'] if d['kind'] == 'sub'),
            'nederhofOnly': sum(1 for p in per_line for d in p['diffs'] if d['kind'] == 'nederhof-only'),
            'nederhofOnlyUnassigned': sum(1 for p in per_line for d in p['diffs'] if d['kind'] == 'nederhof-only' and not d['assigned']),
            'tlaOnly': sum(1 for p in per_line for d in p['diffs'] if d['kind'] == 'tla-only'),
            'groups': len(groups), 'quadrats': sum(g['quadrat'] for g in groups),
        },
        'byToken': tok_c, 'byWord': word_c, 'acrossPairsByPOS': dict(pair.most_common()),
        'perLine': per_line,
        'quadratRows': [r | {'tokens': [toks[i]['tr'] for i in r['units']]} for r in tok_rows],
        'tokens': [{k: t[k] for k in ('i', 'line', 'tr', 'pos', 'gloss', 'how')} | {'signs': ''.join(t['signs']), 'word': word_of[t['i']]} for t in toks],
    }
    print(T['key'], json.dumps(out['coverage'], ensure_ascii=False))
    print('  token', json.dumps(tok_c, ensure_ascii=False))
    print('  word ', json.dumps(word_c, ensure_ascii=False))
    print('  pairs', dict(pair.most_common(12)))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fetch', action='store_true', help='(re)build the data/<key>-*.json inputs from AES and HieroJax at the pinned commits')
    ap.add_argument('--cache', default='/tmp/aes/_aes_sawlit.json')
    a = ap.parse_args()
    for T in TEXTS:
        if a.fetch or not (ROOT / f'data/{T["key"]}-tla-words.json').exists():
            fetch(Path(a.cache), T)
        if T['key'] != 'ea581' and (a.fetch or not (ROOT / f'data/{T["key"]}-lines.json').exists()):
            fetch_lines(T)
    res = [analyse(T) for T in TEXTS]
    out = {'method': __doc__.split('Method')[1].split('A count')[0].strip(),
           'note': 'A count is not a rule. The alignment is not an edition.', 'texts': res}
    (ROOT / 'data/quadrat-word.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf8')

if __name__ == '__main__':
    main()
