# Hieroglyph Operators · ヒエログリフの演算子

Live site: https://hieroglyph-operators.pages.dev

## Mandate

This repository holds a research-notes website that reads Egyptian hieroglyphs through the operator lens of its sister site, [Kanji in Order / 順序の漢字](https://kanji-morphology.pages.dev) ([repo](https://github.com/crimsonflower420/Kanji-Morphology)).

- A **quadrat** is written as an operator tree. The operators are the Unicode Egyptian format controls (vertical joiner U+13430, horizontal joiner U+13431, insertions, overlay) and their Manuel de Codage counterparts (`:`, `*`, `&`, `#`). The arguments are signs, named by Gardiner number.
- The site says what carries over from kanji and what does not. There is no canonical stroke order. Reading direction varies. Quadrats are layout units, not words.
- Glyphs are not syntax. The site makes no Merge, X-bar, θ-role or joint-field claims. Inference and speculation are labelled. Citations and data are never invented.
- Japanese is written first in である調, and the English is fitted to it. Every page has a JA/EN toggle and a Light/Auto/Dark toggle. The header is compact (about 100px) and not sticky.
- The site stands on its own. Other writing systems will get their own sites later.

## Layout

| Path | What |
|---|---|
| `site/` | Static site deployed to Cloudflare Pages (project `hieroglyph-operators`) |
| `site/js/quadrat.js` | Unicode quadrat parser and schematic SVG layout. Noto has no quadrat shaping. |
| `tools/quadrat_census.py` | Parses the pilot text into operator trees and writes `data/pilot-census.json` and `site/js/pilot-data.js` |
| `tools/build_pages.py` | Builds the static pages from the census data and the JA/EN texts |
| `data/ea581-lines.json` | BM EA 581, Unicode encoding by M.-J. Nederhof (HieroJax, GPL-3.0), with line direction from his RES encoding |
| `tools/kanji_heights.py` | Per-character tree height of the 2,136 jōyō kanji from the pinned KanjiVG snapshot, using the Kanji-Morphology composition rule (needs that repo checked out); writes `data/kanji-height-reference.json` |
| `tools/depth_compare.py` | Layout height vs function height for the Rahman derivations, with EA 581 and kanji beside them; writes `data/depth-compare.json` (page `depth`) |
| `tools/second_text.py` | Horizontal-join share by line orientation on EA 581, 614, 567, 162 and 101 (HieroJax, pinned commit); `--fetch` rebuilds `data/second-text-lines.json`; writes `data/second-text.json` (page `second-text`) |
| `tools/quadrat_word_align.py` | Aligns TLA word division (via AES, CC BY-SA 4.0) with Nederhof's quadrats for EA 581 and EA 162; `--fetch` rebuilds `data/ea581-tla-words.json`, `data/ea162-tla-words.json`, `data/ea162-lines.json` from pinned commits; writes `data/quadrat-word.json` (page `boundaries`) |
| `data/kanji-arity-reference.json` | Kanji arity census numbers, pinned to Kanji-Morphology 3e3ba46 and KanjiVG 70a0b7ae |
| `notes/` | Research notes with sources |

## Build and deploy

```sh
python3 tools/quadrat_census.py
# optional, needs crimsonflower420/Kanji-Morphology checked out:
# python3 tools/kanji_heights.py --kanji-repo /path/to/Kanji-Morphology
python3 tools/depth_compare.py
python3 tools/quadrat_word_align.py   # add --fetch to rebuild its inputs
python3 tools/second_text.py         # add --fetch to rebuild data/second-text-lines.json
python3 tools/build_pages.py
WRANGLER_CACHE_DIR=/tmp/wrangler-cache npx wrangler pages deploy site --project-name hieroglyph-operators --branch main --commit-hash "$(git rev-parse HEAD)"
```

## Licences

- Code and the site's own text: CC BY-SA 4.0 for text, MIT for code, unless a file says otherwise.
- `data/ea581-lines.json` and `data/ea162-lines.json` come from HieroJax and stay under GPL-3.0.
- `data/ea581-tla-words.json` and `data/ea162-tla-words.json` are extracts of Thesaurus Linguae Aegyptiae texts via AES (S. D. Schweitzer) and stay under CC BY-SA 4.0.
- `site/fonts/`: Noto Sans Egyptian Hieroglyphs v2.002, SIL OFL 1.1 (see `site/fonts/OFL.txt`).
- Kanji numbers come from Kanji in Order (KanjiVG, CC BY-SA 3.0).

## Two-layer derivations (notation v1)

Sign combinations are written as two linked trees in the shared standard
`notes/SUBLEXICAL-DERIVATIONS-v1.md` (drafted with Syntax · Semantics · Interface; approved by Grant Golland, 2026-11-21):
layer A is the layout (quadrat, headless), layer B the typed sign function (complements, determinatives as heads, endings).

- `data/derivations/rahman.drv` holds the bracket source of truth: 26 derivations from Md. Ridwanur Rahman's
  *Ancient Egyptian Hieroglyph as the Pictorial Scrutiny of Modern Linguistics*.
- `python3 tools/derivations.py` checks arity, shared leaf ids, heads, walks and reorder labels, and reports layer
  mismatches. It exits non-zero on any error and writes `rahman.json` beside the source.
- `notes/rahman-map.md` maps the book's chapters and claims, with page numbers. Speculative parts are flagged and left underived.
- Pages: `derivations` (the formalism), `notation` (the standard), `rahman` (book claims vs derivations).
