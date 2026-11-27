#!/usr/bin/env python3
"""Backlog item 4: resolve the open derivations d03, d20 and d22.

Inputs
  data/derivations/rahman.drv      the derivations as now written (checked against the decisions below)
  data/second-text-lines.json,     M.-J. Nederhof's HieroJax Unicode encodings (GPL-3.0): EA 614, 567, 162, 562, 101
  data/ea581-lines.json            and EA 581; used to see how one editor groups the 2x2 sign group of nswt-bjtj
  data/nswt-aes.json               every TLA token of nswt (lemma 88040) and nswt-bjtj (lemma 88060) that carries a
                                   sign sequence, from AES (S. D. Schweitzer, CC BY-SA 4.0, TLA excerpt of Jan 2018)
                                   at a pinned commit. Made by `--fetch` (downloads the 16 corpus files to --cache).
Output
  data/resolutions.json            one record per derivation: question, decision, evidence with loci, status, what is
                                   still OPEN and what would decide it; plus the counts below.

Counts
  HieroJax  each place where a group holding M23 (sedge) is followed by a group holding L2 (bee): is the t of each
            title written under its own sign (two vertical groups, "by columns") or are sedge, bee, t, t written as a
            row of separate groups ("linear")?
  AES       nswt tokens whose sign sequence has both M23 and N35: is M23 written before N35?
            nswt-bjtj tokens whose sign sequence is exactly M23, L2, X1, X1 in some order (other signs ignored):
            M23-X1-L2-X1 (each t after its own sign, = reading order) or M23-L2-X1-X1 (sedge, bee, then both t).
            A TLA sign sequence is the editors' linearization of the group. It is not a record of the layout, so it
            cannot show rows or columns; it only shows which order the editors chose.
A count is not a rule. The decisions rest on the cited pages; the counts are context.
"""
from __future__ import annotations
import argparse, hashlib, json, sys, urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import derivations as DV  # noqa: E402
from second_text import EncParser, to_u  # noqa: E402

AES_COMMIT = '35276d2527cca1a055e31ed5f6683e777717170f'
AES_RAW = 'https://raw.githubusercontent.com/simondschweitzer/aes/{c}/files/aes/_aes_{n}.json'
AES_CORPORA = ['bbawamarna', 'bbawarchive', 'bbawbriefe', 'bbawfelsinschriften', 'bbawgrabinschriften', 'bbawgraeberspzt',
               'bbawhistbiospzt', 'bbawpyramidentexte', 'bbawramessiden', 'bbawtempelbib', 'bbawtotenlit', 'sawlit',
               'sawmedizin', 'smaek', 'tb', 'tuebingerstelen']
LEMMA = {'88040': 'nswt', '88060': 'nswt-bj.tj'}
M23, L2, X1, N35 = 0x131D3, 0x131A4, 0x133CF, 0x13216

# ------------------------------------------------------------------ sources (checked page by page, 27 Nov 2026)
SOURCES = {
 'Gardiner 1957': 'Gardiner, A. H. Egyptian Grammar. 3rd ed., revised. Oxford: Griffith Institute, 1957 (reprint 2001). Pages checked on scans.',
 'Allen 2010': 'Allen, J. P. Middle Egyptian: An Introduction to the Language and Culture of Hieroglyphs. 2nd ed., revised. Cambridge University Press, 2010. Pages checked on scans.',
 'Poe 2010': 'Poe, W. C. The Writing of a Skillful Scribe: An Introduction to Hieratic Middle Egyptian through the Text of The Shipwrecked Sailor. Santa Rosa, CA, 2010. PDF: https://egyptologyforum.org/bbs/Stableford/Poe%2C%20The_Writing_of_a_Skillful_Scribe_An_intr.pdf',
 'Peust 2007': 'Peust, C. Die honorative Transposition in der ägyptischen Schrift. Lingua Aegyptia 15 (2007): 93–135. https://doi.org/10.11588/propylaeumdok.00003221',
 'Unicode 16 ch. 11': 'The Unicode Standard 16.0, ch. 11, §11.4 Egyptian Hieroglyphs, "Directionality".',
 'Rahman': 'Rahman, Md. R. Ancient Egyptian Hieroglyph as the Pictorial Scrutiny of Modern Linguistics. ILIM Press, 2023 (all rights reserved; paraphrased, figures not reproduced).',
 'HieroJax': 'Nederhof, M.-J. HieroJax text pages, commit da318801 (GPL-3.0); strings in data/second-text-lines.json and data/ea581-lines.json.',
 'AES': f'Schweitzer, S. D. AES - Ancient Egyptian Sentences (TLA excerpt Jan 2018), commit {AES_COMMIT[:8]}, CC BY-SA 4.0; extract in data/nswt-aes.json.',
}

DECISIONS = [
 {'id': 'd03',
  'question': 'ḥb "festival" written V28 D58 W3: is W3 a biliteral ḥb with V28 and D58 as complements (B: CMPL3), or does W3 close a spelling ḥ-b as determinative (B_alt: CLOSE)?',
  'decision': 'CLOSE: [CLOSE [SPELL2 n1:PHON1 n2:PHON1] n3:DET_H] is now layer B; the complement tree is rejected.',
  'rejected': '[CMPL3 n1:COMPL n2:COMPL n3:PHON2]',
  'outcome': 'DECIDED',
  'evidence': [
   {'source': 'Gardiner 1957', 'locus': 'sign list W3, p. 527', 'label': 'source',
    'finding': 'W3 (basin of alabaster as used in purifications) is "det." in ḥb "feast", with this spelling (V28 D58 W3) given as the Dyn. XVIII variant; "hence semi-ideo. or phon. ḥb" only in ḥb "mourn"; also "Det. feast".'},
   {'source': 'Allen 2010', 'locus': 'sign list W3, p. 448', 'label': 'source',
    'finding': 'W3: variant W4; determinative FEAST; ideogram for ḥ3b "feast". No phonetic value is listed.'},
   {'source': 'Rahman', 'locus': 'p. 37', 'label': 'source',
    'finding': 'The book gives /hb-hb/ as the "authentic" and /hb/ as the "bookish" pronunciation; neither candidate tree yields a doubled sound.'},
  ],
  'status': 'HYPOTHESIS (the tree); the choice of B rests on Gardiner 1957 p. 527 and Allen 2010 p. 448.',
  'open': [],
  'would_decide': None},
 {'id': 'd20',
  'question': "Orientation of the book's figure of the Rosetta cartouche (Ptolemy, ever-living, beloved of Ptah): the earlier note said the sequence runs right to left while the animal signs face left.",
  'decision': 'No mismatch. The figure reads right to left and its animal signs face right, towards the start of the line. The earlier note misread the small figure. Layer A, the walks and TRANSPOSE(honorific) are unchanged.',
  'outcome': 'DECIDED',
  'evidence': [
   {'source': 'Gardiner 1957', 'locus': '§16, p. 25', 'label': 'source',
    'finding': 'Signs of persons, animals and birds, and others with fronts and backs, "almost always face the beginning of the inscription"; upper has precedence over lower.'},
   {'source': 'Unicode 16 ch. 11', 'locus': '§11.4, Directionality', 'label': 'source',
    'finding': '"one reads a line facing into the glyphs depicting the faces of people or animals" (already cited on this site).'},
   {'source': 'Rahman', 'locus': 'pp. 65 and 84 (one embedded image used on both pages, 265×49 px)', 'label': 'observation (this site)',
    'finding': 'The vertical line of the cartouche is at the left end. From the right end the signs run Q3/X1, V4, E23/Aa15, M17 M17, S29 (p-t-wꜣ-l-m-i-i-s), then S34, I10/X1/land, Q3/X1, V28, U7, M17 M17. The lion E23 and the cobra I10 face right.'},
   {'source': 'Rahman', 'locus': 'p. 84, short cartouche (ptwlmjs)', 'label': 'observation (this site)',
    'finding': 'The short cartouche runs left to right: vertical line at the right end, Q3/X1 at the left, lion facing left.'},
   {'source': 'Gardiner 1957', 'locus': '§57, p. 51', 'label': 'source',
    'finding': 'Honorific transposition: mry Imn "beloved of Amun" among the examples.'},
   {'source': 'Allen 2010', 'locus': '§4.15, p. 44', 'label': 'source',
    'finding': 'mry-jmn "beloved of Amun": the god\'s name is often put first.'},
  ],
  'status': 'HYPOTHESIS (the tree); orientation settled from the figure and Gardiner 1957 §16.',
  'open': ['N16 vs N17 under ḏt cannot be told apart in the figure.',
           "The layout on the Rosetta Stone itself (BM EA 24) was not checked; the derivation follows the book's figure."],
  'would_decide': 'N16/N17: a larger image of the same cartouche, or a facsimile of the stone (the BM record lists Quirke & Andrews 1988, "The Rosetta Stone: facsimile drawing").'},
 {'id': 'd22',
  'question': 'nswt-bjtj written as a 2×2 group (M23 L2 over X1 X1): is the order difference honorific or graphic transposition ("Allen against Poe")?',
  'decision': 'Graphic. TRANSPOSE(graphic) stays, now decided. Allen and Poe do not disagree: Allen too reads the sedge-first order of nswt as making a compact group under the meaning he prefers.',
  'outcome': 'DECIDED (type); OPEN (whether there is a reorder at all)',
  'evidence': [
   {'source': 'Gardiner 1957', 'locus': '§55, p. 51', 'label': 'source',
    'finding': 'This very group (sedge and bee over two t) is listed among abbreviations as n-sw-bit "king of Upper and Lower Egypt", literally "he who belongs to the sedge of Upper Egypt and the bee of Lower Egypt".'},
   {'source': 'Gardiner 1957', 'locus': '§56, p. 51', 'label': 'source',
    'finding': 'Graphic transpositions: signs are sometimes transposed "in order to give a more pleasing appearance or for some less assignable reason"; economy of space is one reason.'},
   {'source': 'Gardiner 1957', 'locus': '§57, p. 51', 'label': 'source',
    'finding': 'Honorific transposition: nsw "king", nṯr "god" and names of kings and gods are written before closely connected words that were spoken first (sš nsw, ḥm-nṯr, mry Imn).'},
   {'source': 'Gardiner 1957', 'locus': '§54 with n. 1, p. 50', 'label': 'source',
    'finding': '"king" is to be read nsw and not swtn; the note derives it from ni "belonging to" + swt "sedge". No transposition label is given.'},
   {'source': 'Allen 2010', 'locus': '§4.15, p. 44', 'label': 'source',
    'finding': 'Honorific transposition is defined on the direct genitive (possessor nṯr or nswt written first). nswt "itself may involve honorific transposition"; it is n(j) + swt, probably "he to whom the sedge belongs", "in which case the unusual order of the hieroglyphs just reflects the desire to make a compact group".'},
   {'source': 'Poe 2010', 'locus': 'p. 6', 'label': 'source',
    'finding': 'Two kinds of transposition: honorific (order changed by the status of what is represented) and graphic (order changed for balance or symmetry, e.g. two small glyphs grouped to fill an imaginary square).'},
   {'source': 'Poe 2010', 'locus': 'p. 63', 'label': 'source',
    'finding': 'n(y)-swt: "The arrangement of the glyphs is an example of graphic transposition." The placing of nsw before sꜣ in sꜣ nsw is "because of honorific transposition".'},
   {'source': 'Peust 2007', 'locus': 'pp. 93–94 (§0)', 'label': 'source',
    'finding': 'Honorific transposition is to be kept apart from purely calligraphic transposition against spoken order whose aim is to form quadrats.'},
   {'source': 'Rahman', 'locus': 'p. 81', 'label': 'observation (this site)',
    'finding': 'The figure shows sedge and bee over two t; no n (N35) is written.'},
  ],
  'status': 'HYPOTHESIS (the tree); reorder type graphic from Gardiner 1957 §§55–57, Allen 2010 §4.15, Poe 2010 pp. 6, 63; row vs column walk OPEN.',
  'open': ['Whether the 2×2 quadrat is walked by rows (sedge, bee, t, t: a graphic reorder) or by columns (sedge, t, bee, t: no reorder). The book\'s figure fits both trees.'],
  'would_decide': 'A rule for walking a 2×2 quadrat. This is backlog item 5 (a v1 label for column reading order), which needs Grant\'s approval before anything is added.'},
]


# ------------------------------------------------------------------ AES extract
def fetch(cache: Path):
    cache.mkdir(parents=True, exist_ok=True)
    toks, files = [], []
    for n in AES_CORPORA:
        f = cache / f'_aes_{n}.json'
        url = AES_RAW.format(c=AES_COMMIT, n=n)
        if not f.exists():
            print('fetch', url); urllib.request.urlretrieve(url, f)
        raw = f.read_bytes(); files.append({'corpus': n, 'file': url, 'sha256': hashlib.sha256(raw).hexdigest()})
        for sid, s in json.loads(raw).items():
            for t in s.get('token', []):
                if t.get('lemmaID') in LEMMA and t.get('hiero'):
                    toks.append({'corpus': n, 'sentence': sid, 'text': s.get('text'), 'date': s.get('date'),
                                 'lemmaID': t['lemmaID'], 'lemma': t.get('lemma_form'), 'written': t.get('written_form'),
                                 'hiero': t['hiero']})
    data = {'source': {'via': 'AES - Ancient Egyptian Sentences, S. D. Schweitzer, converted from the TLA database excerpt of '
                              'January 2018 (Berlin-Brandenburgische / Sächsische Akademie der Wissenschaften)',
                       'licence': 'CC BY-SA 4.0 (this extract keeps that licence)', 'commit': AES_COMMIT, 'files': files,
                       'selection': 'tokens with lemmaID 88040 (nswt) or 88060 (nswt-bj.tj) that carry a sign sequence (field hiero)'},
            'tokens': toks}
    (ROOT / 'data/nswt-aes.json').write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf8')
    return data


def aes_counts(A):
    n_order, bjtj = Counter(), Counter(); by_corpus = Counter()
    for t in A['tokens']:
        sg = t['hiero'].split('-')
        if t['lemmaID'] == '88040' and 'M23' in sg and 'N35' in sg:
            k = 'M23_before_N35' if sg.index('M23') < sg.index('N35') else 'N35_before_M23'
            n_order[k] += 1; by_corpus[(t['corpus'], k)] += 1
        if t['lemmaID'] == '88060':
            core = [x for x in sg if x in ('M23', 'L2', 'X1', 'N35')]
            if sorted(core) == ['L2', 'M23', 'X1', 'X1']:
                k = '-'.join(core); bjtj[k] += 1; by_corpus[(t['corpus'], k)] += 1
    return {'nswtWithN35': dict(n_order), 'nswtBjtjFourSigns': dict(bjtj),
            'byCorpus': [{'corpus': c, 'class': k, 'n': v} for (c, k), v in sorted(by_corpus.items())],
            'tokens': {LEMMA[k]: sum(1 for t in A['tokens'] if t['lemmaID'] == k) for k in LEMMA}}


# ------------------------------------------------------------------ HieroJax groups of nswt-bjtj
def signs(g):
    return [g['sign']] if 'sign' in g else [s for a in g['args'] for s in signs(a)]


def hierojax_bjtj():
    lines = [('ea581', l['line'], l.get('direction'), l['unicode']) for l in json.load(open(ROOT / 'data/ea581-lines.json', encoding='utf8'))['lines']]
    for t in json.load(open(ROOT / 'data/second-text-lines.json', encoding='utf8'))['texts']:
        lines += [(t['key'], l['label'] or str(l['n']), l['orientation'], l['unicode']) for l in t['lines']]
    out = []
    for key, lab, orient, u in lines:
        fr = EncParser(u).fragment()
        for i, g in enumerate(fr):
            s = signs(g)
            if M23 not in s or i + 1 >= len(fr) or L2 not in signs(fr[i + 1]): continue
            g2 = signs(fr[i + 1])
            if X1 in s and X1 in g2: cls = 'columns'          # each title's t inside its own group
            elif X1 not in s and g2 == [L2] and all(signs(x) == [X1] for x in fr[i + 2:i + 4]): cls = 'linear'
            else: cls = 'other'
            out.append({'text': key, 'line': lab, 'orientation': orient, 'class': cls,
                        'groups': [to_u(x) for x in fr[i:i + (2 if cls == 'columns' else 4)]]})
    return out


# ------------------------------------------------------------------ consistency with the derivations
def check_drv():
    ds = {d['id']: d for d in DV.load(ROOT / 'data/derivations/rahman.drv')}
    errs = []
    d03, d20, d22 = ds['d03'], ds['d20'], ds['d22']
    if d03['B'] != '[CLOSE [SPELL2 n1:PHON1 n2:PHON1] n3:DET_H]' or d03.get('B_alt'): errs.append('d03: layer B is not the decided CLOSE tree')
    if 'OPEN' in d20['status'].split('N16')[0]: errs.append('d20: orientation still marked OPEN')
    if d22['reorder'] != 'TRANSPOSE(graphic)' or 'decided' not in d22['status']: errs.append('d22: reorder type not recorded as decided graphic')
    for d in ds.values():
        if d['errors']: errs.append(f"{d['id']}: {d['errors']}")
    rej = DV.parse_bracket(DECISIONS[0]['rejected'])
    return errs, {'d03_hB': DV.height(d03['B_tree']), 'd03_hB_rejected': DV.height(rej),
                  'd22_walk_write': d22['walk_write'], 'd22_walk_read': d22['read_list']}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fetch', action='store_true', help='rebuild data/nswt-aes.json from AES at the pinned commit')
    ap.add_argument('--cache', default='/tmp/aes')
    a = ap.parse_args()
    A = fetch(Path(a.cache)) if a.fetch else json.load(open(ROOT / 'data/nswt-aes.json', encoding='utf8'))
    errs, heights = check_drv()
    if errs:
        print('\n'.join(errs)); sys.exit(1)
    hj = hierojax_bjtj()
    out = {'date': '2026-11-27', 'item': 'EXPLORATION backlog 4', 'sources': SOURCES, 'decisions': DECISIONS,
           'heights': heights,
           'counts': {'aes': aes_counts(A), 'hierojaxNswtBjtj': {'groups': hj, 'byClass': dict(Counter(g['class'] for g in hj))}},
           'note': 'Counts are context, not rules. TLA sign sequences are editorial linearizations; HieroJax relative positions are '
                   'the editor\'s judgement, not facsimiles.'}
    (ROOT / 'data/resolutions.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf8')
    c = out['counts']
    print('AES nswt with N35:', c['aes']['nswtWithN35'], '| nswt-bjtj four signs:', c['aes']['nswtBjtjFourSigns'])
    print('HieroJax nswt-bjtj:', c['hierojaxNswtBjtj']['byClass'], [(g['text'], g['line'], g['class']) for g in hj])
    print('heights', heights)


if __name__ == '__main__':
    main()
