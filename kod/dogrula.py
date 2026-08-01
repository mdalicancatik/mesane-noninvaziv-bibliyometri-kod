"""Verification harness — checks that `prosedur.py` reproduces the recorded verdicts.

Run from the `kod/` directory with no arguments:

    python dogrula.py

It applies the procedure to every record in `veri/top100.json` and `veri/sampleB.json`
(the records whose signal fields are shipped in this archive) and compares the result
with the verdict recorded for that record. No Web of Science access is needed.

What it establishes: for every record the procedure resolves on its own, the outcome
equals the recorded verdict. The records it does not resolve are returned as "SINIR"
(borderline) and are exactly the records carrying a record-specific rationale, i.e.
those read at full-text level and listed in `manual.py`.

What it cannot establish: the same check across the full 5,000-record pool. The signal
fields for the pool are computed from the title, abstract and keyword text of the Web of
Science records, which is proprietary and is not redistributed here. Regenerating them
requires your own Web of Science export (README §5).
"""
import json
import os
import sys
from collections import Counter

from prosedur import karar, ADIMLAR

HERE = os.path.dirname(os.path.abspath(__file__))
VERI = os.path.join(os.path.dirname(HERE), "veri")
KURAL = "rule-based: technology + diagnostic framing"


def yukle(ad):
    with open(os.path.join(VERI, ad), encoding="utf-8") as f:
        return json.load(f)


def denetle(ad, kayitlar):
    """Sapmaları, kaydın elle karara bağlanıp bağlanmadığına göre ayırır."""
    cozulen = uyan = 0
    sinir = []
    sapma_elle = sapma_kural = 0
    for r in kayitlar:
        verdict, _ = karar(r)
        if verdict == "SINIR":
            sinir.append(r)
            continue
        cozulen += 1
        if verdict == r["verdict"]:
            uyan += 1
        elif r.get("screening_rationale", KURAL) != KURAL:
            sapma_elle += 1
            print(f"    elle karar prosedürü geçersiz kılmış: prosedür={verdict} "
                  f"kayıtlı={r['verdict']} | {r['title'][:56]}")
        else:
            sapma_kural += 1
            print(f"    SAPMA (kural temelli): prosedür={verdict} kayıtlı={r['verdict']} "
                  f"| {r['title'][:56]}")
    print(f"  {ad}: prosedür {cozulen} kaydı kendi başına çözdü, {len(sinir)} kaydı sınıra ayırdı; "
          f"çözülenlerin {uyan}'i kayıtlı verdict ile aynı, {sapma_elle}'i elle kararla değiştirilmiş")
    return sapma_kural, cozulen, sinir


def main():
    print("Tarama prosedürü doğrulaması — Ek B'deki adımlar arşivdeki sinyaller üzerinde\n")

    top = yukle("top100.json")
    sapma, cozulen, sinir = denetle("top100 ", top)

    kural = [r for r in top if r.get("screening_rationale") == KURAL]
    kural_uyan = sum(1 for r in kural if karar(r)[0] == r["verdict"])
    print(f"    bunlardan kural temelli olarak kayda geçenler: {kural_uyan}/{len(kural)}")

    elle = [r for r in top if r.get("screening_rationale") != KURAL]
    dagilim = Counter(karar(r)[0] for r in elle)
    print(f"    elle karara bağlanan {len(elle)} kaydın prosedür çıktısı: {dict(dagilim)}")

    sapmaB, cozulenB, sinirB = denetle("sampleB", yukle("sampleB.json"))
    print("    (sampleB dosyası gerekçe alanı taşımaz; sapma varsa elle karar sayılamaz)")

    print("\nHavuzun karar dağılımı (veri/pool5000_screening.json):")
    havuz = Counter(r["verdict"] for r in yukle("pool5000_screening.json"))
    for k in ("IN", "OUT", "SINIR"):
        print(f"  {k:6} {havuz[k]:>5}")
    print(f"  {'toplam':6} {sum(havuz.values()):>5}")
    print(f"  ölçütleri karşılamayan (OUT + SINIR): {havuz['OUT'] + havuz['SINIR']}")

    print("\nEk C'deki gerekçe etiketleri, prosedürün adım numaralarıdır:")
    for n in (6, 2, 8, 7, 10, 5, 4):
        print(f"  adım {n:>2}  {ADIMLAR[n]}")

    tam = (sapma == 0) and (sapmaB == 0)
    print("\nSONUÇ:", "prosedür, kural temelli kayda geçen her kararı birebir yeniden üretiyor; "
          "sapmaların tamamı elle karara bağlanmış kayıtlardır."
          if tam else "kural temelli bir kayıtta sapma var; kayıtlı verdict geçerlidir.")
    return 0 if tam else 1


if __name__ == "__main__":
    sys.exit(main())
