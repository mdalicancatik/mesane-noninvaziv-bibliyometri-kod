"""Ortak-atıf ağı (>=6 makale), örneklem içi öz-atıf oranı, Kleinberg patlama analizi."""
import json, re, itertools, math
from collections import Counter, defaultdict
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities, modularity

top = json.load(open('/home/claude/top100.json', encoding='utf-8'))
recs = json.load(open('/home/claude/records.json', encoding='utf-8'))
def g(r, k): return (r.get(k, '') or '')

# ---------- kaynakça ayrıştırma ----------
DOI_RE = re.compile(r'DOI\s+(10\.\d{4,9}/[^\s,;\]\}]+)', re.I)

def split_refs(cr):
    """Kaynakça alanını tek tek referanslara böler."""
    if not cr:
        return []
    parts = re.split(r'(?<=\.)\s+(?=[A-Z\[])', cr)
    return [p.strip().rstrip('.') for p in parts if p.strip()]

def ref_key(ref):
    """Referansı tekilleştirme anahtarına çevirir: DOI varsa DOI, yoksa yazar+yıl+dergi."""
    m = DOI_RE.search(ref)
    if m:
        return "doi:" + m.group(1).rstrip('.').lower().replace('\\', '')
    f = [x.strip() for x in ref.split(',')]
    if len(f) >= 3 and re.fullmatch(r'\d{4}', f[1]):
        return f"{f[0].lower()}|{f[1]}|{f[2].lower()}"[:90]
    return None

def ref_label(ref):
    f = [x.strip() for x in ref.split(',')]
    if len(f) >= 3:
        return f"{f[0]} {f[1]}, {f[2][:26]}"
    return ref[:40]

R = [recs[x['rank'] - 1] for x in top]
ref_sets, labels = [], {}
for r in R:
    s = set()
    for ref in split_refs(g(r, 'Cited-References')):
        k = ref_key(ref)
        if k:
            s.add(k)
            labels.setdefault(k, ref_label(ref))
    ref_sets.append(s)

tot_refs = sum(len(s) for s in ref_sets)
print(f"Örneklemin toplam (tekil) kaynakça girdisi: {tot_refs}")
print(f"Benzersiz referans: {len(set().union(*ref_sets))}")

# ---------- ortak-atıf ağı ----------
freq = Counter()
for s in ref_sets:
    freq.update(s)
nodes = {k for k, v in freq.items() if v >= 6}
print(f"\nORTAK-ATIF AĞI (eşik >=6 makale): {len(nodes)} düğüm")
G = nx.Graph()
for k in nodes:
    G.add_node(k, freq=freq[k], label=labels.get(k, k)[:44])
for s in ref_sets:
    for a, b in itertools.combinations(sorted(s & nodes), 2):
        if G.has_edge(a, b):
            G[a][b]['weight'] += 1
        else:
            G.add_edge(a, b, weight=1)

comms = list(greedy_modularity_communities(G, weight='weight')) if G.number_of_edges() else []
Q = modularity(G, comms, weight='weight') if comms else float('nan')
print(f"  {G.number_of_nodes()} düğüm · {G.number_of_edges()} kenar · {len(comms)} küme "
      f"· Q={Q:.3f} · yoğunluk={nx.density(G):.3f}")
for i, c in enumerate(sorted(comms, key=len, reverse=True), 1):
    tn = sorted(c, key=lambda n: -G.nodes[n]['freq'])[:6]
    print(f"    küme {i} ({len(c)}):")
    for n in tn:
        print(f"        {G.nodes[n]['freq']:3d}× {G.nodes[n]['label']}")
nx.write_gexf(G, '/home/claude/net_cocitation.gexf')

print("\n  EN ÇOK ORTAK-ATIF ALAN 12 REFERANS:")
for k, v in freq.most_common(12):
    print(f"    {v:3d}×  {labels.get(k,k)[:70]}")

# ---------- örneklem içi öz-atıf ----------
print("\n" + "=" * 68)
print("ÖRNEKLEM İÇİ ÖZ-ATIF (§5 karar 8, (b) yolu)")
print("=" * 68)
own_dois = {}
for i, r in enumerate(R):
    d = g(r, 'DOI').strip().lower()
    if d:
        own_dois["doi:" + d] = i

def surnames(r):
    out = set()
    for a in g(r, 'Author').split(' and '):
        a = a.strip()
        if a:
            out.add(a.split(',')[0].strip().lower())
    return out

INIT_RE = re.compile(r'\s+[A-Z]{1,3}$')
def ref_surname(ref):
    """'Babjuk M 2017, EUR UROL' -> 'babjuk' ; 'van der Heijden AG 2020, ...' -> 'van der heijden'"""
    first = ref.split(',')[0].strip()
    first = re.sub(r'\s+\d{4}$', '', first)
    prev = None
    while prev != first:
        prev = first
        first = INIT_RE.sub('', first).strip()
    return first.lower()

sample_internal = 0      # örneklemdeki bir makaleye yapılan atıf
author_self = 0          # yazar örtüşmesi olan referans
for i, (r, s) in enumerate(zip(R, ref_sets)):
    mine = surnames(r)
    for k in s:
        if k in own_dois and own_dois[k] != i:
            sample_internal += 1
    for ref in split_refs(g(r, 'Cited-References')):
        first = ref_surname(ref)
        if first and first in mine:
            author_self += 1

print(f"  Toplam kaynakça girdisi                 : {tot_refs}")
print(f"  Örneklem içi atıf (100 makale birbirine): {sample_internal}"
      f"  (%{100*sample_internal/tot_refs:.2f})")
print(f"  Yazar öz-atıfı (ilk yazar soyadı örtüşen): {author_self}"
      f"  (%{100*author_self/tot_refs:.2f})")
print("  NOT: Bu GİDEN atıflar üzerinden hesaplanmıştır. WoS atıf sayıları GELEN")
print("       atıflardır; öz-atıf ayıklaması eksportta yok (§10).")

# ---------- Kleinberg patlama analizi ----------
print("\n" + "=" * 68)
print("KLEINBERG PATLAMA ANALİZİ (s=2, gamma=1, Viterbi; taban oran örnekleme orantılı)")
print("=" * 68)

def kleinberg_two_state(counts, expected, s=2.0, gamma=1.0):
    """İki durumlu Kleinberg otomatı, Viterbi ile en olası durum dizisi.

    KRİTİK (K9): `expected`, her yıl için BEKLENEN taban sayıdır ve örneklemin
    o yıldaki makale sayısıyla ORANTILI verilmelidir. Düz (yıla göre sabit) taban
    oran kullanılırsa, atıf eşikli örneklemin yıl dağılımı yüzünden neredeyse her
    terim erken yıllarda sahte patlama üretir.

    Durum 0: taban oran · Durum 1: s katı yüksek oran
    Maliyet = -log Poisson olabilirliği + gamma * yukarı geçiş cezası
    """
    n = len(counts)
    def nll(k, lam):
        lam = max(lam, 1e-9)
        return lam - k * math.log(lam) + math.lgamma(k + 1)
    C = [[0.0, 0.0] for _ in range(n)]
    P = [[0, 0] for _ in range(n)]
    for j in (0, 1):
        C[0][j] = nll(counts[0], expected[0] * (s if j else 1)) + (gamma if j else 0)
    for i in range(1, n):
        for j in (0, 1):
            best, arg = None, 0
            for k in (0, 1):
                cost = C[i-1][k] + (gamma * (j - k) if j > k else 0)
                if best is None or cost < best:
                    best, arg = cost, k
            C[i][j] = best + nll(counts[i], expected[i] * (s if j else 1))
            P[i][j] = arg
    st = 0 if C[n-1][0] <= C[n-1][1] else 1
    seq = [st]
    for i in range(n-1, 0, -1):
        st = P[i][st]
        seq.append(st)
    return seq[::-1]


from thesaurus import canon, GENERIC
YEARS = list(range(2016, 2026))
n_y = [0]*len(YEARS)                      # örneklemin yıllık makale sayısı
for x in top:
    n_y[YEARS.index(int(x['year']))] += 1
N = sum(n_y)
kw_year = defaultdict(lambda: [0]*len(YEARS))
kw_total = Counter()
for x, r in zip(top, R):
    y = int(x['year'])
    ks = {canon(s.strip().lower()) for s in (g(r,'Keywords')+"; "+g(r,'Keywords-Plus')).split(";") if s.strip()}
    ks = {k for k in ks if k not in GENERIC}
    for k in ks:
        kw_year[k][YEARS.index(y)] += 1
        kw_total[k] += 1

bursts = []
for k, series in kw_year.items():
    if kw_total[k] < 10:            # §5: toplam >=10
        continue
    expected = [kw_total[k] * n_y[i] / N for i in range(len(YEARS))]   # K9
    seq = kleinberg_two_state(series, expected)
    runs, i = [], 0
    while i < len(seq):
        if seq[i] == 1:
            j = i
            while j+1 < len(seq) and seq[j+1] == 1:
                j += 1
            runs.append((i, j))
            i = j+1
        else:
            i += 1
    for a, b in runs:
        if (b - a + 1) >= 3:        # §5: en az 3 yıl
            bursts.append((k, YEARS[a], YEARS[b], sum(series[a:b+1]), kw_total[k]))

print(f"  Aday terim (toplam >=10 makale): {sum(1 for k in kw_total if kw_total[k]>=10)}")
print(f"  Patlama saptanan terim (>=3 yıl): {len(bursts)}\n")
for k, y0, y1, n, tot in sorted(bursts, key=lambda z: -z[3]):
    print(f"    {k:34s} {y0}-{y1}  patlama içi {n}/{tot} makale")
