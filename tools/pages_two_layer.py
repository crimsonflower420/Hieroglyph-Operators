"""Pages for the two-layer derivations: derivations, notation, rahman. Imported by build_pages.py."""
import sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import derivations as DV

ROOT = Path(__file__).resolve().parent.parent
KANJI = 'https://kanji-morphology.pages.dev/'
REPO = 'https://github.com/crimsonflower420/Hieroglyph-Operators'
DS = DV.load(ROOT / 'data/derivations/rahman.drv')
BYID = {d['id']: d for d in DS}

REFS = {
 'Gardiner 1957': ('Gardiner, A. H. <i>Egyptian Grammar</i>. 3rd ed. Oxford: Griffith Institute, 1957.', ''),
 'Allen 2010': ('Allen, J. P. <i>Middle Egyptian: An Introduction to the Language and Culture of Hieroglyphs</i>. 2nd ed. Cambridge University Press, 2010.', ''),
 'Peust 2007': ('Peust, C. “Die honorative Transposition in der ägyptischen Schrift.” <i>Lingua Aegyptia</i> 15 (2007): 93–135.', 'https://doi.org/10.11588/propylaeumdok.00003221'),
 'Callimahos': ('Callimahos, L. D. “The Rosetta Stone and Its Decipherment.” NSA, declassified (PDF).', 'https://media.defense.gov/2021/Jul/02/2002755845/-1/-1/0/ROSETTA-STONE.PDF'),
 'Champollion 1822': ('Champollion, J.-F. <i>Lettre à M. Dacier relative à l’alphabet des hiéroglyphes phonétiques</i>. Paris, 1822.', ''),
 'Poe': ('Poe, W. C. <i>The Writing of a Skillful Scribe: An Introduction to Hieratic Middle Egyptian through the Text of The Shipwrecked Sailor</i>. Santa Rosa, CA, 2010 (PDF, Egyptology Forum).', 'https://egyptologyforum.org/bbs/Stableford/Poe%2C%20The_Writing_of_a_Skillful_Scribe_An_intr.pdf'),
 'Hierolyte': ('Hierolyte. “Why the god comes first: honorific transposition in hieroglyphs” (secondary summary of Gardiner and Allen; used only as a pointer).', 'https://hierolyte.app/discoveries/why-the-god-comes-first-honorific-transposition-in-hieroglyphs'),
 'Rosetta Stone (BM EA 24)': ('British Museum, EA 24, the Rosetta Stone (collection record).', 'https://www.britishmuseum.org/collection/object/Y_EA24'),
}
BOOK = ('Rahman, Md. Ridwanur. <i>Ancient Egyptian Hieroglyph as the Pictorial Scrutiny of Modern Linguistics: The First Research Work on Egyptian Hieroglyphic Language in the Bosom of Bangladesh</i>. First published 2020; ILIM Press edition, Dhaka, 2023. ISBN 978-984-35-4321-9.', '')
STANDARD = ('<span class="ja" lang="ja">SUBLEXICAL-DERIVATIONS-v1、文字の下位語彙の導出のための共有規格。Syntax · Semantics · Interface とともに起草し、2026年11月21日にグラントが承認した（このリポジトリに写しがある）。</span><span class="en" lang="en">SUBLEXICAL-DERIVATIONS-v1, shared standard for sub-lexical derivations, drafted with Syntax · Semantics · Interface; approved by Grant Golland, 21 Nov 2026 (copy in this repository).</span>', REPO + '/blob/main/notes/SUBLEXICAL-DERIVATIONS-v1.md')

CAT = {  # (ja, en)
 'COMPL': ('補音', 'Phonetic complements'), 'DET': ('限定符（主要部）', 'Determinatives (heads)'),
 'INFL': ('数・性・動詞の印', 'Number, gender, verb markers'), 'LOGO': ('表語', 'Logograms'),
 'TRANSPOSE': ('転置（歩きの上の並べ替え）', 'Transposition (reorders on the walk)'),
 'ABBR': ('略記', 'Abbreviated writing'), 'LAYOUT': ('配置のみ（読み順）', 'Layout only (reading order)'),
}
CAT_ORDER = ['COMPL', 'DET', 'INFL', 'LOGO', 'TRANSPOSE', 'ABBR', 'LAYOUT']

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def qrow(d, size='3.2em'):
    cls = 'qrow cart' if d['cartouche'] else 'qrow'
    return f'<div class="{cls}">' + ''.join(f'<span data-q="{q}" data-size="{size}"></span>' for q in d['quadrats']) + '</div>'

def card(d, bi):
    sig = ' '.join(f"{s['id']}={s['code']}" for s in d['signs_list'])
    A = d['A_tree']; B = d['B_tree']; Balt = d['B_alt_tree']
    lay = [f'<div class="layer"><div class="lab">{bi("層 A：配置（主要部なし）", "Layer A: layout (headless)")}</div><pre class="bracket">{esc(d["A"])}</pre><div class="svgscroll">{DV.svg_tree(A, d, "A")}</div></div>']
    if B:
        lay.append(f'<div class="layer"><div class="lab">{bi("層 B：型付きの機能（主要部 _H）", "Layer B: typed function (heads _H)")}</div><pre class="bracket">{esc(d["B"])}</pre><div class="svgscroll">{DV.svg_tree(B, d, "B")}</div></div>')
    else:
        lay.append(f'<div class="layer"><div class="lab">{bi("層 B", "Layer B")}</div><p><b>OPEN</b> — {bi("未決。理由は下の注を見よ。", "unresolved; see the note below.")}</p></div>')
    if Balt:
        lay.append(f'<div class="layer"><div class="lab">{bi("層 B（別案）", "Layer B (alternative)")}</div><pre class="bracket">{esc(d["B_alt"])}</pre><div class="svgscroll">{DV.svg_tree(Balt, d, "B")}</div></div>')
    walk = ''
    if d['reorder'] != '-':
        walk = (f'<div class="layer"><div class="lab">WALK_write ≠ WALK_read · {esc(d["reorder"])}</div>'
                f'<div class="svgscroll">{DV.svg_walk(d)}</div></div>')
    else:
        walk = f'<p class="meta">WALK_write = WALK_read = {" ".join(d["read_list"])}</p>'
    mm = ''
    for key, lab in (('mismatch', 'B'), ('mismatch_alt', 'B_alt')):
        for m in d[key]:
            mm += f'<p class="mm">MISMATCH ({lab}) · {esc(m["op"])} {{{", ".join(m["leaves"])}}} — {bi("配置のどの構成素とも一致しない", "coincides with no layout constituent")}</p>'
    refs = ' · '.join(esc(r) for r in d['refs_list'])
    return f'''<section class="drv" id="{d['id']}">
<h3>{d['id']} · {bi(esc(d['title.ja']), esc(d['title.en']))}</h3>
<p class="meta"><b>{d['status'].split(';')[0]}</b>{esc(d['status'][len(d['status'].split(';')[0]):])} · {bi("本書", "book")} p. {esc(d['book'])} · {sig}</p>
{qrow(d)}
<div class="layers{' one' if len(d['signs_list']) > 8 else ''}">{''.join(lay)}</div>
{walk}{mm}
<p><span class="k">{bi("本書", "Book")}</span>{bi(esc(d['claim.ja']), esc(d['claim.en']))}</p>
<p><span class="k">{bi("標準", "Standard")}</span>{bi(esc(d['std.ja']), esc(d['std.en']))}</p>
<p><span class="k">{bi("注", "Note")}</span>{bi(esc(d['note.ja']), esc(d['note.en']))}</p>
<p class="meta">{bi("出典", "Refs")}: {refs}</p>
</section>'''

def op_table(bi, layer):
    if layer == 'A':
        rows = [('⿰', '2', 'U+13431', '*'), ('⿲', '3', 'U+13431 ×2', '*'), ('⿱', '2', 'U+13430', ':'), ('⿳', '3', 'U+13430 ×2', ':'),
                ('INS_ts / INS_bs / INS_te / INS_be', '2', 'U+13432–U+13435', bi('演算子のページを見よ', 'see Operators page')),
                ('INS_m / INS_t / INS_b', '2', 'U+13439–U+1343B', '—'), ('OVERLAY', '2', 'U+13436', '#'),
                ('LINE<i>k</i>', '<i>k</i>', bi('結合子なし（方形の列）', 'no joiner (a row of quadrats)'), '-'),
                ('CARTOUCHE', '1', bi('囲みの制御文字（U+1343C–U+1343F）', 'enclosure controls (U+1343C–U+1343F)'), '&lt; &gt;')]
        head = f'<tr><th>{bi("演算子", "Operator")}</th><th>{bi("項数", "Arity")}</th><th>Unicode</th><th>MdC</th><th>{bi("意味", "Meaning")}</th></tr>'
        body = ''
        for op, ar, u, m in rows:
            key = op.split(' ')[0].replace('<i>k</i>', '')
            g = DV.OP_GLOSS.get(key, DV.OP_GLOSS.get('INS_te' if key.startswith('INS') else key, ('', '')))
            if key.startswith('INS_ts'): g = ('四隅に差し込む', 'insert at a corner')
            if key.startswith('INS_m'): g = ('中央・上・下に差し込む', 'insert at middle, top or bottom')
            body += f'<tr><td><code>{op}</code></td><td>{ar}</td><td>{u}</td><td><code>{m}</code></td><td>{bi(*g)}</td></tr>'
        return f'<div class="table-scroll"><table>{head}{body}</table></div>'
    rows = [('SPELL<i>k</i>', '<i>k</i>', 'SPELL'), ('CMPL<i>k</i> (k = 2, 3)', '<i>k</i>', 'CMPL'), ('CLOSE', '2', 'CLOSE'), ('LOGO', '2', 'LOGO'),
            ('INFL<i>k</i> (k = 2, 3)', '<i>k</i>', 'INFL'), ('PL', '2', 'PL'), ('SUFF', '2', 'SUFF'), ('GEN', '2', 'GEN'), ('ATTR', '2', 'ATTR'),
            ('COORD', '2', 'COORD'), ('NAME<i>k</i> / PHRASE<i>k</i>', '<i>k</i>', 'NAME'), ('ABBR', '1', 'ABBR')]
    head = f'<tr><th>{bi("演算子", "Operator")}</th><th>{bi("項数", "Arity")}</th><th>{bi("はたらき", "What it does")}</th></tr>'
    body = ''.join(f'<tr><td><code>{o}</code></td><td>{a}</td><td>{bi(*DV.OP_GLOSS[k])}</td></tr>' for o, a, k in rows)
    return f'<div class="table-scroll"><table>{head}{body}</table></div>'

ROLE_ROWS = [('PHON1 / PHON2 / PHON3', '一・二・三子音の表音記号', 'uni-, bi-, triliteral phonogram'), ('LOGO', '表語', 'logogram'),
             ('COMPL', '補音（音を足さない）', 'phonetic complement (adds no sound)'), ('DET_H', '限定符。必ず主要部 _H', 'determinative; always head _H'),
             ('FEM', '女性語尾 -t', 'feminine ending -t'), ('PL', '複数の印・語尾', 'plural marker or ending'), ('INFL', 'その他の語尾・動詞の印', 'other ending or verb marker'),
             ('STROKE', '表語の一本線', 'logogram stroke'), ('SUFF', '接尾代名詞', 'suffix pronoun')]

def pages(bi):
    n = len(DS); cats = Counter(d['cat'] for d in DS)
    n_mm = sum(1 for d in DS if d['mismatch']); n_re = sum(1 for d in DS if d['reorder'] != '-')
    ex = BYID['d10']
    cat_rows = ''.join(f'<tr><td>{bi(*CAT[c])}</td><td>{cats[c]}</td><td>{" ".join(f"<a href=\"rahman#{d["id"]}\">{d["id"]}</a>" for d in DS if d["cat"] == c)}</td></tr>' for c in CAT_ORDER)
    cat_table = f'<div class="table-scroll"><table><tr><th>{bi("種類", "Type")}</th><th>{bi("数", "n")}</th><th>{bi("導出", "Derivations")}</th></tr>{cat_rows}<tr><td><b>{bi("計", "Total")}</b></td><td><b>{n}</b></td><td></td></tr></table></div>'

    derivations = f'''
<p class="tag">{bi("記法 v1 による", "Written in notation v1")}</p>
<h1>{bi("二層の導出", "Two-layer derivations")}</h1>
<p class="lede">{bi(
 "記号の組み合わせを、二つの木で書く。層 A は紙面の配置（方形）であり、層 B は記号のはたらき（表音・補音・限定符・語尾）である。二つの層は同じ葉 n1, n2 … を共有し、葉の番号でつながる。",
 "A sign combination is written as two trees. Layer A is the layout on the surface (the quadrat); layer B is what the signs do (phonogram, complement, determinative, ending). Both layers share the same leaves n1, n2 … and are linked by those ids.")}</p>
<p>{bi(
 f"書式は<a href=\"notation\">記法 v1</a>にしたがう。角括弧の形（ブラケット形式）が正本であり、このサイトの図はすべて <code>tools/derivations.py</code> がそこから生成する。データは <a href=\"{REPO}/blob/main/data/derivations/rahman.drv\">data/derivations/rahman.drv</a> にある。",
 f"The format follows <a href=\"notation\">notation v1</a>. The bracket form is the source of truth, and every figure on this site is generated from it by <code>tools/derivations.py</code>. The data are in <a href=\"{REPO}/blob/main/data/derivations/rahman.drv\">data/derivations/rahman.drv</a>.")}</p>

<h2>{bi("1. 層 A：配置", "1. Layer A: layout")}</h2>
<p>{bi(
 "層 A は幾何だけを書く。主要部はない。演算子は Unicode の書式制御文字にほぼ一対一で対応する。方形の中の左右 ⿰ と、方形を並べた列 LINE<i>k</i> は区別する。前者は横の結合 U+13431 で、後者は結合子なしの並びである。",
 "Layer A records geometry only and has no heads. Its operators map almost one-to-one onto the Unicode format controls. Side by side inside a quadrat (⿰) is kept apart from a row of quadrats (LINE<i>k</i>): the first is the horizontal joiner U+13431, the second is plain juxtaposition.")}</p>
{op_table(bi, 'A')}
<p>{bi(
 "項数は演算子が決める。⿰ は2、⿲ は3、LINE<i>k</i> は <i>k</i> である。娘の数が合わなければ、検査器が落とす。",
 "Arity is fixed by the operator: ⿰ is 2, ⿲ is 3, LINE<i>k</i> is <i>k</i>. A wrong number of daughters fails the checker.")}</p>

<h2>{bi("2. 層 B：型付きの機能", "2. Layer B: typed function")}</h2>
<p>{bi(
 "層 B の演算子は型をもつ。たとえば CMPL は「多子音記号＋補音 → PHON」、CLOSE は「WORD＋限定符 → WORD_closed」である。主要部は層 B にだけ現れ、限定符の葉に _H を付けて示す。",
 "Layer B operators are typed: CMPL is 'multiliteral + complement → PHON', CLOSE is 'WORD + determinative → WORD_closed'. Heads appear only in layer B, marked _H on the determinative leaf.")}</p>
{op_table(bi, 'B')}
<div class="table-scroll"><table><tr><th>{bi("葉の役割", "Leaf role")}</th><th>{bi("意味", "Meaning")}</th></tr>{''.join(f'<tr><td><code>{r}</code></td><td>{bi(j, e)}</td></tr>' for r, j, e in ROLE_ROWS)}</table></div>

<h2>{bi("3. 例：nfrt「美しい（女）」", "3. Example: nfrt 'beautiful (woman)'")}</h2>
{card(ex, bi)}
<p>{bi(
 "この例では、配置の列［⿳ f r t］が機能のまとまりと交差する。検査器は、層 B の節点のうち、葉の集合が層 A のどの節点とも、またどの節点の連続した娘の並びとも一致しないものを MISMATCH として報告する。",
 "Here the layout column [⿳ f r t] cuts across the function grouping. The checker reports a layer-B node as MISMATCH when its leaf set equals no layer-A node and no contiguous run of one layer-A node's daughters.")}</p>

<h2>{bi("4. 順序：木と歩き", "4. Order: trees and walks")}</h2>
<p>{bi(
 "木は階層だけを表す。順序は木の上の線形化として別に書く。WALK_write は層 A の葉を左から、縦の結合では上から辿った並びである。本書（pp. 60–61）が Bruaw から引く「上の記号が先」という規則は、この既定の歩きの定義そのものである（<a href=\"rahman#d25\">d25</a>）。WALK_read は読む順で、層 B の葉の並びと一致しなければならない。",
 "A tree records hierarchy only; order is written separately as linearizations over it. WALK_write is the leaf order of layer A read left to right, top first at vertical joins. The rule the book takes from Bruaw (pp. 60–61), signs above come first, is exactly the definition of this default walk (<a href=\"rahman#d25\">d25</a>). WALK_read is the reading order and must equal the leaf order of layer B.")}</p>
<p>{bi(
 f"二つの歩きが食い違うときは、木は一つのまま、歩きの上に並べ替えを記す（規格の既定 (b)）。ラベルは TRANSPOSE(honorific) または TRANSPOSE(graphic) である。漢字のサイトの<a href=\"{KANJI}walk-permutation\">「書き順と歩き順の置換」</a>の語彙でいえば、敬意による転置は reorder の型に当たる。尊ぶ語のかたまりが、それが追い越すかたまりより先に書かれる。今回の例には return の型に当たるものはない。",
 f"When the two walks differ, the tree stays single and the reorder is marked on the walk (the standard's default (b)), labelled TRANSPOSE(honorific) or TRANSPOSE(graphic). In the vocabulary of the kanji site's <a href=\"{KANJI}walk-permutation\">written order vs walk order</a>, honorific transposition is of the reorder type: the honoured block is written ahead of the block it passes. No case of the return type occurs here.")}</p>
<div class="flag spec">{bi(
 "<strong>並行関係（グラントの承認待ち）。</strong>漢字の reorder（書き順で部品のかたまりが先に出る）と、ヒエログリフの敬意による転置（尊ぶ語が先に書かれる）は、どちらも「一つの木、二つの歩き、かたまり一つの入れ替え」という同じ形で書ける。どちらも文字の層の話であり、統語の主張ではない。",
 "<strong>Parallel (for Grant to approve).</strong> The kanji reorder (a component block comes earlier in stroke order) and hieroglyphic honorific transposition (the honoured word is written first) can both be written in the same shape: one tree, two walks, one block swapped. Both are about the writing layer; neither is a syntactic claim.")}</div>
<p>{bi(
 "Peust（2007）は、敬意による転置が話し言葉の統語上の倒置規則によく似ていると論じる。このサイトはその見方を紹介するにとどめ、移動 (a) は使わない。規格は、層 B がそれを支持するときにだけ移動を許している。",
 "Peust (2007) argues that honorific transposition closely mimics syntactic inversion rules of spoken languages. This site reports that view but does not use movement (a); the standard allows movement only when layer B argues for it.")}</p>

<h2>{bi("5. 検査", "5. Checks")}</h2>
<p>{bi(
 "<code>python3 tools/derivations.py</code> は次を確かめ、一つでも外れれば失敗する。演算子の項数。両層がすべての葉をちょうど一度ずつ使うこと。層 A に役割や主要部がないこと。主要部が限定符だけにあり、限定符はかならず主要部であること。CMPL の娘が多子音記号一つと補音から成ること。CLOSE が限定符で終わること。層 B の葉の並びが WALK_read と等しいこと。歩きが食い違うときに限って並べ替えのラベルがあること。どの木にも HYPOTHESIS が付いていること。",
 "<code>python3 tools/derivations.py</code> checks the following and fails on any breach: operator arity; both layers use every leaf exactly once; no roles or heads in layer A; heads only on determinatives, and every determinative a head; CMPL daughters are one multiliteral plus complements; CLOSE ends in a determinative; layer B's leaf order equals WALK_read; a reorder label is present exactly when the walks differ; every tree carries HYPOTHESIS.")}</p>

<h2>{bi("主張しないこと", "What is not claimed")}</h2>
<div class="flag">{bi(
 "記号の木は統語ではなく、Merge・X バー・θ役割の主張でもない。書き順や読み順は心理的な導出の主張ではない。層 B は語の形態や意味の木そのものではなく、二つの層が同じものだとも主張しない。",
 "Glyph trees are not syntax, and make no claim about Merge, X-bar or θ-roles. Writing or reading order is not claimed as a psychological derivation. Layer B is not word morphology or semantics as such, and the two layers are not claimed to be the same thing.")}</div>
'''

    notation = f'''
<p class="tag">{bi("共有の規格", "Shared standard")}</p>
<h1>{bi("記法 / Notation", "Notation / 記法")}</h1>
<p class="lede">{bi(
 "このサイトの導出は、文字の下位語彙の導出のための共有規格 v1 で書く。規格は Syntax · Semantics · Interface とともに起草し、2026年11月21日にグラントが承認した。改訂はありうる。",
 "The derivations on this site are written in v1 of the shared standard for sub-lexical derivations. It was drafted with Syntax · Semantics · Interface and approved by Grant Golland on 21 November 2026; it may be revised.")}</p>
<p>{bi(
 f"規格の全文（英語）：<a href=\"{STANDARD[1]}\">SUBLEXICAL-DERIVATIONS-v1.md</a>。ここではその要点を述べ、ヒエログリフでの使い方を示す。",
 f"Full text (English): <a href=\"{STANDARD[1]}\">SUBLEXICAL-DERIVATIONS-v1.md</a>. This page gives the main points and how they are used for hieroglyphs.")}</p>
<div class="table-scroll"><table>
<tr><th>§</th><th>{bi("規格の要点", "Standard")}</th><th>{bi("このサイトでの使い方", "Use on this site")}</th></tr>
<tr><td>1</td><td>{bi("根のある順序木。節点は演算子のラベル・項数・娘から成る。葉は字形と語釈。ブラケット形式が正本で、図はそこから生成する。項数は演算子が決め、娘の数が違えば検査器が落とす。", "Rooted ordered tree; node = operator label + arity + daughters; leaves = glyph + gloss. Bracket form is the source of truth; figures are generated from it. Arity is fixed by the operator; a wrong daughter count fails the checker.")}</td><td>{bi("<code>data/derivations/rahman.drv</code> の A・B の行。図は <code>tools/derivations.py</code> が生成する。", "The A and B lines of <code>data/derivations/rahman.drv</code>; figures from <code>tools/derivations.py</code>.")}</td></tr>
<tr><td>2</td><td>{bi("主要部は機能の木にだけ置き、_H で示す。配置の木には主要部がない。", "Heads only in the function tree, marked _H; layout trees are headless.")}</td><td>{bi("限定符（DET）にだけ _H を付ける。", "Only determinatives (DET) carry _H.")}</td></tr>
<tr><td>3</td><td>{bi("二つの層：A 配置、B 型付きの機能。葉の番号でつなぎ、食い違いは明記する。", "Two layers: A layout, B typed function; linked by node ids; mismatches stated.")}</td><td>{bi("方形の木と記号のはたらきの木。食い違いは MISMATCH として自動で報告する。", "Quadrat tree and sign-function tree; mismatches reported automatically as MISMATCH.")}</td></tr>
<tr><td>4</td><td>{bi("木は階層、順序は木の上の名前付きの線形化（WALK）。例外は記録し、木には組み込まない。", "Tree = hierarchy; order = named linearizations (WALK). Exceptions are recorded, not built into the tree.")}</td><td>WALK_write, WALK_read</td></tr>
<tr><td>5</td><td>{bi("並べ替え：(a) 移動（層 B が支持するときだけ）、(b) 線形化の並べ替え。既定は (b) で、WALK_write ≠ WALK_read と記し、TRANSPOSE(honorific) のラベルを付ける。", "Reordering: (a) movement, only if layer B argues for it; (b) linearization reorder, marked WALK_write ≠ WALK_read with TRANSPOSE(honorific). Default (b).")}</td><td>{bi("すべて (b)。書記上の並べ替えには TRANSPOSE(graphic) も使う。", "All (b); TRANSPOSE(graphic) is also used for graphic reorders.")}</td></tr>
<tr><td>6</td><td>{bi("どの木にも HYPOTHESIS。確かな事実には出典。未決は OPEN。CONJECTURE は使わない。グラントの考えは GRANT'S HYPOTHESIS（グラントの仮説）と明記する。", "HYPOTHESIS on every tree; attested facts with source; OPEN for unresolved; no CONJECTURE; Grant's ideas credited as GRANT'S HYPOTHESIS.")}</td><td>{bi("各導出の見出しに表示する。", "Shown in each derivation's header line.")}</td></tr>
<tr><td>7</td><td>{bi("主張しないこと：記号の木は統語・Merge・X バー・θ ではない。書き順・読み順は心理的な導出ではない。機能の木は語の形態・意味そのものではない。二つの水準が同じだとは言わない。並行関係は「グラントの承認待ち」の注に置く。", "Not claimed: glyph trees are syntax / Merge / X-bar / θ; stroke or reading order is a psychological derivation; function tree = word morphology/semantics; the two levels are the same. Any parallel goes in a 'Parallel (for Grant to approve)' note.")}</td><td>{bi("<a href=\"derivations\">二層の導出</a>の最後に明記する。", "Stated at the end of <a href=\"derivations\">Two-layer derivations</a>.")}</td></tr>
<tr><td>8</td><td>{bi("相互リンク：一致する箇所では関連ページへリンクする。用語集の共有は任意。", "Interlinking: link matching pages; an optional shared glossary.")}</td><td>{bi(f"漢字のサイトの<a href=\"{KANJI}walk-permutation\">書き順と歩き順</a>へリンクする。", f"Links to the kanji site's <a href=\"{KANJI}walk-permutation\">written order vs walk order</a>.")}</td></tr>
</table></div>

<h2>{bi("ヒエログリフでの具体化", "The hieroglyph profile")}</h2>
<p>{bi(
 "規格は演算子の名前を ⿰・⿱ など漢字の IDS から取る。ヒエログリフでは、⿰ と ⿱ をそれぞれ横の結合・縦の結合に当て、差し込み・重ね合わせ・カルトゥーシュ・方形の列（LINE<i>k</i>）を加えた。層 B には、補音（CMPL）、限定符による閉じ（CLOSE）、語尾（INFL・PL）、略記（ABBR）などの型を置いた。一覧は<a href=\"derivations\">二層の導出</a>にある。",
 "The standard takes operator names such as ⿰ and ⿱ from kanji IDS. For hieroglyphs, ⿰ and ⿱ are assigned to the horizontal and vertical joiners, and insertion, overlay, cartouche and the quadrat row (LINE<i>k</i>) are added. Layer B gets types for complements (CMPL), closing by a determinative (CLOSE), endings (INFL, PL), abbreviation (ABBR) and others. The full list is on <a href=\"derivations\">Two-layer derivations</a>.")}</p>
<pre class="bracket">=== d05
signs: n1 U7 mr | n2 D21 r | n3 A2
A: [LINE2 [⿱ n1 n2] n3]
B: [CLOSE [CMPL2 n1:PHON2 n2:COMPL] n3:DET_H]
read: n1 n2 n3</pre>
<p class="meta">{bi("クレジット：規格 v1 は Syntax · Semantics · Interface とともに起草し、グラントが承認した。", "Credit: standard v1 drafted with Syntax · Semantics · Interface; approved by Grant Golland.")}</p>
'''

    groups = ''
    for c in CAT_ORDER:
        items = [d for d in DS if d['cat'] == c]
        groups += f'<h2 id="cat-{c.lower()}">{bi(*CAT[c])} ({len(items)})</h2>' + ''.join(card(d, bi) for d in items)

    chapters = [
     ('I–II', '1–7', '序論・方法。二次資料に基づく文献研究', 'Introduction, method: a library study from secondary sources', '—'),
     ('III', '8–13', '解読の起源（中世の学者、ロゼッタ・ストーン）', 'Origins of decipherment (medieval scholars, Rosetta Stone)', 'd20, d26'),
     ('IV', '14–24', '「内的・外的な進化の連鎖」。内的連鎖の大筋は主流。ラテン文字・ヘブライ文字・アラビア文字の直接の由来は推測/非主流', '“Internal and external evolutionary links”; internal in outline mainstream; direct derivation of Latin, Hebrew, Arabic letters speculative/non-mainstream', '—'),
     ('V', '25–38', '記号の分類、音価、三母音の IPA（推測/非主流）、「本来の発音」（補音）', 'Sign classes, phonetic values, three-vowel IPA (speculative/non-mainstream), “authentic pronunciation” (complements)', 'd01–d09, d21'),
     ('VI', '39–48', '文法：属格と敬意の順、数・性、形容詞、時制', 'Grammar: genitive and honorific order, number, gender, adjectives, tense', 'd10, d14–d19'),
     ('VII', '49–50', '反意語・同義語・同音語', 'Antonyms, synonyms, homonyms', '—'),
     ('VIII', '51–58', '形態（切り詰め・複合）と統語（統語は範囲外）', 'Morphology (clipping, compounding) and syntax (syntax out of scope)', 'd05, d11–d13, d23, d26'),
     ('IX', '59–68', '読み方（向き・方形の読み順）、翻訳（カリオンは推測/非主流）', 'Reading (direction, quadrat order), translation (Kariong: speculative/non-mainstream)', 'd20, d25'),
     ('X', '69–80', '心理言語学（範囲外）', 'Psycholinguistics (out of scope)', '—'),
     ('XI', '80–89', '社会言語学：王の称号、ファラオ', 'Sociolinguistics: royal titles, pharaoh', 'd22, d24'),
     ('XII', '90–91', '結論', 'Conclusion', '—'),
     (bi('付録', 'App.'), '98–116', 'デンデラの黄道帯、三母音、ラメセス＝モーセ、アレクサンドロスの角（推測/非主流）', 'Dendera zodiac, three vowels, Ramesses = Moses, horns of Alexander (speculative/non-mainstream)', '—'),
    ]
    ch_rows = ''.join(f'<tr><td class="nw">{a}</td><td class="nw">{p}</td><td>{bi(j, e)}</td><td>{" ".join(f"<a href=\"#{x.strip()}\">{x.strip()}</a>" if x.strip().startswith("d") and "–" not in x else x for x in r.split(","))}</td></tr>' for a, p, j, e, r in chapters)

    rahman = f'''
<p class="tag">{bi("書物の再読", "A book re-read")}</p>
<h1>{bi("ラフマン『現代言語学の絵による精査としての古代エジプト・ヒエログリフ』を演算子で読む", "Rahman's Ancient Egyptian Hieroglyph as the Pictorial Scrutiny of Modern Linguistics, read through operators")}</h1>
<p class="lede">{bi(
 "この本は、現代言語学の各分野をヒエログリフに当てはめる試みである。記号の組み合わせについての主張は多いが、それを明示的な導出として書いたものはない。このページでは、本書が挙げる組み合わせを二層の導出（記法 v1）として書き、標準の参考書と照らし合わせる。",
 "The book applies the branches of modern linguistics to hieroglyphs. It makes many claims about how signs combine, but none is written out as an explicit derivation. This page writes the book's combinations as two-layer derivations (notation v1) and checks them against the standard references.")}</p>
<p>{bi(
 "本書の文は言い換えて引き、ページ番号を付ける。図や表は転載しない。記号はすべて、このサイトのデータから Noto Sans Egyptian Hieroglyphs で描き直している。記号の同定は本書の小さな図から行った。確信できない記号を含む例は導出に入れず、<a href=\"" + REPO + "/blob/main/notes/rahman-map.md\">章と主張の対応表</a>に記した。",
 "The book is paraphrased with page numbers; figures and tables are not reproduced. All signs are redrawn from this site's data in Noto Sans Egyptian Hieroglyphs. Signs were identified from the book's small figures; examples with a sign that could not be identified confidently are left out of the derivations and listed in the <a href=\"" + REPO + "/blob/main/notes/rahman-map.md\">chapter and claim map</a>.")}</p>
<p class="meta">{BOOK[0]}</p>

<h2>{bi("章と主張", "Chapters and claims")}</h2>
<div class="table-scroll"><table><tr><th>{bi("章", "Ch.")}</th><th>pp.</th><th>{bi("内容", "Content")}</th><th>{bi("導出", "Derivations")}</th></tr>{ch_rows}</table></div>
<div class="flag spec">{bi(
 "<strong>推測/非主流。</strong>本書のうち、デンデラの黄道帯から文字を読む付録、三母音の IPA 体系、Alsaadawi による読み（ラテン・ヘブライ・アラビア文字の由来、「サラーム」「イーマーン」「ナビー」、ラメセス2世＝モーセ）、アレクサンドロスの角、カリオンの「ヒエログリフ」は、主流の研究の外にあり、このサイトの範囲外である。導出は作らない。",
 "<strong>Speculative / non-mainstream.</strong> The book's appendix reading letters from the Dendera zodiac, its three-vowel IPA scheme, the readings it takes from Alsaadawi (origins of Latin, Hebrew and Arabic letters; “salam”, “iman”, “nabi”; Ramesses II = Moses), the horns of Alexander, and the Kariong “hieroglyphs” lie outside mainstream scholarship and outside this site's scope. No derivations are made for them.")}</div>

<h2>{bi("結果", "Results")}</h2>
{cat_table}
<p>{bi(
 f"{n}件の導出のうち、{n_re}件で WALK_write ≠ WALK_read となり、{n_mm}件で層 B の構成素が層 A のどの構成素とも一致しない（MISMATCH）。",
 f"Of {n} derivations, {n_re} have WALK_write ≠ WALK_read, and in {n_mm} a layer-B constituent coincides with no layer-A constituent (MISMATCH).")}</p>
<ol>
<li>{bi(
 "本書のいう「本来の発音」（pp. 36–38）は、どれも補音の付いた綴りを、補音も読んで発音したものである。層 B では補音は CMPL の中で多子音記号に吸収され、音を足さない。食い違いの大半はこの一点から出ている。",
 "Every 'authentic pronunciation' in the book (pp. 36–38) is a spelling with phonetic complements, read with the complements sounded. In layer B a complement is absorbed into the multiliteral inside CMPL and adds no sound. Most of the discrepancies trace back to this one point.")}</li>
<li>{bi(
 "本書が自分の貢献とする「複合」（pp. 53–56）は、標準では限定符による閉じに当たる。ただし「右端の表語が語の部類を決める（内心的）」という本書の観察は、限定符を主要部（_H）とする規格 v1 の扱いとほぼ同じである。呼び名は違っても、観察は一致している。",
 "What the book presents as its own 'compounding' (pp. 53–56) is, in standard terms, a word closed by a determinative. Yet the book's remark that the rightmost ideogram fixes the word's class (endocentric) says almost the same as v1's marking of the determinative as head (_H). Different labels, same observation.")}</li>
<li>{bi(
 "敬意による転置について、本書は規則を正しく述べる（p. 40）が、音写は書き順のままにする（/ntr-hw-t-pr/、pth-mrj）。二層に分けると、この食い違いは「一つの木、二つの歩き」として正確に書ける（d19・d20）。神名が先頭でも転置ではない例（d21）と並べると、転置は木ではなく歩きの性質だとわかる。",
 "On honorific transposition the book states the rule correctly (p. 40) but transcribes in written order (/ntr-hw-t-pr/, pth-mrj). With two layers this gap is stated exactly as one tree with two walks (d19, d20). Set beside a god-first name that is not transposed (d21), transposition shows up as a property of the walk, not the tree.")}</li>
<li>{bi(
 "方形はしばしば機能の構成素を横切る。nfrt の［⿳ f r t］、iꜣwt の差し込み［w ⿻ t］、nswt-bjtj の 2×2 の方形、クレオパトラの［t ⿱ 卵］がそうである。本書の「切り詰め」（nswt → スゲ一つ、「クレオパトラツァ」）は、層 B の上では語の短縮ではなく、書き方の短縮（ABBR）や読まない限定符として書ける。",
 "Quadrats often cut across function constituents: [⿳ f r t] in nfrt, the insertion [w + t] in iꜣwt, the 2×2 quadrat of nswt-bjtj, [t ⿱ egg] in Cleopatra. The book's 'clipping' (nswt → one sedge; 'Cleopatratsa') can be written in layer B not as a shortened word but as a shortened writing (ABBR) or a silent determinative.")}</li>
</ol>

<h2>{bi("標準の参考書との食い違い", "Discrepancies with the standard references")}</h2>
<div class="table-scroll"><table><tr><th>{bi("導出", "Deriv.")}</th><th>{bi("本書", "Book")}</th><th>{bi("標準", "Standard")}</th></tr>
<tr><td><a href="#d01">d01</a>–<a href="#d07">d07</a>, <a href="#d13">d13</a></td><td>{bi("補音も発音する（d03 では限定符も）", "complements are sounded (in d03, the determinative too)")}</td><td>{bi("補音も限定符も音を足さない（Gardiner 1957）", "complements and determinatives add no sound (Gardiner 1957)")}</td></tr>
<tr><td><a href="#d04">d04</a></td><td>{bi("Šw を「神」と訳す", "Šw glossed 'god'")}</td><td>{bi("神名シュー。A40 は限定符", "the god Shu; A40 is the determinative")}</td></tr>
<tr><td><a href="#d11">d11</a>, <a href="#d12">d12</a></td><td>{bi("表音＋表語の複合語", "phonogram + ideogram compound")}</td><td>{bi("限定符で閉じた語", "a word closed by a determinative")}</td></tr>
<tr><td><a href="#d18">d18</a></td><td>{bi("sḏm を「考える」", "sḏm glossed 'to think'")}</td><td>{bi("sḏm は「聞く」（Gardiner 1957、Allen 2010）", "sḏm 'hear' (Gardiner 1957; Allen 2010)")}</td></tr>
<tr><td><a href="#d19">d19</a>, <a href="#d20">d20</a></td><td>{bi("規則は正しいが、音写は書き順", "rule stated correctly; transcription in written order")}</td><td>{bi("話し言葉の順で読む（Gardiner 1957 §57）", "read in spoken order (Gardiner 1957, §57)")}</td></tr>
<tr><td><a href="#d22">d22</a></td><td>/swtnt-nt/</td><td>nswt-bjtj（Allen 2010; Poe）</td></tr>
<tr><td><a href="#d23">d23</a></td><td>{bi("形態論の切り詰め", "morphological clipping")}</td><td>{bi("書き方の略記（Gardiner 1957）", "abbreviated writing (Gardiner 1957)")}</td></tr>
<tr><td><a href="#d26">d26</a></td><td>{bi("「クレオパトラツァ」", "'Cleopatratsa'")}</td><td>{bi("t は女性語尾、卵は読まない限定符（Champollion 1822、Callimahos）", "t is the feminine ending, the egg a silent determinative (Champollion 1822; Callimahos)")}</td></tr>
</table></div>

{groups}

<h2>{bi("未決の問い", "Open questions")}</h2>
<ul>
<li>{bi("解決（2026年11月27日）：d03 ḥb の W3 は綴りを閉じる限定符とした（Gardiner 1957, p. 527; Allen 2010, p. 448）。<a href=\"resolutions#d03\">未決の解決</a>を見よ。", "Resolved (27 Nov 2026): in d03 ḥb, W3 is the determinative closing the spelling (Gardiner 1957, p. 527; Allen 2010, p. 448). See <a href=\"resolutions#d03\">Resolutions</a>.")}</li>
<li>{bi("解決（2026年11月27日）：d22 の転置は書記上のもの（graphic）とした。2×2 の方形を行ごとに辿るか列ごとに辿るかは OPEN のまま。<a href=\"resolutions#d22\">未決の解決</a>を見よ。", "Resolved (27 Nov 2026): the d22 reorder is graphic. Whether the 2×2 quadrat is walked by rows or by columns stays OPEN. See <a href=\"resolutions#d22\">Resolutions</a>.")}</li>
<li>{bi("解決（2026年11月27日）：d20 の図は右から左に読み、記号は右を向く。向きの食い違いはなかった。<a href=\"resolutions#d20\">未決の解決</a>を見よ。", "Resolved (27 Nov 2026): the d20 figure reads right to left and its signs face right; there was no mismatch. See <a href=\"resolutions#d20\">Resolutions</a>.")}</li>
<li>{bi("方形の中で列ごとに読む並べ替え（d22）に、規格 v1 で専用のラベルを設けるべきか。", "Should v1 add a label for column-wise reading inside a quadrat (d22)?")}</li>
</ul>
'''
    return derivations, notation, rahman

SOURCES_EXTRA = [BOOK, STANDARD] + [REFS[k] for k in ('Allen 2010', 'Peust 2007', 'Champollion 1822', 'Callimahos', 'Poe', 'Rosetta Stone (BM EA 24)', 'Hierolyte')]
