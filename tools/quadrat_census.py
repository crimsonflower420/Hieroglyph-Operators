#!/usr/bin/env python3
"""Quadrat census: Unicode Egyptian hieroglyphic text -> operator trees -> counts.

Input  data/ea581-lines.json   (Nederhof's Unicode encoding of BM EA 581, one string per line)
       data/sign-names.json    (code point -> Unicode name, from UnicodeData.txt 18.0.0)
Output data/pilot-census.json  and  site/js/pilot-data.js

Parsing follows the grammar on https://nederhof.github.io/hierojax/syntax.html
(see also Nederhof, L2/24-079). Only the parts this text needs are implemented:
joiners, segments, the seven insertion controls, overlay, mirroring, rotation
variation selectors, damage modifiers. Brackets and enclosures raise an error.

Definitions (chosen to match the kanji site's arity census where they can):
  group     a top-level unit of the fragment (a quadrat, or a lone sign).
  node      an operator application with arity >= 2.
  arity     vertical / horizontal: number of members as encoded (a:b:c = 3).
            insertion: 1 + number of inserted groups. overlay: 2.
  depth     the quadrat's root node is depth 1; each step into a child node adds 1.
  height    the largest node depth in the quadrat (0 for a lone sign).
A count is not a rule. Nothing here claims the trees are grammar.
"""
from __future__ import annotations
import json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VJ, HJ, BS, ES, OV = 0x13430, 0x13431, 0x13437, 0x13438, 0x13436
INS = {0x13432: 'ts', 0x13433: 'bs', 0x13434: 'te', 0x13435: 'be',
       0x13439: 'm', 0x1343A: 't', 0x1343B: 'b'}
MIRROR = 0x13440
DAMAGE = set(range(0x13447, 0x13456))
VS = set(range(0xFE00, 0xFE07))

def is_sign(c):
    return 0x13000 <= c <= 0x1342F or 0x13460 <= c <= 0x143FF or 0x13441 <= c <= 0x13446

class Parser:
    def __init__(self, s):
        self.s = [ord(ch) for ch in s]; self.i = 0
    def peek(self):
        return self.s[self.i] if self.i < len(self.s) else None
    def take(self, want=None):
        c = self.peek()
        if want is not None and c != want:
            raise ValueError(f'expected U+{want:X} at {self.i}, got {c!r}')
        self.i += 1; return c
    def fragment(self):
        out = []
        while self.peek() is not None:
            out.append(self.vgroup())
        return out
    def vgroup(self):
        items = [self.hgroup()]
        while self.peek() == VJ:
            self.take(); items.append(self.hgroup())
        return items[0] if len(items) == 1 else {'op': 'ver', 'args': items}
    def hgroup(self):
        items = [self.hsub()]
        while self.peek() == HJ:
            self.take(); items.append(self.hsub())
        return items[0] if len(items) == 1 else {'op': 'hor', 'args': items}
    def hsub(self):
        if self.peek() == BS:
            self.take(); g = self.vgroup(); self.take(ES)
            if self.peek() == OV:          # bracketed flat group before an overlay
                self.take(); g = {'op': 'ovl', 'args': [g, self.flat()]}
            return self.insertions(g)
        return self.basic()
    def basic(self):
        return self.insertions(self.core())
    def insertions(self, base):
        ins = []
        while self.peek() in INS:
            pos = INS[self.take()]; ins.append((pos, self.ingroup()))
        if not ins:
            return base
        return {'op': 'ins', 'pos': [p for p, _ in ins], 'args': [base] + [g for _, g in ins]}
    def ingroup(self):
        if self.peek() == BS:
            self.take(); g = self.vgroup(); self.take(ES); return g
        return self.core()
    def core(self):
        a = self.literal()
        if self.peek() == OV:
            self.take(); return {'op': 'ovl', 'args': [a, self.flat()]}
        return a
    def flat(self):
        if self.peek() == BS:
            self.take(); g = self.vgroup(); self.take(ES); return g
        return self.literal()
    def literal(self):
        c = self.peek()
        if c is None or not is_sign(c):
            raise ValueError(f'expected sign at {self.i}, got {c!r} ({chr(c) if c else ""})')
        self.take(); leaf = {'sign': c}
        if self.peek() in VS: leaf['rot'] = self.take() - 0xFE00 + 1
        if self.peek() == MIRROR: self.take(); leaf['mirror'] = True
        if self.peek() in DAMAGE: leaf['damage'] = self.take()
        return leaf

def op_label(n):
    return n['op'] if n['op'] != 'ins' else 'ins:' + '+'.join(n['pos'])

def walk(n, depth=1, acc=None):
    """Yield (node, depth) for every operator node."""
    if acc is None: acc = []
    if 'op' in n:
        acc.append((n, depth))
        for a in n['args']: walk(a, depth + 1, acc)
    return acc

def leaves(n):
    return [n] if 'sign' in n else [l for a in n['args'] for l in leaves(a)]

def arity(n):
    return len(n['args'])

def to_unicode(n, top=True):
    if 'sign' in n:
        s = chr(n['sign'])
        if 'rot' in n: s += chr(0xFE00 + n['rot'] - 1)
        if n.get('mirror'): s += chr(MIRROR)
        if 'damage' in n: s += chr(n['damage'])
        return s
    def br(x, need):
        u = to_unicode(x, False)
        return chr(BS) + u + chr(ES) if need else u
    if n['op'] == 'ver':
        return chr(VJ).join(br(a, a.get('op') == 'ver') for a in n['args'])
    if n['op'] == 'hor':
        return chr(HJ).join(br(a, a.get('op') in ('ver', 'hor')) for a in n['args'])
    if n['op'] == 'ovl':
        return br(n['args'][0], 'op' in n['args'][0]) + chr(OV) + br(n['args'][1], 'op' in n['args'][1])
    rev = {v: k for k, v in INS.items()}
    s = br(n['args'][0], n['args'][0].get('op') in ('ver', 'hor'))
    for p, a in zip(n['pos'], n['args'][1:]):
        s += chr(rev[p]) + br(a, 'op' in a)
    return s

def main():
    names = json.load(open(ROOT / 'data/sign-names.json', encoding='utf8'))
    def gname(c):
        nm = names.get('%04X' % c, '')
        if nm.startswith('EGYPTIAN HIEROGLYPH ') and '-' not in nm[20:]:
            code = nm[20:]
            # A001 -> A1, G007A -> G7a, AA011 -> Aa11
            import re
            m = re.match(r'([A-Z]{1,2})(\d{3})([A-Z]?)$', code)
            if m:
                cat = m.group(1).capitalize() if len(m.group(1)) == 2 else m.group(1)
                return f'{cat}{int(m.group(2))}{m.group(3).lower()}'
            return code
        return 'U+%04X' % c
    def expr(n):
        if 'sign' in n:
            s = gname(n['sign'])
            if n.get('mirror'): s += '[mirror]'
            if 'rot' in n: s += f'[rot{90*n["rot"]}]'
            return s
        sep = {'ver': ' : ', 'hor': ' * ', 'ovl': ' # '}
        def sub(a, parent):
            e = expr(a)
            return f'({e})' if 'op' in a and (a['op'] != parent or parent == 'ins') else e
        if n['op'] in sep:
            return sep[n['op']].join(sub(a, n['op']) for a in n['args'])
        s = sub(n['args'][0], 'ins')
        for p, a in zip(n['pos'], n['args'][1:]):
            s += f' ⟨{p}⟩ ' + sub(a, 'ins')
        return s

    src = json.load(open(ROOT / 'data/ea581-lines.json', encoding='utf8'))
    groups = []
    for ln in src['lines']:
        frag = Parser(ln['unicode']).fragment()
        assert ''.join(to_unicode(g) for g in frag) == ln['unicode'], f"round-trip failed on line {ln['line']}"
        for k, g in enumerate(frag, 1):
            nodes = walk(g)
            groups.append({'line': ln['line'], 'dir': ln['direction'], 'pos': k, 'tree': g,
                           'u': to_unicode(g), 'expr': expr(g), 'signs': len(leaves(g)),
                           'nodes': [(op_label(n), arity(n), d) for n, d in nodes],
                           'height': max((d for _, d in nodes), default=0)})

    def census(gs):
        multi = [g for g in gs if g['nodes']]
        nodes = [x for g in multi for x in g['nodes']]
        ops = Counter(o.split(':')[0] for o, _, _ in nodes)
        ins_pos = Counter(p for o, _, _ in nodes if o.startswith('ins:') for p in o[4:].split('+'))
        root_ops = Counter(g['nodes'][0][0].split(':')[0] for g in multi)
        return {
            'groups': len(gs), 'single': len(gs) - len(multi), 'quadrats': len(multi),
            'signs': sum(g['signs'] for g in gs), 'signsInQuadrats': sum(g['signs'] for g in multi),
            'nodes': len(nodes),
            'arity': dict(sorted(Counter(a for _, a, _ in nodes).items())),
            'depth': dict(sorted(Counter(d for _, _, d in nodes).items())),
            'height': dict(sorted(Counter(g['height'] for g in multi).items())),
            'signsPerQuadrat': dict(sorted(Counter(g['signs'] for g in multi).items())),
            'ops': dict(ops.most_common()), 'rootOps': dict(root_ops.most_common()),
            'insPos': dict(ins_pos.most_common()),
            'mirrored': sum(1 for g in gs for l in leaves(g['tree']) if l.get('mirror')),
            'opByDepth': {d: dict(Counter(o.split(':')[0] for o, _, dd in nodes if dd == d))
                          for d in sorted({d for _, _, d in nodes})},
        }

    multi = [g for g in groups if g['nodes']]
    pilot = multi[:50]
    pilot_span = (pilot[0]['line'], pilot[-1]['line'])
    out = {
        'source': src['source'],
        'definitions': __doc__.split('Definitions')[1].split('A count')[0].strip(),
        'pilot': {'rule': 'the first 50 multi-sign groups in encoded order', 'lines': pilot_span,
                  'census': census(pilot),
                  'items': [{k: g[k] for k in ('line', 'dir', 'pos', 'u', 'expr', 'signs', 'height')} |
                            {'nodes': [[o, a, d] for o, a, d in g['nodes']]} for g in pilot]},
        'stela': {'census': census(groups),
                  'byDirection': {d: census([g for g in groups if g['dir'] == d]) for d in ('hrl', 'vrl')}},
    }
    (ROOT / 'data/pilot-census.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf8')
    js = ('/* Quadrat census for BM EA 581, generated by tools/quadrat_census.py.\n'
          '   Encoding: M.-J. Nederhof, HieroJax texts (GPL-3.0). Counts in one text, not rules. */\n'
          'window.HO_PILOT = ' + json.dumps(out, ensure_ascii=False) + ';\n')
    (ROOT / 'site/js/pilot-data.js').write_text(js, encoding='utf8')
    c = out['pilot']['census']; s = out['stela']['census']
    print('pilot', json.dumps(c, ensure_ascii=False))
    print('stela', json.dumps(s, ensure_ascii=False))
    for d, cc in out['stela']['byDirection'].items():
        print(d, cc['groups'], cc['quadrats'], cc['arity'], cc['height'], cc['ops'])

if __name__ == '__main__':
    main()
