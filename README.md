# The 100 most-cited articles on non-invasive diagnosis and surveillance of bladder cancer — analysis code and derived data

**Author:** Alican Çatık · University of Health Sciences, Bakırköy Dr. Sadi Konuk Training and Research Hospital, İstanbul, Türkiye
**ORCID:** [0000-0002-0226-7804](https://orcid.org/0000-0002-0226-7804)
**Data source:** Web of Science Core Collection, SCI-EXPANDED only
**Search date:** 30 July 2026
**Version:** 1.0.0
**Licence:** code MIT · derived data CC BY 4.0

---

## 1. Contents

```
README.md               this file
CITATION.cff            citation metadata (read automatically by GitHub)
LICENSE                 MIT (code) and CC BY 4.0 (derived data)
kod/                    analysis scripts and script guide
veri/                   derived data
  DATA_DICTIONARY.md    field definitions, and what was removed and why
```

The directory names `kod/` (code) and `veri/` (data) are Turkish and are retained because
the scripts reference these paths. File contents and documentation are in English; inline
code comments and the manual screening rationales in `manual.py` remain in Turkish, as
they form part of the original audit trail.

## 2. Execution order

```
bib_parse.py  →  screen2.py  →  analiz.py  →  analiz2.py  →  sekiller.py
```

| Script | Purpose |
|---|---|
| `bib_parse.py` | Parses Web of Science `.bib` exports (**requires files downloaded with your own WoS access**, see §5) |
| `screen2.py` | Applies the inclusion/exclusion criteria on a rule basis |
| `manual.py` | Holds every manual decision (rank → decision + rationale). Corrects the false positives and false negatives of the rule-based engine |
| `thesaurus.py` | Synonym-merging table (`THESAURUS`) and generic terms excluded from networks (`GENERIC`). Shared as an open file by design |
| `analiz.py` | Keyword, country and author networks |
| `analiz2.py` | Co-citation network, self-citation rate, Kleinberg citation burst |
| `sekiller.py` | Twelve figures (300 dpi PNG) |
| `screen.py` | First-pass screening, used only to gauge eligibility density; **plays no role in the final sample** |

## 3. Software and versions

Analyses were run in a single Linux (Ubuntu 24) environment.

| | Version | Note |
|---|---|---|
| Python | 3.12.3 | |
| networkx | 3.6.1 | imported directly by the scripts |
| matplotlib | 3.10.8 | imported directly by the scripts |
| numpy | 2.4.4 | not imported directly; present as a matplotlib dependency |

**Scope note:** the code that writes the audit and sensitivity `.xlsx` tables is not
included in this package; those outputs were produced with unversioned helper code. Their
contents can be regenerated from the JSON files in `veri/`.

## 4. Locked parameters

The following were fixed throughout the study and never changed:

- **Layout:** Fruchterman–Reingold (spring), `seed = 42`, `k = 0.6`, `iterations = 200`
- **Clustering:** Clauset–Newman–Moore greedy modularity, edge-weighted
- **Kleinberg citation burst:** two-state automaton, `s = 2`, `gamma = 1`, Viterbi solution;
  terms lasting at least 3 years and appearing in at least 10 articles in total.
  **The base rate is proportional to the sample's annual article count** — a flat base rate
  produces bursts that are artefacts of the sample's year distribution.
- **Network thresholds:** keyword ≥ 4 articles · co-citation ≥ 6 articles ·
  country ≥ 3 articles · author ≥ 4 articles
- **Edge filtering in figures:** keyword network w ≥ 3, co-citation network w ≥ 4.
  This is for legibility only; **clustering and modularity were computed on the full
  networks.**
- **Sample ordering:** citations descending; ties broken in favour of the earlier
  publication year → `(-citations, year ascending)`
- **Country counting:** full counting (one credit per country in multi-address articles)

## 5. Raw data — not shareable

The raw Web of Science records are proprietary content of Clarivate and are **not
redistributed** in this archive. This is declared explicitly under the data-availability
item of the GLOBAL reporting guideline.

The following fields were **deliberately removed** from the derived data files: abstracts
(`Abstract`), Clarivate index terms (`Keywords-Plus`), reference strings
(`Cited-References`), raw and normalised address fields (`Affiliation`, `Affiliations`),
and Web of Science subject categories and research areas.

**To reproduce the study from scratch,** run the three queries as of 30 July 2026 under
your own institutional Web of Science subscription, download the top 5,000 full records
from Query 3 in descending citation order (Full Record + Cited References) as `.bib`
together with the citation reports as `.xlsx`, and start from `bib_parse.py`. Query strings
are given in Appendix 1 of the article. Citation counts will differ because the database is
continuously updated; the DOI lists in `veri/` let you identify exactly which records were
used.

**To continue from an intermediate step,** raw data is not required:
`veri/top100.json` and `veri/eligible252_identifiers.json` define the sample and the
eligible-record pool at identifier level.

### Reproducibility boundary — stated plainly

**Directly re-runnable with this package:** auditing the screening logic (`screen2.py` +
`manual.py` + `thesaurus.py` allow every record's decision to be traced), sample selection
and the tie-breaking rule, descriptive statistics, the sensitivity-test denominator, and
the overlap analysis.

**Not directly re-runnable:** the network analyses, co-citation, self-citation and
Kleinberg burst detection. These read the `Affiliation`, `Keywords-Plus` and
`Cited-References` fields in `analiz.py`, `analiz2.py` and `sekiller.py`; those fields are
proprietary and absent from this package. Regenerating `records_uygun252.json` with your
own Web of Science access makes these steps runnable. The required records are listed in
`veri/eligible252_identifiers.json`.

**Also:** the scripts contain hard-coded paths of the form `/home/claude/...`, which must
be updated before running in another environment (see `kod/README_kod.md`).

## 6. Known pitfalls

- The Web of Science `Address` field is the **publisher's** address. Country must be
  derived from the singular `Affiliation` field; using `Address` makes every Elsevier
  journal resolve to the Netherlands.
- The `Author` field is formatted "Surname, Firstname" while references use "Surname F".
  Self-citation matching uses `ref_surname()` in `analiz2.py`.
- BibTeX escaping: `\_` must be cleaned to `_` in DOIs.
- "Urothelial carcinoma-associated 1" (UCA1) is a gene name; studies of other organs
  carrying this name leak into the disease block and were removed manually.
- The rule-based screening engine cannot reach a record whose title contains no invasive
  term; the corresponding exclusion is hard-coded in `manual.py`.

## 7. Limitation

The screening engine's sensitivity is not 100%. Cross-checking against a reference set
independent of the sample revealed false negatives arising from gaps in the thesaurus. One
false negative detected above the citation threshold was added to the sample, and one
record left the sample under the tie-breaking rule. False negatives falling below the
threshold do not affect the sample. Details are given in the Limitations section of the
article.

## 8. Citing this package

Once the Zenodo DOI has been issued, the article's data- and code-availability statement
should cite the **Concept DOI**, which represents all versions, rather than a version DOI.
This keeps the citation valid even if the code is later corrected.

```
Çatık A. The 100 most-cited articles on non-invasive diagnosis and surveillance of
bladder cancer: analysis code and derived data. Version 1.0.0. Zenodo; 2026.
doi:[CONCEPT DOI]
```
