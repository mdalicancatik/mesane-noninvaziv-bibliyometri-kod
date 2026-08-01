"""Screening procedure — executable form of the ordered rule set in Appendix B.

`screen2.py` computes 15 inclusion and exclusion signals per record but assigns no
decision. This module contains the rule that turns those signals into a decision, so
that the procedure printed in Appendix B of the supplementary file and the procedure
actually applied are the same object.

Input: a record dict carrying the signal fields written by `screen2.py`
       (bladder_t, tech_t/a, diag_s_t/a, diag_w_t, mech_t/a, treat_t/a,
        tissue_t/a, invas_t, general_t, mrd).

Output: (verdict, step) where verdict is "IN", "OUT" or "SINIR" (borderline) and
        step is the number of the rule that fired. The step number doubles as the
        exclusion reason: the counts in Appendix C are the tally of these steps.

Records returned as "SINIR" are not decided here. Those read at full-text level are
in `manual.py`; the rest remain undecided and are counted as not meeting the criteria.

Authoritative record: the `verdict` field of `veri/pool5000_screening.json`. Where
this module and the recorded verdict differ, the recorded verdict governs.
"""

# Adım numarası -> Ek B ve Ek C'de görünen etiket
ADIMLAR = {
    1:  "minimal residual disease exception",
    2:  "no bladder or urothelial term",
    3:  "upper urinary tract urothelial carcinoma only",
    4:  "tissue- or histopathology-based",
    5:  "invasive or endoscopic method as the subject of the study",
    6:  "no non-invasive diagnostic technology focus",
    7:  "mechanism and tumour biology",
    8:  "treatment, surgery, drug development or radiotherapy",
    9:  "no diagnostic framing",
    10: "clinical guideline or general disease review",
    11: "otherwise",
}


def karar(r):
    """Apply the ordered procedure to one record's signals."""
    var = lambda k: bool(r.get(k))

    # 1 — ctDNA/MRD istisnası tedavi dışlamasının önünde gelir
    if var("mrd"):
        return "IN", 1

    # 2 — başlıkta mesane/ürotelyal terim yok
    if not var("bladder_t"):
        return "OUT", 2

    # 3 — yalnızca üst üriner sistem. screen2.py bunun için ayrı bir sinyal
    #     alanı yazmaz; bu adım tam kayıt düzeyinde uygulanmıştır ve burada
    #     yeniden üretilemez (bkz. README §5).

    # 4-5 — doku temelli ve invaziv yöntem konulu çalışmalar
    if var("tissue_t"):
        return "OUT", 4
    if var("invas_t"):
        return "OUT", 5

    # 6 — başlıkta teknoloji terimi yok. Öz hem teknoloji hem güçlü tanısal
    #     terim taşıyorsa karar verilmez, sınıra düşer.
    if not var("tech_t"):
        if var("tech_a") and var("diag_s_a"):
            return "SINIR", 6
        return "OUT", 6

    # 7 — mekanizma / tümör biyolojisi
    if var("mech_t"):
        return "OUT", 7

    # 8 — tedavi. Başlıkta güçlü tanısal çerçeveleme varsa dışlama uygulanmaz:
    #     "Early Detection ... and Monitoring of Therapeutic Efficacy" gibi
    #     başlıklarda tedavi terimi geçer ama çalışma tanısaldır.
    if var("treat_t") and not var("diag_s_t"):
        return "OUT", 8

    # 10 — genel derleme kalıbı ("overview of", "advances in"). Tanısal
    #      çerçeveleme varsa uygulanmaz: "Overview of VI-RADS in Bladder
    #      Cancer" belirli bir teknolojinin evreleme derlemesidir.
    if var("general_t") and not (var("diag_s_t") or var("diag_s_a")):
        return "OUT", 10

    # 9 — hiçbir tanısal çerçeveleme terimi yok: sınır
    if not (var("diag_s_t") or var("diag_s_a") or var("diag_w_t")):
        return "SINIR", 9

    # 11 — kalanlar dahil
    return "IN", 11


def gerekce(r):
    """Return the exclusion reason label used in Appendix C."""
    verdict, adim = karar(r)
    return ADIMLAR[adim] if verdict == "OUT" else None
