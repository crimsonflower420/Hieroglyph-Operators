"""Page 'depth' (where the depth sits). Imported by build_pages.py; numbers from data/depth-compare.json."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
KANJI = 'https://kanji-morphology.pages.dev/'
REPO = 'https://github.com/crimsonflower420/Hieroglyph-Operators'
D = json.load(open(ROOT / 'data/depth-compare.json', encoding='utf8'))
KH = json.load(open(ROOT / 'data/kanji-height-reference.json', encoding='utf8'))

SOURCES = [
 ('KanjiVG, Ulrich Apel et al., snapshot 70a0b7ae (30 Sep 2026), CC BY-SA 3.0. Per-character heights computed by tools/kanji_heights.py with the composition rule and jōyō list of Kanji in Order (crimsonflower420/Kanji-Morphology, tools/valence_atlas.py, tools/positions.py).', 'https://github.com/KanjiVG/kanjivg/tree/70a0b7ae0c18ceb5cb358274b029cce0234a43bc'),
 ('Kanji in Order, arity census (6,176 compositions, deepest group depth 7; reproduced by tools/kanji_heights.py as a check).', KANJI + 'arity-census'),
]

def pc(a, b): return f'{100 * a / b:.0f}%'

def pages(bi):
    R = D['rahman']; A = R['all']; W = R['words']; I = D['intef']; K = D['kanji']
    rows = R['rows']
    ih = I['height']; kh = K['height']
    i_ge2 = sum(v for k, v in ih.items() if int(k) >= 2); k_ge2 = sum(v for k, v in kh.items() if int(k) >= 2)
    k_max = max(int(k) for k in kh); i_max = max(int(k) for k in ih)
    k6 = '、'.join(c for c, v in KH['perChar'].items() if v == k_max)
    k6en = ', '.join(c for c, v in KH['perChar'].items() if v == k_max)
    hq2 = [r['id'] for r in rows if r['hB'] is not None and r['hQ'] >= 2]
    hb_max = max(int(k) for k in A['hB']); hb_top = [r['id'] for r in rows if r['hB'] == hb_max]
    single_q = [r['id'] for r in rows if r['hB'] is not None and r['quadrats'] == 1]
    rev = [r['id'] for r in rows if r['hB'] is not None and r['hBx'] < r['hBin']]
    d03 = next(r for r in rows if r['id'] == 'd03')

    # ------------------------------------------------ distribution table
    H = range(0, k_max + 1)
    def cells(dist, total):
        out = ''
        for h in H:
            n = dist.get(str(h), 0)
            out += f'<td class="num">{n}<br><span class="bar" style="width:{round(60 * n / total)}px"></span></td>' if n else '<td class="num">–</td>'
        return out
    dist_rows = [
        (bi('漢字（常用2,136字）・字の中の配置の木', 'Kanji (2,136 jōyō) · layout tree inside the character'), kh, K['chars'], K['mean']),
        (bi('EA 581（インテフ）・方形の配置の木', 'EA 581 (Intef) · layout tree of a quadrat'), ih, I['groups'], I['mean']),
        (bi(f'ラフマン{A["n"]}件・hQ（方形の中）', f'Rahman, {A["n"]} · hQ (inside a quadrat)'), A['hQ'], A['n'], A['meanHQ']),
        (bi(f'ラフマン{A["n"]}件・hA（層 A 全体）', f'Rahman, {A["n"]} · hA (all of layer A)'), A['hA'], A['n'], A['meanHA']),
        (bi(f'ラフマン{A["n"]}件・hB（層 B）', f'Rahman, {A["n"]} · hB (layer B)'), A['hB'], A['n'], A['meanHB']),
    ]
    dist_html = (f'<div class="table-scroll"><table><tr><th>{bi("木", "Tree")}</th><th class="num">n</th>'
                 + ''.join(f'<th class="num">{h}</th>' for h in H) + f'<th class="num">{bi("平均", "mean")}</th></tr>'
                 + ''.join(f'<tr><td>{lab}</td><td class="num">{n:,}</td>{cells(dist, n)}<td class="num">{m:.2f}</td></tr>' for lab, dist, n, m in dist_rows)
                 + '</table></div>')

    # ------------------------------------------------ per-derivation table
    unit = {'word': bi('語', 'word'), 'multi': bi('名・句', 'name/phrase'), None: '–'}
    def v(x): return '–' if x is None else str(x)
    per = ''
    for r in rows:
        alt = f' <small>(alt {r["hB_alt"]})</small>' if 'hB_alt' in r else ''
        per += (f'<tr><td><a href="rahman#{r["id"]}">{r["id"]}</a></td><td>{unit[r["unit"]]}</td><td class="num">{r["signs"]}</td>'
                f'<td class="num">{r["quadrats"]}</td><td class="num">{r["hQ"]}</td><td class="num">{r["hA"]}</td>'
                f'<td class="num">{"OPEN" if r["hB"] is None else v(r["hB"]) + alt}</td><td class="num">{v(r["hBx"])}</td><td class="num">{v(r["hBin"])}</td></tr>')
    per_html = (f'<div class="table-scroll"><table><tr><th>id</th><th>{bi("単位", "unit")}</th><th class="num">{bi("記号", "signs")}</th>'
                f'<th class="num">{bi("方形", "quadrats")}</th><th class="num">hQ</th><th class="num">hA</th><th class="num">hB</th>'
                f'<th class="num">hBx</th><th class="num">hBin</th></tr>{per}</table></div>')

    body = f'''
<p class="tag">{bi("探索・2026年11月21日", "Exploration · 21 Nov 2026")}</p>
<h1>{bi("深さの在りか", "Where the depth sits")}</h1>
<p class="lede">{bi(
 "同じ語について、配置の木（層 A）と機能の木（層 B）の高さを測り、漢字の字の中の木の高さと並べる。漢字では深さが字の内側にあり、ヒエログリフでは語の記号のあいだ、方形をまたいだところにある（HYPOTHESIS。第3節）。これは置き場所の違いであって、優劣ではない。",
 "For the same words, the height of the layout tree (layer A) is measured against the height of the function tree (layer B), and set beside the height of the tree inside a kanji. In kanji the depth sits inside the character; in hieroglyphs it sits between the signs of a word, across quadrats (HYPOTHESIS; section 3). This is a difference in where the depth is placed, not a ranking.")}</p>

<h2>{bi("1. 測り方", "1. How it is measured")}</h2>
<p>{bi(
 "<b>高さ</b>は、根から葉までの一本の道の上にある、項数2以上の演算子の節点の最大数である。項数1の節点（層 A の CARTOUCHE、層 B の ABBR、KanjiVG の一枠だけの入れ物）は数えない。三つの資料に同じ規則を当てる。",
 "<b>Height</b> is the largest number of operator nodes of arity 2 or more on one path from the root to a leaf. Arity-1 nodes (CARTOUCHE in layer A, ABBR in layer B, one-slot wrapper groups in KanjiVG) are not counted. The same rule is applied to all three sources.")}</p>
<ul>
<li>{bi("<b>hQ</b>：語の中でいちばん高い方形一つの高さ（方形の中の深さ）。", "<b>hQ</b>: the height of the tallest single quadrat in the word (depth inside a quadrat).")}</li>
<li>{bi("<b>hA</b>：層 A 全体の高さ。記号が二つ以上の方形に分かれるときは、方形を並べる LINE の一段が hQ に加わる。", "<b>hA</b>: the height of all of layer A. When the signs are spread over two or more quadrats, the LINE step that sets the quadrats in a row adds one to hQ.")}</li>
<li>{bi("<b>hB</b>：層 B（記号のはたらき）の高さ。", "<b>hB</b>: the height of layer B (sign function).")}</li>
<li>{bi("<b>hBx / hBin</b>：層 B の一本の道の上で、葉が二つ以上の方形にまたがる節点の最大数（hBx、方形をまたぐ深さ）と、葉が一つの方形に収まる節点の最大数（hBin、方形の中の深さ）。", "<b>hBx / hBin</b>: on one path of layer B, the largest number of nodes whose leaves lie in two or more quadrats (hBx, depth across quadrats), and the largest number whose leaves lie inside one quadrat (hBin, depth inside a quadrat).")}</li>
</ul>
<p>{bi(
 f"資料は三つ。（1）<a href=\"rahman\">ラフマン再読</a>の26件の導出（記法 v1。どの木も HYPOTHESIS）。層 B が OPEN の d25 を除く{A['n']}件を使う。（2）大英博物館 EA 581（インテフの石碑）の方形調査（Nederhof の HieroJax 符号化。<a href=\"pilot\">パイロット調査</a>）。（3）常用漢字2,136字の木（KanjiVG 70a0b7ae、「順序の漢字」の組み立ての規則）。計算は <code>tools/kanji_heights.py</code> と <code>tools/depth_compare.py</code>、結果は <code>data/depth-compare.json</code> にある。漢字側の計算は、項数調査の数（組み立て6,176、入れ子の深さ最大7）を再現できなければ止まる。",
 f"Three sources. (1) The 26 derivations of the <a href=\"rahman\">Rahman re-read</a> (notation v1; every tree HYPOTHESIS); the {A['n']} with a layer B are used, leaving out d25, whose layer B is OPEN. (2) The quadrat census of British Museum EA 581, the stela of Intef (Nederhof's HieroJax encoding; see <a href=\"pilot\">Pilot</a>). (3) The trees of the 2,136 jōyō kanji (KanjiVG 70a0b7ae, with the composition rule of Kanji in Order). The scripts are <code>tools/kanji_heights.py</code> and <code>tools/depth_compare.py</code>; the results are in <code>data/depth-compare.json</code>. The kanji script stops unless it reproduces the arity census totals (6,176 compositions, deepest group depth 7).")}</p>

<h2>{bi("2. 結果：高さの分布", "2. Results: distribution of heights")}</h2>
{dist_html}
<p class="meta">{bi("数は件数（字・方形・導出）。棒は各行の中の割合。", "Counts of characters, quadrats or derivations. Bars show the share within each row.")}</p>

<h3>{bi("ラフマンの導出：同じ語で層 A と層 B を比べる", "Rahman derivations: layer A against layer B for the same words")}</h3>
<p>{bi(
 f"方形の中の高さ hQ は平均{A['meanHQ']:.2f}で、2に届くのは{len(hq2)}件（{', '.join(hq2)}）だけである。層 B の高さ hB は平均{A['meanHB']:.2f}、最大{hb_max}（{', '.join(hb_top)}）。{A['n']}件のうち hB が hQ より高いのが{A['B_gt_Q']}件、等しいのが{A['B_eq_Q']}件で、低いものはない。層 A 全体（hA、平均{A['meanHA']:.2f}）と比べても、hB が高いのが{A['B_gt_A']}件、等しいのが{A['B_eq_A']}件、低いのは{A['B_lt_A']}件である（例はラフマンの本により、頁は各導出に記す。数はこのリポジトリで数えた）。",
 f"Height inside a quadrat, hQ, averages {A['meanHQ']:.2f}; only {len(hq2)} derivation reaches 2 ({', '.join(hq2)}). Layer B height, hB, averages {A['meanHB']:.2f}, with a maximum of {hb_max} ({', '.join(hb_top)}). Of the {A['n']}, hB is greater than hQ in {A['B_gt_Q']}, equal in {A['B_eq_Q']}, and smaller in none. Against all of layer A (hA, mean {A['meanHA']:.2f}), hB is greater in {A['B_gt_A']}, equal in {A['B_eq_A']} and smaller in {A['B_lt_A']} (examples from Rahman's book, page per derivation; counts computed in this repository).")}</p>
<p>{bi(
 f"層 B の深さがどこにあるかを見ると、方形をまたぐ段数 hBx は平均{A['meanHBx']:.2f}、方形の中の段数 hBin は平均{A['meanHBin']:.2f}である。{A['n']}件のうち{A['Bx_gt_in']}件で hBx が hBin を上回り、{A['Bx_eq_in']}件で等しく、{A['Bx_lt_in']}件（{', '.join(rev)}）で逆になる。逆の{A['Bx_lt_in']}件は、どれも記号がただ一つの方形に収まる例である（一方形の例は{len(single_q)}件：{', '.join(single_q)}）。",
 f"As to where layer B's depth sits: the number of steps across quadrats, hBx, averages {A['meanHBx']:.2f}, and the number inside a quadrat, hBin, averages {A['meanHBin']:.2f}. In {A['Bx_gt_in']} of the {A['n']} hBx exceeds hBin, in {A['Bx_eq_in']} they are equal, and in {A['Bx_lt_in']} ({', '.join(rev)}) it is the other way round. Those {A['Bx_lt_in']} are all cases whose signs fit in a single quadrat (the single-quadrat cases are {len(single_q)}: {', '.join(single_q)}).")}</p>
<p>{bi(
 f"名や句（GEN・NAME・PHRASE・COORD・ATTR を含むもの：{', '.join(R['multi'])}）を除いた語だけの{W['n']}件でも形は同じである。hQ 平均{W['meanHQ']:.2f}、hB 平均{W['meanHB']:.2f}、hB が hQ より高いのは{W['n']}件中{W['B_gt_Q']}件。d03 は層 B の別案（限定符として閉じる木）をとると hB が{d03['hB']}から{d03['hB_alt']}になるが、どちらも方形をまたぐ段である。",
 f"Keeping only the {W['n']} single words (leaving out names and phrases, i.e. trees with GEN, NAME, PHRASE, COORD or ATTR: {', '.join(R['multi'])}) gives the same shape: hQ mean {W['meanHQ']:.2f}, hB mean {W['meanHB']:.2f}, hB above hQ in {W['B_gt_Q']} of {W['n']}. For d03, the alternative layer B (closing with a determinative) raises hB from {d03['hB']} to {d03['hB_alt']}; both steps are across quadrats.")}</p>
{per_html}

<h3>{bi("インテフの石碑（EA 581）：配置だけ", "Intef stela (EA 581): layout only")}</h3>
<p>{bi(
 f"石碑全体の{I['groups']}グループ（一記号だけのもの{ih['0']}を含む）で、方形の高さは平均{I['mean']:.2f}、最大{i_max}。2以上は{i_ge2}（{pc(i_ge2, I['groups'])}）である（Nederhof の符号化、このサイトの調査）。この石碑については、語の区切りも記号のはたらきの注記もまだリポジトリにないので、層 B の高さは <b>OPEN</b> である。",
 f"Over the stela's {I['groups']} groups (including {ih['0']} lone signs), quadrat height averages {I['mean']:.2f}, with a maximum of {i_max}; {i_ge2} ({pc(i_ge2, I['groups'])}) reach 2 or more (Nederhof's encoding; this site's census). For this stela the repository has no word segmentation and no sign-function annotation yet, so its layer-B height is <b>OPEN</b>.")}</p>

<h3>{bi("漢字：字の中の木", "Kanji: the tree inside the character")}</h3>
<p>{bi(
 f"常用2,136字の字の中の木は平均{K['mean']:.2f}で、2以上が{k_ge2:,}字（{pc(k_ge2, K['chars'])}）、最大{k_max}（{k6}）である（KanjiVG 70a0b7ae、「順序の漢字」の規則）。高さ0、つまり組み立てのない字は{kh['0']}字。漢字側の数は配置（部品の組み立て）の木だけで、意符・音符の機能の木はこの比較にはない（<b>OPEN</b>）。したがって漢字の数と並べるべきなのは hQ と hA であり、hB ではない。",
 f"The tree inside a jōyō kanji averages {K['mean']:.2f}; {k_ge2:,} characters ({pc(k_ge2, K['chars'])}) reach 2 or more, and the maximum is {k_max} ({k6en}) (KanjiVG 70a0b7ae, Kanji in Order's rule). {kh['0']} characters have height 0, that is, no composition. The kanji number is a layout tree (how components are put together) only; there is no semantic/phonetic function tree for kanji in this comparison (<b>OPEN</b>). So the kanji number should be set against hQ and hA, not against hB.")}</p>

<h2>{bi("3. 読み", "3. Reading")}</h2>
<div class="flag spec">{bi(
 f"<b>HYPOTHESIS.</b> 漢字の配置の深さは字の内側にある（平均{K['mean']:.2f}）。ヒエログリフの配置の深さは方形の中では浅く（EA 581 で平均{I['mean']:.2f}、ラフマンの例で{A['meanHQ']:.2f}）、同じ語の機能の深さ（平均{A['meanHB']:.2f}）の多くは方形をまたいだところで組まれる（hBx {A['meanHBx']:.2f} 対 hBin {A['meanHBin']:.2f}）。深さは消えたのではなく、置き場所が違う。",
 f"<b>HYPOTHESIS.</b> Kanji layout depth sits inside the character (mean {K['mean']:.2f}). Hieroglyphic layout depth is shallow inside a quadrat (mean {I['mean']:.2f} on EA 581, {A['meanHQ']:.2f} in the Rahman cases), while most of the function depth of the same words (mean {A['meanHB']:.2f}) is built across quadrats (hBx {A['meanHBx']:.2f} against hBin {A['meanHBin']:.2f}). The depth has not gone missing; it sits somewhere else.")}</div>
<p>{bi("限界。", "Limits.")}</p>
<ul>
<li>{bi("ラフマンの例は本が説明のために選んだもので、無作為の標本ではない。件数も25と少ない。", "Rahman's examples were chosen by the book to make teaching points; they are not a random sample, and there are only 25.")}</li>
<li>{bi("層 B の高さは記法 v1 の決め方に左右される（たとえば CMPL は多子音記号と補音を一つの節点で閉じ、INFL や PL は一段ずつ積む）。別の記法なら数は変わりうる。", "Layer-B height depends on choices in notation v1 (for example, CMPL closes a multiliteral and its complements in one node, while INFL and PL stack one step at a time). Another notation could give other numbers.")}</li>
<li>{bi("漢字の高さは KanjiVG の入れ子の付け方に左右される。単位も違う。漢字の木は一字の中の部品の組み立てで、方形の木は語をまたぎうる配置の単位である。", "Kanji heights depend on how KanjiVG nests its groups. The units also differ: a kanji tree is the composition of components inside one character, while a quadrat tree is a layout unit that may cut across words.")}</li>
<li>{bi("高さは木の形の数であり、読みやすさや書く人の頭の中の手順については何も言わない。", "Height is a number about tree shape; it says nothing about legibility or about any procedure in the writer's mind.")}</li>
</ul>
<div class="flag spec">{bi(
 "<strong>並行関係（Grant の承認待ち）。</strong>漢字では配置の深さが集まる単位が「字」であり、ここで測ったヒエログリフの例では機能の深さが集まる単位が「語」（いくつかの方形の列）である、と書ける。どちらも文字の層についての記述であり、統語の主張ではない。",
 "<strong>Parallel (for Grant to approve).</strong> One could write it this way: in kanji the unit that collects layout depth is the character, while in the hieroglyphic cases measured here the unit that collects function depth is the word (a row of several quadrats). Both describe the writing layer; neither is a syntactic claim.")}</div>

<h2>{bi("未決の問い", "Open questions")}</h2>
<ul>
<li>{bi("OPEN：EA 581 の語ごとの層 B。語の区切りのある公開の転写（TLA など）と方形の符号化を突き合わせる必要がある。", "OPEN: layer B word by word for EA 581. It needs a published transcription with word division (such as the TLA) aligned with the quadrat encoding.")}</li>
<li>{bi("OPEN：漢字の機能の木（意符・音符）の高さ。KanjiVG の部首や音符の属性から木を作れるかは未確認。", "OPEN: the height of a kanji function tree (semantic and phonetic components). Whether one can be built from KanjiVG's radical and phonetic attributes is not yet checked.")}</li>
</ul>
'''
    return body
