# Research pass 1 — 2026-11-21

Primary sources first. Every item below was fetched and read on 2026-11-21 unless marked otherwise.

## 1. Unicode Egyptian hieroglyph format controls

Source: UnicodeData.txt and DerivedAge.txt, UCD 18.0.0 (https://www.unicode.org/Public/UCD/latest/ucd/).

| Code point | Name | Since |
|---|---|---|
| U+13430 | EGYPTIAN HIEROGLYPH VERTICAL JOINER | 12.0 |
| U+13431 | EGYPTIAN HIEROGLYPH HORIZONTAL JOINER | 12.0 |
| U+13432 | EGYPTIAN HIEROGLYPH INSERT AT TOP START | 12.0 |
| U+13433 | EGYPTIAN HIEROGLYPH INSERT AT BOTTOM START | 12.0 |
| U+13434 | EGYPTIAN HIEROGLYPH INSERT AT TOP END | 12.0 |
| U+13435 | EGYPTIAN HIEROGLYPH INSERT AT BOTTOM END | 12.0 |
| U+13436 | EGYPTIAN HIEROGLYPH OVERLAY MIDDLE | 12.0 |
| U+13437 | EGYPTIAN HIEROGLYPH BEGIN SEGMENT | 12.0 |
| U+13438 | EGYPTIAN HIEROGLYPH END SEGMENT | 12.0 |
| U+13439 | EGYPTIAN HIEROGLYPH INSERT AT MIDDLE | 15.0 |
| U+1343A | EGYPTIAN HIEROGLYPH INSERT AT TOP | 15.0 |
| U+1343B | EGYPTIAN HIEROGLYPH INSERT AT BOTTOM | 15.0 |
| U+1343C | EGYPTIAN HIEROGLYPH BEGIN ENCLOSURE | 15.0 |
| U+1343D | EGYPTIAN HIEROGLYPH END ENCLOSURE | 15.0 |
| U+1343E | EGYPTIAN HIEROGLYPH BEGIN WALLED ENCLOSURE | 15.0 |
| U+1343F | EGYPTIAN HIEROGLYPH END WALLED ENCLOSURE | 15.0 |
| U+13440 | EGYPTIAN HIEROGLYPH MIRROR HORIZONTALLY (Mn) | 15.0 |
| U+13441–13442 | FULL BLANK, HALF BLANK (Lo) | 15.0 |
| U+13443–13446 | LOST SIGN, HALF / TALL / WIDE LOST SIGN (Lo) | 15.0 |
| U+13447–13455 | 15 × MODIFIER DAMAGED … (Mn) | 15.0 |

- In the 12.0 proposal, L2/17-112R (Glass, Hafemann, Nederhof, Polis, Richmond, Rosmorduc, Schweitzer, 2017), U+13436 was called "STACK MIDDLE" and U+13437/8 "SEGMENT START/END". The names changed before encoding. L2/17-112R also says all 45 quadrat structures attested in L2/16-232 can be encoded.
- The Unicode 15 additions came from L2/21-248 (Glass, Grotenhuis, Nederhof, Polis, Rosmorduc, Werning, 22 Dec 2021). It asked for 30 characters, and Unicode 15.0 added 29. The 15.0 announcement says "Twenty-nine additional Egyptian hieroglyph format controls".
- The Unicode Standard 16.0, ch. 11, §11.4.3, says four controls derive from MdC: the vertical joiner = `:`, the horizontal joiner = `*`, begin segment = `(` and end segment = `)`. Overlay "stack[s] at their center points". Corner insertion names use start/end, not left/right. Rotation uses VS1–VS3 for 90/180/270° (StandardizedVariants.txt). Mirroring (U+13440) is relative to line direction.
- Grammar: Nederhof, HieroJax "Syntax" page and L2/24-079 (17 Feb 2024). `*` binds tighter than `:`, and a vertical group inside a horizontal group needs segments. Bracket matching is beyond regular languages, so OpenType is not expected to render every valid encoding.
- Font check: Noto Sans Egyptian Hieroglyphs v2.002 (2024-04-15) has no glyphs for U+13430–13440 and no GSUB/GPOS quadrat shaping (features: aalt, ccmp, locl, ordn). It does not cover Extended-A (0 of U+13460–143FF). The site therefore uses its own schematic layout.

## 2. Manuel de Codage and JSesh

- Buurman, Grimal, Hainsworth, Hallof, van der Plas, *Manuel de codage des textes hiéroglyphiques en vue de leur saisie sur ordinateur*, Informatique et Égyptologie 2, Paris 1988. Its origin is the 1984 round table at the Fondation Hugot (AIBL catalogue page).
- MdC operators, as described in the JSesh documentation (rosmord/jsesh user guide; "A description of the manuel de codage (2)"; "About JSesh 6 sign placement"):
  - `-` separates quadrats.
  - `:` stacks vertically.
  - `*` places side by side.
  - `( )` groups.
  - `&` makes a ligature.
  - `#` (official) or `##` (JSesh) overlays.
  - `^^^` and `&&&` are the JSesh complex-ligature insertions.
  - `!` ends a line and `!!` ends a page.
  - JSeshJs adds `%insert[dir]`.
- JSesh licence: CeCILL-C. Some files are CC0, CC-BY-SA or CC-BY. The fonts have separate terms.

## 3. Gardiner's sign list

- Gardiner, *Egyptian Grammar*, 3rd ed., 1957 (1st ed. 1927).
- Per the Unicode Standard §11.4.1, the chief source of the "Gardiner set" is that sign list, plus his font catalogues (1928, 1929, 1931, 1953). Names pad numbers to three digits (E034 = E34 "desert hare", wn).
- Categories run A–Z plus Aa (catchpenny.org MdC page; Unicode names list).
- Page numbers are NOT verified, so none are cited.

## 4. Quadrats and reading direction

- Unicode Standard §11.4: signs are "arranged next to one another in an aesthetically-pleasing manner … within a notional rectangle … quadrat".
- Direction: text runs left to right or right to left, in rows or columns. "One reads a line facing into the glyphs depicting the faces of people or animals." Unicode gives strong LTR and says glyphs should be mirrored when the text is shown RTL.

## 5. Stroke or drawing order

- Hieratic: AKU-PAL (Mainz) v1.3 (27 Feb 2024) adds "Display of stroke sequence as vector graphics" for graphemes.
- Regulski, I. 2018, "Writing habits as identity marker: on sign formation in Papyrus Gardiner II", in *Ägyptologische „Binsen"-Weisheiten III*, Franz Steiner, doi:10.25358/openscience-395. The abstract studies "individual brush strokes that constitute the building blocks of a hieroglyph" and levels of standardisation within one document (P. Gardiner II = BM EA 10676).
- NOTE: a search-engine summary credited this paper to Verhoeven. That was wrong; the DOI metadata gives Regulski.
- SPECULATIVE / OPEN: whether any shared, prescribed stroke order existed (as with kanji). Nothing found for monumental hieroglyphs. Not yet searched: unfinished-inscription studies (red draft lines, grids).

## 6. Machine-readable corpora

| Corpus | Layout (quadrat) info? | Licence |
|---|---|---|
| TLA HF datasets (Earlier Egyptian v18, Late Egyptian v19, Demotic v18) | Unicode signs, but **no format controls** (0/12,773 sentences in EE v18) | CC BY-SA 4.0 |
| TLA raw data publications (aaew.bbaw.de) | JSON; MdC in parts | usually CC BY-SA 4.0 |
| AES (simondschweitzer/aes) | per-word MdC / Unicode hieroglyphs | CC BY-SA 4.0 |
| St Andrews corpus (Nederhof; PhilologEg 0.5.14 jar) | RES with full layout | licence not stated |
| HieroJax texts (nederhof.github.io/hierojax/texts/) | Unicode with controls | repo GPL-3.0 |
| JSesh text library (rosmord/jsesh, jsesh-texts) | MdC with layout | CeCILL-C (code) |
| Ramses Online (Liège) | yes (82,531 hieroglyphic spellings) | no download, licence or API; agreement needed (Polis, slides, 21 Oct 2026) |

## 7. Pilot

- Text: BM EA 581, stela of Intef son of Senet. The BM record gives limestone, Abydos, early 12th Dyn., Senusret I.
- Encoding: HieroJax `texts/BritishMuseumEA581.html` (27 lines).
- Line direction: from the St Andrews RES. Lines 1–7 are hrl and lines 8–27 vrl.
- The RES → Unicode conversion with hieropy 0.1.10 was also run, as a cross-check (work dir only). Nederhof's own HieroJax Unicode is the version used; it differs in a few atomic or Extended-A signs.
