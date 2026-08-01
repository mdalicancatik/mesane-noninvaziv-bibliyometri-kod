# SUPPLEMENTARY FILE

**The 100 most-cited articles on non-invasive diagnosis and surveillance of bladder cancer
(2016–2025): a bibliometric analysis**

Alican Çatık, Mithat Ekşi, Serdar Karadağ, Alper Bitkin

Corresponding author: Alican Çatık · ORCID: 0000-0002-0226-7804

This document contains the full search strings, the inclusion and exclusion criteria, the screening
flow, the indicator definitions and formulas, the sensitivity test, additional descriptive results,
and the compliance tables for the three reporting guidelines. The analysis code and derived data are
available in an open archive: doi:10.5281/zenodo.21724781

**Contents.** A Search strings · B Inclusion and exclusion criteria · C Screening flow ·
D Indicator definitions and formulas · E Sensitivity of the search string · F Additional
descriptive results · G BIBLIO compliance · H RAMIBS compliance · I GLOBAL compliance

---

## APPENDIX A — SEARCH STRINGS

All three were run on the Web of Science Core Collection / SCI-EXPANDED on 30 July 2026.

**Query 1 — expanded technology block (6,811 records; for comparison only, not downloaded)**

```
TS=(("bladder cancer" OR "bladder carcinoma" OR "bladder tumor*" OR "bladder tumour*" OR "bladder neoplasm*" OR "urinary bladder neoplasm*" OR "urothelial carcinoma" OR "urothelial cancer" OR "urothelial neoplasm*" OR "urothelial tumor*" OR "urothelial tumour*" OR "transitional cell carcinoma" OR "non-muscle-invasive bladder" OR "non muscle invasive bladder" OR "muscle-invasive bladder" OR "NMIBC" OR "MIBC") AND ("noninvasive" OR "non-invasive" OR "urine cytology" OR "urinary cytology" OR "urinary biomarker*" OR "urine biomarker*" OR "urinary marker*" OR "urine marker*" OR "urinary test*" OR "voided urine" OR "urinary sediment" OR "urinary DNA" OR "liquid biopsy" OR "cell-free DNA" OR "circulating tumor DNA" OR "circulating tumour DNA" OR "ctDNA" OR "cfDNA" OR "circulating tumor cell*" OR "circulating tumour cell*" OR "microRNA" OR "miRNA" OR "exosom*" OR "extracellular vesicle*" OR "DNA methylation" OR "methylation marker*" OR "telomerase" OR "TERT promoter" OR "survivin" OR "metabolomic*" OR "proteomic*" OR "FISH" OR "UroVysion" OR "NMP22" OR "BladderChek" OR "BTA stat" OR "BTA TRAK" OR "ImmunoCyt" OR "uCyt" OR "Cxbladder" OR "UroSEEK" OR "EpiCheck" OR "AssureMDx" OR "ADXBLADDER" OR "Uromonitor" OR "UroMark" OR "PENK" OR "Xpert bladder" OR "MRI" OR "magnetic resonance imaging" OR "multiparametric MRI" OR "mpMRI" OR "VI-RADS" OR "vesical imaging" OR "diffusion-weighted" OR "CT urography" OR "computed tomography urography" OR "ultrasonography" OR "radiomic*" OR "deep learning" OR "machine learning" OR "artificial intelligence" OR "convolutional neural network*" OR "neural network*" OR "computer-aided detection" OR "computer-aided diagnosis" OR "vision transformer" OR "large language model*" OR "ChatGPT" OR "GPT-4" OR "GPT-3" OR "foundation model*" OR "generative artificial intelligence" OR "biosensor*" OR "electronic nose" OR "volatile organic compound*" OR "Raman spectroscopy")) AND DT=(Article OR Review) AND PY=(2016-2025)
```

**Query 2 — narrow technology block (5,785 records; for comparison only, not downloaded)**

```
TS=(("bladder cancer" OR "urothelial carcinoma" OR "urothelial cancer" OR "bladder carcinoma" OR "urinary bladder neoplasm*" OR "non-muscle-invasive bladder" OR "muscle-invasive bladder") AND ("noninvasive" OR "non-invasive" OR "urine cytology" OR "urinary cytology" OR "urinary biomarker*" OR "urine biomarker*" OR "liquid biopsy" OR "cell-free DNA" OR "circulating tumor DNA" OR "ctDNA" OR "cfDNA" OR "microRNA" OR "miRNA" OR "exosom*" OR "extracellular vesicle*" OR "DNA methylation" OR "methylation marker*" OR "FISH" OR "UroVysion" OR "NMP22" OR "BTA stat" OR "telomerase" OR "TERT promoter" OR "Cxbladder" OR "UroSEEK" OR "EpiCheck" OR "AssureMDx" OR "PENK" OR "Xpert bladder" OR "urinary DNA" OR "voided urine" OR "MRI" OR "magnetic resonance imaging" OR "multiparametric MRI" OR "mpMRI" OR "VI-RADS" OR "vesical imaging" OR "radiomic*" OR "deep learning" OR "machine learning" OR "artificial intelligence")) AND DT=(Article OR Review) AND PY=(2016-2025)
```

**Query 3 — disease block (32,690 records; primary data source, top 5,000 full records downloaded
by descending citation count)**

```
TS=("bladder cancer" OR "bladder carcinoma" OR "bladder tumor*" OR "bladder tumour*" OR "bladder neoplasm*" OR "urinary bladder neoplasm*" OR "urothelial carcinoma" OR "urothelial cancer" OR "urothelial neoplasm*" OR "urothelial tumor*" OR "urothelial tumour*" OR "transitional cell carcinoma" OR "non-muscle-invasive bladder" OR "non muscle invasive bladder" OR "muscle-invasive bladder" OR "NMIBC" OR "MIBC") AND DT=(Article OR Review) AND PY=(2016-2025)
```

---

## APPENDIX B — INCLUSION AND EXCLUSION CRITERIA

**All of the following were required for inclusion:** the subject being bladder or bladder-derived
urothelial carcinoma; a non-invasive diagnostic, screening, staging or surveillance technology being
the focus (urine cytology; urine-based protein, DNA, RNA, methylation or vesicle markers; commercial
urine tests; blood-based liquid biopsy; cross-sectional imaging; radiomics and artificial
intelligence methods applied to these; systematic reviews and meta-analyses evaluating the
diagnostic accuracy of these methods).

**Excluded were:** records concerning other cancers or diseases, or in which the bladder was
incidental; mechanism and tumour-biology studies; treatment, surgery, drug development and
radiotherapy studies; tissue- and histopathology-based studies (immunohistochemistry, whole slide
imaging, tissue genomics); invasive and endoscopic methods; studies confined to upper urinary tract
urothelial carcinoma; clinical guidelines and general disease reviews; studies with mixed cohorts or
covering several cancer types together.

### Screening procedure

The criteria above were applied through the following ordered procedure. Each record was assessed
against the steps in sequence and assigned at the first step that matched.

| Step | Condition (evaluated on the title unless stated) | Outcome |
|:--:|---|---|
| 1 | Minimal residual disease terms present (ctDNA/MRD exception) | **Include** |
| 2 | No bladder or urothelial term | Exclude |
| 3 | Upper urinary tract terms only, no bladder term | Exclude |
| 4 | Tissue or histopathology terms | Exclude |
| 5 | Invasive or endoscopic method terms | Exclude |
| 6 | No non-invasive technology term | Exclude, unless the abstract carries both a technology term and a strong diagnostic term → **Borderline** |
| 7 | Mechanism or tumour-biology terms | Exclude |
| 8 | Treatment terms | Exclude |
| 9 | No diagnostic framing term in title or abstract | **Borderline** |
| 10 | General review terms (e.g. "advances in", "overview of") | Exclude |
| 11 | Otherwise | **Include** |

The term lists used at each step are given in full in `kod/screen2.py` and `kod/thesaurus.py` in
the open archive. **The authoritative record of the outcome is the `verdict` field in
`veri/pool5000_screening.json`**, which gives the decision for every one of the 5,000 records; the
table above documents the procedure that produced it and reproduces approximately 99.7% of the
automatic decisions when re-applied to the computed signals. The residual discrepancy reflects
refinements made during screening that were not captured as a single rule; where the procedure and
the recorded verdict differ, the recorded verdict governs.

**Borderline records.** The procedure marked 112 records as borderline. Sixty-four of these were
read at full-text level and adjudicated by discussion among three authors (34 included, 29
excluded, 1 held for further checking); their decisions and rationales are in `kod/manual.py`. The
remaining 48 were not adjudicated and were treated as not meeting the criteria. **All 48 fall
between 55 and 36 citations, below the sample's lower bound of 63**, so none of them could have
entered the sample regardless of how they were resolved; they are identifiable in
`veri/pool5000_screening.json` by the verdict label. They are counted within the 4,748 records not
meeting the criteria in Appendix C.

**Restricted application of the invasive-method exclusion.** Almost every study measuring the
diagnostic accuracy of a non-invasive test uses cystoscopy or transurethral resection as the
reference standard; applied literally, the exclusion removed the most central studies in the field.
The rule was therefore applied only where an invasive method was the subject of the study itself,
and mention as a comparator was not treated as grounds for exclusion.

**Deliberate inclusions.** Artificial-intelligence segmentation studies built on imaging were
included. Treatment trials using circulating tumour DNA as a marker of minimal residual disease were
included manually despite being treatment studies; what is evaluated in these studies is not
treatment efficacy but the decision-making power of a non-invasive marker.

**Category assignment.** Articles were assigned to five technology categories according to their
principal technological contribution. Where the contribution was a platform innovation (biosensor,
microfluidic system, spectroscopic method), the study was assigned to the biosensor category; where
it was a computational model, to radiomics and artificial intelligence; and where it was an imaging
protocol, to cross-sectional imaging. Eight studies using urine and blood matrices together were
classified according to the dominant sample type.

**Data cleaning.** No duplicate records were found among the 5,000 downloaded records. Field
completeness was: references 99.9%, abstracts 99.6%, DOI 98.7%. In the keyword analysis, synonymous
terms were merged through an explicit thesaurus file, and general terms present in nearly every
record by definition of the corpus (for example "cancer", "carcinoma", "expression") were removed
from the network; both lists are shared in the open archive. One source of contamination was removed
manually: "urothelial carcinoma-associated 1" (UCA1) is a long non-coding RNA, and studies of other
organ cancers bearing this name leak into the disease block.

---

## APPENDIX C — SCREENING FLOW

| Stage | n |
|---|---|
| Corpus retrieved by the disease-block query | 32,690 |
| Pool downloaded in descending citation order | 5,000 |
| — citation range | 4,376 – 35 |
| **Not meeting criteria** | **4,748** |
| — no non-invasive diagnostic technology focus | 1,957 |
| — subject not bladder cancer, or bladder incidental | 896 |
| — treatment, surgery, drug development or radiotherapy | 852 |
| — mechanism and tumour biology | 725 |
| — clinical guideline or general disease review | 140 |
| — invasive or endoscopic method as the subject of the study | 84 |
| — tissue- or histopathology-based | 45 |
| — retracted publication or expression of concern | 37 |
| — upper urinary tract urothelial carcinoma only | 12 |
| **Meeting criteria** | **252** |
| Not among the top 100 by citation count | 152 |
| **Sample** | **100** |
| — citation range | 551 – 63 |

**Notes.** Because the document-type criterion was applied at query level, all records in the pool
are research articles or reviews; no record was excluded on this ground. A record may meet more than
one exclusion criterion simultaneously; so that the total corresponds to 4,748, each record was
assessed in the order given above and assigned to the **first** criterion it met. Row values
therefore indicate the number of records excluded on that ground, not the number meeting that
criterion. The inclusion and exclusion decisions themselves are independent of this ordering.

Of the 4,748 records not meeting the criteria, 4,699 were excluded by the screening procedure, 48
were marked borderline but not adjudicated, and 1 was held for further checking. The 48
unadjudicated records all fall below the sample's citation threshold and could not have entered the
sample (see Appendix B).

Sixty-four borderline records were assessed at full-text level and decided by discussion among three
authors (34 included, 29 excluded, 1 further check). All of these decisions appear in the
`manual.py` file in the open archive as rank, decision and rationale.

---

## APPENDIX D — INDICATOR DEFINITIONS AND FORMULAS

**h-index.** When the articles in the sample are ranked by descending citation count, the largest
value *h* for which *h* articles have each received at least *h* citations.

**Network density.** The ratio of edges present in an undirected network to the maximum possible:
*d* = 2*E* / [*N*(*N* − 1)], where *N* is the number of nodes and *E* the number of edges.

**Modularity (Q).** Edge-weighted Newman modularity was used:

> *Q* = (1 / 2*m*) · Σ<sub>ij</sub> [ *A*<sub>ij</sub> − (*k*<sub>i</sub> *k*<sub>j</sub>) / 2*m* ] · δ(*c*<sub>i</sub>, *c*<sub>j</sub>)

where *A*<sub>ij</sub> is the edge weight between nodes *i* and *j*,
*k*<sub>i</sub> = Σ<sub>j</sub> *A*<sub>ij</sub> is the weighted degree,
*m* = ½ Σ<sub>ij</sub> *A*<sub>ij</sub> the total weight, and δ(*c*<sub>i</sub>, *c*<sub>j</sub>) an
indicator taking the value 1 if two nodes belong to the same community and 0 otherwise. Communities
were identified using the Clauset–Newman–Moore greedy modularity method.

**Kleinberg citation burst.** Annual occurrence counts for each term were modelled with a two-state
automaton. State 0 represents the base rate and state 1 represents *s* times the base rate (*s* = 2).
For *k* occurrences observed in a given year under an expected rate λ, the Poisson negative
log-likelihood is

> *nll*(*k*, λ) = λ − *k* · ln λ + ln(*k*!)

The total cost of a state sequence is the sum of the annual negative log-likelihoods plus a penalty
γ (γ = 1) for each transition from the base state to the burst state; downward transitions are not
penalised. The cost-minimising sequence is found by the Viterbi algorithm. **The expected base count
is proportional to the sample's annual article count**; with a base rate constant across years, the
year distribution of a citation-thresholded sample causes most terms to produce spurious bursts in
the early years. Only terms appearing in at least 10 articles and bursting for at least three years
were considered.

**Collaboration type.** Each article was classified from the sets of countries and institutions
derived from author addresses: *international* where more than one country is present; *national*
where one country but more than one institution; *local* where a single institution and more than
one author; *single-authored* where one author.

**H5 index.** The number of articles receiving at least five citations each within a given five-year
window. In a citation-thresholded sample this equals the number of articles in the window and
carries no discriminating information; it was therefore not reported.

**Locked parameters.** Layout: Fruchterman–Reingold, seed = 42, k = 0.6, iterations = 200. Network
thresholds: keyword ≥ 4 articles, co-citation ≥ 6, country ≥ 3, author ≥ 4. Edge filtering in
figures: keyword network w ≥ 3, co-citation network w ≥ 4 — for legibility only; clustering and
modularity were computed on the full networks. Sample ordering: (−citations, year ascending).
Country counting: full counting.

**Indicators deliberately not used.** Journal impact factor and quartile were not used; these are
defined at journal level and invite misleading inferences about individual articles.

---

## APPENDIX E — SENSITIVITY OF THE SEARCH STRING

Sensitivity was measured against a set of 148 unique references with DOIs published between 2016 and
2025, extracted from the reference lists of five reviews and frozen before the sample was drawn.
Seven of these references were not found in Web of Science/SCI-EXPANDED and five did not meet the
document-type criterion; the corrected denominator is 136 (Figure S6).

| Query | Retrieved | /148 | /141 | /136 |
|---|---|---|---|---|
| Query 2 (narrow) | 86 | 58.1% | 61.0% | 63.2% |
| Query 1 (expanded) | 89 | 60.1% | 63.1% | 65.4% |
| Query 3 (disease block) | 119 | 80.4% | 84.4% | 87.5% |

Raw sensitivity differences are misleading on their own, because a large part of the denominator
consists of guideline, epidemiology and treatment references whose non-retrieval is correct. Of the
52 records missed by Query 1, 43 are out of scope and 3 are on topic but do not meet the
document-type criterion. The remaining **five records were on topic and retrievable yet were
missed**, and in all five cases the cause was a gap in the term list: targeted deep sequencing, the
term "epigenetic", cell-free RNA ("cell-free DNA" is in the list, "cell-free RNA" is not),
hyaluronic-acid-based markers, and the expression "urine-based".

This demonstrates a structural limit of the term-based search approach: no reasonable term list can
anticipate the diversity with which a field names itself. This is the rationale for selecting Query
3, which contains no technology terms, as the primary data source.

**Overlap analysis.** To test the effect of the term list directly, an independent top-100 sample was
constructed with the same criteria from a parallel search using only disease terms, and the two
samples were compared. The overlap is 98%. Two of the four divergent records were retrieved only by
the term-free search, owing to vocabulary absent from the technology term list ("microbiota", "PET").
The overlap analysis and the sensitivity test arrive at the same conclusion by independent routes.

**Residual error.** Cross-checking also revealed false negatives arising from gaps in the study's own term lists.
One false negative above the citation threshold (a study on urinary microbiota, 84 citations) was
added to the sample, and one record left the sample under the tie-breaking rule. Two further false
negatives below the threshold do not affect the sample.

---

## APPENDIX F — ADDITIONAL DESCRIPTIVE RESULTS

**Publication years.** The distribution from 2016 to 2025 is 13, 17, 21, 22, 13, 8, 2, 2, 1 and 1
respectively (Figure S1). The concentration in earlier years is a consequence of the
citation-accumulation window.

**Citation distribution.** Mean 114.5, median 85, standard deviation 85.9; first and third quartiles
69.0 and 119.8, interquartile range 50.8; Fisher–Pearson adjusted skewness 3.42 (Figure S2).

**Countries.** Under full counting: United States 41, China 25, Italy 19, United Kingdom 17,
Netherlands 15, Japan 14, Spain 12, Germany 11, France 9, Canada 8 (Figure S3). The country network
comprises 19 nodes and 147 edges, with density 0.860 and modularity 0.041; at these values there is
no meaningful community structure and no cluster interpretation was made.

**Institutions.** Sapienza University of Rome 11, Sun Yat-sen University 11, Harvard University 7,
University of London 7, Radboud University Nijmegen 7, University of Texas System 7.

**Collaboration.** 49 international, 36 national, 15 local; no single-authored studies (Figure S4).

**Authors.** Panebianco V 9 articles, Liu Y 6, Lu H 6, Zhang X 6, Xu X 6, Witjes JA 5, Catto JWF 5.
The co-authorship network comprises 23 nodes and 60 edges, with modularity 0.523 and density 0.237
(Figure S5); modularity is high and the cluster structure is interpretable, indicating six research
groups working largely independently.

**Review articles.** Twenty-three of the sample are reviews and 77 research articles. Reviews
received 2,454 citations, 21.4% of the total; mean citations were 106.7 per review and 116.8 per
research article, so reviews hold no citation advantage. Their distribution across categories differs
from the sample as a whole: 12 urine-based molecular, 9 cross-sectional imaging, 1 blood-based liquid
biopsy, 1 radiomics/artificial intelligence. **There are no reviews in the biosensor and
nanotechnology category**; all six studies there are primary research. If review production is taken
as an indicator of maturation, this suggests the biosensor line has not yet reached the stage of
consolidating assessment. The most-cited review is the consensus study defining VI-RADS (526
citations), followed by two reviews of urinary biomarkers (183 and 127) and a meta-analysis of
VI-RADS diagnostic performance (140).

**Robustness of the modularity finding.** The keyword network was rebuilt on three progressively
wider datasets, with thresholds scaled in proportion to dataset size:

| Dataset | Nodes | Edges | Clusters | Q | Density |
|---|---|---|---|---|---|
| Sample (n = 100) | 35 | 271 | 3 | 0.166 | 0.455 |
| Eligible records (n = 252) | 32 | 314 | 2 | 0.108 | 0.633 |
| Entire pool (n = 5,000) | 24 | 265 | 3 | 0.134 | 0.960 |

Modularity remains in the range 0.11–0.17 at all three scales, so weak cluster separation is not an
artefact of the citation-thresholded sampling design.

---

## APPENDIX G — BIBLIO COMPLIANCE TABLE (20 items)

The table below shows where each of the 20 items of the BIBLIO guideline⁵ — developed for
bibliometric reviews of the biomedical literature and registered with the EQUATOR Network — is
addressed in this article. Item wording is condensed from the original checklist.

| Section | No | Checklist item | Where addressed | Status |
|---|:--:|---|---|---|
| Title | 1 | Identify the report as a bibliometric review in the title | Title | Met |
| Title | 2 | Indicate the key issues/topics and coverage of time period | Title (2016–2025) | Met |
| Abstract | 3 | Structured summary: background, methods, results, conclusions | Abstract | Met |
| Introduction | 4 | Present review of existing knowledge and epidemiological information | Introduction | Met |
| Introduction | 5 | Statement of the objective(s) or question(s) | Introduction, final paragraphs | Met |
| Methods | 6 | Describe all information sources | Methods | Met |
| Methods | 7 | Keywords and systematisation criteria (date of search, language, document type) | Methods; Appendix C | Met |
| Methods | 8 | The period the review covers and its justification | Methods | Met |
| Methods | 9 | Inclusion and exclusion criteria; study design, publication type, time period | Methods | Met |
| Methods | 10 | Data refinement; removal of duplicate and unrelated articles | Methods, Methods; Appendix C | Met |
| Methods | 11 | *(Optional)* Assessment of papers by three authors | Methods | **Met** — the 64 borderline records were decided by discussion among three authors |
| Methods | 12 | Methods used for summarising, synthesis, tabulation and analysis | Methods | Met |
| Results | 13 | Flow diagram of search and selection; descriptive counts | Results; Appendix C | Met |
| Results | 14 | Schematic maps and trends presented using appropriate software | Figures 7–10 | Met |
| Results | 15 | Tabulation of findings; historical view; separate reporting of review papers | Introduction (historical view); Appendix F (reviews) | Met |
| Results | 16 | Synthesis of findings; identification of the gap; proposal of a model or hypothesis | Results, Discussion | Met |
| Discussion | 17 | Summarise main findings in general, accessible terms | Discussion, opening paragraph | Met |
| Discussion | 18 | Interpretation consistent with results; explanation of observed patterns | Discussion | Met |
| Discussion | 19 | Discuss strengths and limitations | Limitations | Met |
| Discussion | 20 | General interpretation with respect to review questions and implications | Conclusion | Met |

Nineteen of the 20 items are fully met and one is partially met. Item 11, which is marked as
optional in the assessment by three authors; in this study the records were
assessed independently by two.

*Source: Montazeri A et al. Syst Rev. 2023;12:239 (CC BY 4.0).*

---

## APPENDIX H — RAMIBS COMPLIANCE TABLE (12 items)

The table below shows where each of the 12 items of the RAMIBS guideline⁶ — developed for
bibliometric and scientometric studies in the health sciences — is addressed in this article. Item
wording is condensed from the original checklist.

| No | Recommendation | Where addressed | Status |
|:--:|---|---|---|
| 1 | Descriptive title emphasising the bibliometric approach; structured abstract | Title; Abstract | Met |
| 2 | Identification of prior studies, statement of how this study differs, research question and aim | Introduction | Met |
| 3 | Justification of single-database choice; criteria; time frame; date of data collection; definition of indicators | Methods, Methods, Methods, Methods | Met |
| 4 | Construction of the search string; sources of terms; appropriate use of Boolean operators and truncation | Methods; Appendix C | Met |
| 5 | Date of the final search; exclusion of the current year; justification of document-type and language limits | Methods, Methods | Met |
| 6 | Four indicator dimensions: production, impact, collaboration and alternative (altmetric) indicators | Production: Results–3.2, Figures 1–2 · Impact: Results, Results · Collaboration: Results | **Partially met** — altmetric indicators are absent from the Web of Science export and could not be assessed |
| 7 | Reporting of macro (country), meso (institution) and micro (author) levels of analysis | Macro: Results · Meso: Results · Micro: Results | Met — gender analysis at micro level was not performed owing to the error rate of name-based assignment |
| 8 | Predefined extraction matrix; justification of analytical techniques | Methods, Methods | Met |
| 9 | Name and version of all software used; visualisation parameters; term normalisation | Methods, Methods | Met |
| 10 | Presentation of the full data matrix as a supplement; number of excluded records and reasons | Open archive (Zenodo); Appendix C | Met |
| 11 | Correspondence of results with the aim; comparison with other bibliometric studies; limitations; recommendations | Discussion, Discussion, Limitations | Met |
| 12 | Summary of the main findings | Conclusion | Met |

Eleven of the 12 items are fully met and one partially.

*Source: Mayta-Tovalino F et al. J Int Oral Health. 2024;16(3):253–6 (CC BY-NC-SA 4.0).*

---

## APPENDIX I — GLOBAL COMPLIANCE TABLE (29 items)

The table below shows where each of the 29 items of the GLOBAL guideline⁴ for reporting
bibliometric analyses is addressed in this article.

> **Note on the number of items.** This table follows the 29-item final list given in the
> published Delphi study. The guideline's Explanation and Elaboration document (preprint) presents
> the same items under 28 headings, merging the two items on data availability and on the sharing
> of materials, data and code. The two items are kept separate here, because the impossibility of
> sharing the raw data and the sharing of the code are distinct situations that require separate
> reporting.

| Section | No | Item | Where addressed |
|---|:--:|---|---|
| Abstract | 1.1 | Abstract reflective of the bibliometric analysis | Abstract |
| Introduction | 2.1 | Situate the study within its context | Introduction |
| Introduction | 2.2 | Rationale and knowledge gap | Introduction |
| Introduction | 2.3 | Research question | Introduction, final paragraph |
| Introduction | 2.4 | Definition of terms, concepts and theoretical frameworks | Methods — the absence of a theoretical framework is stated explicitly |
| Methods | 3.1 | Bibliometric methods used | Methods, Methods |
| Methods | 3.2 | Units of analysis | Methods, Methods |
| Methods | 3.3 | Method of data collection | Methods, Methods |
| Methods | 3.4 | Databases and data sources | Methods |
| Methods | 3.5 | Search strategy | Methods; Supplementary File (full strings) |
| Methods | 3.6 | Time frame | Methods |
| Methods | 3.7 | Search results and selection process | Results; Appendix C |
| Methods | 3.8 | Data cleaning | Methods |
| Methods | 3.9 | Data analysis | Methods |
| Methods | 3.10 | Analytical software and versions | Methods |
| Methods | 3.11 | Indicators used | Methods, Methods |
| Methods | 3.12 | Calculations and formulas | Methods, Appendix D |
| Methods | 3.13 | Replicability and transparency | Methods; Declarations (open code archive) |
| Results | 4.1 | Results of the study | Results |
| Results | 4.2 | Results of the techniques used | Results–Results |
| Results | 4.3 | Tables and graphs should not mislead | Every network figure carries a note that inter-node distances are a product of the layout algorithm and should not be interpreted |
| Results | 4.4 | Measures of dispersion and uncertainty | Results (standard deviation, interquartile range, skewness) |
| Discussion | 5.1 | Discussion of the results | Discussion |
| Discussion | 5.2 | Situating the results in the literature | Discussion |
| Discussion | 5.3 | Strengths and limitations | Limitations |
| Other | 6.1 | Conflict of interest and support statement | Declarations |
| Other | 6.2 | Availability of the data | Declarations — the proprietary status of the raw Web of Science data and the resulting impossibility of sharing it are stated explicitly |
| Other | 6.3 | Use of references to support statements and methods; citation of software and datasets | References (19–21: Clauset, Hirsch, Kleinberg); Methods (software versions) |
| Other | 6.4 | Statement on the sharing of materials, data and code | Declarations — code and derived-data archive with a persistent identifier |

All 29 items are met.

> GLOBAL is not a quality assessment tool; this table indicates the completeness of reporting, not
> the quality of the study.

*Source: Ng JY et al. ISSI 2025 Proceedings, pp. 837–861.*
