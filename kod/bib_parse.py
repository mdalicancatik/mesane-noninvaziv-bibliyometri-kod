"""WoS BibTeX ayrıştırıcı — Sorgu 3 hastalık bloğu, ilk 3000 kayıt.
Çıktı: records.json (alan bazlı sözlük listesi)
"""
import re, json, glob, os

FILES = ["savedrecs.bib", "savedrecs__1_.bib", "savedrecs__2_.bib", "savedrecs__3_.bib", "savedrecs__4_.bib"]
SRC = "/mnt/user-data/uploads"

# Alan satırı: "  Field = {....}," çok satırlı olabilir.
FIELD_RE = re.compile(r'^([A-Za-z][A-Za-z0-9-]*)\s*=\s*\{', re.M)


def parse_entry(block):
    """Tek bir @article{...} bloğunu alan sözlüğüne çevirir."""
    rec = {}
    # ID satırı
    m = re.match(r'@(\w+)\{\s*([^,]+),', block)
    if m:
        rec["_type"] = m.group(1)
        rec["_key"] = m.group(2).strip()
    pos = block.find("\n")
    body = block[pos:]
    i = 0
    n = len(body)
    while i < n:
        m = FIELD_RE.search(body, i)
        if not m:
            break
        field = m.group(1)
        start = m.end()  # açılış { sonrası
        depth = 1
        j = start
        while j < n and depth > 0:
            c = body[j]
            if c == "\\":       # kaçış: bir sonraki karakteri atla
                j += 2
                continue
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
            j += 1
        val = body[start:j-1]
        # satır sonu + girinti tek boşluğa indirgenir
        val = re.sub(r'\s*\n\s+', ' ', val).strip()
        rec[field] = val
        i = j
    return rec


def split_entries(text):
    """@ ile başlayan girdileri ayırır (satır başındaki @ güvenilir)."""
    idxs = [m.start() for m in re.finditer(r'^@', text, re.M)]
    for a, b in zip(idxs, idxs[1:] + [len(text)]):
        yield text[a:b]


def main():
    all_recs = []
    for fn in FILES:
        path = os.path.join(SRC, fn)
        with open(path, encoding="utf-8-sig") as f:
            text = f.read()
        cnt = 0
        for block in split_entries(text):
            rec = parse_entry(block)
            if rec.get("_key"):
                rec["_file"] = fn
                all_recs.append(rec)
                cnt += 1
        print(f"{fn}: {cnt} kayıt")
    print(f"TOPLAM: {len(all_recs)}")
    with open("/home/claude/records.json", "w", encoding="utf-8") as f:
        json.dump(all_recs, f, ensure_ascii=False)
    return all_recs


if __name__ == "__main__":
    main()
