#!/usr/bin/env python3
"""Build the static pages in site/ from the census data and the page texts below.
Japanese is written first (である調); English is fitted to it."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
P = json.load(open(ROOT / 'data/pilot-census.json', encoding='utf8'))
K = json.load(open(ROOT / 'data/kanji-arity-reference.json', encoding='utf8'))
KANJI = 'https://kanji-morphology.pages.dev/'
REPO = 'https://github.com/crimsonflower420/Hieroglyph-Operators'

NAV = [('index', 'トップ', 'Top'), ('concept', '考え方', 'Concept'), ('operators', '演算子', 'Operators'),
       ('pilot', 'パイロット調査', 'Pilot'), ('sources', '出典', 'Sources')]

def bi(ja, en, tag='span', cls=''):
    c = f' {cls}' if cls else ''
    return f'<{tag} class="ja{c}" lang="ja">{ja}</{tag}><{tag} class="en{c}" lang="en">{en}</{tag}>'

def page(slug, title_ja, title_en, body):
    nav = ''.join(f'<li><a href="{s if s != "index" else "./"}"{" aria-current=\"page\"" if s == slug else ""}>{bi(j, e)}</a></li>' for s, j, e in NAV)
    nav += f'<li><a href="{KANJI}">{bi("順序の漢字 ↗", "Kanji in Order ↗")}</a></li>'
    return f'''<!DOCTYPE html>
<html lang="ja" data-lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_ja} — ヒエログリフの演算子</title>
<meta name="title-ja" content="{title_ja} — ヒエログリフの演算子">
<meta name="title-en" content="{title_en} — Hieroglyph Operators">
<meta name="description" content="Egyptian hieroglyphic quadrats read as operator trees over Gardiner signs. A sister site to Kanji in Order.">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preload" href="fonts/NotoSansEgyptianHieroglyphs-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/main.css">
<script>
(function () {{
  try {{
    var r = document.documentElement, t = localStorage.getItem('ho-theme');
    var th = (t === 'light' || t === 'dark') ? t : (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    r.setAttribute('data-theme', th); r.style.colorScheme = th;
    var q = (location.search.match(/[?&]lang=(ja|en)/) || [])[1];
    var l = q || localStorage.getItem('ho-lang'); if (l !== 'en' && l !== 'ja') l = 'ja';
    r.lang = l; r.setAttribute('data-lang', l);
  }} catch (e) {{}}
}})();
</script>
</head>
<body>
<a class="skip" href="#main">{bi("本文へ", "Skip to content")}</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="./"><span class="brand-glyph" aria-hidden="true" data-q="𓊪𓐰𓏏" data-size="1.7em"></span>{bi("ヒエログリフの演算子", "Hieroglyph Operators")}<small>{bi("方形を演算子の木として読む", "quadrats as operator trees")}</small></a>
    <div class="controls">
      <form class="seg lang-toggle" aria-label="Language"><label><input type="radio" name="lang" value="ja"><span>JA</span></label><label><input type="radio" name="lang" value="en"><span>EN</span></label></form>
      <form class="seg theme-toggle" aria-label="Theme"><label><input type="radio" name="theme" value="light"><span>{bi("明", "Light")}</span></label><label><input type="radio" name="theme" value="auto"><span>{bi("自動", "Auto")}</span></label><label><input type="radio" name="theme" value="dark"><span>{bi("暗", "Dark")}</span></label></form>
    </div>
    <nav class="primary" aria-label="Primary"><ul>{nav}</ul></nav>
  </div>
</header>
<main id="main"><div class="wrap">
{body}
</div></main>
<footer class="site-footer"><div class="wrap">
<p>{bi("研究ノートのサイトであり、随時改訂する。", "A research-notes site, revised as the work goes on.")} <a href="{REPO}">Hieroglyph-Operators</a> · {bi("姉妹サイト", "Sister site")}: <a href="{KANJI}">{bi("順序の漢字", "Kanji in Order")}</a></p>
<p>{bi("ヒエログリフの字形：Noto Sans Egyptian Hieroglyphs（SIL OFL 1.1）。EA 581 の符号化：M.-J. Nederhof（HieroJax、GPL-3.0）。", "Glyphs: Noto Sans Egyptian Hieroglyphs (SIL OFL 1.1). EA 581 encoding: M.-J. Nederhof (HieroJax, GPL-3.0).")}</p>
<p>Theory Desk · Grant Golland</p>
</div></footer>
<script src="js/site.js" defer></script>
<script src="js/quadrat.js" defer></script>
</body>
</html>
'''

def pct(a, b):
    return f'{100 * a / b:.0f}%' if b else '–'

# ---------------------------------------------------------------- numbers
pc, sc = P['pilot']['census'], P['stela']['census']
bd = P['stela']['byDirection']
def nodes_of(c): return c['nodes']
hor_h = bd['hrl']['ops'].get('hor', 0); n_h = bd['hrl']['nodes']
hor_v = bd['vrl']['ops'].get('hor', 0); n_v = bd['vrl']['nodes']
k_nodes = K['nodes']
k_a2 = K['arity']['2']; k_a3p = k_nodes - k_a2
k_maxd = max(int(d) for d in K['depth'])
s_a2 = sc['arity'].get('2', 0); s_a3p = sc['nodes'] - s_a2
s_maxd = max(int(d) for d in sc['depth'])
p_h1 = pc['height'].get('1', 0)

# ---------------------------------------------------------------- top
ex_q = '𓆑𓐰𓈖𓐰𓄓𓐳𓀀'
index = f'''
<p class="tag">{bi("姉妹サイト・パイロット段階", "Sister site · pilot stage")}</p>
<h1>{bi("ヒエログリフの演算子", "Hieroglyph Operators")}</h1>
<p class="lede">{bi(
 "古代エジプトのヒエログリフは、記号を「方形（クァドラート）」と呼ばれる見えない四角の中に、上下・左右・差し込み・重ね合わせで並べて書く。このサイトは、その並べ方を演算子の木として書き出し、数えてみる試みである。",
 "Ancient Egyptian hieroglyphs are written by packing signs into an invisible square called a quadrat: one above another, side by side, tucked into a corner, or laid over one another. This site writes those arrangements out as operator trees and counts them.")}</p>
<p>{bi(
 f"見方は姉妹サイト<a href=\"{KANJI}\">「順序の漢字」</a>から借りている。漢字のサイトでは、字を「画→部品→字」という順序づけの過程の出力として扱う。ここでは同じ見方をヒエログリフに当て、どこまで通用し、どこで通用しないかを確かめる。",
 f"The lens is borrowed from the sister site, <a href=\"{KANJI}\">Kanji in Order</a>, which treats a kanji as the output of an ordering process: strokes, then components, then characters. Here the same lens is pointed at hieroglyphs, to see where it holds and where it does not.")}</p>
<figure>
<span data-q="{ex_q}" data-size="5.5em"></span>
<figcaption>{bi(
 "Unicode 標準の例（図11-5）。I9 の下に N35、その下に F20 を置き、F20 の左下の隅に A1 を差し込む。符号列は &lt;13191, 13430, 13216, 13430, 13113, 13433, 13000&gt;。描画はこのサイトの簡易レイアウトである。",
 "An example from the Unicode Standard (Figure 11-5): I9 above N35 above F20, with A1 inserted at F20's bottom-start corner. Sequence &lt;13191, 13430, 13216, 13430, 13113, 13433, 13000&gt;. Drawn by this site's schematic layout.")}</figcaption>
</figure>

<h2>{bi("いまの結果（パイロット）", "Results so far (pilot)")}</h2>
<p>{bi(
 f"中王国の石碑、大英博物館 EA 581（インテフの石碑）で、複数の記号からなる最初の50の方形を演算子の木にした。演算子の節点は{pc['nodes']}個で、縦の結合が{pc['ops'].get('ver',0)}、横の結合が{pc['ops'].get('hor',0)}、差し込みが{pc['ops'].get('ins',0)}、重ね合わせは0である。50のうち{p_h1}は演算子一つだけの方形で、木の深さは最大でも{max(int(k) for k in pc['height'])}である。",
 f"On a Middle Kingdom stela, British Museum EA 581 (the stela of Intef), the first 50 multi-sign quadrats were written as operator trees. They have {pc['nodes']} operator nodes: {pc['ops'].get('ver',0)} vertical joins, {pc['ops'].get('hor',0)} horizontal joins, {pc['ops'].get('ins',0)} insertions and no overlays. {p_h1} of the 50 quadrats use a single operator, and no tree is deeper than {max(int(k) for k in pc['height'])}.")}</p>
<p>{bi(
 f"石碑全体（{sc['quadrats']}方形、節点{sc['nodes']}）では、横の結合の割合が、横書きの行では{pct(hor_h,n_h)}、縦書きの列では{pct(hor_v,n_v)}になる。演算子の内訳は行の向きとともに変わる。方形が語の構造よりも紙面の配置に従っていることと合う（推測）。",
 f"Over the whole stela ({sc['quadrats']} quadrats, {sc['nodes']} nodes), horizontal joins are {pct(hor_h,n_h)} of nodes in the horizontal lines and {pct(hor_v,n_v)} in the vertical columns. The operator mix moves with line direction, which fits the idea that quadrats follow page layout more than word structure (inference).")}</p>
<div class="cards">
<a class="card" href="concept"><strong>{bi("考え方", "Concept")}</strong><span>{bi("漢字から引き継げるものと、引き継げないもの。", "What carries over from kanji, and what does not.")}</span></a>
<a class="card" href="operators"><strong>{bi("演算子", "Operators")}</strong><span>{bi("Unicode の書式制御文字と Manuel de Codage の記号。", "The Unicode format controls and the Manuel de Codage signs.")}</span></a>
<a class="card" href="pilot"><strong>{bi("パイロット調査", "Pilot")}</strong><span>{bi("EA 581 の50方形：項数・深さ・演算子の頻度。", "50 quadrats from EA 581: arity, depth, operator counts.")}</span></a>
<a class="card" href="sources"><strong>{bi("出典", "Sources")}</strong><span>{bi("一次資料、コーパス、ライセンス。", "Primary sources, corpora, licences.")}</span></a>
</div>
<div class="flag spec">{bi(
 "<strong>注意。</strong>ここでの木は配置の記述であり、ヒエログリフが統語構造をもつという主張ではない。推測や推論はその都度そう明記する。",
 "<strong>Note.</strong> The trees here describe arrangement. They are not a claim that hieroglyphs have syntax. Inference and speculation are labelled where they appear.")}</div>
<p>{bi("ほかの文字体系も、今後それぞれ独立したサイトで扱う予定である。", "Other writing systems will get their own sites later.")}</p>
'''

# ---------------------------------------------------------------- concept
concept = f'''
<h1>{bi("考え方：漢字から何を引き継ぐか", "Concept: what carries over from kanji")}</h1>
<p class="lede">{bi(
 "漢字のサイトは、字を三層の順序の出力として読む。画の並び（筆順）、部品の並び、そして部品を組み合わせる演算子の木である。ヒエログリフでは、この三層のうち一つはそのまま当てはまり、一つは足場がなく、一つは意味が変わる。",
 "The kanji site reads a character as the output of three layers of order: the order of strokes, the order of components, and the operator tree that combines components. For hieroglyphs, one of these layers fits as it is, one has nothing to stand on, and one changes its meaning.")}</p>

<h2>{bi("1. 引き継げるもの：配置の演算子", "1. What carries over: operators of arrangement")}</h2>
<p>{bi(
 "ヒエログリフの方形は、少数の配置操作で書ける。Unicode は 12.0 で9個の書式制御文字（縦の結合 U+13430、横の結合 U+13431、四隅への差し込み、重ね合わせ、区切りの開始と終了）を加え、15.0 でさらに29個（中央・上・下への差し込み、囲み、鏡映、欠損の印など）を加えた。縦の結合は Manuel de Codage の「:」、横の結合は「*」に当たる。",
 "A hieroglyphic quadrat can be written with a handful of arrangement operations. Unicode 12.0 added nine format controls (vertical joiner U+13430, horizontal joiner U+13431, insertion at the four corners, overlay, begin and end segment), and Unicode 15.0 added 29 more (insertion at middle, top and bottom, enclosures, mirroring, damage marks and others). The vertical joiner corresponds to the Manuel de Codage colon “:” and the horizontal joiner to the asterisk “*”.")}</p>
<p>{bi(
 "縦の結合は漢字の ⿱、横の結合は ⿰ に近く、差し込みは ⿴ や ⿺ などの囲みの仲間に近い。どちらの体系でも、方形や字は「演算子が引数を取る木」として書ける。<a href=\"operators\">演算子のページ</a>に一覧がある。",
 "The vertical joiner is close to the kanji ⿱, the horizontal joiner to ⿰, and insertion to the enclosure family such as ⿴ and ⿺. In both systems a quadrat or a character can be written as a tree of operators taking arguments. The <a href=\"operators\">operators page</a> lists them.")}</p>

<h2>{bi("2. 引き継げないもの：正準的な筆順", "2. What does not carry over: a canonical stroke order")}</h2>
<p>{bi(
 "漢字のサイトの大部分は、筆順を木のたどり方として調べている。ヒエログリフの記号は絵であり、記号の中の線を引く順序が規範として定められていたことを示す資料は、少なくとも記念碑の書体については見つかっていない。だからこの層には足場がない。",
 "Most of the kanji site studies stroke order as a walk through the tree. Hieroglyphic signs are pictures, and for the monumental script there is no evidence we have found that the order of lines inside a sign was ever prescribed. So this layer has nothing to stand on.")}</p>
<p>{bi(
 "筆記体のヒエラティックには手がかりがある。マインツの AKU-PAL データベースは、版1.3（2024年）から、ヒエラティックの字形ごとに筆の運び（Strichfolge）をベクトル画像で示している。Regulski（2018）は、パピルス Gardiner II（BM EA 10676）で、記号を組み立てる個々の筆の運びを調べ、一つの文書の中でどこまで揃っているかを論じている。",
 "The cursive hieratic script offers some leads. Since version 1.3 (2024) the AKU-PAL database in Mainz shows the stroke sequence (Strichfolge) of hieratic graphemes as vector graphics. Regulski (2018) studies the individual brush strokes that build signs in Papyrus Gardiner II (BM EA 10676) and asks how standardised they are within a single document.")}</p>
<div class="flag spec">{bi(
 "<strong>推測。</strong>ヒエラティックの筆の運びが、漢字の筆順のような共有の規範だったのか、書き手ごとの癖だったのかは、ここではまだ確かめていない。Regulski の論文は個人の書き癖を手がかりにしており、規範の存在を示すものではない。",
 "<strong>Speculation.</strong> Whether hieratic stroke sequences were a shared norm like kanji stroke order, or individual habit, has not been checked here. Regulski's paper works from individual writing habits; it does not show that a norm existed.")}</div>

<h2>{bi("3. 意味が変わるもの：読む向き", "3. What changes meaning: reading direction")}</h2>
<p>{bi(
 "ヒエログリフは右から左にも左から右にも、横にも縦にも書かれる。人や動物の顔は行の始まりの方を向くので、読み手は顔に向かって読む。Unicode はヒエログリフに左から右の強い方向性を与え、右から左に表示するときは字形を鏡映すべきだとしている。",
 "Hieroglyphs are written right to left or left to right, in rows or in columns. The faces of people and animals look toward the start of the line, so the reader reads into the faces. Unicode gives hieroglyphs strong left-to-right directionality and says glyphs should be mirrored when the text is displayed right to left.")}</p>
<p>{bi(
 "漢字では、部品の並びの順序が字の中で固定されている。ヒエログリフでは、方形の中の「始まりの側」が行の向きで入れ替わる。Unicode の差し込みの名前が「左上」ではなく「上の始まり側（top start）」になっているのは、このためだと考えられる（推論）。順序の問いは、字の組み立ての問いから、紙面の配置の問いに移る。",
 "In kanji, the order of components inside a character is fixed. In a hieroglyphic quadrat, which side counts as the start flips with the line direction. This is presumably why the Unicode insertion controls are named “top start” and not “top left” (inference). The ordering question moves from how a character is built to how a surface is laid out.")}</p>

<h2>{bi("4. 意味が変わるもの：方形は語ではない", "4. What changes meaning: a quadrat is not a word")}</h2>
<p>{bi(
 "漢字一字は、ふつう一つの形態素に当たる。方形はそうではない。Unicode 標準は、記号が「見た目のよい形で」概念上の四角の中に並べられると書いている。EA 581 でも、地名アビドス（3行目）は二つの方形（U23 * D58 と N26 : O49）にまたがって書かれている。逆に、3行目の D21 : I9 では、語の終わりの r と、続く接尾代名詞 =f の f が一つの方形に入っている（読みは推定）。",
 "One kanji usually corresponds to one morpheme. A quadrat does not. The Unicode Standard says signs were arranged “in an aesthetically-pleasing manner” within a notional rectangle. On EA 581 the place name Abydos (line 3) runs over two quadrats (U23 * D58 and N26 : O49). The other way round, D21 : I9 in line 3 holds the final r of one word and the f of the suffix pronoun =f that follows it (reading inferred).")}</p>
<p>{bi(
 f"パイロット調査の数字もこれと合う。EA 581 では、横の結合の割合が横書きの行で{pct(hor_h,n_h)}、縦書きの列で{pct(hor_v,n_v)}である。同じ文章の中で、行の形が演算子の選び方を変えている（推論）。",
 f"The pilot numbers fit this. On EA 581, horizontal joins make up {pct(hor_h,n_h)} of nodes in horizontal lines and {pct(hor_v,n_v)} in vertical columns. Within one text, the shape of the line changes which operators are used (inference).")}</p>

<h2>{bi("まとめ", "Summary")}</h2>
<div class="table-scroll"><table>
<tr><th>{bi("層", "Layer")}</th><th>{bi("漢字", "Kanji")}</th><th>{bi("ヒエログリフ", "Hieroglyphs")}</th></tr>
<tr><td>{bi("画の並び", "Stroke order")}</td><td>{bi("規範がある", "Prescribed")}</td><td>{bi("記念碑体では規範の証拠なし。ヒエラティックに手がかり", "No evidence of a norm in the monumental script; leads in hieratic")}</td></tr>
<tr><td>{bi("演算子の木", "Operator tree")}</td><td>{bi("字の内部構造", "Inner structure of a character")}</td><td>{bi("方形の配置（Unicode・MdC で符号化できる）", "Layout of a quadrat (encodable in Unicode and MdC)")}</td></tr>
<tr><td>{bi("読む向き", "Reading direction")}</td><td>{bi("字の中では固定", "Fixed inside a character")}</td><td>{bi("行ごとに変わる。顔は行の始まりを向く", "Varies by line; faces look to the line's start")}</td></tr>
<tr><td>{bi("単位", "Unit")}</td><td>{bi("ほぼ形態素", "Roughly a morpheme")}</td><td>{bi("配置の単位で、語とは一致しない", "A layout unit, not aligned with words")}</td></tr>
</table></div>
<div class="flag">{bi(
 "演算子の木は記述のための道具であり、ヒエログリフが統語をもつという主張ではない。",
 "The operator tree is a descriptive tool. It is not a claim that hieroglyphs have syntax.")}</div>
'''

# ---------------------------------------------------------------- operators
OPS = [
 ('13430', 'VERTICAL JOINER', ':', '12.0', '縦の結合。前の記号を上、後の記号を下に置く。', 'Vertical join: the first sign above, the next below.', '⿱', '𓀀𓐰𓉐'),
 ('13431', 'HORIZONTAL JOINER', '*', '12.0', '横の結合。論理順に並べる。', 'Horizontal join, in logical order.', '⿰', '𓏌𓐱𓏲'),
 ('13432', 'INSERT AT TOP START', '', '12.0', '前の記号の、上の始まり側の隅に差し込む。', 'Insert into the top-start corner of the preceding sign.', '⿽ (U+2FFD)', '𓄂𓐲𓏏'),
 ('13433', 'INSERT AT BOTTOM START', '', '12.0', '下の始まり側の隅に差し込む。', 'Insert into the bottom-start corner.', '⿹', '𓆓𓐳𓀀'),
 ('13434', 'INSERT AT TOP END', '', '12.0', '上の終わり側の隅に差し込む。', 'Insert into the top-end corner.', '⿺', '𓂇𓐴𓏏'),
 ('13435', 'INSERT AT BOTTOM END', '', '12.0', '下の終わり側の隅に差し込む。', 'Insert into the bottom-end corner.', '⿸', '𓅜𓐵𓏏'),
 ('13436', 'OVERLAY MIDDLE', '# / ##', '12.0', '後の記号を前の記号の上に重ねる。中心で揃える。', 'Lay the next sign over the preceding one, centred.', '⿻', '𓂝𓐶𓎛'),
 ('13437', 'BEGIN SEGMENT', '(', '12.0', '入れ子のまとまりを開く。', 'Open a nested group.', '', ''),
 ('13438', 'END SEGMENT', ')', '12.0', '入れ子のまとまりを閉じる。', 'Close a nested group.', '', ''),
 ('13439', 'INSERT AT MIDDLE', '', '15.0', '記号の中央に差し込む。', 'Insert in the middle of a sign.', '⿴', '𓈙𓐹𓊃'),
 ('1343A', 'INSERT AT TOP', '', '15.0', '上が開いた記号の中に差し込む。', 'Insert into a sign open at the top.', '⿶', '𓂓𓐺𓐍'),
 ('1343B', 'INSERT AT BOTTOM', '', '15.0', '下が開いた記号の中に差し込む。', 'Insert into a sign open at the bottom.', '⿵', '𓂘𓐻𓎛'),
 ('1343C', 'BEGIN ENCLOSURE', '', '15.0', '囲み（カルトゥーシュなど）を開く。', 'Open an enclosure such as a cartouche.', '', ''),
 ('1343D', 'END ENCLOSURE', '', '15.0', '囲みを閉じる。', 'Close an enclosure.', '', ''),
 ('1343E', 'BEGIN WALLED ENCLOSURE', '', '15.0', '壁のある囲みを開く。', 'Open a walled enclosure.', '', ''),
 ('1343F', 'END WALLED ENCLOSURE', '', '15.0', '壁のある囲みを閉じる。', 'Close a walled enclosure.', '', ''),
 ('13440', 'MIRROR HORIZONTALLY', '', '15.0', '記号を行の向きに対して鏡映する（結合文字）。', 'Mirror a sign relative to line direction (combining mark).', '', ''),
]
def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;')
rows = ''.join(f'<tr><td class="mono">U+{c}</td><td class="mono">{n}</td><td class="mono">{esc(m) or "–"}</td><td>{v}</td><td>{bi(j, e)}</td><td>{k or "–"}</td><td>{f"<span data-q=\"{x}\" data-size=\"2.6em\"></span>" if x else ""}</td></tr>' for c, n, m, v, j, e, k, x in OPS)
operators = f'''
<h1>{bi("演算子：Unicode の書式制御文字と Manuel de Codage", "Operators: Unicode format controls and the Manuel de Codage")}</h1>
<p class="lede">{bi(
 "方形の配置を書くための記号は、二つの系統がある。一つは1980年代にエジプト学者がまとめた Manuel de Codage（MdC）の ASCII 記号、もう一つは Unicode の書式制御文字である。Unicode の制御文字のうち4つ（縦と横の結合、区切りの開始と終了）は MdC から来ている。",
 "There are two families of signs for writing quadrat layout. One is the ASCII notation of the Manuel de Codage (MdC), drawn up by Egyptologists in the 1980s. The other is the Unicode format controls. Four of the Unicode controls (the vertical and horizontal joiners, begin and end segment) derive from MdC.")}</p>

<h2>{bi("Unicode の書式制御文字（U+13430–U+1345F）", "Unicode format controls (U+13430–U+1345F)")}</h2>
<p>{bi(
 "名前と版は Unicode 文字データベース（UnicodeData.txt と DerivedAge.txt、18.0.0）による。働きの説明は Unicode 標準 第11章 §11.4.3 の要約である。「漢字の近いもの」の列は、左から右に書くときの見た目の類似を示すだけで、同じものだという主張ではない（差し込みの「始まり側」は行の向きで左右が入れ替わる）。",
 "Names and versions are from the Unicode Character Database (UnicodeData.txt and DerivedAge.txt, 18.0.0). The descriptions summarise the Unicode Standard, chapter 11, §11.4.3. The “kanji analogue” column shows a visual likeness for left-to-right text only; it does not claim the two are the same (the “start” side of an insertion flips with line direction).")}</p>
<div class="table-scroll wide"><table>
<tr><th>{bi("符号位置", "Code point")}</th><th>{bi("名前（EGYPTIAN HIEROGLYPH …）", "Name (EGYPTIAN HIEROGLYPH …)")}</th><th>MdC</th><th>{bi("版", "Version")}</th><th>{bi("働き", "Function")}</th><th>{bi("漢字の近いもの", "Kanji analogue")}</th><th>{bi("例", "Example")}</th></tr>
{rows}
</table></div>
<p>{bi(
 "このほか 15.0 では、空白（U+13441–13442）、失われた記号（U+13443–13446）、欠損の位置を示す15個の修飾文字（U+13447–13455）が加わった。これらは校訂のための印であり、配置の演算子ではない。回転は StandardizedVariants.txt の異体字セレクタ VS1–VS3（90°・180°・270°）で表す。",
 "Unicode 15.0 also added blanks (U+13441–13442), lost signs (U+13443–13446) and 15 modifiers marking where a sign is damaged (U+13447–13455). These are editorial marks, not arrangement operators. Rotation is written with variation selectors VS1–VS3 (90°, 180°, 270°) defined in StandardizedVariants.txt.")}</p>
<div class="flag">{bi(
 "<strong>描画について。</strong>Noto Sans Egyptian Hieroglyphs（v2.002）には、これらの制御文字による方形の組版機能がない（制御文字の字形もない）。このサイトの方形は、記号ごとに Noto の字形を使い、このサイトのスクリプトで簡易に配置したものである。左から右に描いている。Noto にない拡張A（U+13460 以降）の記号は点線の枠で示す。",
 "<strong>About rendering.</strong> Noto Sans Egyptian Hieroglyphs (v2.002) does not shape quadrats from these controls and has no glyphs for them. The quadrats on this site use Noto glyphs for each sign and are laid out by this site's own script, approximately and left to right. Extended-A signs (U+13460 and up), which Noto lacks, are shown as dotted boxes.")}</div>

<h2>{bi("文法：何が何の引数になるか", "Grammar: what can be an argument of what")}</h2>
<p>{bi(
 "Nederhof が公開している文法（HieroJax の「Syntax」ページ、および L2/24-079）では、横の結合が縦の結合より強く結びつく。縦のまとまりの各段は横のまとまりでもよいが、横のまとまりの中に縦のまとまりを入れるには区切り（U+13437/13438）が要る。差し込みと重ね合わせは、さらに強く結びつく。",
 "In the grammar Nederhof publishes (the HieroJax “Syntax” page, and L2/24-079), the horizontal joiner binds tighter than the vertical joiner. Each tier of a vertical group may be a horizontal group, but a vertical group inside a horizontal group needs segment brackets (U+13437/13438). Insertion and overlay bind tighter still.")}</p>
<figure><span data-q="𓅊𓐴𓐷𓈌𓐰𓈌𓐸" data-size="4em"></span> <span data-q="𓐝𓐰𓏶𓐱𓐷𓁷𓐱𓐷𓂋𓐰𓏏𓐸𓐰𓈉𓐸" data-size="4em"></span>
<figcaption>{bi(
 "Unicode 標準 図11-5 の例。左：G9 の上の終わり側に（N27 : N27）を差し込む。右：J15 : (Z11 * (D2 * (D21 : X1) : N25)) のような入れ子。",
 "Examples from Unicode Standard Figure 11-5. Left: (N27 : N27) inserted at the top-end of G9. Right: a nesting of the form J15 : (Z11 * (D2 * (D21 : X1) : N25)).")}</figcaption></figure>
<p>{bi(
 "Nederhof は、区切りの対応づけは正規言語の能力を超え、入れ子の深さに上限がないため、OpenType がすべての正しい符号列を描けるとは期待されていないと書いている（L2/24-079）。",
 "Nederhof notes that matching segment brackets is beyond the power of regular languages, and that because nesting depth is unbounded, OpenType fonts are not expected to render every valid encoding (L2/24-079).")}</p>

<h2>{bi("Manuel de Codage と JSesh", "The Manuel de Codage and JSesh")}</h2>
<p>{bi(
 "MdC（Buurman ほか 1988）は、記号をガーディナー番号（A1、N35 など）か音価（n、ra など）で書き、配置を ASCII の記号で書く。JSesh はその代表的な実装で、JSesh の文書は次の記号を挙げている。",
 "The MdC (Buurman et al. 1988) writes each sign by its Gardiner number (A1, N35, …) or by a phonetic value (n, ra, …), and writes layout with ASCII symbols. JSesh is its main implementation; JSesh's documentation gives these symbols.")}</p>
<div class="table-scroll"><table>
<tr><th>MdC</th><th>{bi("意味", "Meaning")}</th><th>Unicode</th></tr>
<tr><td class="mono">-</td><td>{bi("方形（または記号）の区切り", "Separates quadrats (or signs)")}</td><td>{bi("（区切り文字なし。並べるだけ）", "(no character; groups simply follow)")}</td></tr>
<tr><td class="mono">:</td><td>{bi("上下に重ねる", "Stack vertically")}</td><td class="mono">U+13430</td></tr>
<tr><td class="mono">*</td><td>{bi("左右に並べる", "Place side by side")}</td><td class="mono">U+13431</td></tr>
<tr><td class="mono">( )</td><td>{bi("まとまりを作る", "Grouping")}</td><td class="mono">U+13437 / U+13438</td></tr>
<tr><td class="mono">&amp;</td><td>{bi("合字", "Ligature")}</td><td>{bi("差し込みまたは単一の合成記号", "Insertion, or an atomic compound sign")}</td></tr>
<tr><td class="mono">#、##</td><td>{bi("重ね合わせ（公式は #、JSesh は保存時に ## に直す）", "Overlay (officially #; JSesh rewrites it as ## on saving)")}</td><td class="mono">U+13436</td></tr>
<tr><td class="mono">^^^、&amp;&amp;&amp;</td><td>{bi("JSesh の拡張：まとまりを記号の所定の領域に差し込む", "JSesh extensions: insert a group into a sign's predefined zone")}</td><td>{bi("差し込みの制御文字", "Insertion controls")}</td></tr>
<tr><td class="mono">!、!!</td><td>{bi("行末、ページ末", "End of line, end of page")}</td><td>–</td></tr>
</table></div>
<p>{bi(
 "MdC 自体は単一の厳密な規格ではなく、実装ごとに方言がある。上の表は JSesh の文書（MdC の説明と JSesh 6 の配置の解説）に従う。",
 "MdC is not one strict standard; implementations have dialects. The table follows JSesh's documentation (its MdC description and the note on JSesh 6 sign placement).")}</p>

<h2>{bi("ガーディナーの記号表", "Gardiner's sign list")}</h2>
<p>{bi(
 "引数になる記号は、ガーディナーの『エジプト語文法』（第3版 1957）の記号表の番号で呼ぶ。記号は主題ごとに A（人とその仕事）、B（女）、C（神）、D（人体の部分）…… Z（線・幾何形）、Aa（未分類）に分けられる。Unicode の基本ブロックはこの「ガーディナーの集合」を収め、名前は番号を3桁に埋めたもの（例：E034 は E34、砂漠の野うさぎ、音価 wn）である。",
 "Signs, the arguments, are named by their number in the sign list of Gardiner's Egyptian Grammar (3rd ed. 1957). Signs are grouped by subject: A (man and his occupations), B (woman), C (deities), D (parts of the human body) … Z (strokes and geometric figures), Aa (unclassified). The basic Unicode block holds this “Gardiner set”, and its names pad the number to three digits (for example E034 is E34, the desert hare, read wn).")}</p>
'''

# ---------------------------------------------------------------- pilot
def dist_table(rows_spec, cols):
    head = ''.join(f'<th class="num">{c}</th>' for c in cols)
    return head

def counts_row(label, d, keys, total):
    return f'<tr><td>{label}</td>' + ''.join(f'<td class="num">{d.get(k,0)} <small>({pct(d.get(k,0), total)})</small></td>' for k in keys) + f'<td class="num">{total}</td></tr>'

def arity_bins(d):
    a2 = d.get('2', 0); a3 = d.get('3', 0); rest = sum(v for k, v in d.items() if int(k) >= 4)
    return {'2': a2, '3': a3, '4+': rest}
def depth_bins(d):
    return {'1': d.get('1', 0), '2': d.get('2', 0), '3+': sum(v for k, v in d.items() if int(k) >= 3)}

kops = K['ops']
k_sur = sum(kops.get(x, 0) for x in '⿴⿵⿶⿷⿸⿹⿺⿻')
k_tri = kops.get('⿲', 0) + kops.get('⿳', 0)

def census_block(c):
    ab = arity_bins(c['arity']); db = depth_bins(c['depth'])
    return ab, db

pab, pdb = census_block(pc); sab, sdb = census_block(sc)
hab, hdb = census_block(bd['hrl']); vab, vdb = census_block(bd['vrl'])
kab = arity_bins(K['arity']); kdb = depth_bins(K['depth'])

def row3(label, b, keys, total):
    return f'<tr><td>{label}</td>' + ''.join(f'<td class="num">{b[k]} <small>({pct(b[k], total)})</small></td>' for k in keys) + f'<td class="num">{total}</td></tr>'

arity_tbl = f'''<div class="table-scroll"><table>
<tr><th></th><th class="num">{bi("2項","2-place")}</th><th class="num">{bi("3項","3-place")}</th><th class="num">{bi("4項以上","4+")}</th><th class="num">{bi("節点","Nodes")}</th></tr>
{row3(bi("パイロット（50方形）","Pilot (50 quadrats)"), pab, ['2','3','4+'], pc['nodes'])}
{row3(bi("石碑全体","Whole stela"), sab, ['2','3','4+'], sc['nodes'])}
{row3(bi("　横書きの行（1–7行）","　horizontal lines (1–7)"), hab, ['2','3','4+'], bd['hrl']['nodes'])}
{row3(bi("　縦書きの列（8–27行）","　vertical columns (8–27)"), vab, ['2','3','4+'], bd['vrl']['nodes'])}
{row3(bi("参考：常用漢字（KanjiVG）","Reference: jōyō kanji (KanjiVG)"), kab, ['2','3','4+'], K['nodes'])}
</table></div>'''
depth_tbl = f'''<div class="table-scroll"><table>
<tr><th></th><th class="num">{bi("深さ1","Depth 1")}</th><th class="num">{bi("深さ2","Depth 2")}</th><th class="num">{bi("深さ3以上","Depth 3+")}</th><th class="num">{bi("最大","Max")}</th></tr>
<tr><td>{bi("パイロット","Pilot")}</td>''' + ''.join(f'<td class="num">{pdb[k]} <small>({pct(pdb[k], pc["nodes"])})</small></td>' for k in ['1','2','3+']) + f'''<td class="num">{max(int(k) for k in pc['depth'])}</td></tr>
<tr><td>{bi("石碑全体","Whole stela")}</td>''' + ''.join(f'<td class="num">{sdb[k]} <small>({pct(sdb[k], sc["nodes"])})</small></td>' for k in ['1','2','3+']) + f'''<td class="num">{s_maxd}</td></tr>
<tr><td>{bi("参考：常用漢字","Reference: jōyō kanji")}</td>''' + ''.join(f'<td class="num">{kdb[k]} <small>({pct(kdb[k], K["nodes"])})</small></td>' for k in ['1','2','3+']) + f'''<td class="num">{k_maxd}</td></tr>
</table></div>'''
def opsrow(label, c):
    o = c['ops']; n = c['nodes']
    return f'<tr><td>{label}</td>' + ''.join(f'<td class="num">{o.get(k,0)} <small>({pct(o.get(k,0), n)})</small></td>' for k in ['ver','hor','ins','ovl']) + f'<td class="num">{n}</td></tr>'
ops_tbl = f'''<div class="table-scroll"><table>
<tr><th></th><th class="num">{bi("縦","Vertical")}</th><th class="num">{bi("横","Horizontal")}</th><th class="num">{bi("差し込み","Insertion")}</th><th class="num">{bi("重ね","Overlay")}</th><th class="num">{bi("節点","Nodes")}</th></tr>
{opsrow(bi("パイロット","Pilot"), pc)}
{opsrow(bi("石碑全体","Whole stela"), sc)}
{opsrow(bi("　横書きの行","　horizontal lines"), bd['hrl'])}
{opsrow(bi("　縦書きの列","　vertical columns"), bd['vrl'])}
</table></div>
<p>{bi(
 f"参考：常用漢字の節点{k_nodes}のうち、⿱ は{kops.get('⿱',0)}（{pct(kops.get('⿱',0),k_nodes)}）、⿰ は{kops.get('⿰',0)}（{pct(kops.get('⿰',0),k_nodes)}）、囲みの仲間（⿴⿵⿷⿸⿹⿺）は{k_sur}（{pct(k_sur,k_nodes)}）、⿲⿳ は{k_tri}、演算子の記録がないものが{kops.get('none',0)}（{pct(kops.get('none',0),k_nodes)}）である。",
 f"Reference: of the {k_nodes} jōyō kanji nodes, ⿱ is {kops.get('⿱',0)} ({pct(kops.get('⿱',0),k_nodes)}), ⿰ is {kops.get('⿰',0)} ({pct(kops.get('⿰',0),k_nodes)}), the enclosure family (⿴⿵⿷⿸⿹⿺) is {k_sur} ({pct(k_sur,k_nodes)}), ⿲⿳ is {k_tri}, and {kops.get('none',0)} ({pct(kops.get('none',0),k_nodes)}) have no recorded operator.")}</p>'''
ins_pos = ', '.join(f'{k} {v}' for k, v in sc['insPos'].items())
cells = ''.join(f'<div class="qcell"><span class="q" data-q="{it["u"]}" data-size="3.4em"></span><span class="x">{esc(it["expr"])}</span><br><span class="ln">{bi(f"{it["line"]}行 · {it["pos"]}番目", f"line {it["line"]} · #{it["pos"]}")}</span></div>' for it in P['pilot']['items'])
spq = ', '.join(f'{k}: {v}' for k, v in pc['signsPerQuadrat'].items())

pilot = f'''
<h1>{bi("パイロット調査：EA 581 の50方形", "Pilot: 50 quadrats from EA 581")}</h1>
<p class="lede">{bi(
 "一つの記念碑のテキストから、実際の方形を演算子の木として書き出し、項数・深さ・演算子の頻度を数えた。数え方はできるだけ漢字のサイトの項数調査に合わせたが、比較は記述にとどめる。",
 "Real quadrats from one monumental text were written out as operator trees, and their arity, depth and operator frequencies were counted. The definitions follow the kanji site's arity census where they can, but the comparison stays descriptive.")}</p>

<h2>{bi("資料", "Source")}</h2>
<p>{bi(
 "大英博物館 EA 581、インテフ（セネトの子）の石碑。石灰岩、アビドス出土、第12王朝初め（センウセレト1世の治世）。Unicode による符号化は M.-J. Nederhof が HieroJax のテキストページで公開しているものを使った（27行）。行の向きは同じ編者の RES による符号化（St Andrews コーパス）から取った：1–7行は横書き右→左、8–27行は縦書き右→左である。",
 "British Museum EA 581, the stela of Intef son of Senet. Limestone, from Abydos, early 12th Dynasty (reign of Senusret I). The Unicode encoding is the one M.-J. Nederhof publishes on a HieroJax text page (27 lines). Line direction comes from the same editor's RES encoding in the St Andrews corpus: lines 1–7 are horizontal right-to-left, lines 8–27 vertical right-to-left.")}</p>
<div class="flag spec">{bi(
 "<strong>注意。</strong>方形の中の相対位置は編者の符号化であり、複写（ファクシミリ）ではない。編者自身、St Andrews 版では大英博物館の写真と Sethe（1928）から起こしたと書いている。Unicode は記号の細かな大きさや間隔を表さない。",
 "<strong>Caveat.</strong> The relative positions inside quadrats are the editor's encoding, not a facsimile. In the St Andrews version the editor says it was transcribed from a British Museum photograph, with Sethe (1928). Unicode does not record fine sizes or spacing of signs.")}</div>

<h2>{bi("数え方", "Definitions")}</h2>
<ul>
<li>{bi("<b>まとまり</b>：符号列の最上位の単位（方形、または単独の記号）。", "<b>Group</b>: a top-level unit of the encoding (a quadrat, or a lone sign).")}</li>
<li>{bi("<b>節点</b>：項数2以上の演算子の適用。", "<b>Node</b>: an operator application with arity 2 or more.")}</li>
<li>{bi("<b>項数</b>：縦・横の結合は符号化どおりの要素数（a:b:c は3）。差し込みは1＋差し込まれたまとまりの数。重ね合わせは2。", "<b>Arity</b>: for vertical and horizontal joins, the number of members as encoded (a:b:c is 3). For insertion, 1 plus the number of inserted groups. For overlay, 2.")}</li>
<li>{bi("<b>深さ</b>：方形の根の節点を1とし、子の節点に入るごとに1を足す（漢字のサイトと同じ）。", "<b>Depth</b>: the quadrat's root node is depth 1, and each step into a child node adds one (as on the kanji site).")}</li>
<li>{bi("<b>パイロットの50</b>：符号列の順で、複数の記号からなる最初の50のまとまり（1–7行）。", "<b>The pilot 50</b>: the first 50 multi-sign groups in encoded order (lines 1–7).")}</li>
</ul>
<p>{bi(
 "解析器は Nederhof の文法に従い、27行すべてで符号列を木に変えてから元の符号列に戻し、完全に一致することを確かめた。スクリプトは <code>tools/quadrat_census.py</code>、データは <code>data/ea581-lines.json</code> と <code>data/pilot-census.json</code> である。",
 "The parser follows Nederhof's grammar. For all 27 lines, each string was parsed to trees and written back, and the result matched the original exactly. The script is <code>tools/quadrat_census.py</code>; the data are <code>data/ea581-lines.json</code> and <code>data/pilot-census.json</code>.")}</p>

<h2>{bi("結果", "Results")}</h2>
<p>{bi(
 f"パイロットの50方形には記号が{pc['signs']}個、節点が{pc['nodes']}個ある。方形あたりの記号数は {spq} である。50のうち{p_h1}は演算子一つだけの方形で、重ね合わせは一度も出てこない。石碑全体では、まとまり{sc['groups']}のうち{sc['single']}が単独の記号、{sc['quadrats']}が方形で、鏡映された記号が{sc['mirrored']}個ある。差し込みの位置は {ins_pos} である。",
 f"The pilot 50 quadrats hold {pc['signs']} signs and {pc['nodes']} nodes. Signs per quadrat: {spq}. {p_h1} of the 50 use a single operator, and overlay never occurs. Over the whole stela, {sc['single']} of {sc['groups']} groups are lone signs and {sc['quadrats']} are quadrats, with {sc['mirrored']} mirrored signs. Insertion positions: {ins_pos}.")}</p>
<h3>{bi("項数", "Arity")}</h3>
{arity_tbl}
<h3>{bi("節点の深さ", "Node depth")}</h3>
{depth_tbl}
<h3>{bi("演算子", "Operators")}</h3>
{ops_tbl}

<h2>{bi("漢字との比較（記述のみ）", "Comparison with kanji (descriptive only)")}</h2>
<p>{bi(
 f"常用漢字の節点では2項が{pct(k_a2,k_nodes)}、深さ3以上が{pct(kdb['3+'],k_nodes)}、最大の深さは{k_maxd}である。EA 581 の方形では2項が{pct(s_a2,sc['nodes'])}、深さ3以上が{pct(sdb['3+'],sc['nodes'])}、最大の深さは{s_maxd}である。方形の木は漢字の木より浅く、3項以上の節点が多い。",
 f"For jōyō kanji nodes, {pct(k_a2,k_nodes)} are 2-place, {pct(kdb['3+'],k_nodes)} are at depth 3 or more, and the maximum depth is {k_maxd}. For EA 581 quadrats, {pct(s_a2,sc['nodes'])} are 2-place, {pct(sdb['3+'],sc['nodes'])} are at depth 3 or more, and the maximum depth is {s_maxd}. Quadrat trees are shallower than kanji trees and have more nodes with three or more arguments.")}</p>
<div class="flag spec">{bi(
 "<strong>比較の限界。</strong>単位が違う。漢字の木は一字の内部構造で、引数は部品である。方形の木は数個の記号の配置で、記号は別々の語に属することがある。符号化の慣習も違う。Unicode は a:b:c を一つの3項の節点として書き、KanjiVG には独自の括り方がある。3項以上の割合の差の一部は、この慣習の差かもしれない（推測）。資料も、2,136字の一覧と、一つの石碑の294のまとまりで、規模が大きく違う。",
 "<strong>Limits of the comparison.</strong> The units differ. A kanji tree is the inner structure of one character, with components as arguments. A quadrat tree is the layout of a few signs, which may belong to different words. Encoding conventions differ too: Unicode writes a:b:c as one 3-place node, and KanjiVG has its own grouping habits. Part of the gap in 3+-place nodes may come from those conventions (speculation). The samples also differ greatly in size: a list of 2,136 characters against 294 groups on one stela.")}</div>

<h2>{bi("50の方形", "The 50 quadrats")}</h2>
<p>{bi(
 "式の「:」は縦、「*」は横、「⟨bs⟩」などは差し込みの位置（b＝下、t＝上、s＝始まり側、e＝終わり側）である。描画は左から右の簡易レイアウトで、原物は右から左に書かれている。",
 "In the expressions, “:” is vertical, “*” horizontal, and “⟨bs⟩” and the like give the insertion position (b bottom, t top, s start, e end). The drawings use a simple left-to-right layout; the original runs right to left.")}</p>
<div class="qgrid wide">{cells}</div>

<h2>{bi("未解決の問い", "Open questions")}</h2>
<ul>
<li>{bi("方形の境界は語の境界とどれだけ一致するか。TLA の語ごとの符号化と照らし合わせれば数えられるかもしれない。", "How often do quadrat boundaries match word boundaries? Matching against TLA's word-by-word encodings might make this countable.")}</li>
<li>{bi("縦書きの列で横の結合が増えるのは、列の幅に記号を詰めるためか。ほかの石碑やパピルスの転写でも同じか。", "Do horizontal joins rise in columns because signs are packed to the column's width? Does the same hold on other stelae, and in transcriptions of papyri?")}</li>
<li>{bi("ヒエラティックの筆の運び（AKU-PAL の Strichfolge）は、書き手を越えて共有された順序だったか。", "Were hieratic stroke sequences (AKU-PAL's Strichfolge) an order shared across scribes?")}</li>
<li>{bi("同じ語の方形の組み方は、時代や素材でどれだけ揺れるか。", "How much does the quadrat layout of the same word vary by period and medium?")}</li>
</ul>
'''

# ---------------------------------------------------------------- sources
SRC = [
 ('Unicode', [
  ('The Unicode Consortium. <i>The Unicode Standard, Version 16.0 – Core Specification</i>, ch. 11 “Cuneiform and Hieroglyphs”, §11.4 Egyptian Hieroglyphs.', 'https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-11/'),
  ('Unicode Character Database 18.0.0: UnicodeData.txt and DerivedAge.txt (names and versions of U+13430–U+13455).', 'https://www.unicode.org/Public/UCD/latest/ucd/'),
  ('Unicode 15.0.0 announcement (“Twenty-nine additional Egyptian hieroglyph format controls”).', 'https://www.unicode.org/versions/Unicode15.0.0/'),
  ('Glass, A., I. Hafemann, M.-J. Nederhof, S. Polis, B. Richmond, S. Rosmorduc, S. Schweitzer. “A method for encoding Egyptian quadrats in Unicode.” L2/17-112R, 2017.', 'https://www.unicode.org/L2/L2017/17112r-quadrat-encoding.pdf'),
  ('Glass, A., J. Grotenhuis, M.-J. Nederhof, S. Polis, S. Rosmorduc, D. A. Werning. “Additional control characters for Ancient Egyptian hieroglyphic texts.” L2/21-248, 22 Dec 2021.', 'https://www.unicode.org/L2/L2021/21248-egyptian-controls.pdf'),
  ('Nederhof, M.-J. “Notes on the control characters for Ancient Egyptian in Unicode 15.” L2/24-079, 17 Feb 2024.', 'https://www.unicode.org/L2/L2024/24079-egyptian-fmt-controls.pdf'),
  ('Unicode Technical Committee. Egyptian Hieroglyphs document list.', 'https://www.unicode.org/L2/topical/egyptian/'),
 ]),
 (bi('符号化の記法と道具', 'Notations and tools'), [
  ('Buurman, J., N. Grimal, M. Hainsworth, J. Hallof, D. van der Plas. <i>Manuel de codage des textes hiéroglyphiques en vue de leur saisie sur ordinateur</i>. Informatique et Égyptologie 2. Paris, 1988.', 'https://en.wikipedia.org/wiki/Manuel_de_Codage'),
  ('Rosmorduc, S. JSesh documentation: “A description of the manuel de codage” and “About JSesh 6 sign placement”. JSesh source: CeCILL-C.', 'https://github.com/rosmord/jsesh'),
  ('Nederhof, M.-J. HieroJax: “Syntax of Unicode encoding of Ancient Egyptian”. GPL-3.0.', 'https://nederhof.github.io/hierojax/syntax.html'),
  ('Noto Sans Egyptian Hieroglyphs v2.002 (2024). SIL Open Font License 1.1.', 'https://github.com/notofonts/egyptian-hieroglyphs'),
 ]),
 (bi('記号表', 'Sign list'), [
  ('Gardiner, A. H. <i>Egyptian Grammar: Being an Introduction to the Study of Hieroglyphs</i>. 3rd ed. Oxford: Griffith Institute, 1957. (Sign list; source of the Unicode “Gardiner set”, per the Unicode Standard §11.4.1.)', ''),
 ]),
 (bi('パイロットの資料', 'Pilot text'), [
  ('British Museum, EA 581, stela of Intef son of Senet (collection record).', 'https://www.britishmuseum.org/collection/object/Y_EA581'),
  ('Nederhof, M.-J. “British Museum EA581”, Unicode encoding on HieroJax (GPL-3.0 repository). Fetched 21 Nov 2026.', 'https://nederhof.github.io/hierojax/texts/BritishMuseumEA581.html'),
  ('Nederhof, M.-J. St Andrews corpus, “Intef son of Senet, Stela of” (RES; created 2016-08-04, modified 2017-01-19), distributed with PhilologEg 0.5.14. Licence not stated; used here only for line direction.', 'https://sites.cs.st-andrews.ac.uk/people/mn31/egyptian/texts/corpus/pdf/IntefSonSenet.pdf'),
  ('Sethe, K. <i>Aegyptische Lesestücke</i>. Leipzig: Hinrichs, 1928, pp. 80–81 (as cited by the encoder).', ''),
 ]),
 (bi('筆の運び（ヒエラティック）', 'Stroke sequence (hieratic)'), [
  ('Regulski, I. “Writing habits as identity marker: on sign formation in Papyrus Gardiner II.” In <i>Ägyptologische „Binsen“-Weisheiten III</i>. Stuttgart: Franz Steiner, 2018. doi:10.25358/openscience-395.', 'https://doi.org/10.25358/openscience-395'),
  ('AKU-PAL: Paläographie des Hieratischen und der Kursivhieroglyphen, Mainz. Version 1.3 (27 Feb 2024) adds “display of stroke sequence as vector graphics”.', 'https://en.aku.uni-mainz.de/2024/02/27/aku-pal-version-1-3-released/'),
 ]),
 (bi('コーパスとライセンス', 'Corpora and licences'), [
  ('Thesaurus Linguae Aegyptiae, Original Earlier Egyptian sentences, corpus v18, premium (Hugging Face; CC BY-SA 4.0). Hieroglyphs in Unicode, but without format controls: 0 of 12,773 sentences contain U+13430–U+1345F (checked 21 Nov 2026).', 'https://huggingface.co/datasets/thesaurus-linguae-aegyptiae/tla-Earlier_Egyptian_original-v18-premium'),
  ('Thesaurus Linguae Aegyptiae raw data publications (usually CC BY-SA 4.0).', 'https://aaew.bbaw.de/daten-veroeffentlichungen'),
  ('Schweitzer, S. D. AES – Ancient Egyptian Sentences (CC BY-SA 4.0; word forms with optional MdC and Unicode hieroglyphic encodings).', 'https://github.com/simondschweitzer/aes'),
  ('JSesh text sources in the Manuel de Codage (list maintained by S. Rosmorduc).', 'https://jsesh.qenherkhopeshef.org/varia/externaltextsources'),
  ('Ramses Online, Late Egyptian corpus (Université de Liège). Free to read online; no download, stated licence or documented API; intensive use by agreement with the team. Polis, S. “Layers of openness in the Ramses corpus of Late Egyptian”, slides, Open Access in Egyptology, 21 Oct 2026.', 'https://orbi.uliege.be/bitstream/2268/349874/1/Polis_2026_OAW_Ramses_OpenAccess.pdf'),
  ('Ramses Online.', 'https://ramses.ulg.ac.be/'),
 ]),
]
src_html = ''
for head, items in SRC:
    src_html += f'<h2>{head}</h2><ul>' + ''.join(f'<li>{t}' + (f' <a href="{u}">{u}</a>' if u else '') + '</li>' for t, u in items) + '</ul>'
sources = f'''
<h1>{bi("出典", "Sources")}</h1>
<p class="lede">{bi(
 "一次資料を先に挙げる。リンクはすべて2026年11月21日に確認した。ページ番号は、確かめたものだけを書いている。",
 "Primary sources come first. All links were checked on 21 November 2026. Page numbers are given only where they were checked.")}</p>
{src_html}
<h2>{bi("このサイトのライセンス", "Licences of this site")}</h2>
<p>{bi(
 "EA 581 の Unicode 符号列（data/ea581-lines.json）は HieroJax（GPL-3.0）から取ったもので、GPL-3.0 の下にある。字形は Noto Sans Egyptian Hieroglyphs（OFL 1.1）。漢字側の数字は「順序の漢字」の項数調査（KanjiVG、CC BY-SA 3.0）による。",
 "The EA 581 Unicode strings (data/ea581-lines.json) come from HieroJax (GPL-3.0) and stay under GPL-3.0. Glyphs are Noto Sans Egyptian Hieroglyphs (OFL 1.1). Kanji numbers come from the Kanji in Order arity census (KanjiVG, CC BY-SA 3.0).")}</p>
'''

PAGES = [('index', 'トップ', 'Top', index), ('concept', '考え方', 'Concept', concept),
         ('operators', '演算子', 'Operators', operators), ('pilot', 'パイロット調査', 'Pilot', pilot),
         ('sources', '出典', 'Sources', sources)]
for slug, tj, te, body in PAGES:
    (ROOT / 'site' / f'{slug}.html').write_text(page(slug, tj, te, body), encoding='utf8')
print('built', [p[0] for p in PAGES])
