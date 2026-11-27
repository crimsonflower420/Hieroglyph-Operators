"""Page 'resolutions' (backlog item 4: the open derivations d03, d20, d22).
Imported by build_pages.py; decisions and counts from data/resolutions.json (tools/resolutions.py)."""
import json, re
from pathlib import Path
import pages_two_layer as TL
import derivations as DV
ROOT = Path(__file__).resolve().parent.parent
R = json.load(open(ROOT / 'data/resolutions.json', encoding='utf8'))
DEC = {d['id']: d for d in R['decisions']}
C = R['counts']; AES = C['aes']; HJ = C['hierojaxNswtBjtj']
REPO = 'https://github.com/crimsonflower420/Hieroglyph-Operators'

SOURCES = [
 ('Gardiner, A. H. <i>Egyptian Grammar</i>. 3rd ed., revised. Oxford: Griffith Institute, 1957. Checked: §16 (p. 25), §54 with n. 1 (p. 50), §§55–57 (p. 51), sign list W3 (p. 527).', ''),
 ('Allen, J. P. <i>Middle Egyptian: An Introduction to the Language and Culture of Hieroglyphs</i>. 2nd ed., revised. Cambridge University Press, 2010. Checked: §4.15 (p. 44), sign list W3 (p. 448).', ''),
 ('Poe, W. C. <i>The Writing of a Skillful Scribe: An Introduction to Hieratic Middle Egyptian through the Text of The Shipwrecked Sailor</i>. Santa Rosa, CA, 2010. Checked: “Transposition of glyphs” (p. 6) and the titles of the king (p. 63).', 'https://egyptologyforum.org/bbs/Stableford/Poe%2C%20The_Writing_of_a_Skillful_Scribe_An_intr.pdf'),
 ('Peust, C. “Die honorative Transposition in der ägyptischen Schrift.” <i>Lingua Aegyptia</i> 15 (2007): 93–135. Checked: §0 Einführung (pp. 93–94).', 'https://doi.org/10.11588/propylaeumdok.00003221'),
 ('Schweitzer, S. D. AES – Ancient Egyptian Sentences (TLA database excerpt, January 2018), all 16 corpus files at commit 35276d25, CC BY-SA 4.0. Extract: data/nswt-aes.json.', 'https://github.com/simondschweitzer/aes'),
 ('Rahman, Md. R. <i>Ancient Egyptian Hieroglyph as the Pictorial Scrutiny of Modern Linguistics</i>. ILIM Press, 2023. pp. 37, 65–66, 81, 84 (paraphrased; figures not reproduced).', ''),
]

LAB = {'source': ('出典', 'source'), 'observation (this site)': ('観察（このサイト）', 'observation (this site)')}

# Japanese first, English fitted to it. Each pair paraphrases the evidence in data/resolutions.json.
EV = {
 'd03': [
  ('Gardiner 1957, p. 527（記号表 W3）', 'W3（清めに使う雪花石膏の鉢）は ḥb「祭り」の限定符であり、まさにこの綴り V28・D58・W3 が第18王朝の異体として挙がる。音価 ḥb は、ḥb「嘆く」などで半表語・表音として使う場合だけに挙げられる。',
   'Gardiner 1957, p. 527 (sign list W3)', "W3 (basin of alabaster used in purifications) is the determinative of ḥb 'feast', and exactly this spelling, V28 D58 W3, is cited as the Dyn. XVIII variant. The value ḥb is given only for its use as semi-ideogram or phonogram in words such as ḥb 'mourn'.", 'source'),
  ('Allen 2010, p. 448（記号表 W3）', 'W3 は「祭り」の限定符で、ḥ3b「祭り」の表語である。音価は挙げない。', 'Allen 2010, p. 448 (sign list W3)', "W3 is the determinative FEAST and the ideogram for ḥ3b 'feast'. No sound value is listed.", 'source'),
  ('Rahman, p. 37', '本書は「本来の発音」を /hb-hb/、「書物上の発音」を /hb/ とする。どちらの木からも二重の音は出てこない。', 'Rahman, p. 37', "The book gives /hb-hb/ as the 'authentic' and /hb/ as the 'bookish' pronunciation. Neither tree yields a doubled sound.", 'source'),
 ],
 'd20': [
  ('Gardiner 1957 §16, p. 25', '人・動物・鳥など前と後ろのある記号は、ほとんどつねに銘文の始まりを向く。上は下に先立つ。', 'Gardiner 1957, §16, p. 25', 'Signs of persons, animals and birds, and others with a front and a back, almost always face the beginning of the inscription; upper comes before lower.', 'source'),
  ('Unicode 16.0 第11章 §11.4', '人や動物の顔を向かい合うように読む（このサイトですでに引いている）。', 'Unicode 16.0, ch. 11, §11.4', 'One reads a line facing into the faces of people or animals (already cited on this site).', 'source'),
  ('Rahman, pp. 65, 84（同じ画像）', 'カルトゥーシュの縦線は左端にある。右端から p・t、wꜣ、l・m、i・i、s と名の綴りが並び、ついで ꜥnḫ、ḏ・t・土地、p・t、ḥ、mr、i・i となる。ライオン E23 とコブラ I10 は右を向く。', 'Rahman, pp. 65, 84 (the same image)', "The cartouche's vertical line is at the left end. From the right end the name runs p·t, wꜣ, l·m, i·i, s, then ꜥnḫ, ḏ·t·land, p·t, ḥ, mr, i·i. The lion E23 and the cobra I10 face right.", 'observation (this site)'),
  ('Rahman, p. 84（短いカルトゥーシュ）', '名だけの短いカルトゥーシュは左から右に読む。縦線は右端、p・t は左端にあり、ライオンは左を向く。', 'Rahman, p. 84 (short cartouche)', 'The short cartouche with the name only reads left to right: the vertical line is at the right end, p·t at the left end, and the lion faces left.', 'observation (this site)'),
  ('Gardiner 1957 §57, p. 51; Allen 2010 §4.15, p. 44', '敬意による転置の例として、どちらも mry Imn「アメンに愛された」を挙げる。', 'Gardiner 1957, §57, p. 51; Allen 2010, §4.15, p. 44', "Both give mry Imn 'beloved of Amun' as an example of honorific transposition.", 'source'),
 ],
 'd22': [
  ('Gardiner 1957 §55, p. 51', 'まさにこの組（スゲとハチの下に t と t）を略記の例に挙げ、n-sw-bit「上下エジプトの王」、字義どおりには「上エジプトのスゲと下エジプトのハチに属する者」と読む。', 'Gardiner 1957, §55, p. 51', "This very group (sedge and bee over t and t) is listed among abbreviations and read n-sw-bit 'king of Upper and Lower Egypt', literally 'he who belongs to the sedge of Upper Egypt and the bee of Lower Egypt'.", 'source'),
  ('Gardiner 1957 §56, p. 51', '書記上の転置：見た目をよくするため、あるいはそれほどはっきりしない理由で、記号の順が入れ替わることがある。場所の節約もその理由の一つである。', 'Gardiner 1957, §56, p. 51', 'Graphic transpositions: signs are sometimes transposed to give a more pleasing appearance, or for some less assignable reason; economy of space is one reason.', 'source'),
  ('Gardiner 1957 §57, p. 51', '敬意による転置：nsw「王」や nṯr「神」、王や神の名を、話すときには先に来る密接な語より前に書く（sš nsw、ḥm-nṯr、mry Imn）。', 'Gardiner 1957, §57, p. 51', "Honorific transposition: nsw 'king', nṯr 'god' and the names of kings and gods are written before closely connected words that were spoken first (sš nsw, ḥm-nṯr, mry Imn).", 'source'),
  ('Gardiner 1957 §54 注1, p. 50', '「王」は nsw と読み、swtn とは読まない。注は ni「属する」＋ swt「スゲ」から説明する。転置という語は使わない。', 'Gardiner 1957, §54 n. 1, p. 50', "'King' is read nsw, not swtn; the note explains it from ni 'belonging to' + swt 'sedge'. It does not use the word transposition.", 'source'),
  ('Allen 2010 §4.15, p. 44', '敬意による転置を直接属格で定義する（所有者 nṯr や nswt を先に書く）。nswt そのものも敬意による転置を含むかもしれない、と述べたうえで、n(j)＋swt がおそらく「スゲをもつ者」の意味なら、変わった並びはまとまった組を作りたいからにすぎない、と書く。', 'Allen 2010, §4.15, p. 44', "Honorific transposition is defined on the direct genitive (the possessor nṯr or nswt written first). Allen says nswt itself may involve honorific transposition, then adds that if n(j) + swt means, as is probable, 'he to whom the sedge belongs', the unusual order just reflects the wish to make a compact group.", 'source'),
  ('Poe 2010, p. 6', '転置は二種類ある。敬意による転置（表すものの地位による）と、書記上の転置（釣り合いや対称のため。小さな記号二つを組んで想像上の四角を埋めるなど）。', 'Poe 2010, p. 6', 'There are two kinds: honorific transposition (order changed by the status of what is represented) and graphic transposition (order changed for balance or symmetry, e.g. two small glyphs grouped to fill an imaginary square).', 'source'),
  ('Poe 2010, p. 63', 'n(y)-swt の記号の並びは書記上の転置の例である。一方、sꜣ nsw で nsw が sꜣ の前に来るのは敬意による転置である。', 'Poe 2010, p. 63', 'The arrangement of the glyphs of n(y)-swt is an example of graphic transposition; nsw standing before sꜣ in sꜣ nsw is honorific transposition.', 'source'),
  ('Peust 2007, pp. 93–94', '敬意による転置は、方形を作るための純粋に書法上の転置とは区別すべきである。', 'Peust 2007, pp. 93–94', 'Honorific transposition is to be kept apart from purely calligraphic transposition whose aim is to form quadrats.', 'source'),
  ('Rahman, p. 81', '図はスゲとハチの下に t と t を置く。n（N35）は書かれていない。', 'Rahman, p. 81', 'The figure puts sedge and bee over t and t; no n (N35) is written.', 'observation (this site)'),
 ],
}


def pc(a, b): return f'{100 * a / b:.0f}%' if b else '—'


def pages(bi):
    def ev_list(k):
        items = ''
        for sja, tja, sen, ten, lab in EV[k]:
            l = LAB[lab]
            items += f'<li><span class="k">{bi(*l)}</span>{bi(f"<b>{sja}</b>：{tja}", f"<b>{sen}</b>: {ten}")}</li>'
        return f'<ul class="ev">{items}</ul>'

    def card(k):
        return TL.card(TL.BYID[k], bi).replace(f'<section class="drv" id="{k}">', f'<section class="drv" id="card-{k}">', 1)

    rej = DV.parse_bracket(DEC['d03']['rejected']); d03 = TL.BYID['d03']
    rej_svg = DV.svg_tree(rej, d03, 'B')
    H = R['heights']
    n_n = AES['nswtWithN35'].get('M23_before_N35', 0); n_rev = AES['nswtWithN35'].get('N35_before_M23', 0)
    bj = AES['nswtBjtjFourSigns']; col = bj.get('M23-X1-L2-X1', 0); row = bj.get('M23-L2-X1-X1', 0); bj_all = sum(bj.values())
    hj_c = HJ['byClass'].get('columns', 0); hj_l = HJ['byClass'].get('linear', 0); hj_n = len(HJ['groups'])
    hj_rows = ''.join(
        f'<tr><td>{g["text"].upper().replace("EA", "EA ")}</td><td>{g["line"]}</td><td>{bi("行（横）", "row") if g["orientation"] == "row" else (bi("列（縦）", "column") if g["orientation"] == "col" else "—")}</td>'
        f'<td>{" | ".join(g["groups"])}</td><td>{bi("列ごと（各 t が自分の記号の下）", "by columns (each t under its own sign)") if g["class"] == "columns" else bi("一列（スゲ・ハチ・t・t）", "linear (sedge, bee, t, t)")}</td></tr>'
        for g in HJ['groups'])
    corp = {}
    for r in AES['byCorpus']:
        corp.setdefault(r['corpus'], {})[r['class']] = r['n']
    corp_rows = ''.join(f'<tr><td>{c}</td><td class="num">{v.get("M23_before_N35", 0)}</td><td class="num">{v.get("N35_before_M23", 0)}</td>'
                        f'<td class="num">{v.get("M23-X1-L2-X1", 0)}</td><td class="num">{v.get("M23-L2-X1-X1", 0)}</td></tr>' for c, v in sorted(corp.items()))

    summary = f'''<div class="table-scroll"><table>
<tr><th>{bi("導出", "Deriv.")}</th><th>{bi("問い", "Question")}</th><th>{bi("決定", "Decision")}</th><th>{bi("拠りどころ", "Resting on")}</th><th>{bi("残る未決", "Still OPEN")}</th></tr>
<tr><td><a href="#d03">d03</a></td><td>{bi("ḥb「祭り」の W3 は、補音を伴う二子音記号か、綴りを閉じる限定符か", "ḥb 'festival': is W3 a biliteral with complements, or a determinative closing the spelling?")}</td><td>{bi("限定符（CLOSE の木）。補音の木は退ける", "determinative (the CLOSE tree); the complement tree is rejected")}</td><td>Gardiner 1957, p. 527; Allen 2010, p. 448</td><td>—</td></tr>
<tr><td><a href="#d20">d20</a></td><td>{bi("本書の図の向き（記号列は右から左なのに、動物は左を向く？）", "orientation of the book's figure (sequence right to left, animals facing left?)")}</td><td>{bi("食い違いはない。図は右から左に読み、動物は右を向く", "no mismatch: the figure reads right to left and the animals face right")}</td><td>{bi("Gardiner 1957 §16, p. 25；図の観察", "Gardiner 1957, §16, p. 25; observation of the figure")}</td><td>{bi("土地の記号 N16 か N17 か", "land sign N16 or N17")}</td></tr>
<tr><td><a href="#d22">d22</a></td><td>{bi("nswt-bjtj の並べ替えは敬意によるものか、書記上のものか", "nswt-bjtj: honorific or graphic reorder?")}</td><td>{bi("書記上（graphic）。Allen と Poe は対立していなかった", "graphic; Allen and Poe did not in fact disagree")}</td><td>Gardiner 1957 §§55–57; Allen 2010 §4.15; Poe 2010, pp. 6, 63; Peust 2007, pp. 93–94</td><td>{bi("2×2 の方形を行ごとに辿るか、列ごとに辿るか", "whether the 2×2 quadrat is walked by rows or by columns")}</td></tr>
</table></div>'''

    body = f'''
<p class="tag">{bi("探索・2026年11月27日", "Exploration · 27 Nov 2026")}</p>
<h1>{bi("未決の解決：d03・d20・d22", "Resolutions: d03, d20 and d22")}</h1>
<p class="lede">{bi(
 "ラフマン再読の26の導出のうち、三つに未決（OPEN）の点が残っていた。d03 の機能の木をどちらにするか、d20 の図の向き、d22 の並べ替えが敬意によるものか書記上のものか、である。文法書の該当ページを一つずつ確かめて、三つとも決めた。d03 は限定符で閉じる木、d20 は食い違いなし、d22 は書記上の転置である。ただし d22 には、2×2 の方形を行ごとに辿るか列ごとに辿るかという、別の未決が一つ残る。",
 "Of the 26 derivations in the Rahman re-read, three still had OPEN points: which function tree d03 takes, the orientation of the d20 figure, and whether the d22 reorder is honorific or graphic. Each was checked against the relevant pages of the grammars, and all three are now decided: d03 is the tree closed by a determinative, d20 has no mismatch, and d22 is a graphic transposition. One further point stays OPEN in d22: whether its 2×2 quadrat is walked by rows or by columns.")}</p>
{summary}
<p class="meta">{bi(
 f"決定・根拠・状態は <a href=\"{REPO}/blob/main/data/resolutions.json\">data/resolutions.json</a> に、計算は <code>tools/resolutions.py</code> にある。このスクリプトは、導出のデータ（<code>data/derivations/rahman.drv</code>）が決定どおりに書き換えられているかも確かめ、合わなければ失敗する。ラフマンの本は全権利保留なので、言い換えてページを示し、図は載せない。",
 f"Decisions, evidence and status are in <a href=\"{REPO}/blob/main/data/resolutions.json\">data/resolutions.json</a>; the script is <code>tools/resolutions.py</code>. It also checks that the derivation data (<code>data/derivations/rahman.drv</code>) have been rewritten to match the decisions, and fails if not. Rahman's book is all rights reserved, so it is paraphrased with page numbers, and its figures are not reproduced.")}</p>

<h2 id="d03">{bi("1. d03 ḥb「祭り」：W3 は限定符", "1. d03 ḥb 'festival': W3 is the determinative")}</h2>
<p>{bi(
 "綴りは ḥ（V28）・b（D58）・W3（雪花石膏の鉢）の三つである。配置の木は一つ（三つの記号を並べた列）で、機能の木には二つの候補があった。一つは W3 を二子音記号 ḥb とし、V28 と D58 をその補音とする木（CMPL3）、もう一つは ḥ と b で語を綴り、W3 を限定符として閉じる木（CLOSE）である。どちらも検査器を通るので、検査器では決まらない。決めるのは、W3 がこの語で音をもつかどうかである。",
 "The spelling is ḥ (V28), b (D58) and W3 (alabaster basin). There is one layout tree (a row of three signs) and there were two candidate function trees: W3 as the biliteral ḥb with V28 and D58 as its complements (CMPL3), or ḥ and b spelling the word with W3 closing it as determinative (CLOSE). Both pass the checker, so the checker cannot decide. What decides is whether W3 has a sound value in this word.")}</p>
{ev_list('d03')}
<div class="flag ok">{bi(
 f"<b>決定。</b>二つの文法書の記号表は、どちらもこの語の W3 を限定符とし、音価を与えない。Gardiner は、まさにこの綴りを限定符の例として挙げる。そこで層 B は CLOSE の木とし、補音の木は退ける。木そのものは、ほかの木と同じく HYPOTHESIS である。この決定で d03 の層 B の高さは{H['d03_hB_rejected']}から{H['d03_hB']}になり、種類は「補音」から「限定符」に移った。<a href=\"depth\">深さの在りか</a>の数字もそれに合わせて計算し直してある。",
 f"<b>Decision.</b> Both grammars' sign lists treat W3 in this word as a determinative and give it no sound value; Gardiner cites exactly this spelling as the example. Layer B is therefore the CLOSE tree, and the complement tree is rejected. The tree itself, like every tree here, is a HYPOTHESIS. With this decision the height of d03's layer B goes from {H['d03_hB_rejected']} to {H['d03_hB']}, and d03 moves from 'complements' to 'determinatives'. The figures on <a href=\"depth\">Where the depth sits</a> have been recomputed to match.")}</div>
<details><summary>{bi("退けた木（補音の木）", "The rejected tree (complements)")}</summary><pre class="bracket">{DEC['d03']['rejected']}</pre><div class="svgscroll">{rej_svg}</div></details>
{card('d03')}

<h2 id="d20">{bi("2. d20 プトレマイオスのカルトゥーシュ：図の向き", "2. d20 Ptolemy's cartouche: the orientation of the figure")}</h2>
<p>{bi(
 "以前の注は「本書の図では記号列は右から左に読まねばならないのに、動物の記号は左を向いている」として、向きを未決にしていた。本書の PDF から図の画像そのもの（pp. 65 と 84 で同じ画像）を取り出し、拡大して見直した。",
 "The earlier note said that 'in the book's figure the sequence must be read right to left while the animal signs face left' and left the orientation OPEN. The image itself (the same image on pp. 65 and 84) was extracted from the book's PDF and re-examined enlarged.")}</p>
{ev_list('d20')}
<div class="flag ok">{bi(
 "<b>決定。</b>食い違いはない。図は右から左に読み、ライオンとコブラは右、つまり行の始まりを向いている。これは Gardiner の規則（§16）どおりである。同じ頁の短いカルトゥーシュは逆向きで、左から右に読み、ライオンは左を向く。二つの図はたがいに鏡像の関係にあり、どちらも規則に合う。以前の注は、小さな図の読み誤りであった。層 A、二つの歩き、TRANSPOSE(honorific) は変わらない。",
 "<b>Decision.</b> There is no mismatch. The figure reads right to left, and the lion and the cobra face right, towards the start of the line, as Gardiner's rule (§16) requires. The short cartouche on the same page runs the other way, left to right, with the lion facing left. The two figures mirror each other, and both follow the rule. The earlier note was a misreading of the small figure. Layer A, the two walks and TRANSPOSE(honorific) are unchanged.")}</div>
<p>{bi(
 "OPEN のまま残るのは二点である。一つは、ḏt の下の土地の記号が N16 か N17 かで、図が小さすぎて見分けられない。もう一つは、ロゼッタ・ストーン（大英博物館 EA 24）そのものでの配置で、これは確かめていない。導出は本書の図にしたがう。前者は、同じカルトゥーシュの大きな図か、石の写し（大英博物館の記録は Quirke & Andrews 1988 の写しを挙げる）で決まる。",
 "Two points stay OPEN. One is whether the land sign under ḏt is N16 or N17; the figure is too small to tell. The other is the layout on the Rosetta Stone itself (British Museum EA 24), which was not checked; the derivation follows the book's figure. The first would be decided by a larger image of the same cartouche or a facsimile of the stone (the BM record lists the facsimile drawing by Quirke & Andrews 1988).")}</p>
{card('d20')}

<h2 id="d22">{bi("3. d22 nswt-bjtj：書記上の転置", "3. d22 nswt-bjtj: graphic transposition")}</h2>
<p>{bi(
 "本書の図は、スゲ M23 とハチ L2 を上段に、t と t を下段に置いた 2×2 の方形である。配置の木を行ごとにとると、書き順の歩きは M23・L2・X1・X1、読みは M23・X1（nswt）、L2・X1（bjtj）となり、二つの歩きが食い違う。問いは、この食い違いを敬意による転置と呼ぶか、書記上の転置と呼ぶかであった。メモには「Allen は転置とみなしうるとし、Poe は書記上と呼ぶ」とあり、二人が対立しているように書いていた。",
 "The book's figure is a 2×2 quadrat: sedge M23 and bee L2 on top, t and t below. Taking the layout tree by rows, the writing walk is M23, L2, X1, X1 and the reading is M23·X1 (nswt), L2·X1 (bjtj), so the walks differ. The question was whether to call this honorific or graphic transposition. The notes said 'Allen suggests transposition; Poe calls it graphic', as if the two disagreed.")}</p>
{ev_list('d22')}
<div class="flag ok">{bi(
 "<b>決定：書記上（graphic）。</b>理由は三つある。(1) 敬意による転置は、神や王を表す語を、それと結びつく語より前に書くことである（Gardiner §57、Allen §4.15）。この組では、そうして前に出た語はない。nswt は書いても話しても先頭にある。(2) 食い違いは、ハチ L2 が nswt の t より先に来ることだけである。これは小さな記号を組んで方形を埋める並びで、Gardiner の §56、Poe（p. 6）、Peust（pp. 93–94）のいう書記上・書法上の転置にあたる。(3)「Allen 対 Poe」は対立ではなかった。Allen は nswt の並びが敬意による転置かもしれないとしたうえで、自分の推す語義のもとでは、まとまった組を作るための並びだとする。Poe はそれを書記上の転置と呼ぶ。二人の言うことは同じ方向を向いている。そのうえ本書の図には n が書かれていないので、n とスゲの順という Allen と Poe の論点は、この導出には現れない。",
 "<b>Decision: graphic.</b> Three reasons. (1) Honorific transposition writes a word for a god or king ahead of a word it is bound to (Gardiner §57; Allen §4.15). No word in this group is brought forward that way; nswt is first both in writing and in speech. (2) The only difference is that the bee L2 comes before the t of nswt. That is small signs grouped to fill the square, the graphic or calligraphic transposition of Gardiner §56, Poe (p. 6) and Peust (pp. 93–94). (3) 'Allen against Poe' was not a disagreement. Allen says the order of nswt may involve honorific transposition, then explains it, under the meaning he prefers, as making a compact group; Poe calls the same order graphic. They point the same way. Moreover the book's figure has no n, so the point Allen and Poe discuss, the order of n and sedge, does not arise in this derivation.")}</div>

<h3>{bi("数で見る：編者は同じ組をどう並べるか", "In numbers: how editors line up the same group")}</h3>
<p>{bi(
 f"決定は上のページに拠る。数は背景として示す。AES（TLA の2018年1月の抜粋、全16コーパス）で、記号列をもつ nswt の語例のうち、M23 と N35 の両方を含むものは{n_n + n_rev}例ある。そのすべて（{n_n}例）で M23 が N35 より先に来る。n を先に書く例は{n_rev}例である。nswt-bjtj で、記号列がちょうど M23・L2・X1・X1 の四つから成る語例は{bj_all}例ある。そのうち{col}例（{pc(col, bj_all)}）が M23-X1-L2-X1、つまり読む順に並べ、{row}例（{pc(row, bj_all)}）が M23-L2-X1-X1、つまり行ごとの順に並べる。TLA の記号列は編者が組を一列に並べたものであり、配置の記録ではない。行か列かはそこからは分からない。分かるのは、編者が同じ組を両方の順で並べているということである。",
 f"The decision rests on the pages above; the numbers are context. In AES (the January 2018 TLA excerpt, all 16 corpora), {n_n + n_rev} tokens of nswt with a sign sequence contain both M23 and N35. In all of them ({n_n}) M23 comes before N35; n is written first in {n_rev}. Of the tokens of nswt-bjtj whose sign sequence is exactly the four signs M23, L2, X1, X1, {col} of {bj_all} ({pc(col, bj_all)}) list them as M23-X1-L2-X1, in reading order, and {row} ({pc(row, bj_all)}) as M23-L2-X1-X1, row by row. A TLA sign sequence is the editors' linearization of a group, not a record of its layout, so it cannot show rows or columns. It shows only that editors line the same group up both ways.")}</p>
<div class="table-scroll"><table><tr><th>{bi("AES のコーパス", "AES corpus")}</th><th class="num">nswt: M23 → N35</th><th class="num">nswt: N35 → M23</th><th class="num">nswt-bjtj: M23-X1-L2-X1</th><th class="num">nswt-bjtj: M23-L2-X1-X1</th></tr>{corp_rows}
<tr><td><b>{bi("計", "Total")}</b></td><td class="num"><b>{n_n}</b></td><td class="num"><b>{n_rev}</b></td><td class="num"><b>{col}</b></td><td class="num"><b>{row}</b></td></tr></table></div>
<p>{bi(
 f"M.-J. Nederhof の HieroJax 符号化（このサイトで使っている6つの石碑）には、nswt-bjtj の組が{hj_n}か所ある。{hj_c}か所はスゲと t、ハチと t をそれぞれ縦の組にした二つの方形として符号化され（列ごと）、{hj_l}か所（EA 567 の1行目）はスゲ・ハチ・t・t を別々の組として一列に並べている。相対位置は編者の判断であり、石の写しではない。",
 f"M.-J. Nederhof's HieroJax encodings (the six stelae used on this site) contain the nswt-bjtj group {hj_n} times. {hj_c} are encoded as two quadrats, sedge over t and bee with t (by columns); {hj_l} (EA 567, line 1) lines up sedge, bee, t, t as separate groups in a row. Relative positions are the editor's judgement, not a facsimile.")}</p>
<div class="table-scroll"><table><tr><th>{bi("石碑", "Stela")}</th><th>{bi("行", "line")}</th><th>{bi("向き", "orient.")}</th><th>{bi("符号列", "encoding")}</th><th>{bi("組み方", "grouping")}</th></tr>{hj_rows}</table></div>
<div class="flag spec">{bi(
 "<b>OPEN：2×2 の方形の歩き。</b>本書の図は 2×2 の方形で、行ごとの木［⿱［⿰ M23 L2］［⿰ X1 X1］］にも、列ごとの木［⿰［⿱ M23 X1］［⿱ L2 X1］］にも合う。行ごとにとれば上の書記上の転置があり、列ごとにとれば二つの歩きは一致して並べ替えは消える。このサイトは今の木（行ごと、Gardiner §16 の「上は下に先立つ」を方形全体に当てたもの）を残し、列ごとの木を別案として記す。どちらにするかは、方形の中を列ごとに読む順のラベル（探索の項目5）の問題であり、グラントの承認があるまで規格には何も足さない。",
 "<b>OPEN: the walk of the 2×2 quadrat.</b> The book's figure is a 2×2 quadrat and fits both the row tree [⿱ [⿰ M23 L2] [⿰ X1 X1]] and the column tree [⿰ [⿱ M23 X1] [⿱ L2 X1]]. By rows there is the graphic transposition above; by columns the two walks coincide and the reorder disappears. This site keeps the present tree (by rows, applying Gardiner §16's 'upper before lower' to the whole quadrat) and records the column tree as the alternative. Which to use is the question of a label for column-wise reading order inside a quadrat (exploration item 5), and nothing is added to the standard until Grant approves.")}</div>
{card('d22')}

<h2>{bi("4. ついでに確かめたこと", "4. Checked along the way")}</h2>
<ul>
<li>{bi("<a href=\"rahman#d23\">d23</a>：Gardiner の記述の節を確かめた。略記が多いことは §57（p. 51）、「王」を nsw と読み swtn とは読まないことは §54（p. 50）にある。本書 p. 84 の /swtn/ は、まさに Gardiner が退ける読みである。", "<a href=\"rahman#d23\">d23</a>: the Gardiner references were checked. Abbreviated writings being frequent is §57 (p. 51); 'king' read nsw and not swtn is §54 (p. 50). The book's /swtn/ (p. 84) is exactly the reading Gardiner rejects.")}</li>
<li>{bi("Poe の文献表示を直した。著者は William Clay Poe で、2010年に Santa Rosa で出ている（表題ページ）。以前は「Poe, A.」としていた。", "The Poe citation was corrected: the author is William Clay Poe, Santa Rosa, 2010 (title page); it was listed as 'Poe, A.'.")}</li>
</ul>

<h2>{bi("主張しないこと", "What is not claimed")}</h2>
<div class="flag">{bi(
 "ここでの決定は、記号の機能と書き方の層についてのものである。転置を統語の移動とはみなさず、Merge・X バー・θ役割の主張もしない。Peust（2007）は敬意による転置が統語の倒置に似ていると論じるが、このサイトはその見方を使わない。",
 "These decisions concern the sign-function and writing layers. Transposition is not treated as syntactic movement, and nothing is claimed about Merge, X-bar or θ-roles. Peust (2007) argues that honorific transposition resembles syntactic inversion; this site does not use that view.")}</div>
'''
    glyphs = re.compile('([\U00013000-\U000143FF]+)')
    body = re.sub(r'>([^<]+)<', lambda m: '>' + glyphs.sub(r'<span class="h">\1</span>', m.group(1)) + '<', body)
    return body
