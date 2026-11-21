# Shared standard for sub-lexical derivations — v1 (drafted by Syntax · Semantics · Interface; approved by Grant 2026-11-21 9:48 AM PT, "perfect (i think)" — revisable)

1. Nodes & labels: rooted ordered tree; node = operator label + arity + daughters. Labels: small-caps name + Unicode symbol (⿰ LR, ⿱ TB, ⿴ SURROUND, OVERLAY, INSERT). Leaves = glyph + 'gloss'. Bracket form is source of truth, e.g. [⿰ 木 [⿱ 日 一]]; figures generated from it. Arity fixed by operator; wrong daughter count fails the checker.
2. Heads: only in the function tree (semantic radical / determinative), marked _H (氵_H). Layout trees are headless.
3. Two layers: A layout (geometry: quadrat, IDS joins); B typed function (PHON, SEM, DET, COMPL roles; e.g. PHON(multiliteral)+COMPL → PHON; WORD+DET → WORD_closed). Linked by node ids n1, n2…; mismatches stated.
4. Order vs hierarchy: tree = hierarchy; order = named linearization functions over it (WALK_stroke, WALK_read). Walk classes (walk/reorder/return) are recorded exceptions to the default function, not built into the tree.
5. Reordering: (a) movement = two hierarchical positions, ⟨X⟩ … X with dashed arrow, only if Layer B argues for it; (b) linearization reorder = one position, walk out of order, marked on the walk: WALK_write ≠ WALK_read, label TRANSPOSE(honorific). Default (b).
6. Status labels: HYPOTHESIS on every tree; attested facts labelled with source; OPEN for unresolved; no CONJECTURE; Grant's ideas credited as GRANT'S HYPOTHESIS.
7. Not claimed: glyph trees are syntax / Merge / X-bar / θ; stroke or reading order is a psychological derivation; function tree = word morphology/semantics; the two levels are the same (any parallel goes in a "Parallel (for Grant to approve)" note).
8. Interlinking: glyph pages link to ESD / syntax-semantics-notes pages where they match; optional shared notation glossary (SSI offers to host).
