"""Şekil üretimi.
KURAL (§10): şekillerin içine BAŞLIK veya AÇIKLAMA METNİ gömülmez.
Yalnızca eksen etiketi ve gösterge bulunur; tüm açıklamalar belgede şekil altındadır.
Yerleşim: Fruchterman-Reingold (spring), seed=42, k ve iterations raporlanır.
"""
import json, itertools, math, os
from collections import Counter, defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities, modularity
from thesaurus import canon, GENERIC

OUT = "/mnt/user-data/outputs/sekiller"
os.makedirs(OUT, exist_ok=True)
SEED, K_SPRING, ITERS = 42, 0.6, 200

plt.rcParams.update({
    "figure.dpi": 300, "savefig.dpi": 300,
    "font.family": "DejaVu Sans", "font.size": 9,
    "axes.labelsize": 10, "xtick.labelsize": 9, "ytick.labelsize": 9,
    "legend.fontsize": 9, "axes.grid": True, "grid.alpha": 0.25,
    "axes.spines.top": False, "axes.spines.right": False,
})
C = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B3', '#937860']

top = json.load(open('/home/claude/top100.json', encoding='utf-8'))
recs = json.load(open('/home/claude/records.json', encoding='utf-8'))
def g(r, k): return (r.get(k, '') or '')
R = [recs[x['rank'] - 1] for x in top]


def save(fig, name):
    fig.savefig(f"{OUT}/{name}.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ", name)


def barh(labels, values, xlabel, name, color=C[0], figsize=(7, 4.2)):
    fig, ax = plt.subplots(figsize=figsize)
    y = range(len(labels))
    b = ax.barh(list(y), values, color=color)
    ax.set_yticks(list(y)); ax.set_yticklabels(labels)
    ax.invert_yaxis(); ax.set_xlabel(xlabel)
    ax.grid(axis="y", visible=False)
    for r_, v in zip(b, values):
        ax.text(v + max(values) * 0.012, r_.get_y() + r_.get_height() / 2,
                f"{v:,}".replace(",", "."), va="center", fontsize=8)
    ax.set_xlim(0, max(values) * 1.12)
    save(fig, name)


def draw_net(G, name, label_key=None, figsize=(7.5, 6.5), label_top=None, fontsize=7, edge_min=1):
    comms = list(greedy_modularity_communities(G, weight="weight"))
    Q = modularity(G, comms, weight="weight")
    cmap = {}
    for i, c in enumerate(sorted(comms, key=len, reverse=True)):
        for n in c:
            cmap[n] = C[i % len(C)]
    pos = nx.spring_layout(G, seed=SEED, k=K_SPRING, iterations=ITERS, weight="weight")
    fig, ax = plt.subplots(figsize=figsize)
    # ANALİZ tam ağ üzerinde; aşağıdaki süzme YALNIZCA görüntüleme içindir.
    E = [(u, v) for u, v in G.edges() if G[u][v]["weight"] >= edge_min]
    w = [G[u][v]["weight"] for u, v in E]
    mw = max(w) if w else 1
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=E, alpha=0.22,
                           width=[0.25 + 2.4 * (x / mw) for x in w], edge_color="#666666")
    freqs = [G.nodes[n].get("freq", 1) for n in G.nodes()]
    mf = max(freqs)
    nx.draw_networkx_nodes(G, pos, ax=ax,
                           node_size=[70 + 620 * (f / mf) for f in freqs],
                           node_color=[cmap[n] for n in G.nodes()],
                           linewidths=0.4, edgecolors="white")
    show = set(G.nodes())
    if label_top:
        show = set(sorted(G.nodes(), key=lambda n: -G.nodes[n].get("freq", 0))[:label_top])
    lab = {n: (G.nodes[n].get(label_key, n) if label_key else n) for n in show}
    nx.draw_networkx_labels(G, pos, labels=lab, ax=ax, font_size=fontsize)
    ax.axis("off")
    save(fig, name)
    return G.number_of_nodes(), G.number_of_edges(), len(comms), Q, nx.density(G)


def build_cooc(sets, threshold):
    freq = Counter()
    for s in sets: freq.update(s)
    nodes = {k for k, v in freq.items() if v >= threshold}
    G = nx.Graph()
    for k in nodes: G.add_node(k, freq=freq[k])
    for s in sets:
        for a, b in itertools.combinations(sorted(s & nodes), 2):
            if G.has_edge(a, b): G[a][b]["weight"] += 1
            else: G.add_edge(a, b, weight=1)
    return G, freq


print("Şekiller üretiliyor:")
stats = {}

# --- Ş1 teknoloji kategorileri ---
cc = Counter(x["cat"] for x in top)
order = sorted(cc.items(), key=lambda z: -z[1])
barh([k for k, _ in order], [v for _, v in order], "Makale sayısı", "S01_teknoloji_kategorileri")

# --- Ş2 yıl dağılımı ---
yr = Counter(int(x["year"]) for x in top)
years = list(range(2016, 2026))
fig, ax = plt.subplots(figsize=(7, 3.4))
ax.bar(years, [yr.get(y, 0) for y in years], color=C[0])
ax.set_xlabel("Yayın yılı"); ax.set_ylabel("Makale sayısı")
ax.set_xticks(years); ax.grid(axis="x", visible=False)
save(fig, "S02_yil_dagilimi")

# --- Ş3 atıf dağılımı ---
tc = [x["tc"] for x in top]
import statistics as st
fig, ax = plt.subplots(figsize=(7, 3.8))
ax.hist(tc, bins=24, color=C[0], edgecolor="white")
ax.axvline(st.mean(tc), color=C[3], ls="--", lw=1.4, label=f"Ortalama {st.mean(tc):.1f}")
ax.axvline(st.median(tc), color=C[2], ls=":", lw=1.6, label=f"Medyan {st.median(tc):.0f}")
ax.set_xlabel("Atıf sayısı"); ax.set_ylabel("Makale sayısı"); ax.legend()
ax.grid(axis="x", visible=False)
save(fig, "S03_atif_dagilimi")

# --- Ş4 dergiler ---
jj = Counter(g(r, "Journal").title() for r in R).most_common(10)
barh([k[:34] for k, _ in jj], [v for _, v in jj], "Makale sayısı", "S04_dergiler", C[1], (7, 4.6))

# --- Ş5 ülkeler ---
CTY = [("ABD",41),("Çin",25),("İtalya",19),("Birleşik Krallık",17),("Hollanda",15),
       ("Japonya",14),("İspanya",12),("Almanya",11),("Fransa",9),("Kanada",8)]
barh([k for k,_ in CTY],[v for _,v in CTY],"Makale sayısı (tam sayım)","S05_ulkeler",C[2],(7,4.2))

# --- Ş6 iş birliği türü ---
CO = [("Uluslararası",49),("Ulusal (çok kurumlu)",36),("Yerel (tek kurum)",15),("Tek yazar",0)]
barh([k for k,_ in CO],[v for _,v in CO],"Makale sayısı","S06_isbirligi",C[4],(7,3.0))

# --- Ş7 anahtar kelime ağı (generik terimler çıkarıldı) ---
ksets = []
for r in R:
    ks = {s.strip().lower() for s in (g(r,"Keywords")+"; "+g(r,"Keywords-Plus")).split(";") if s.strip()}
    ksets.append({canon(k) for k in ks} - GENERIC)
Gk, _ = build_cooc(ksets, 4)
stats["anahtar kelime"] = draw_net(Gk, "S07_anahtar_kelime_agi", figsize=(8, 7), fontsize=7, edge_min=3)

# --- Ş8 ortak-atıf ağı ---
import re
DOI_RE = re.compile(r'DOI\s+(10\.\d{4,9}/[^\s,;\]\}]+)', re.I)
def split_refs(cr):
    return [p.strip().rstrip('.') for p in re.split(r'(?<=\.)\s+(?=[A-Z\[])', cr or "") if p.strip()]
def ref_key(ref):
    m = DOI_RE.search(ref)
    if m: return "doi:" + m.group(1).rstrip('.').lower().replace('\\','')
    f = [x.strip() for x in ref.split(',')]
    if len(f) >= 3 and re.fullmatch(r'\d{4}', f[1]):
        return f"{f[0].lower()}|{f[1]}|{f[2].lower()}"[:90]
def ref_label(ref):
    f = [x.strip() for x in ref.split(',')]
    return f"{f[0]} {f[1]}" if len(f) >= 2 else ref[:24]
rsets, rlab = [], {}
for r in R:
    s = set()
    for ref in split_refs(g(r, "Cited-References")):
        k = ref_key(ref)
        if k: s.add(k); rlab.setdefault(k, ref_label(ref))
    rsets.append(s)
Gc, cf = build_cooc(rsets, 6)
for n in Gc.nodes(): Gc.nodes[n]["lab"] = rlab.get(n, n)[:22]
stats["ortak-atıf"] = draw_net(Gc, "S08_ortak_atif_agi", label_key="lab",
                               figsize=(8.5, 7.5), label_top=28, fontsize=6, edge_min=4)

# --- Ş9 yazar ağı ---
asets = [{a.strip() for a in g(r, "Author").split(" and ") if a.strip()} for r in R]
Ga, _ = build_cooc(asets, 4)
for n in Ga.nodes(): Ga.nodes[n]["lab"] = n.split(",")[0]
stats["yazar"] = draw_net(Ga, "S09_yazar_agi", label_key="lab", figsize=(7.5, 6), fontsize=7)

# --- Ş10 Kleinberg patlamaları ---
BURSTS = [("Multiparametrik MRG", 2020, 2022), ("Tanısal doğruluk", 2021, 2023),
          ("Radikal sistektomi", 2022, 2025)]
fig, ax = plt.subplots(figsize=(7, 2.6))
for i, (lab, a, b) in enumerate(BURSTS):
    ax.barh(i, b - a + 1, left=a, height=0.45, color=C[i])
ax.set_yticks(range(len(BURSTS))); ax.set_yticklabels([b[0] for b in BURSTS])
ax.invert_yaxis(); ax.set_xlim(2016, 2026); ax.set_xticks(range(2016, 2027, 2))
ax.set_xlabel("Yıl"); ax.grid(axis="y", visible=False)
save(fig, "S10_atif_patlamalari")

# --- Ş11 duyarlılık ---
fig, ax = plt.subplots(figsize=(7, 3.4))
q = ["Sorgu 2\n(eski)", "Sorgu 1\n(genişletilmiş)", "Sorgu 3\n(hastalık bloğu)"]
ham = [58.1, 60.1, 80.4]; duz = [63.2, 65.4, 87.5]
xs = range(len(q))
ax.bar([x - 0.19 for x in xs], ham, 0.38, label="Ham (n=148)", color=C[0])
ax.bar([x + 0.19 for x in xs], duz, 0.38, label="Belge türü uygun (n=136)", color=C[1])
ax.set_xticks(list(xs)); ax.set_xticklabels(q)
ax.set_ylabel("Duyarlılık (%)"); ax.legend(); ax.grid(axis="x", visible=False)
ax.set_ylim(0, 100)
save(fig, "S11_duyarlilik")

# --- Ş12 ticari testler ---
T = [("UroVysion",13,3),("ImmunoCyt/uCyt+",14,3),("BTA stat/TRAK",12,4),("NMP22/BladderChek",12,2),
     ("Cxbladder",9,2),("Bladder EpiCheck",8,3),("Xpert Bladder",5,3),("UroSEEK",3,2),
     ("ADXBLADDER",3,1),("Uromonitor",3,2),("UroMark",2,1),("AssureMDx",1,0)]
fig, ax = plt.subplots(figsize=(7, 4.6))
y = range(len(T))
ax.barh([v - 0.2 for v in y], [t[1] for t in T], 0.4, label="Havuzda (5.000)", color=C[0])
ax.barh([v + 0.2 for v in y], [t[2] for t in T], 0.4, label="Örneklemde (100)", color=C[3])
ax.set_yticks(list(y)); ax.set_yticklabels([t[0] for t in T]); ax.invert_yaxis()
ax.set_xlabel("Kayıt sayısı"); ax.legend(); ax.grid(axis="y", visible=False)
save(fig, "S12_ticari_testler")

print("\nAĞ PARAMETRELERİ (şekil altına yazılacak):")
print(f"  Yerleşim: Fruchterman-Reingold, seed={SEED}, k={K_SPRING}, iterations={ITERS}")
for k, (n, e, c, Q, d) in stats.items():
    print(f"  {k:14s}: {n} düğüm · {e} kenar · {c} küme · Q={Q:.3f} · yoğunluk={d:.3f}")
