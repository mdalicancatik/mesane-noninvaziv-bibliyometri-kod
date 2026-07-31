"""§6 dahil/dışlama ölçütleri — ilk geçiş kural tabanlı tarama.
Üç kova üretir: AUTO_IN, AUTO_OUT, SINIR (elle okunacak).
Amaç şu aşamada kesin örneklem değil, uygun kayıt yoğunluğunu ölçmek.
"""
import json, re

recs = json.load(open('/home/claude/records.json', encoding='utf-8'))
def g(r, k): return (r.get(k, '') or '')

def txt(r):
    return " ".join([g(r,'Title'), g(r,'Abstract'), g(r,'Keywords'), g(r,'Keywords-Plus')]).lower()

def has(t, terms):
    return [x for x in terms if re.search(r'(?<![a-z])' + re.escape(x) + r'(?![a-z])', t)]

# --- Hastalık odağı ---
BLADDER = ["bladder cancer","bladder carcinoma","bladder tumor","bladder tumour",
    "bladder neoplasm","bladder neoplasms","urothelial carcinoma","urothelial cancer",
    "nmibc","mibc","non-muscle-invasive bladder","muscle-invasive bladder",
    "non-muscle invasive bladder","muscle invasive bladder","bladder"]

# --- Noninvaziv teknoloji blokları ---
T_URINE = ["urine cytology","urinary cytology","urinary biomarker","urinary biomarkers",
    "urine biomarker","urine biomarkers","urinary marker","urinary markers","urine marker",
    "urinary test","urinary tests","voided urine","urinary sediment","urinary dna",
    "urine dna","urinary rna","urine-based","urine based","urinary cell-free"]
T_BLOOD = ["liquid biopsy","cell-free dna","cfdna","circulating tumor dna",
    "circulating tumour dna","ctdna","circulating tumor cell","circulating tumor cells",
    "circulating tumour cell","circulating tumour cells","ctcs"]
T_MOL   = ["dna methylation","methylation marker","methylation markers","tert promoter",
    "telomerase","survivin","metabolomic","metabolomics","proteomic","proteomics",
    "exosome","exosomes","exosomal","extracellular vesicle","extracellular vesicles"]
T_COMM  = ["urovysion","nmp22","bladderchek","bta stat","bta trak","immunocyt","ucyt",
    "cxbladder","uroseek","epicheck","assuremdx","adxbladder","uromonitor","uromark",
    "penk","xpert bladder","fish"]
T_IMG   = ["mri","magnetic resonance imaging","multiparametric mri","mpmri","vi-rads",
    "virads","vesical imaging","diffusion-weighted","diffusion weighted","ct urography",
    "computed tomography urography","urography","ultrasonography","ultrasound","pet/ct",
    "fdg pet"]
T_AI    = ["radiomic","radiomics","deep learning","machine learning",
    "artificial intelligence","convolutional neural network","neural network",
    "computer-aided detection","computer-aided diagnosis","vision transformer",
    "large language model","chatgpt","gpt-4","foundation model"]
T_SENS  = ["biosensor","biosensors","electronic nose","volatile organic compound",
    "volatile organic compounds","raman spectroscopy","sers"]
TECH = T_URINE + T_BLOOD + T_MOL + T_COMM + T_IMG + T_AI + T_SENS

# --- Tanısal bağlam ---
DIAG = ["diagnosis","diagnostic","diagnose","detection","detect","screening","surveillance",
    "follow-up","monitoring","staging","recurrence detection","sensitivity","specificity",
    "diagnostic accuracy","auc","roc curve","noninvasive","non-invasive","predictive value"]

# --- Dışlama blokları ---
X_MECH = ["proliferation","migration and invasion","epithelial-mesenchymal","emt",
    "cerna","sponge","knockdown","overexpression","signaling pathway","signalling pathway",
    "apoptosis","cell cycle","tumor microenvironment","tumour microenvironment",
    "xenograft","in vitro","cell lines","cell line","carcinogenesis","mechanism"]
X_TREAT = ["bcg","bacillus calmette","intravesical","chemotherapy","immunotherapy",
    "pembrolizumab","atezolizumab","nivolumab","durvalumab","avelumab","enfortumab",
    "erdafitinib","sacituzumab","cystectomy","neoadjuvant","adjuvant","radiotherapy",
    "chemoradiation","trimodal","checkpoint inhibitor","drug delivery","nanoparticle"]
X_INVAS = ["cystoscopy","cystoscopic","blue light","photodynamic","narrow band imaging",
    "hexaminolevulinate","ureteroscopy","turbt","transurethral resection","en bloc"]
X_TISSUE = ["immunohistochemistry","immunohistochemical","whole slide","histopathology",
    "histopathological","tissue microarray","pathomics","hematoxylin"]

out = []
for i, r in enumerate(recs):
    t = txt(r)
    ttl = g(r,'Title').lower()
    rec = {
        "rank": i+1,
        "tc": int(g(r,'Times-Cited') or 0),
        "year": g(r,'Year'),
        "doi": g(r,'DOI'),
        "title": g(r,'Title'),
        "type": g(r,'Type'),
        "tech": has(t, TECH),
        "tech_title": has(ttl, TECH),
        "diag": has(t, DIAG),
        "x_mech": has(t, X_MECH),
        "x_treat": has(t, X_TREAT),
        "x_invas": has(t, X_INVAS),
        "x_tissue": has(t, X_TISSUE),
        "bladder_title": bool(has(ttl, BLADDER)),
    }
    out.append(rec)

json.dump(out, open('/home/claude/screen1.json','w',encoding='utf-8'), ensure_ascii=False)

# --- İki sınır: LİBERAL (üst sınır) ve KATI (alt sınır) ---
def liberal(x):
    # teknoloji terimi var + tanısal bağlam var + mesane başlıkta
    return bool(x["tech"]) and bool(x["diag"]) and x["bladder_title"]

def strict(x):
    if not (x["tech_title"] and x["bladder_title"]):
        return False
    if not x["diag"]:
        return False
    if x["x_invas"] or x["x_tissue"]:
        return False
    if len(x["x_mech"]) >= 2 or len(x["x_treat"]) >= 2:
        return False
    return True

for name, fn in [("LİBERAL (üst sınır)", liberal), ("KATI (alt sınır)", strict)]:
    hits = [x for x in out if fn(x)]
    print(f"\n=== {name} — toplam {len(hits)} uygun ===")
    if len(hits) >= 100:
        h100 = hits[99]
        print(f"  100. uygun kayıt: havuz sırası {h100['rank']}, atıf {h100['tc']}")
    else:
        print(f"  100'e ULAŞMIYOR ({len(hits)})")
    for cut in (500, 1000, 1500, 2000, 2500, 3000):
        n = sum(1 for x in hits if x["rank"] <= cut)
        print(f"  ilk {cut:4d} kayıtta uygun: {n}")
