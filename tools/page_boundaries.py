"""Page 'boundaries' (quadrat boundaries against word boundaries). Imported by build_pages.py;
numbers from data/quadrat-word.json (tools/quadrat_word_align.py)."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
REPO = 'https://github.com/crimsonflower420/Hieroglyph-Operators'
D = json.load(open(ROOT / 'data/quadrat-word.json', encoding='utf8'))
T = {t['key']: t for t in D['texts']}

SOURCES = [
 ('Thesaurus Linguae Aegyptiae (TLA), text 5D5ST6HPRRG4FEQKZZEWHNX36E, “Antef, Sohn der Senet (BM EA 581)”, ed. Renata Landgrafová & Peter Dils; and text RGI3F7G3OFDJ5A44XJ7DOFL55U (BM EA 162, Imeny), ed. Alexander Schütze. Berlin-Brandenburgische Akademie der Wissenschaften / Sächsische Akademie der Wissenschaften zu Leipzig. The live TLA page answered with a bot-verification page on 22 Nov 2026, so the word division was taken from the copy below.', 'https://tla.digital/text/5D5ST6HPRRG4FEQKZZEWHNX36E'),
 ('Schweitzer, S. D. AES – Ancient Egyptian Sentences, file files/aes/_aes_sawlit.json at commit 35276d25 (converted from the TLA database excerpt of January 2018, urn:nbn:de:kobv:b4-opus4-29190). CC BY-SA 4.0. Word forms with Unicode or Gardiner hieroglyphic encodings and line numbers.', 'https://github.com/simondschweitzer/aes/tree/35276d2527cca1a055e31ed5f6683e777717170f'),
 ('Schweitzer, S. D. AED-TEI, file 5D5ST6HPRRG4FEQKZZEWHNX36E.xml (TEI header: title, editors, BM EA 581, Sesostris I, CC BY-SA 4.0).', 'https://github.com/simondschweitzer/aed-tei/blob/master/files/5D5ST6HPRRG4FEQKZZEWHNX36E.xml'),
 ('Nederhof, M.-J. HieroJax, “British Museum EA162” (Stela of Imeny), Unicode encoding, repository commit da318801 (GPL-3.0).', 'https://nederhof.github.io/hierojax/texts/BritishMuseumEA162.html'),
]

def pc(a, b): return f'{100 * a / b:.0f}%'

def pages(bi):
    A, B = T['ea581'], T['ea162']

    def qrow(t, unit, lab_ja, lab_en):
        c = t[unit]['quadrats']; n = t['coverage']['quadrats']
        return (f'<tr><td>{bi(lab_ja, lab_en)}</td><td class="num">{n}</td>'
                f'<td class="num">{c.get("inside", 0)} ({pc(c.get("inside", 0), n)})</td>'
                f'<td class="num">{c.get("across", 0)} ({pc(c.get("across", 0), n)})</td>'
                f'<td class="num">{c.get("open", 0)}</td>'
                f'<td class="num">{c.get("insideExact", 0)} / {c.get("acrossExact", 0)}</td></tr>')
    qtable = (f'<div class="table-scroll"><table><tr><th>{bi("テキスト・単位", "Text · unit")}</th><th class="num">{bi("方形", "quadrats")}</th>'
              f'<th class="num">{bi("一語の中", "inside one")}</th><th class="num">{bi("境目をまたぐ", "across")}</th><th class="num">OPEN</th>'
              f'<th class="num">{bi("完全一致のみ（中／またぐ）", "exact-only (inside / across)")}</th></tr>'
              + qrow(A, 'byToken', 'EA 581・TLA の語（要素）', 'EA 581 · TLA token')
              + qrow(A, 'byWord', 'EA 581・語＋接尾代名詞', 'EA 581 · word + suffix pronoun')
              + qrow(B, 'byToken', 'EA 162・TLA の語（要素）', 'EA 162 · TLA token')
              + qrow(B, 'byWord', 'EA 162・語＋接尾代名詞', 'EA 162 · word + suffix pronoun')
              + '</table></div>')

    def urow(t, unit, lab_ja, lab_en):
        u = t[unit]['units']; g = u['groupsTouched']; w = u['written']
        multi = sum(v for k, v in g.items() if int(k) >= 2)
        mx = max(int(k) for k in g)
        return (f'<tr><td>{bi(lab_ja, lab_en)}</td><td class="num">{u["total"]}</td><td class="num">{w}</td>'
                f'<td class="num">{u["dist"].get("oneGroupAlone", 0)}</td><td class="num">{u["dist"].get("oneGroupShared", 0)}</td>'
                f'<td class="num">{multi} ({pc(multi, w)})</td><td class="num">{mx}</td></tr>')
    utable = (f'<div class="table-scroll"><table><tr><th>{bi("テキスト・単位", "Text · unit")}</th><th class="num">{bi("数", "n")}</th>'
              f'<th class="num">{bi("記号あり", "with signs")}</th><th class="num">{bi("一群をひとりで占める", "fills one group alone")}</th>'
              f'<th class="num">{bi("一群を他と分ける", "shares one group")}</th><th class="num">{bi("二群以上にわたる", "spans 2+ groups")}</th>'
              f'<th class="num">{bi("最大群数", "max groups")}</th></tr>'
              + urow(A, 'byToken', 'EA 581・TLA の語', 'EA 581 · TLA token')
              + urow(A, 'byWord', 'EA 581・語＋接尾代名詞', 'EA 581 · word + suffix')
              + urow(B, 'byToken', 'EA 162・TLA の語', 'EA 162 · TLA token')
              + urow(B, 'byWord', 'EA 162・語＋接尾代名詞', 'EA 162 · word + suffix')
              + '</table></div>')

    def cov(t):
        c = t['coverage']
        return (f'<tr><td>{t["key"].upper().replace("EA", "EA ")}</td><td class="num">{c["lines"]}</td><td class="num">{c["linesMappedAndBestMatch"]}</td>'
                f'<td class="num">{c["tlaTokens"]}</td><td class="num">{c["nederhofSigns"]}</td><td class="num">{c["tlaSigns"]}</td>'
                f'<td class="num">{c["exact"]} ({pc(c["exact"], c["nederhofSigns"])})</td><td class="num">{c["wildcard"]}</td>'
                f'<td class="num">{c["substituted"]}</td><td class="num">{c["nederhofOnly"]} / {c["tlaOnly"]}</td></tr>')
    ctable = (f'<div class="table-scroll"><table><tr><th>{bi("テキスト", "Text")}</th><th class="num">{bi("行", "lines")}</th>'
              f'<th class="num">{bi("行の対応を確認", "line map confirmed")}</th><th class="num">{bi("TLA の語", "TLA tokens")}</th>'
              f'<th class="num">{bi("Nederhof の記号", "Nederhof signs")}</th><th class="num">{bi("TLA の記号", "TLA signs")}</th>'
              f'<th class="num">{bi("完全一致", "exact")}</th><th class="num">{bi("ワイルドカード", "wildcard")}</th>'
              f'<th class="num">{bi("置換", "substituted")}</th><th class="num">{bi("片方だけ（N／T）", "one side only (N / T)")}</th></tr>'
              + cov(A) + cov(B) + '</table></div>')

    def across_list(t):
        rows = ''
        for r in t['quadratRows']:
            if r['class'] == 'inside': continue
            tag = 'OPEN' if r['class'] == 'open' else ''
            rows += (f'<tr><td class="num">{r["line"]}.{r["pos"]}</td><td><span class="q" data-q="{r["u"]}" data-size="2.4em"></span></td>'
                     f'<td><i>{" | ".join(r["tokens"])}</i></td><td>{tag}</td></tr>')
        return (f'<div class="table-scroll"><table><tr><th>{bi("行.位置", "line.pos")}</th><th>{bi("方形", "quadrat")}</th>'
                f'<th>{bi("TLA の語（翻字）", "TLA tokens (transliteration)")}</th><th></th></tr>{rows}</table></div>')

    pairs = list(A['acrossPairsByPOS'].items())[:6]
    pos_ja = {'verb': '動詞', 'substantive': '名詞', 'preposition': '前置詞', 'pronoun': '代名詞', 'adjective': '形容詞', 'entity_name': '固有名'}
    def pj(s): return '＋'.join(pos_ja.get(x, x) for x in s.split(' + '))
    pairs_ja = '、'.join(f'{pj(k)} {v}' for k, v in pairs)
    pairs_en = ', '.join(f'{k} {v}' for k, v in pairs)

    a_t, a_w, b_t, b_w = A['byToken']['quadrats'], A['byWord']['quadrats'], B['byToken']['quadrats'], B['byWord']['quadrats']
    nA, nB = A['coverage']['quadrats'], B['coverage']['quadrats']
    dA = A['byToken']['quadratsByDirection']
    hrl_n = sum(dA['hrl'].values()); vrl_n = sum(dA['vrl'].values())
    a_multi = sum(v for k, v in A['byToken']['units']['groupsTouched'].items() if int(k) >= 2)
    b_multi = sum(v for k, v in B['byToken']['units']['groupsTouched'].items() if int(k) >= 2)
    a_wr, b_wr = A['byToken']['units']['written'], B['byToken']['units']['written']

    lo, hi = sorted([pc(b_t['across'], nB), pc(a_t['across'], nA)], key=lambda x: int(x[:-1]))
    lo = lo[:-1]
    body = f'''
<p class="tag">{bi("探索・2026年11月22日", "Exploration · 22 Nov 2026")}</p>
<h1>{bi("方形の境目と語の境目", "Quadrat boundaries and word boundaries")}</h1>
<p class="lede">{bi(
 f"方形は配置の単位であり、語の単位ではない。では、方形が語の境目をまたぐことはどれほどあるか。EA 581（インテフ）の方形{nA}個のうち{a_t['across']}個（{pc(a_t['across'], nA)}）が TLA の二つ以上の語の記号を含み、接尾代名詞を前の語に含めても{a_w['across']}個（{pc(a_w['across'], nA)}）が残る。二つ目のテキスト EA 162（イメニ）では{nB}個のうち{b_t['across']}個（{pc(b_t['across'], nB)}）、接尾代名詞を含めると{b_w['across']}個（{pc(b_w['across'], nB)}）である。数は二つのテキストについての数であり、規則ではない。",
 f"A quadrat is a unit of layout, not a unit of the word. So how often does a quadrat cut across a word boundary? Of the {nA} quadrats of EA 581 (Intef), {a_t['across']} ({pc(a_t['across'], nA)}) hold signs of two or more TLA words; with suffix pronouns counted as part of the word before them, {a_w['across']} ({pc(a_w['across'], nA)}) remain. In a second text, EA 162 (Imeny), it is {b_t['across']} of {nB} ({pc(b_t['across'], nB)}), and {b_w['across']} ({pc(b_w['across'], nB)}) with suffix pronouns attached. These are counts in two texts, not rules.")}</p>

<h2>{bi("1. 資料", "1. Sources")}</h2>
<ul>
<li>{bi("<b>方形</b>：M.-J. Nederhof による Unicode 符号化（HieroJax、GPL-3.0）。EA 581 は<a href=\"pilot\">パイロット調査</a>と同じファイル、EA 162 は HieroJax のリポジトリ（コミット da318801）から取った。方形とは、演算子の節点を一つ以上もつ群のことである（<a href=\"pilot\">パイロット調査</a>と同じ定義）。", "<b>Quadrats</b>: M.-J. Nederhof's Unicode encodings (HieroJax, GPL-3.0). EA 581 is the same file as the <a href=\"pilot\">pilot</a>; EA 162 comes from the HieroJax repository (commit da318801). A quadrat is a group with at least one operator node (the <a href=\"pilot\">pilot</a> definition).")}</li>
<li>{bi("<b>語</b>：Thesaurus Linguae Aegyptiae（TLA）の語の区切り。EA 581 は TLA テキスト 5D5ST6HPRRG4FEQKZZEWHNX36E（編者 R. Landgrafová・P. Dils）、EA 162 は RGI3F7G3OFDJ5A44XJ7DOFL55U（編者 A. Schütze）。TLA のページ（tla.digital）は2026年11月22日にボット確認の画面を返したため、S. D. Schweitzer の AES（TLA データベース2018年1月の抜粋から変換、CC BY-SA 4.0）にある同じテキストを使った。語ごとに行番号と記号（Unicode か Gardiner 番号）がある。", "<b>Words</b>: the word division of the Thesaurus Linguae Aegyptiae (TLA). EA 581 is TLA text 5D5ST6HPRRG4FEQKZZEWHNX36E (eds R. Landgrafová and P. Dils); EA 162 is RGI3F7G3OFDJ5A44XJ7DOFL55U (ed. A. Schütze). The TLA page (tla.digital) returned a bot-verification page on 22 Nov 2026, so the same texts were taken from S. D. Schweitzer's AES (converted from the TLA database excerpt of January 2018, CC BY-SA 4.0). Each word carries its line number and its signs (Unicode or Gardiner numbers).")}</li>
<li>{bi("Hugging Face の TLA「premium」版（v18）は、損傷のない文だけを集めたもので、EA 581 の文は一つも見つからなかった（12,773文を記号列で照合、0件）。そのため使っていない。", "The TLA “premium” set on Hugging Face (v18) keeps only undamaged sentences; no EA 581 sentence was found in it (12,773 sentences matched by sign string, 0 hits), so it is not used.")}</li>
</ul>
<p>{bi("抜き出したデータは <code>data/ea581-tla-words.json</code> と <code>data/ea162-tla-words.json</code>（CC BY-SA 4.0 のまま）、計算は <code>tools/quadrat_word_align.py</code>、結果は <code>data/quadrat-word.json</code> にある。", "The extracts are <code>data/ea581-tla-words.json</code> and <code>data/ea162-tla-words.json</code> (still CC BY-SA 4.0); the computation is <code>tools/quadrat_word_align.py</code>; the results are in <code>data/quadrat-word.json</code>.")}</p>

<h2>{bi("2. 突き合わせの方法", "2. How the two are aligned")}</h2>
<ol>
<li>{bi("TLA の k 番目の行を HieroJax の k 番目の行とみなす。行の数が違えば止まる。各行について、整列の費用がいちばん低い HieroJax の行がその行であることを確かめる（EA 581 は27行中27、EA 162 は18行中18）。", "The k-th TLA line is taken as the k-th HieroJax line; the script stops if the counts differ. For each line it checks that the HieroJax line with the lowest alignment cost is that same line (27 of 27 for EA 581, 18 of 18 for EA 162).")}</li>
<li>{bi("行ごとに、TLA の語の記号の列と Nederhof の方形の記号の列を編集距離で整列する（一致0、ワイルドカード0.5、置換1、欠落1）。Unicode にない記号（TLA・JSesh の拡張符号）はワイルドカードとする。", "Line by line, the signs of the TLA words are aligned with the signs of Nederhof's quadrats by edit distance (match 0, wildcard 0.5, substitution 1, gap 1). Signs with no Unicode code point (TLA/JSesh extension codes) become wildcards.")}</li>
<li>{bi("Nederhof の各記号は、一致または置換した TLA の記号の語に属する。余った記号は、前後が同じ語ならその語に、そうでなければ OPEN とする。", "Each Nederhof sign belongs to the word of the TLA sign it matched or replaced. A leftover sign goes to the word on both sides of it if that is one word; otherwise it is OPEN.")}</li>
<li>{bi("方形は、記号がすべて一語に属すれば「一語の中」、二語以上に属すれば「境目をまたぐ」、OPEN の記号があり残りが一語だけなら OPEN である。", "A quadrat is “inside one” if all its signs belong to one word, “across” if they belong to two or more, and OPEN if a sign is OPEN and the rest belong to one word only.")}</li>
<li>{bi("TLA は接尾代名詞（=f など）を別の要素として書く。そこで、TLA の要素ごとの数と、接尾代名詞を前の語に含めた数の両方を出す。", "The TLA writes suffix pronouns (=f etc.) as separate elements, so the counts are given both per TLA element and with suffix pronouns attached to the word before them.")}</li>
</ol>
{ctable}
<p class="meta">{bi("置換の多くは同じ記号の別の符号化である（例：複数の三本線 𓏤𓏤𓏤 と 𓏥、𓅜𓐍 の順序）。一語の語順が二つの符号化で入れ替わる例が一つある（EA 581 第27行の s,t.pl。下の注）。「完全一致のみ」の列は、記号が完全に一致したものだけで判定した数である。", "Most substitutions are two encodings of the same writing (e.g. three plural strokes 𓏤𓏤𓏤 against 𓏥, or the order of 𓅜𓐍). In one case a word sits in a different order in the two encodings (EA 581 line 27, s,t.pl; see the note below). The exact-only column counts only quadrats decided by exactly matched signs.")}</p>

<h2>{bi("3. 方形は語の境目をまたぐか", "3. Do quadrats cross word boundaries?")}</h2>
{qtable}
<p>{bi(
 f"EA 581 の横書きの行（第1〜7行）では方形{hrl_n}個のうち{dA['hrl'].get('across', 0)}個、縦書きの列（第8〜27行）では{vrl_n}個のうち{dA['vrl'].get('across', 0)}個がまたぐ。またぐ方形に入る語の組み合わせ（TLA の品詞）は、多い順に{pairs_ja}である。前置詞 n と次の語、動詞と =f のように、短い語が隣の語と一つの方形を分ける例が目立つ。",
 f"In the horizontal rows of EA 581 (lines 1–7), {dA['hrl'].get('across', 0)} of {hrl_n} quadrats cross; in the columns (lines 8–27), {dA['vrl'].get('across', 0)} of {vrl_n}. The word pairs inside crossing quadrats (TLA parts of speech), most frequent first: {pairs_en}. Short words sharing a quadrat with a neighbour are prominent, such as the preposition n with the next word, or a verb with =f.")}</p>

<h2>{bi("4. 語はいくつの方形にわたるか", "4. How many groups does a word span?")}</h2>
{utable}
<p>{bi(
 f"「群」は方形と単独の記号の両方を数える。EA 581 では記号のある TLA の語{a_wr}のうち{a_multi}（{pc(a_multi, a_wr)}）が二つ以上の群にわたり、EA 162 では{b_wr}のうち{b_multi}（{pc(b_multi, b_wr)}）である。つまり、方形は語の一部を収め、ときに二つの語の端を収める。語の境目と方形の境目は、別々に引かれている（EA 581・EA 162 で観察。TLA と Nederhof の符号化による）。",
 f"A “group” counts quadrats and lone signs alike. In EA 581, {a_multi} of the {a_wr} TLA words with signs ({pc(a_multi, a_wr)}) span two or more groups; in EA 162, {b_multi} of {b_wr} ({pc(b_multi, b_wr)}). So a quadrat holds part of a word, and sometimes the edges of two words. Word boundaries and quadrat boundaries are drawn independently (observed in EA 581 and EA 162; TLA and Nederhof encodings).")}</p>
<div class="note"><p>{bi(
 "<strong>注：順序の違い。</strong>EA 581 第27行で、Nederhof の符号化は m・ḥns・s,t.pl・jb の順に記号を置き、TLA は m s,t.pl ḥns-jb の順に語を並べる。整列では s,t.pl の記号（𓊨𓏪）を TLA の位置に見つけられず、同じ行の余った記号の列として見つけて s,t.pl に与えた。その結果 ḥns-jb は記号の列の上で途切れる。これが石の上の転置なのか、どちらかの符号化の都合なのかは OPEN である。",
 "<strong>Note: an order difference.</strong> In EA 581 line 27, Nederhof's encoding has the signs in the order m · ḥns · s,t.pl · jb, while the TLA lists the words as m s,t.pl ḥns-jb. The alignment did not find the signs of s,t.pl (𓊨𓏪) at the TLA position; it found them as a leftover run in the same line and gave them to s,t.pl. As a result ḥns-jb is discontinuous in the sign sequence. Whether this is a transposition on the stone or a convention of one of the encodings is OPEN.")}</p></div>

<h2>{bi("5. 境目をまたぐ方形の一覧", "5. List of crossing quadrats")}</h2>
<details><summary>{bi(f"EA 581（{a_t['across']}個と OPEN {a_t.get('open', 0)}個）", f"EA 581 ({a_t['across']}, plus {a_t.get('open', 0)} OPEN)")}</summary>
{across_list(A)}
</details>
<details><summary>{bi(f"EA 162（{b_t['across']}個）", f"EA 162 ({b_t['across']})")}</summary>
{across_list(B)}
</details>

<h2>{bi("6. 深さの在りかとのつながり", "6. How this connects to where the depth sits")}</h2>
<p>{bi(
 "<a href=\"depth\">深さの在りか</a>では、ラフマンの例で、機能の木の深さが方形をまたいだところにあることを見た（HYPOTHESIS）。ここでの数はその前提の一つを二つのテキスト全体で確かめる。語は方形に収まらないことが多く、方形は語の区切りに従わないことがある。層 B を語ごとに書くこと（バックログ9）は、この突き合わせを土台にできる。",
 "<a href=\"depth\">Where the depth sits</a> found, on Rahman's examples, that function-tree depth sits across quadrats (HYPOTHESIS). The counts here check one premise of that across two whole texts: words often do not fit in a quadrat, and quadrats sometimes ignore word division. Writing layer B word by word (backlog item 9) can build on this alignment.")}</p>
<div class="note"><p>{bi(
 f"<strong>並行関係（グラントの承認待ち）。</strong>漢字では、一字が二つの語の一部を収めることはふつうない。字の境目は語の境目の内側にある。ここで測ったヒエログリフの二つのテキストでは、方形の{lo}〜{hi}（TLA の要素で数えた場合）が二つ以上の語の記号を収める。書記の単位と語の単位の関係の違いとして書けるが、統語の主張ではない。",
 f"<strong>Parallel (for Grant to approve).</strong> In kanji a single character does not ordinarily hold parts of two words: character boundaries fall inside word boundaries. In the two hieroglyphic texts measured here, {lo}–{hi} of quadrats (counting TLA elements) hold signs of two or more words. This can be written as a difference in how the writing unit relates to the word, but it is not a syntactic claim.")}</p></div>

<h2>{bi("未決の問い", "Open questions")}</h2>
<ul>
<li>{bi(f"OPEN：EA 581 の方形{a_t.get('open', 0)}個と EA 162 の単独記号{B['byToken']['lone'].get('open', 0)}個（失われた記号 𓑃）。符号化の片方にしかない記号を含む。", f"OPEN: {a_t.get('open', 0)} quadrats in EA 581 and {B['byToken']['lone'].get('open', 0)} lone signs in EA 162 (lost-sign 𓑃). They contain a sign present in only one of the encodings.")}</li>
<li>{bi("OPEN：TLA の現行版（tla.digital）が2018年の抜粋と同じ語の区切りかどうか。現行版はボット確認のため読めなかった。", "OPEN: whether the current TLA (tla.digital) has the same word division as the 2018 excerpt. The current version could not be read because of the bot-verification page.")}</li>
<li>{bi("OPEN：方形の中の記号の順序が二つの符号化で違うとき（例：第2行の gr,t の t と ꜥḥꜥ,t の記号）、どの記号がどの語に属するかは位置で決めている。方形単位の数には影響しないが、記号単位の割り当ては確かではない。", "OPEN: where the two encodings order the signs inside a quadrat differently (e.g. line 2, the t of gr,t and the signs of ꜥḥꜥ,t), which sign belongs to which word is decided by position. This does not change the per-quadrat counts, but the per-sign assignment is not certain.")}</li>
<li>{bi("EA 162 の行の向き：上段の第1〜5行は横の行（大英博物館の記録「five rows」）、中段の第6〜8行は列（HieroJax の注「rightmost three columns」）。<a href=\"second-text\">二つ目のテキスト</a>を見よ。ここでの数には使っていない。", "EA 162 line orientation: upper-register lines 1–5 are rows (BM record, “five rows”), middle-register lines 6–8 are columns (HieroJax note, “rightmost three columns”); see <a href=\"second-text\">Second texts</a>. Not used in the counts here.")}</li>
</ul>
'''
    # inline glyphs in running text get the hieroglyph font (attributes such as data-q are left alone)
    glyphs = re.compile('([\U00013000-\U000143FF]+)')
    body = re.sub(r'>([^<]+)<', lambda m: '>' + glyphs.sub(r'<span class="h">\1</span>', m.group(1)) + '<', body)
    return body
