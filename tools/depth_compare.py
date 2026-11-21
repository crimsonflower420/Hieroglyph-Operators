#!/usr/bin/env python3
"""Where the depth sits: layout-tree height against function-tree height, with kanji for comparison.

Inputs (all in this repository):
  data/derivations/rahman.drv        26 two-layer derivations (bracket form, source of truth; notation v1)
  data/pilot-census.json             BM EA 581 (Intef) quadrat census (layout only; written by tools/quadrat_census.py)
  data/kanji-height-reference.json   per-character height of the 2,136 jōyō kanji (written by tools/kanji_heights.py)
Output:
  data/depth-compare.json

Counting rule (the same on all three):
  height  the largest number of operator nodes of arity >= 2 on one path from the root to a leaf.
          Unary nodes (CARTOUCHE in layer A, ABBR in layer B, one-slot wrapper groups in KanjiVG) add nothing.
Per derivation:
  hQ      the largest height of one quadrat inside the word (the quadrats are the daughters of LINE k, or the
          whole layer A when it is a single quadrat)
  hA      the height of layer A (= hQ, plus 1 when the signs are spread over 2 or more quadrats by LINE k)
  hB      the height of layer B (OPEN trees are left out)
  hBx     the largest number of layer-B nodes on one path whose leaves lie in 2 or more quadrats ("across")
  hBin    the largest number of layer-B nodes on one path whose leaves lie inside one quadrat ("inside")
  unit    'word', or 'multi' when layer B contains PHRASE, NAME, GEN, COORD or ATTR (names, phrases, compounds)
A count is not a rule. The trees are HYPOTHESIS (notation v1); nothing here is a syntactic claim.
"""
import json, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import derivations as DV

ROOT = Path(__file__).resolve().parent.parent
MULTI = {'PHRASE', 'NAME', 'GEN', 'COORD', 'ATTR'}

def h(t):
    if 'id' in t: return 0
    return max(h(k) for k in t['kids']) + (1 if len(t['kids']) >= 2 else 0)

def quadrat_units(A):
    t = A
    if 'op' in t and t['op'] == 'CARTOUCHE': t = t['kids'][0]
    if 'op' in t and DV.op_base(t['op']) == 'LINE': return t['kids'], len(t['kids']) >= 2
    return [t], False

def path_count(t, pred):
    if 'id' in t: return 0
    here = 1 if (len(t['kids']) >= 2 and pred(t)) else 0
    return here + max(path_count(k, pred) for k in t['kids'])

def ops_in(t): return [] if 'id' in t else [DV.op_base(t['op'])] + [o for k in t['kids'] for o in ops_in(k)]

def row(d):
    A, B = d['A_tree'], d['B_tree']
    qs, line = quadrat_units(A)
    qof = {}
    for i, q in enumerate(qs):
        for lid in DV.yield_ids(q): qof[lid] = i
    hQ = max(h(q) for q in qs); hA = h(A)
    assert hA == hQ + (1 if line else 0), d['id']
    r = {'id': d['id'], 'cat': d['cat'], 'signs': len(d['signs_list']), 'quadrats': len(qs), 'hQ': hQ, 'hA': hA,
         'cartouche': d['cartouche'], 'reorder': d['reorder'], 'mismatch': len(d['mismatch'])}
    def span(t): return len({qof[l] for l in DV.yield_ids(t)})
    for key, T in (('', B), ('_alt', d['B_alt_tree'])):
        if T is None:
            if key == '': r.update({'hB': None, 'hBx': None, 'hBin': None, 'unit': None})
            continue
        r['hB' + key] = h(T)
        r['hBx' + key] = path_count(T, lambda n: span(n) >= 2)
        r['hBin' + key] = path_count(T, lambda n: span(n) == 1)
        if key == '': r['unit'] = 'multi' if MULTI & set(ops_in(T)) else 'word'
    return r

def dist(vals): c = Counter(vals); return {str(k): c[k] for k in sorted(c)}
def mean(vals): return round(sum(vals) / len(vals), 3) if vals else None

def main():
    ds = DV.load(ROOT / 'data/derivations/rahman.drv')
    if any(d['errors'] for d in ds): sys.exit('derivation errors; run tools/derivations.py')
    rows = [row(d) for d in ds]
    withB = [r for r in rows if r['hB'] is not None]
    words = [r for r in withB if r['unit'] == 'word']
    def summ(rs):
        return {
            'n': len(rs),
            'hQ': dist(r['hQ'] for r in rs), 'hA': dist(r['hA'] for r in rs), 'hB': dist(r['hB'] for r in rs),
            'meanHQ': mean([r['hQ'] for r in rs]), 'meanHA': mean([r['hA'] for r in rs]), 'meanHB': mean([r['hB'] for r in rs]),
            'B_gt_A': sum(r['hB'] > r['hA'] for r in rs), 'B_eq_A': sum(r['hB'] == r['hA'] for r in rs),
            'B_lt_A': sum(r['hB'] < r['hA'] for r in rs),
            'B_gt_Q': sum(r['hB'] > r['hQ'] for r in rs), 'B_eq_Q': sum(r['hB'] == r['hQ'] for r in rs),
            'B_lt_Q': sum(r['hB'] < r['hQ'] for r in rs),
            'multiQuadrat': sum(r['quadrats'] >= 2 for r in rs),
            'hBx': dist(r['hBx'] for r in rs), 'hBin': dist(r['hBin'] for r in rs),
            'meanHBx': mean([r['hBx'] for r in rs]), 'meanHBin': mean([r['hBin'] for r in rs]),
            'Bx_gt_in': sum(r['hBx'] > r['hBin'] for r in rs), 'Bx_eq_in': sum(r['hBx'] == r['hBin'] for r in rs),
            'Bx_lt_in': sum(r['hBx'] < r['hBin'] for r in rs),
        }
    P = json.load(open(ROOT / 'data/pilot-census.json', encoding='utf8'))['stela']['census']
    intef_h = {'0': P['single'], **P['height']}
    assert sum(intef_h.values()) == P['groups']
    K = json.load(open(ROOT / 'data/kanji-height-reference.json', encoding='utf8'))
    out = {
        'generated_by': 'tools/depth_compare.py',
        'standard': 'SUBLEXICAL-DERIVATIONS-v1 (notation v1); every tree HYPOTHESIS',
        'definition': 'height = largest number of operator nodes of arity >= 2 on one root-to-leaf path; unary nodes add nothing',
        'rahman': {'all': summ(withB), 'words': summ(words), 'openB': [r['id'] for r in rows if r['hB'] is None],
                   'multi': [r['id'] for r in withB if r['unit'] == 'multi'], 'rows': rows},
        'intef': {'source': 'data/pilot-census.json (stela census, BM EA 581, Nederhof HieroJax encoding)',
                  'groups': P['groups'], 'height': intef_h,
                  'mean': round(sum(int(k) * v for k, v in intef_h.items()) / P['groups'], 3),
                  'function': 'OPEN: no word segmentation or sign-function annotation for EA 581 in this repository'},
        'kanji': {'source': K['_source'], 'chars': K['chars'], 'height': K['height'], 'mean': K['mean']},
    }
    (ROOT / 'data/depth-compare.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf8')
    for k in ('all', 'words'):
        s = out['rahman'][k]; print(k, {x: s[x] for x in s})
    print('intef', out['intef']['height'], out['intef']['mean']); print('kanji', K['height'], K['mean'])
    for r in rows: print(r)

if __name__ == '__main__':
    main()
