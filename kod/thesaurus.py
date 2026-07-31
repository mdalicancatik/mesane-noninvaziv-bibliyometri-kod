"""TEZAURUS — anahtar kelime eşanlamlı birleştirme tablosu
§5 karar 7 gereği açık ve tekrarlanabilir biçimde tutulur; kod deposuna konur.

Kural: sol taraftaki her varyant, sağdaki kanonik terime eşlenir.
Birleştirme yalnızca EŞANLAMLI veya yazım/çekim varyantları için yapılır;
kavramsal olarak farklı terimler (ör. 'tanı' ve 'evreleme') birleştirilmez.
"""

THESAURUS = {
    # --- hastalık terimleri ---
    "bladder cancer": "bladder cancer",
    "bladder-cancer": "bladder cancer",
    "bladder neoplasms": "bladder cancer",
    "urinary bladder neoplasms": "bladder cancer",
    "urinary bladder cancer": "bladder cancer",
    "bladder tumor": "bladder cancer",
    "bladder tumors": "bladder cancer",
    "bladder tumour": "bladder cancer",
    "bladder carcinoma": "bladder cancer",

    "urothelial carcinoma": "urothelial carcinoma",
    "urothelial cancer": "urothelial carcinoma",
    "transitional cell carcinoma": "urothelial carcinoma",
    "transitional-cell carcinoma": "urothelial carcinoma",
    "invasive urothelial carcinoma": "urothelial carcinoma",
    "urothelial neoplasms": "urothelial carcinoma",
    "urothelial bladder cancer": "urothelial carcinoma",

    "non-muscle-invasive bladder cancer": "non-muscle-invasive bladder cancer",
    "non muscle invasive bladder cancer": "non-muscle-invasive bladder cancer",
    "nonmuscle-invasive bladder cancer": "non-muscle-invasive bladder cancer",
    "nmibc": "non-muscle-invasive bladder cancer",
    "muscle-invasive bladder cancer": "muscle-invasive bladder cancer",
    "muscle invasive bladder cancer": "muscle-invasive bladder cancer",
    "mibc": "muscle-invasive bladder cancer",

    # --- görüntüleme ---
    "mri": "MRI",
    "magnetic resonance imaging": "MRI",
    "magnetic-resonance-imaging": "MRI",
    "mr imaging": "MRI",
    "multiparametric mri": "multiparametric MRI",
    "multiparametric magnetic resonance imaging": "multiparametric MRI",
    "mp-mri": "multiparametric MRI",
    "mpmri": "multiparametric MRI",
    "diffusion magnetic resonance imaging": "diffusion-weighted imaging",
    "diffusion-weighted imaging": "diffusion-weighted imaging",
    "diffusion weighted imaging": "diffusion-weighted imaging",
    "dwi": "diffusion-weighted imaging",
    "vi-rads": "VI-RADS",
    "vesical imaging reporting and data system": "VI-RADS",
    "computed tomography": "computed tomography",
    "ct urography": "CT urography",
    "computed tomography urography": "CT urography",

    # --- belirteçler ---
    "biomarker": "biomarker",
    "biomarkers": "biomarker",
    "marker": "biomarker",
    "markers": "biomarker",
    "tumor markers": "biomarker",
    "tumour markers": "biomarker",
    "urinary biomarker": "urinary biomarker",
    "urinary biomarkers": "urinary biomarker",
    "urine biomarker": "urinary biomarker",
    "urine biomarkers": "urinary biomarker",
    "urinary marker": "urinary biomarker",
    "urinary markers": "urinary biomarker",

    "extracellular vesicles": "extracellular vesicles",
    "extracellular vesicle": "extracellular vesicles",
    "exosome": "extracellular vesicles",
    "exosomes": "extracellular vesicles",
    "exosomal": "extracellular vesicles",

    "cell-free dna": "cell-free DNA",
    "cell free dna": "cell-free DNA",
    "cfdna": "cell-free DNA",
    "circulating tumor dna": "circulating tumour DNA",
    "circulating tumour dna": "circulating tumour DNA",
    "ctdna": "circulating tumour DNA",
    "liquid biopsy": "liquid biopsy",

    "microrna": "microRNA",
    "micrornas": "microRNA",
    "mirna": "microRNA",
    "mirnas": "microRNA",
    "long non-coding rna": "long non-coding RNA",
    "long noncoding rna": "long non-coding RNA",
    "lncrna": "long non-coding RNA",

    "dna methylation": "DNA methylation",
    "methylation": "DNA methylation",
    "hypermethylation": "DNA methylation",
    "promoter hypermethylation": "DNA methylation",
    "tert promoter mutations": "TERT promoter mutation",
    "tert promoter mutation": "TERT promoter mutation",
    "tert promoter": "TERT promoter mutation",

    "cytology": "urine cytology",
    "urine cytology": "urine cytology",
    "urinary cytology": "urine cytology",
    "voided urine": "voided urine",
    "urine": "urine",

    "in-situ hybridization": "fluorescence in situ hybridization",
    "in situ hybridization": "fluorescence in situ hybridization",
    "fluorescence in situ hybridization": "fluorescence in situ hybridization",
    "fish": "fluorescence in situ hybridization",

    # --- yapay zekâ ---
    "radiomics": "radiomics",
    "radiomic": "radiomics",
    "texture features": "radiomics",
    "texture analysis": "radiomics",
    "deep learning": "deep learning",
    "deep-learning": "deep learning",
    "machine learning": "machine learning",
    "machine-learning": "machine learning",
    "artificial intelligence": "artificial intelligence",
    "convolutional neural network": "convolutional neural network",
    "convolutional neural networks": "convolutional neural network",
    "neural network": "neural network",
    "neural networks": "neural network",
    "segmentation": "segmentation",

    # --- klinik kavramlar ---
    "diagnosis": "diagnosis",
    "diagnostic accuracy": "diagnostic accuracy",
    "diagnostic-accuracy": "diagnostic accuracy",
    "accuracy": "diagnostic accuracy",
    "surveillance": "surveillance",
    "follow-up": "surveillance",
    "follow up": "surveillance",
    "monitoring": "surveillance",
    "recurrence": "recurrence",
    "disease recurrence": "recurrence",
    "tumor recurrence": "recurrence",
    "staging": "staging",
    "stage": "staging",
    "tumor staging": "staging",
    "radical cystectomy": "radical cystectomy",
    "cystectomy": "radical cystectomy",
    "cystoscopy": "cystoscopy",
    "hematuria": "haematuria",
    "haematuria": "haematuria",
    "meta-analysis": "meta-analysis",
    "systematic review": "systematic review",
}

# Korpusun tanımı gereği her kayıtta bulunan veya ayırt edici bilgi taşımayan terimler.
# Ağdan çıkarılıp çıkarılmayacağı KULLANICI KARARINA bağlıdır (bkz. rapor).
GENERIC = {
    "cancer", "carcinoma", "tumor", "tumors", "tumour", "tumours", "neoplasm",
    "expression", "genes", "gene", "protein", "proteins", "cells", "cell",
    "management", "classification", "prediction", "survival", "outcomes",
    "patients", "risk", "identification", "association", "impact", "performance",
    "assay", "test", "tests", "system", "validation", "study", "review",
}


def canon(term: str) -> str:
    """Bir anahtar kelimeyi kanonik biçime çevirir."""
    t = " ".join(term.strip().lower().split())
    return THESAURUS.get(t, t)
