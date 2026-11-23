"""Page 'second-text' (does the share of horizontal joins rise in columns in other texts?).
Imported by build_pages.py; numbers from data/second-text.json (tools/second_text.py)."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
D = json.load(open(ROOT / 'data/second-text.json', encoding='utf8'))
T = {t['key']: t for t in D['texts']}
COMMIT = 'da318801'

SOURCES = [
 ('Nederhof, M.-J. HieroJax, “British Museum EA614” (Stela of Tjetji), Unicode encoding with section headings “rows” and “columns”, repository commit da318801 (GPL-3.0).', 'https://nederhof.github.io/hierojax/texts/BritishMuseumEA614.html'),
 ('Nederhof, M.-J. HieroJax, “British Museum EA567” (Stela of Amenemhat), section headings “rows” and “columns”, commit da318801.', 'https://nederhof.github.io/hierojax/texts/BritishMuseumEA567.html'),
 ('Nederhof, M.-J. HieroJax, “British Museum EA101” (Stela of Nebipusenusret), central register “(rightmost columns)”, commit da318801.', 'https://nederhof.github.io/hierojax/texts/BritishMuseumEA101.html'),
 ('Nederhof, M.-J. HieroJax, “Syntax of Unicode encoding of Ancient Egyptian” (grammar, including the enclosure production).', 'https://nederhof.github.io/hierojax/syntax.html'),
 ('British Museum, collection record EA614 (stela of Tjetji): “a fourteen-line autobiographical inscription reading from right to left … an elaborate offering prayer written in five vertical rows”. Read 23 Nov 2026.', 'https://www.britishmuseum.org/collection/object/Y_EA614'),
 ('British Museum, collection record EA162 (Imeny): “five rows of recessed Hieroglyphic text above two sunk relief figured scenes”. Read 23 Nov 2026.', 'https://www.britishmuseum.org/collection/object/Y_EA162'),
 ('British Museum, collection record EA567 (Amenemhat): round-topped limestone stela; the record does not describe the layout of the text. Read 23 Nov 2026.', 'https://www.britishmuseum.org/collection/object/Y_EA567'),
 ('British Museum, collection record EA101 (Nebipusenusret): “columns and rows of Hieroglyphic text”; lower register “an address in seven lines” (Strudwick 2006). Read 23 Nov 2026.', 'https://www.britishmuseum.org/collection/object/Y_EA101'),
]

def pc(a, b): return f'{100 * a / b:.0f}%' if b else '—'

def fp(p):
    if p < 0.0001: return '&lt; 0.0001'
    if p < 0.001: return f'{p:.4f}'
    return f'{p:.3f}'

def pages(bi):
    A, E614, E567, E162, E101, E562 = T['ea581'], T['ea614'], T['ea567'], T['ea162'], T['ea101'], T['ea562']
    P = D['pooledSecondTexts']; S = P['stratifiedPermutation']

    def row(t, ja, en):
        R, C = t['rows'], t['cols']
        x = t.get('exactPermutation')
        perm = f'{x["atLeastAsExtreme"]:,} / {x["permutations"]:,} = {fp(x["p"])}' if x else (bi('—（列だけ）', '— (columns only)') if C['lines'] else bi('—（行だけ）', '— (rows only)'))
        fish = fp(t['fisherNodes']) if 'fisherNodes' in t else '—'
        rr = (f'{R["hor"]} / {R["nodes"]} ({pc(R["hor"], R["nodes"])})' if R['lines'] else '—')
        return (f'<tr><td>{bi(ja, en)}</td><td class="num">{R["lines"]}</td><td class="num">{rr}</td>'
                f'<td class="num">{C["lines"]}</td><td class="num">{(str(C["hor"]) + " / " + str(C["nodes"]) + " (" + pc(C["hor"], C["nodes"]) + ")") if C["lines"] else "—"}</td>'
                f'<td class="num">{perm}</td><td class="num">{fish}</td></tr>')
    table = (f'<div class="table-scroll"><table><tr><th>{bi("テキスト", "Text")}</th><th class="num">{bi("行（横）", "rows")}</th>'
             f'<th class="num">{bi("横の結合／節点（行）", "hor / nodes (rows)")}</th><th class="num">{bi("列（縦）", "columns")}</th>'
             f'<th class="num">{bi("横の結合／節点（列）", "hor / nodes (columns)")}</th>'
             f'<th class="num">{bi("行ラベルの並べ替え検定（片側）", "line-label permutation (one-sided)")}</th>'
             f'<th class="num">{bi("フィッシャー（節点、参考）", "Fisher (nodes, reference)")}</th></tr>'
             + row(A, 'EA 581（インテフ）・比較の基準', 'EA 581 (Intef) · the reference')
             + row(E614, 'EA 614（チェチ）', 'EA 614 (Tjetji)')
             + row(E567, 'EA 567（アメンエムハト）', 'EA 567 (Amenemhat)')
             + row(E162, 'EA 162（イメニ）', 'EA 162 (Imeny)')
             + row(E101, 'EA 101（ネブイプセンウセレト）', 'EA 101 (Nebipusenusret)')
             + row(E562, 'EA 562（インテフ）', 'EA 562 (Intef)')
             + f'<tr><td>{bi("二つ目のテキスト3点の合計（EA 614・567・162）", "Second texts pooled (EA 614, 567, 162)")}</td>'
               f'<td class="num">{P["rows"]["lines"]}</td><td class="num">{P["rows"]["hor"]} / {P["rows"]["nodes"]} ({pc(P["rows"]["hor"], P["rows"]["nodes"])})</td>'
               f'<td class="num">{P["cols"]["lines"]}</td><td class="num">{P["cols"]["hor"]} / {P["cols"]["nodes"]} ({pc(P["cols"]["hor"], P["cols"]["nodes"])})</td>'
               f'<td class="num">{bi(f"テキスト内で並べ替え {S["iterations"]:,}回：{S["atLeastAsExtreme"]}回", f"within-text, {S["iterations"]:,} draws: {S["atLeastAsExtreme"]}")}</td><td class="num">—</td></tr>'
             + '</table></div>')

    def orient_rows():
        out = ''
        for t in (E614, E567, E162, E101, E562):
            src = next(x for x in json.load(open(ROOT / 'data/second-text-lines.json', encoding='utf8'))['texts'] if x['key'] == t['key'])
            for ev in src['evidence']:
                n = sum(1 for l in t['lines'] if l['section'] == ev['section'] and l['orientation'] == ev['orientation'])
                part = ev['section'] + (f' ({ev["note"]})' if ev['note'] else '')
                o = bi('行（横）', 'row') if ev['orientation'] == 'row' else bi('列（縦）', 'column')
                out += f'<tr><td>{t["key"].upper().replace("EA", "EA ")}</td><td>{part}</td><td class="num">{n}</td><td>{o}</td><td>{ev["evidence"]}</td></tr>'
            if t['excludedLines']:
                out += (f'<tr><td>{t["key"].upper().replace("EA", "EA ")}</td><td>{bi("その他（場面や人物に添えた文字、向きの書かれていない段）", "other (captions beside scenes and figures, registers whose orientation is not stated)")}</td>'
                        f'<td class="num">{len(t["excludedLines"])}</td><td>{bi("除外", "excluded")}</td><td>{bi("向きの記述が資料にない。推測しない。", "No stated orientation in the sources; not guessed.")}</td></tr>')
        return (f'<div class="table-scroll"><table><tr><th>{bi("テキスト", "Text")}</th><th>{bi("部分（HieroJax の見出し）", "part (HieroJax heading)")}</th>'
                f'<th class="num">{bi("行数", "lines")}</th><th>{bi("向き", "orientation")}</th><th>{bi("根拠", "evidence")}</th></tr>{out}</table></div>')

    def line_table(t):
        rows = ''.join(f'<tr><td class="num">{l["n"]}</td><td>{l["section"] or ""}</td><td>{bi("行", "row") if l["orientation"] == "row" else bi("列", "col")}</td>'
                       f'<td class="num">{l["hor"]} / {l["nodes"]}</td><td class="num">{pc(l["hor"], l["nodes"])}</td></tr>' for l in t['lines'])
        return (f'<div class="table-scroll"><table><tr><th>{bi("通し番号", "no.")}</th><th>{bi("部分", "part")}</th><th>{bi("向き", "orient.")}</th>'
                f'<th class="num">{bi("横／節点", "hor / nodes")}</th><th class="num">{bi("割合", "share")}</th></tr>{rows}</table></div>')

    def ratio(t, k): return pc(t[k]['hor'], t[k]['nodes'])
    rmax614 = max(l['hor'] / l['nodes'] for l in E614['lines'] if l['orientation'] == 'row')
    cmin614 = min(l['hor'] / l['nodes'] for l in E614['lines'] if l['orientation'] == 'col')
    enc_n = sum(T[k]['enclosures'] for k in ('ea614', 'ea567', 'ea101', 'ea562'))
    enc_nodes = sum(T[k]['nodesInsideEnclosures'] for k in ('ea614', 'ea567', 'ea101', 'ea562'))
    _h = sum(l['hor'] + l['opsInsideEnclosure'].get('hor', 0) for l in E101['lines']); _n = sum(l['nodes'] + sum(l['opsInsideEnclosure'].values()) for l in E101['lines'])
    e101 = pc(_h, _n)
    excl = sum(len(T[k]['excludedLines']) for k in ('ea614', 'ea567', 'ea162', 'ea101', 'ea562'))

    body = f'''
<p class="tag">{bi("探索・2026年11月23日", "Exploration · 23 Nov 2026")}</p>
<h1>{bi("二つ目のテキスト：列では横の結合が増えるか", "Second texts: do horizontal joins rise in columns?")}</h1>
<p class="lede">{bi(
 f"EA 581 では、演算子の節点のうち横の結合が、横書きの行で{ratio(A, 'rows')}、縦書きの列で{ratio(A, 'cols')}であった。同じ数え方を、行と列の両方をもつ別の石碑3点に当てた。EA 614（チェチ）では行{ratio(E614, 'rows')}・列{ratio(E614, 'cols')}、EA 162（イメニ）では行{ratio(E162, 'rows')}・列{ratio(E162, 'cols')}で、同じ向きの差がある。EA 567（アメンエムハト）では行{ratio(E567, 'rows')}・列{ratio(E567, 'cols')}で、向きは同じだが差は小さく、偶然と区別できない。行だけ・列だけの石碑2点（EA 562・EA 101）も、それぞれ行と列の値の範囲に入る。数は六つの石碑での観察であり、規則ではない。",
 f"On EA 581, horizontal joins were {ratio(A, 'rows')} of operator nodes in horizontal rows and {ratio(A, 'cols')} in vertical columns. The same count was run on three other stelae that have both rows and columns. EA 614 (Tjetji): rows {ratio(E614, 'rows')}, columns {ratio(E614, 'cols')}; EA 162 (Imeny): rows {ratio(E162, 'rows')}, columns {ratio(E162, 'cols')} — the same direction. EA 567 (Amenemhat): rows {ratio(E567, 'rows')}, columns {ratio(E567, 'cols')} — the same direction, but the difference is small and cannot be told apart from chance. Two stelae with only one orientation (EA 562 rows, EA 101 columns) fall inside the row and column ranges respectively. These are observations on six stelae, not a rule.")}</p>

<h2>{bi("1. 資料と行の向き", "1. Sources and line orientation")}</h2>
<p>{bi(
 f"符号列はすべて M.-J. Nederhof の HieroJax（GPL-3.0、リポジトリのコミット {COMMIT}）による。ほかの HieroJax の石碑のうち、EA 574 は使っていない。ページに行と列の見出しがなく、大英博物館の記録も行の向きを書いていないからである。行の向きは推測しない。HieroJax のページ自体が「rows」「columns」と見出しを付けているか、「右端の三列」のような注を付けている部分、または大英博物館の収蔵記録が行数と向きを書き、その数が符号化の行数と合う部分だけを使う。それ以外の{excl}行（場面や人物に添えた文字、向きの書かれていない段）は除外した。EA 581 の向きは、<a href=\"pilot\">パイロット調査</a>と同じく同じ編者の RES 符号化（St Andrews コーパス）による。",
 f"All encodings are M.-J. Nederhof's HieroJax (GPL-3.0, repository commit {COMMIT}). Of the other HieroJax stelae, EA 574 is not used: its page does not label rows or columns, and the BM record does not state the orientation. Line orientation is never guessed. A part is used only if the HieroJax page itself heads it “rows” or “columns” or notes something like “the rightmost three columns”, or if the British Museum collection record states the number and orientation of its lines and that number matches the encoded lines. The other {excl} lines (captions beside scenes and figures, registers whose orientation is not stated) are excluded. EA 581's orientation comes, as in the <a href=\"pilot\">pilot</a>, from the same editor's RES encoding (St Andrews corpus).")}</p>
{orient_rows()}
<p class="meta">{bi("EA 101 は向きの確かな部分が中段の列だけなので、片側だけの参考値として扱う（下段7行は大英博物館の記録で「seven lines」とあるが、横か縦かは書かれていないため除外）。EA 562 は行（15行）しかないので、これも片側の参考値である。", "EA 101 has checked orientation only for the columns of the central register, so it is a one-sided data point only (the BM record calls the lower register “seven lines” without saying whether they are rows or columns, so it is excluded). EA 562 has rows only (15 lines), so it too is a one-sided data point.")}</p>

<h2>{bi("2. 数え方", "2. How the count is made")}</h2>
<ul>
<li>{bi("節点の定義は<a href=\"pilot\">パイロット調査</a>と同じ（<code>tools/quadrat_census.py</code> の構文解析を使う）。縦の結合・横の結合・差し込み・重ね合わせの適用一つが節点一つで、項数は2以上。", "Nodes are defined as in the <a href=\"pilot\">pilot</a> (the parser of <code>tools/quadrat_census.py</code> is reused): one application of a vertical joiner, horizontal joiner, insertion or overlay is one node, with arity 2 or more.")}</li>
<li>{bi(f"王名の囲み（カルトゥーシュ、U+1343C／D）は、HieroJax の文法の enclosure の規則どおりに解析できるようにした。囲みそのものは節点に数えない。囲みの中の節点（{enc_n}個の囲みに{enc_nodes}個）は別に数え、主な比較から外した。行と列をもつ三つの石碑では、入れても割合の動きは1ポイント未満である（data/second-text.json の withEnclosureNodes）。EA 101 の列は入れると{e101}になる（外すと{ratio(E101, 'cols')}）。解析に失敗した行は0行である。", f"Royal-name enclosures (cartouches, U+1343C/D) are now parsed by the enclosure production of the HieroJax grammar. The enclosure itself is not counted as a node. Nodes inside enclosures ({enc_nodes} inside {enc_n} enclosures) are counted separately and left out of the main comparison; for the three stelae with rows and columns, including them moves no share by a full point (withEnclosureNodes in data/second-text.json); EA 101's columns go to {e101} with them (from {ratio(E101, 'cols')}). No line failed to parse.")}</li>
<li>{bi("検定は片側で、「列の方が横の結合の割合が高い」を見る。同じ行の節点は互いに独立ではないので、単位は行である。列の行数を固定して、どの行が列かのあらゆる選び方を数え上げ、列と行の割合の差が観察値以上になる割合を p とする（正確な並べ替え検定）。節点を独立とみなすフィッシャーの正確検定は参考として並べる。", "The tests are one-sided: are horizontal joins a larger share in columns? Nodes in one line are not independent, so the unit is the line. With the number of column lines fixed, every way of choosing which lines are columns is enumerated, and p is the fraction whose column-minus-row difference is at least the observed one (exact permutation test). Fisher's exact test, which treats nodes as independent, is shown for reference only.")}</li>
</ul>
<p>{bi("計算は <code>tools/second_text.py</code>、符号列と向きの根拠は <code>data/second-text-lines.json</code>（GPL-3.0 のまま）、結果は <code>data/second-text.json</code> にある。", "The script is <code>tools/second_text.py</code>; the strings and orientation evidence are in <code>data/second-text-lines.json</code> (still GPL-3.0); the results are in <code>data/second-text.json</code>.")}</p>

<h2>{bi("3. 結果", "3. Results")}</h2>
{table}
<ul>
<li>{bi(f"<b>EA 614</b>：差はいちばんはっきりしている。列5行はどれも、行14行のどれよりも横の結合の割合が高い（列の最小{100 * cmin614:.0f}%、行の最大{100 * rmax614:.0f}%）。そのため並べ替え検定では観察値がもっとも極端な選び方（{E614['exactPermutation']['permutations']:,}通りのうち1通り）になる。", f"<b>EA 614</b>: the clearest case. Each of the 5 columns has a higher share of horizontal joins than any of the 14 rows (column minimum {100 * cmin614:.0f}%, row maximum {100 * rmax614:.0f}%), so the observed split is the single most extreme of the {E614['exactPermutation']['permutations']:,} possible ones.")}</li>
<li>{bi(f"<b>EA 162</b>：同じ向き。ただし行5・列3しかなく、選び方は{E162['exactPermutation']['permutations']}通りなので、p は最小でも1/56（≈ 0.018）である。観察値はその最小に当たる。", f"<b>EA 162</b>: the same direction. With only 5 rows and 3 columns there are {E162['exactPermutation']['permutations']} splits, so the smallest possible p is 1/56 (≈ 0.018); the observed split reaches it.")}</li>
<li>{bi(f"<b>EA 567</b>：向きは同じだが、列は4行・節点{E567['cols']['nodes']}個しかなく（最後の列は節点2個）、差（{100 * E567['exactPermutation']['observedDiff']:.0f}ポイント）は偶然と区別できない（p = {fp(E567['exactPermutation']['p'])}）。この石碑では、型は「成り立たない」とも「成り立つ」とも言えない。", f"<b>EA 567</b>: the same direction, but the columns are only 4 lines with {E567['cols']['nodes']} nodes (the last column has 2), and the difference ({100 * E567['exactPermutation']['observedDiff']:.0f} points) cannot be told from chance (p = {fp(E567['exactPermutation']['p'])}). On this stela the pattern can be called neither confirmed nor refuted.")}</li>
<li>{bi(f"<b>EA 101</b>（列だけ）：列9行で横の結合は{ratio(E101, 'cols')}。ほかの石碑の列の値（{ratio(E567, 'cols')}〜{ratio(E614, 'cols')}）の範囲にあり、どの石碑の行の値よりも高い。比べる行がないので、片側の参考値にとどまる。", f"<b>EA 101</b> (columns only): horizontal joins are {ratio(E101, 'cols')} over 9 columns, inside the range of the other stelae's columns ({ratio(E567, 'cols')}–{ratio(E614, 'cols')}) and above every stela's rows. With no rows to compare, it is a one-sided data point only.")}</li>
<li>{bi(f"<b>EA 562</b>（行だけ）：行15行で横の結合は{ratio(E562, 'rows')}（{E562['rows']['hor']}/{E562['rows']['nodes']}）。ほかの石碑の行の値（{ratio(E162, 'rows')}〜{ratio(E614, 'rows')}）の範囲にあり、どの石碑の列の値よりも低い。これも片側の参考値である。", f"<b>EA 562</b> (rows only): horizontal joins are {ratio(E562, 'rows')} ({E562['rows']['hor']}/{E562['rows']['nodes']}) over 15 rows, inside the range of the other stelae's rows ({ratio(E162, 'rows')}–{ratio(E614, 'rows')}) and below every stela's columns. This too is a one-sided data point.")}</li>
<li>{bi(f"三つの石碑をまとめると、行{P['rows']['hor']}/{P['rows']['nodes']}（{pc(P['rows']['hor'], P['rows']['nodes'])}）、列{P['cols']['hor']}/{P['cols']['nodes']}（{pc(P['cols']['hor'], P['cols']['nodes'])}）。石碑ごとに行と列のラベルを並べ替え（{S['iterations']:,}回、乱数の種 {S['seed']}）、三つの差の和が観察値以上になったのは{S['atLeastAsExtreme']}回であった（p &lt; 0.0001）。この合計は EA 614 の重みが大きい。", f"Pooling the three stelae: rows {P['rows']['hor']}/{P['rows']['nodes']} ({pc(P['rows']['hor'], P['rows']['nodes'])}), columns {P['cols']['hor']}/{P['cols']['nodes']} ({pc(P['cols']['hor'], P['cols']['nodes'])}). Permuting row/column labels within each stela ({S['iterations']:,} draws, seed {S['seed']}), the sum of the three differences reached the observed value {S['atLeastAsExtreme']} times (p &lt; 0.0001). EA 614 carries most of the weight in this total.")}</li>
</ul>
<div class="flag spec">{bi(
 f"<b>HYPOTHESIS.</b> 縦の列では横の結合の割合が上がる、という EA 581 の観察は、行と列をもつ三つの石碑のうち二つ（EA 614・EA 162）で同じ向きにくり返され、残る一つ（EA 567）では同じ向きだが小さすぎて判断できない。片側の参考値（EA 562 の行、EA 101 の列）もこれと矛盾しない。列は幅が狭いので、記号を横に並べて方形を作る、という説明と合う（推論）。ただし、下の注のとおり、向きは文の内容や書き手の符号化の癖と分けられていない。",
 f"<b>HYPOTHESIS.</b> The EA 581 observation that horizontal joins make up a larger share in vertical columns repeats in the same direction on two of the three stelae with both rows and columns (EA 614, EA 162); on the third (EA 567) it points the same way but is too small to judge. The one-sided data points (EA 562 rows, EA 101 columns) do not contradict it. It fits the explanation that a column is narrow, so signs are set side by side to fill a quadrat (inference). As the notes below say, orientation has not been separated from text content or from the encoder's habits.")}</div>

<h2>{bi("4. 行ごとの数", "4. Counts line by line")}</h2>
<details><summary>{bi("EA 614", "EA 614")}</summary>{line_table(E614)}</details>
<details><summary>{bi("EA 567", "EA 567")}</summary>{line_table(E567)}</details>
<details><summary>{bi("EA 162", "EA 162")}</summary>{line_table(E162)}</details>
<details><summary>{bi("EA 101（列だけ）", "EA 101 (columns only)")}</summary>{line_table(E101)}</details>
<details><summary>{bi("EA 562（行だけ）", "EA 562 (rows only)")}</summary>{line_table(E562)}</details>
<details><summary>{bi("EA 581（基準）", "EA 581 (reference)")}</summary>{line_table(A)}</details>

<h2>{bi("5. 注意", "5. Caveats")}</h2>
<ul>
<li>{bi("<b>内容との交絡。</b>どの石碑でも、行と列には文の別々の部分が書かれている（たとえば EA 614 では、大英博物館の記録によれば行が自伝、列が供物の祈りである）。同じ語句を行と列で比べたわけではないので、ここでの差が向きによるのか、語句の違いによるのかは分けられない。", "<b>Confounded with content.</b> On every stela the rows and the columns carry different parts of the text (on EA 614, per the BM record, the rows are the autobiography and the columns the offering prayer). The same phrases were not compared across orientations, so whether the difference comes from orientation or from the wording cannot be separated here.")}</li>
<li>{bi("<b>編者は一人。</b>四つの符号化はすべて Nederhof のもので、方形の中の相対位置は編者の判断である（写しではない）。型が石の上のものか、一人の編者の符号化の癖かは、別の編者の符号化と比べるまで OPEN である。", "<b>One encoder.</b> All four encodings are Nederhof's, and relative positions inside a quadrat are the editor's judgement (not a facsimile). Whether the pattern is on the stone or a habit of one encoder stays OPEN until it is compared with another editor's encoding.")}</li>
<li>{bi("<b>数が少ない。</b>EA 162 と EA 567 の列はそれぞれ3行・4行しかない。p 値は列の行数に強く縛られる。", "<b>Small numbers.</b> The columns of EA 162 and EA 567 are only 3 and 4 lines. The p-values are tightly bounded by the number of column lines.")}</li>
</ul>

<h2>{bi("未決の問い", "Open questions")}</h2>
<ul>
<li>{bi("OPEN：EA 162 の下段5行と場面の文字、EA 101 の上段と下段、EA 614 の人物の脇の文字の向き。資料に記述がないため数えていない。", "OPEN: the orientation of EA 162's lower register and scene texts, EA 101's upper and lower registers, and the captions beside the figures on EA 614. The sources do not state it, so they are not counted.")}</li>
<li>{bi("OPEN：同じ語句（たとえば供物の定型句）を行と列の両方で比べたとき、差が残るかどうか。", "OPEN: whether the difference remains when the same phrase (for example the offering formula) is compared in rows and in columns.")}</li>
</ul>
'''
    glyphs = re.compile('([\U00013000-\U000143FF]+)')
    body = re.sub(r'>([^<]+)<', lambda m: '>' + glyphs.sub(r'<span class="h">\1</span>', m.group(1)) + '<', body)
    return body
