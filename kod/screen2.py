"""§6 ikinci geçiş — kalibrasyon diliminde onaylanan yargıyla.

Kilitlenen kurallar:
  K1  İnvaziv dışlama yalnızca yöntem KONU olduğunda (başlıkta) uygulanır.
      Referans standart olarak anılması dışlama gerekçesi değildir.
  K2  Kılavuzlar ve genel hastalık derlemeleri dışlanır.
  K3  Karma kohortlu (mesane odak değil) ctDNA tedavi-yanıtı çalışmaları dışlanır.
      §6 istisnası yalnızca ctDNA'nın MRD belirteci olduğu denemeleri kapsar.
  K4  Görüntüleme + YZ segmentasyon çalışmaları dahildir.
"""
import json, re

recs = json.load(open('/home/claude/records.json', encoding='utf-8'))
def g(r, k): return (r.get(k, '') or '')

def norm(s): return re.sub(r'\s+', ' ', s.lower())

def hit(t, terms):
    return [x for x in terms if re.search(r'(?<![a-z0-9])' + re.escape(x) + r'(?![a-z])', t)]

# ---------- hastalık odağı ----------
BLADDER = ["bladder cancer","bladder carcinoma","bladder tumor","bladder tumour",
    "bladder neoplasm","bladder neoplasms","urothelial carcinoma","urothelial cancer",
    "nmibc","mibc","non-muscle-invasive bladder","muscle-invasive bladder",
    "non-muscle invasive bladder","muscle invasive bladder","bladder"]

# ---------- noninvaziv teknoloji ----------
TECH_URINE = ["urine cytology","urinary cytology","urinary biomarker","urinary biomarkers",
    "urine biomarker","urine biomarkers","urinary marker","urinary markers","urine marker",
    "urinary test","voided urine","urinary sediment","urinary dna","urine dna","urinary rna",
    "urine-based","urine based","urinary cell-free","urinary exosom","urine exosom",
    "urinary extracellular vesicle","urinary microrna","urinary mirna","urinary protein",
    "urinary metabolom","urinary tumor dna","urine tumor dna","urinary tert"]
TECH_BLOOD = ["liquid biopsy","cell-free dna","cfdna","circulating tumor dna",
    "circulating tumour dna","ctdna","circulating tumor cell","circulating tumor cells",
    "circulating tumour cell","circulating micrornas","circulating mirna","serum biomarker",
    "plasma biomarker","serum microrna","plasma cell-free"]
TECH_IMG = ["mri","magnetic resonance imaging","multiparametric mri","mpmri","vi-rads",
    "virads","vesical imaging","diffusion-weighted","diffusion weighted","ct urography",
    "computed tomography urography","urography","ultrasonography","pet/ct","fdg pet",
    "computed tomography"]
TECH_AI = ["radiomic","radiomics","deep learning","machine learning","artificial intelligence",
    "convolutional neural network","neural network","computer-aided detection",
    "computer-aided diagnosis","vision transformer","large language model","chatgpt","gpt-4"]
TECH_SENS = ["biosensor","biosensors","electronic nose","volatile organic compound",
    "volatile organic compounds","raman spectroscopy","sers","microfluidic","lab-on-a-chip",
    "aptamer","electrochemical detection","electrochemical biosensor"]
TECH_COMM = ["urovysion","nmp22","bladderchek","bta stat","bta trak","immunocyt","ucyt",
    "cxbladder","uroseek","epicheck","assuremdx","adxbladder","uromonitor","uromark",
    "penk","xpert bladder"]
TECH_ALL = (TECH_URINE + TECH_BLOOD + TECH_IMG + TECH_AI + TECH_SENS + TECH_COMM
            + ["dna methylation","methylation marker","tert promoter","telomerase",
               "survivin","metabolomic","metabolomics","proteomic","proteomics",
               "exosome","exosomes","exosomal","extracellular vesicle","extracellular vesicles",
               "fish","microrna","mirna"])

# ---------- tanısal çerçeve ----------
DIAG_STRONG = ["diagnostic accuracy","diagnostic performance","diagnostic value","detection of",
    "early detection","noninvasive detection","non-invasive detection","screening","surveillance",
    "recurrence detection","serve as biomarkers","serve as novel","as biomarkers","biomarker panel",
    "diagnostic biomarker","sensitivity and specificity","staging","preoperative prediction",
    "risk stratification","monitoring"]
DIAG_WEAK = ["diagnosis","diagnostic","detect","detection","prognostic","predict","sensitivity",
    "specificity","auc","roc"]

# ---------- dışlama ----------
X_MECH = ["promotes","suppresses","inhibits","facilitate","facilitates","accelerates",
    "proliferation","migration and invasion","epithelial-mesenchymal","cerna","sponge",
    "knockdown","overexpression","silencing","signaling pathway","signalling pathway",
    "apoptosis","cell cycle","tumor microenvironment","tumour microenvironment","xenograft",
    "in vitro","cell lines","carcinogenesis","targeting","axis","regulates","mediated",
    "functional role"]
X_TREAT = ["bacillus calmette","intravesical","chemotherapy","immunotherapy","pembrolizumab",
    "atezolizumab","nivolumab","durvalumab","avelumab","enfortumab","erdafitinib","sacituzumab",
    "cystectomy","neoadjuvant","adjuvant chemotherapy","radiotherapy","chemoradiation",
    "trimodal","checkpoint inhibitor","drug delivery","photothermal","sonodynamic",
    "drug resistance","cisplatin resistance","therapeutic efficacy","antitumor"]
X_TISSUE = ["immunohistochemistry","immunohistochemical","whole slide","histopathology",
    "histopathological","tissue microarray","pathomics","hematoxylin","molecular subtypes",
    "molecular subtyping","tissue expression","tumor tissue","resected specimen"]
X_INVAS_TITLE = ["cystoscopy","cystoscopic","blue light","photodynamic","narrow band imaging",
    "hexaminolevulinate","ureteroscopy","turbt","transurethral resection","en bloc"]
X_GENERAL = ["guidelines","guideline","epidemiology","global trends","incidence and mortality",
    "advances in","overview of","seer","cost-effectiveness","quality of life"]

# §6 elle dahil istisnası — ctDNA/MRD denemeleri
MRD_OK = ["imvigor010","imvigor011","minimal residual disease","molecular residual disease",
          "ctdna guiding","adjuvant immunotherapy in urothelial"]

out = []
for i, r in enumerate(recs):
    ttl = norm(g(r, 'Title'))
    full = norm(" ".join([g(r,'Title'), g(r,'Abstract'), g(r,'Keywords'), g(r,'Keywords-Plus')]))

    d = {
        "rank": i+1, "tc": int(g(r,'Times-Cited') or 0), "year": g(r,'Year'),
        "doi": g(r,'DOI'), "title": g(r,'Title'), "journal": g(r,'Journal'),
        "type": g(r,'Type'),
    }
    d["bladder_t"]  = bool(hit(ttl, BLADDER))
    d["tech_t"]     = hit(ttl, TECH_ALL)
    d["tech_a"]     = hit(full, TECH_ALL)
    d["diag_s_t"]   = hit(ttl, DIAG_STRONG)
    d["diag_s_a"]   = hit(full, DIAG_STRONG)
    d["diag_w_t"]   = hit(ttl, DIAG_WEAK)
    d["mech_t"]     = hit(ttl, X_MECH)
    d["mech_a"]     = hit(full, X_MECH)
    d["treat_t"]    = hit(ttl, X_TREAT)
    d["treat_a"]    = hit(full, X_TREAT)
    d["tissue_t"]   = hit(ttl, X_TISSUE)
    d["tissue_a"]   = hit(full, X_TISSUE)
    d["invas_t"]    = hit(ttl, X_INVAS_TITLE)
    d["general_t"]  = hit(ttl, X_GENERAL)
    d["mrd"]        = hit(full, MRD_OK)
    out.append(d)

json.dump(out, open('/home/claude/screen2.json','w',encoding='utf-8'), ensure_ascii=False)
print("screen2.json yazıldı:", len(out), "kayıt")
