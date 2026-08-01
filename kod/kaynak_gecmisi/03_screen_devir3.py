import json, re
pool=json.load(open('pool.json',encoding='utf-8'))

BLADDER=r'bladder|urothel|nmibc|\bmibc\b|urinary tract cancer|upper tract urothelial|\butuc\b'
NOTBLADDER=r'gallbladder|gall bladder'
OTHER=(r'hepatocellular|liver cancer|liver carcinoma|lung cancer|lung adenocarcin|breast cancer|breast carcinoma|'
 r'prostate cancer|prostate carcinoma|renal cell|kidney cancer|colorectal|colon cancer|gastric cancer|stomach cancer|'
 r'pancrea|cervical cancer|ovarian cancer|endometrial cancer|glioma|glioblastoma|melanoma|esophageal|oesophageal|'
 r'thyroid cancer|leukemia|leukaemia|lymphoma|myeloma|head and neck|nasopharyngeal|biliary|cholangiocarcinoma|'
 r'oral squamous|osteosarcoma|testicular|penile|sarcoma|neuroblastoma|retinoblastoma|mesothelioma|thymoma|'
 r'fatty liver|hepatitis|cirrhosis|tuberculosis|covid|diabet|alzheimer|parkinson|air pollution')
TECH=(r'urine|urinary|cytolog|biomarker|bio-marker|liquid biops|cell-free dna|cell free dna|cfdna|circulating tumou?r dna|'
 r'ctdna|circulating tumou?r cell|\bctc\b|exosom|extracellular vesicle|\bev\b|methylation|methylome|epigenetic marker|'
 r'\bfish\b|urovysion|nmp22|bta stat|bta trak|telomerase|tert promoter|cxbladder|uroseek|epicheck|assuremdx|'
 r'xpert|\bpenk\b|uromonitor|adxbladder|\bmri\b|magnetic resonance|mpmri|vi-rads|virads|vesical imaging|radiomic|'
 r'deep learning|machine learning|artificial intelligence|neural network|computer-aided|\bct urograph|urography|'
 r'noninvasive|non-invasive|diagnos|detect|surveillance|screening|serum|plasma|blood-based|salivary|'
 r'sensitivity and specificity|diagnostic accuracy|diagnostic performance|predictive model|nomogram|'
 r'cystoscop|narrow band imaging|photodynamic diagnosis|blue light|confocal|optical coherence|raman|'
 r'mirna|microrna|\blncrna\b|circrna|transcriptom|proteom|metabolom|genomic profil|mutation analysis|panel')
MECH=(r'promotes|inhibits|suppresses|facilitat|accelerat|attenuat|proliferation|migration and invasion|apoptosis|'
 r'sponge|sponging|axis|knockdown|overexpression|silencing|ferroptosis|autophagy|pyroptosis|'
 r'epithelial-mesenchymal|\bemt\b|signaling pathway|signalling pathway|regulates|modulates|mediates|targeting|'
 r'in vitro|in vivo|mouse model|xenograft|cell line')
TREAT=(r'immune checkpoint|immunotherap|pembrolizumab|atezolizumab|nivolumab|durvalumab|avelumab|erdafitinib|'
 r'enfortumab|sacituzumab|chemotherap|neoadjuvant|adjuvant|gemcitabine|cisplatin|\bbcg\b|intravesical|'
 r'cystectom|turbt|\bsurger|surgical|radiotherap|radiation therapy|clinical trial|randomi[sz]ed|'
 r'\btreatment of|therapeutic target|drug deliver|nanoparticle|vaccine|car-t|prognos')

def s(r): return (r['title']+' | '+r['keywords']+' | '+r['keywords_plus']+' | '+r['abstract'][:900]).lower()
def t(r): return r['title'].lower()

for r in pool:
    txt=s(r); ti=t(r)
    r['_bl'] = bool(re.search(BLADDER,ti)) or bool(re.search(BLADDER,txt))
    r['_bl_title'] = bool(re.search(BLADDER,ti)) and not re.search(NOTBLADDER,ti)
    r['_other'] = bool(re.search(OTHER,ti))
    r['_tech'] = bool(re.search(TECH,txt))
    r['_tech_title'] = bool(re.search(TECH,ti))
    r['_mech'] = bool(re.search(MECH,ti))
    r['_treat'] = bool(re.search(TREAT,ti))

# aşama 1: kesin dışlananlar
auto_out=[r for r in pool if (not r['_bl']) or r['_other'] or re.search(NOTBLADDER,t(r))]
cand=[r for r in pool if r not in auto_out]
print("Havuz:",len(pool)," Otomatik dışlanan (mesane dışı):",len(auto_out)," Kalan aday:",len(cand))
json.dump(cand,open('cand1.json','w',encoding='utf-8'),ensure_ascii=False)
print("\n--- Mesane başlıklı + teknik başlıklı adaylar, atıfa göre (ilk 160) ---")
n=0
for r in cand:
    if r['_bl_title'] and r['_tech_title']:
        n+=1
        if n<=160: print(f"{r['times_cited']:>5} {r['year']} {'M' if r['_mech'] else '-'}{'T' if r['_treat'] else '-'} | {r['title'][:115]}")
print("...toplam:",n)
import json, re
cand=json.load(open('cand1.json',encoding='utf-8'))

def T(r): return r['title'].lower()
def FULL(r): return (r['title']+' '+r['keywords']+' '+r['keywords_plus']+' '+r['abstract']).lower()

# --- Mesane odağı (başlıkta) ---
BL=r'bladder|urothel|nmibc|\bmibc\b'
UTUC_ONLY=r'upper tract|upper urinary tract|nephroureterectomy|ureteroscop|renal pelvi|\butuc\b'

# --- Noninvaziv tanı/takip teknolojisi (başlıkta güçlü sinyal) ---
NONINV=(r'urine|urinary|urin\b|cytolog|liquid biops|cell-free dna|cell free dna|cfdna|circulating tumou?r dna|ctdna|'
 r'circulating tumou?r cell|\bctcs?\b|exosom|extracellular vesicle|methylation|epicheck|uromark|uroseek|cxbladder|'
 r'nmp22|nmp-22|bta |urovysion|\bfish\b|telomerase|tert promoter|xpert|adxbladder|uromonitor|\bpenk\b|assuremdx|'
 r'\bmri\b|magnetic resonance|mpmri|vi-rads|virads|vesical imaging|radiomic|computed tomograph|\bct\b|urograph|'
 r'deep learning|machine learning|artificial intelligence|convolutional|neural network|pathomic|'
 r'serum|plasma|blood-based|blood serum|breath|olfaction|volatile organic|biosensor|sensor|biochip|immunoassay|'
 r'noninvasive|non-invasive|nonivasive')
DIAGAIM=(r'diagnos|detect|screening|surveillance|monitor|staging|stage|grade|grading|predict|discriminat|'
 r'differentiat|identif|classif|accuracy|performance|sensitivity|specificity|biomarker|marker|recurrence|'
 r'muscle invasi|muscle-invasi|invasiveness|assessment|evaluat|nomogram|signature|panel|test\b|assay')

# --- Kesin dışlama: doku temelli / invaziv / mekanizma / tedavi ---
TISSUE=(r'histopatholog|whole slide|whole-slide|pathomic|tissue microarray|immunohistochem|\bihc\b|'
 r'who classification|tumou?r tissue|biopsy specimen|surgical specimen|cystectomy specimen|tcga')
INVASIVE=r'cystoscop|ureteroscop|transurethral|\bturbt\b|blue light|hexaminolevulinate|photodynamic diagnos|narrow band imaging|confocal laser|optical coherence'
MECH=(r'\bpromotes?\b|\binhibits?\b|\bsuppress|facilitat|accelerat|attenuat|\bsponge|sponging|'
 r'knockdown|overexpression|silencing|ferroptosis|autophagy|pyroptosis|disulfidptosis|cuproptosis|'
 r'epithelial-mesenchymal|\bemt\b|signal+ing pathway|signal+ing axis|\baxis\b|regulat|modulat|mediat|'
 r'targeting|tumorigenesis|tumourigenesis|carcinogenesis|pathogenesis|proliferation|migration and invasion|'
 r'cell aggressiveness|stemness|macrophage|microenvironment|immune infiltrat|t cell exhaustion|'
 r'chemoresistance|chemosensitiv|cisplatin resistance|gemcitabine resistance|drug resistance|'
 r'anti-oncogenic|oncogenic function|biological function|regulatory network|competing endogenous')
TREAT=(r'immunotherap(?!y-)|pembrolizumab|atezolizumab|nivolumab|durvalumab|avelumab|erdafitinib|enfortumab|'
 r'chemotherap|neoadjuvant|adjuvant (?!atezolizumab|immunotherapy)|intravesical|\bbcg\b|cystectom|'
 r'radiotherap|radiation therapy|drug deliver|nano ?drug|nanoparticle|therapeutic|treatment of|'
 r'kidney-sparing|surger|surgical|clinical therap')
PROG_ONLY=r'prognostic signature|prognostic model|survival prediction|overall survival|prognosis for|prognostic value of'

def classify(r):
    ti=T(r); full=FULL(r)
    if not re.search(BL,ti): return 'X','mesane başlıkta değil'
    if re.search(UTUC_ONLY,ti) and not re.search(r'bladder',ti): return 'X','yalnızca üst üriner sistem'
    if re.search(TISSUE,ti): return 'X','doku/histopatoloji temelli'
    if re.search(INVASIVE,ti): return 'X','invaziv/endoskopik yöntem'
    if not re.search(NONINV,ti): return 'X','başlıkta noninvaziv teknik yok'
    if re.search(MECH,ti): return 'M','mekanizma/biyoloji odaklı'
    if re.search(TREAT,ti): return 'B','tedavi odaklı olabilir'
    if not re.search(DIAGAIM,full): return 'B','tanısal amaç belirsiz'
    return 'I','dahil'

for r in cand:
    r['_cls'],r['_why']=classify(r)

inc=[r for r in cand if r['_cls']=='I']
bor=[r for r in cand if r['_cls'] in ('M','B')]
print(f"Otomatik DAHİL: {len(inc)} | SINIRDA: {len(bor)}")
print(f"\n=== DAHİL, atıfa göre ilk 120 ===")
for i,r in enumerate(inc[:120],1):
    print(f"{i:>3}. {r['times_cited']:>4} {r['year']} | {r['title'][:110]}")
print(f"\n100. sıradaki atıf: {inc[99]['times_cited'] if len(inc)>99 else 'YOK'} | 120. : {inc[119]['times_cited'] if len(inc)>119 else '-'}")
print(f"\n=== SINIRDA olanlar (atıf >= 60), elle karar gerekli ===")
for r in bor:
    if r['times_cited']>=60: print(f"  {r['times_cited']:>4} {r['year']} [{r['_cls']}] {r['title'][:112]}")
json.dump({'inc':[r['wos_id'] for r in inc]},open('auto_inc.json','w'))
import json, re
cand=json.load(open('cand1.json',encoding='utf-8'))
exec(open('screen2.py').read().split("inc=[r for")[0].split("cand=json.load")[0]) if False else None
import importlib.util
# yeniden sınıflandır (screen2 kurallarını içe al)
src=open('screen2.py',encoding='utf-8').read()
body=src.split("for r in cand:")[0].replace("cand=json.load(open('cand1.json',encoding='utf-8'))","")
ns={'re':re,'json':json}
exec(body,ns)
classify=ns['classify']; T=ns['T']

# ELLE DAHİL ET (kural dışı ama gerçekten noninvaziv tanı/takip)
MAN_IN=[
 'ctdna guiding adjuvant immunotherapy',
 'early detection of metastatic relapse and monitoring of therapeutic efficacy',
 'early reduction in ctdna predicts survival',
 'updated overall survival by circulating tumor dna status',
 'ctdna-guided adjuvant atezolizumab',
 'multiparametric magnetic resonance imaging as a noninvasive assessment of tumor response',
 'urine tumor dna detection of minimal residual disease',
 'a urine-based dna methylation assay to facilitate early detection',
]
# ELLE DIŞLA (kural dahil etti ama konu dışı)
MAN_OUT=[
 'genomic subtypes of non-invasive bladder cancer',
 'tumor-derived exosomal bcyrn1',
 'integrated multiomics analysis and machine learning refine molecular subtypes',
 'artificial intelligence-based detection of fgfr3 mutational status directly from routine histology',
 'carcinogen biomarkers in the urine of electronic cigarette users',
 'tissue-resident memory t cells are epigenetically cytotoxic',
 'identification of extracellular vesicle-borne periostin',
 'combined genetic and epigenetic alterations of the tert promoter',
 'machine learning models for predicting post-cystectomy recurrence',
 'implications of tert promoter mutations and telomerase activity',
 'dna methylation as a therapeutic target',
 'the urinary microbiome',
 'expression of the long non-coding rna hotair correlates' ,  # tekrar değerlendirildi -> dahil (aşağıda geri alınıyor)
]
MAN_OUT=[m for m in MAN_OUT if 'hotair' not in m]

def final(r):
    ti=T(r)
    for m in MAN_OUT:
        if m in ti: return 'X','elle dışlandı'
    for m in MAN_IN:
        if m in ti: return 'I','elle dahil edildi'
    return classify(r)

for r in cand: r['_cls'],r['_why']=final(r)
inc=[r for r in cand if r['_cls']=='I']
print("Uygun bulunan toplam kayıt:",len(inc))
print("100. atıf:",inc[99]['times_cited'],"| 95-115. bant:")
for i,r in enumerate(inc[92:118],93):
    print(f"{i:>3}. {r['times_cited']:>4} {r['year']} | {r['title'][:105]}")
json.dump(inc,open('eligible.json','w',encoding='utf-8'),ensure_ascii=False)
# eşikteki eşitlik
th=inc[99]['times_cited']
ties=[r for r in inc if r['times_cited']==th]
print(f"\nEşik atıf = {th}; bu değerde {len(ties)} kayıt var:")
for r in ties: print("   ",r['year'],r['title'][:95])
