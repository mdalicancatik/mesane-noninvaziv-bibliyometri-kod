"""Paketteki türetilmiş dosyalardan records.json'u yeniden kurar.

Analiz betikleri 5.000'lik listeye sıra numarasıyla erişir (recs[rank-1]).
Bu betik, uygun 252 kaydın tam metadatasını doğru sıralara yerleştirir; kalan
sıraları hafif dizinden gelen temel alanlarla doldurur. Ağ analizleri yalnızca
örneklemdeki kayıtları kullandığı için bu yeterlidir.

Tam yeniden TARAMA gerekiyorsa (özet/anahtar kelime düzeyinde) ham .bib
dosyaları gerekir; o durumda bib_parse.py çalıştırılmalıdır.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
VERI = os.path.join(os.path.dirname(HERE), "veri")

def kur(hedef="records.json"):
    tam = json.load(open(os.path.join(VERI, "records_uygun252.json"), encoding="utf-8"))
    dizin = json.load(open(os.path.join(VERI, "havuz5000_dizin.json"), encoding="utf-8"))
    out = []
    for x in dizin:
        rk = str(x["rank"])
        if rk in tam:
            out.append(tam[rk])
        else:
            out.append({"Title": x["title"], "Year": x["year"], "DOI": x["doi"],
                        "Times-Cited": str(x["tc"]), "Type": x["type"],
                        "Journal": x["journal"], "_eksik": True})
    json.dump(out, open(hedef, "w", encoding="utf-8"), ensure_ascii=False)
    dolu = sum(1 for r in out if not r.get("_eksik"))
    print(f"{hedef} kuruldu: {len(out)} sıra, {dolu} tam metadata")
    return out

if __name__ == "__main__":
    kur(sys.argv[1] if len(sys.argv) > 1 else "records.json")
