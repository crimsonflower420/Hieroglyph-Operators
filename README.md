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
| `tools/build_pages.py` | Builds the five pages from the census data and the JA/EN texts |
| `data/ea581-lines.json` | BM EA 581, Unicode encoding by M.-J. Nederhof (HieroJax, GPL-3.0), with line direction from his RES encoding |
| `data/kanji-arity-reference.json` | Kanji arity census numbers, pinned to Kanji-Morphology 3e3ba46 and KanjiVG 70a0b7ae |
| `notes/` | Research notes with sources |

## Build and deploy

```sh
python3 tools/quadrat_census.py
python3 tools/build_pages.py
WRANGLER_CACHE_DIR=/tmp/wrangler-cache npx wrangler pages deploy site --project-name hieroglyph-operators --branch main --commit-hash "$(git rev-parse HEAD)"
```

## Licences

- Code and the site's own text: CC BY-SA 4.0 for text, MIT for code, unless a file says otherwise.
- `data/ea581-lines.json` comes from HieroJax and stays under GPL-3.0.
- `site/fonts/`: Noto Sans Egyptian Hieroglyphs v2.002, SIL OFL 1.1 (see `site/fonts/OFL.txt`).
- Kanji numbers come from Kanji in Order (KanjiVG, CC BY-SA 3.0).
