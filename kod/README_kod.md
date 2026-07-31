# Code — execution order

Required packages: `networkx` 3.6.1 · `matplotlib` 3.10.8 (Python 3.12.3).
`numpy` 2.4.4 is present as a matplotlib dependency but is not imported directly.

```
bib_parse.py  →  screen2.py  →  analiz.py  →  analiz2.py  →  sekiller.py
```

## Before running

The scripts contain hard-coded paths of the form `/home/claude/...`. Update them for your
environment, for example:

```bash
sed -i 's|/home/claude|/your/path|g' *.py
```

`bib_parse.py` expects the Web of Science `.bib` exports (`savedrecs*.bib`) and the
citation report `.xlsx` files in the working directory. **These files are not included in
this package**; they are proprietary Clarivate content and must be downloaded with your
own institutional access. See §5 of the top-level `README.md`.

## Files

| File | Role |
|---|---|
| `bib_parse.py` | Parses `.bib` exports, merges citation reports, writes `records.json` |
| `screen.py` | First-pass screening. Used only to gauge eligibility density; **no role in the final sample** |
| `screen2.py` | Final rule-based screening against the inclusion/exclusion criteria |
| `manual.py` | Every manual decision, as rank → decision + rationale. Corrects the rule engine's false positives and false negatives |
| `thesaurus.py` | `THESAURUS` synonym-merging table and `GENERIC` terms excluded from networks |
| `veri_yukle.py` | Rebuilds the ranked pool list from derived data |
| `analiz.py` | Keyword, country and author networks |
| `analiz2.py` | Co-citation network, self-citation rate, Kleinberg citation burst |
| `sekiller.py` | Twelve figures, 300 dpi PNG |

## Language note

Inline comments and the rationale strings in `manual.py` are written in Turkish. They form
part of the original screening audit trail and were deliberately left unchanged so that the
recorded decisions remain identical to those made during the study. All documentation and
all data field names are in English.

## Note on `veri_yukle.py`

This script was written to rebuild `records.json` from the pool index. It can no longer do
so from this package alone, because titles and journal names were removed from the pool
file for licensing reasons. Regenerate `records.json` from your own `.bib` exports using
`bib_parse.py` instead.
