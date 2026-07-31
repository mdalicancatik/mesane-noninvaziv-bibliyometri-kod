"""Bibliyometrik analiz — ağlar, ülke/kurum, iş birliği, öz-atıf.
Parametreler §5'te kilitlenmiştir:
  Anahtar kelime eşiği >=4 makale · Ortak-atıf >=6 · Ülke >=3 · Yazar >=4
  Kümeleme: Clauset-Newman-Moore açgözlü modülerlik
  Yerleşim: Fruchterman-Reingold (spring), seed=42
  Ülke sayımı: tam sayım (her ülkeye 1 kredi, çoklu adres)
"""
import json, re, itertools
from collections import Counter, defaultdict
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities, modularity
from thesaurus import canon, GENERIC

SEED = 42
top = json.load(open('/home/claude/top100.json', encoding='utf-8'))
recs = json.load(open('/home/claude/records.json', encoding='utf-8'))
def g(r, k): return (r.get(k, '') or '')

COUNTRIES = {
 "usa":"USA","peoples r china":"China","china":"China","england":"United Kingdom",
 "scotland":"United Kingdom","wales":"United Kingdom","north ireland":"United Kingdom",
 "italy":"Italy","japan":"Japan","spain":"Spain","south korea":"South Korea",
 "portugal":"Portugal","france":"France","canada":"Canada","austria":"Austria",
 "netherlands":"Netherlands","germany":"Germany","iran":"Iran","denmark":"Denmark",
 "taiwan":"Taiwan","egypt":"Egypt","belgium":"Belgium","australia":"Australia",
 "brazil":"Brazil","poland":"Poland","new zealand":"New Zealand","russia":"Russia",
 "greece":"Greece","turkey":"Turkiye","turkiye":"Turkiye","israel":"Israel",
 "sweden":"Sweden","switzerland":"Switzerland","norway":"Norway","finland":"Finland",
 "india":"India","singapore":"Singapore","ireland":"Ireland","czech republic":"Czechia",
 "hungary":"Hungary","mexico":"Mexico","chile":"Chile","argentina":"Argentina",
 "saudi arabia":"Saudi Arabia","u arab emirates":"UAE","thailand":"Thailand",
 "malaysia":"Malaysia","south africa":"South Africa","serbia":"Serbia","croatia":"Croatia",
 "romania":"Romania","bulgaria":"Bulgaria","slovenia":"Slovenia","slovakia":"Slovakia",
 "lithuania":"Lithuania","latvia":"Latvia","estonia":"Estonia","luxembourg":"Luxembourg",
 "colombia":"Colombia","peru":"Peru","pakistan":"Pakistan","bangladesh":"Bangladesh",
 "indonesia":"Indonesia","vietnam":"Vietnam","philippines":"Philippines","jordan":"Jordan",
 "lebanon":"Lebanon","qatar":"Qatar","kuwait":"Kuwait","nigeria":"Nigeria","kenya":"Kenya",
 "morocco":"Morocco","tunisia":"Tunisia","algeria":"Algeria","ukraine":"Ukraine",
 "belarus":"Belarus","kazakhstan":"Kazakhstan","cyprus":"Cyprus","iceland":"Iceland",
 "malta":"Malta","uruguay":"Uruguay","venezuela":"Venezuela","ecuador":"Ecuador",
 "cuba":"Cuba","costa rica":"Costa Rica","panama":"Panama","hong kong":"China",
 "macau":"China", "u s a":"USA",
}
ENTRY = re.compile(r'(?<=\.)\s+(?=[A-Z])')

def country_of(seg):
    s = seg.strip().rstrip('.').lower()
    if s.endswith(" usa") or s == "usa":
        return "USA"
    return COUNTRIES.get(s)

def countries_of_record(r):
    """Tam sayım: kayıttaki her benzersiz ülkeye 1 kredi."""
    out = set()
    for e in ENTRY.split(g(r, 'Affiliation')):
        e = e.strip().rstrip('.')
        if not e:
            continue
        c = country_of(e.split(',')[-1])
        if c:
            out.add(c)
    return out

def institutions_of_record(r):
    return {s.strip() for s in g(r, 'Affiliations').split(';') if s.strip()}

def authors_of_record(r):
    return [a.strip() for a in g(r, 'Author').split(' and ') if a.strip()]

def keywords_of_record(r, drop_generic):
    ks = {s.strip().lower() for s in (g(r, 'Keywords') + "; " + g(r, 'Keywords-Plus')).split(";") if s.strip()}
    c = {canon(k) for k in ks}
    return {k for k in c if not (drop_generic and k in GENERIC)}


def build_cooc(sets, threshold):
    """Eş-oluşum ağı: düğüm = eşik üstü terim, kenar = birlikte geçme sayısı."""
    freq = Counter()
    for s in sets:
        freq.update(s)
    nodes = {k for k, v in freq.items() if v >= threshold}
    G = nx.Graph()
    for k in nodes:
        G.add_node(k, freq=freq[k])
    for s in sets:
        for a, b in itertools.combinations(sorted(s & nodes), 2):
            if G.has_edge(a, b):
                G[a][b]['weight'] += 1
            else:
                G.add_edge(a, b, weight=1)
    return G, freq


def describe(G, name):
    if G.number_of_nodes() == 0:
        print(f"{name}: boş"); return None
    comms = list(greedy_modularity_communities(G, weight='weight'))
    Q = modularity(G, comms, weight='weight')
    dens = nx.density(G)
    print(f"{name}: {G.number_of_nodes()} düğüm · {G.number_of_edges()} kenar · "
          f"{len(comms)} küme · Q={Q:.3f} · yoğunluk={dens:.3f}")
    for i, c in enumerate(sorted(comms, key=len, reverse=True), 1):
        top_n = sorted(c, key=lambda n: -G.nodes[n].get('freq', 0))[:7]
        print(f"    küme {i} ({len(c)}): " + ", ".join(top_n))
    return comms


if __name__ == "__main__":
    R = [recs[x['rank'] - 1] for x in top]

    print("=" * 68)
    print("ANAHTAR KELİME EŞ-OLUŞUM AĞI (eşik >=4 makale)")
    print("=" * 68)
    for drop in (False, True):
        sets = [keywords_of_record(r, drop) for r in R]
        G, freq = build_cooc(sets, 4)
        describe(G, f"  generik terimler {'ÇIKARILDI' if drop else 'DURUYOR'}")
        if drop:
            nx.write_gexf(G, '/home/claude/net_keyword.gexf')

    print()
    print("=" * 68)
    print("ÜLKE İŞ BİRLİĞİ AĞI (eşik >=3 makale, tam sayım)")
    print("=" * 68)
    csets = [countries_of_record(r) for r in R]
    nocountry = sum(1 for s in csets if not s)
    print(f"  ülke çıkarılamayan kayıt: {nocountry}")
    Gc, cfreq = build_cooc(csets, 3)
    describe(Gc, "  ülke ağı")
    print("  en üretken ülkeler:", ", ".join(f"{k} ({v})" for k, v in cfreq.most_common(10)))
    nx.write_gexf(Gc, '/home/claude/net_country.gexf')

    print()
    print("=" * 68)
    print("İŞ BİRLİĞİ TÜRÜ")
    print("=" * 68)
    kinds = Counter()
    for r, cs in zip(R, csets):
        insts = institutions_of_record(r)
        if len(cs) > 1:
            kinds["uluslararası"] += 1
        elif len(insts) > 1:
            kinds["ulusal (çok kurumlu)"] += 1
        elif len(authors_of_record(r)) > 1:
            kinds["yerel (tek kurum)"] += 1
        else:
            kinds["tek yazar"] += 1
    for k, v in kinds.most_common():
        print(f"  {v:3d}  {k}")

    print()
    print("=" * 68)
    print("YAZAR AĞI (eşik >=4 makale)")
    print("=" * 68)
    asets = [set(authors_of_record(r)) for r in R]
    afreq = Counter()
    for s in asets:
        afreq.update(s)
    print("  en üretken yazarlar:", ", ".join(f"{k} ({v})" for k, v in afreq.most_common(10)))
    Ga, _ = build_cooc(asets, 4)
    describe(Ga, "  yazar ağı")

    print()
    print("=" * 68)
    print("KURUM (eşik >=3 makale)")
    print("=" * 68)
    ifreq = Counter()
    for r in R:
        ifreq.update(institutions_of_record(r))
    for k, v in ifreq.most_common(12):
        print(f"  {v:3d}  {k}")
