import base64, csv, re, sys
from pathlib import Path
from urllib.request import Request, urlopen

UA = {"User-Agent": "Mozilla/5.0"}
BASE = "https://materiais.abac.org.br"


def get(url):
    req = Request(url, headers=UA)
    with urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


html = get(BASE + "/e-books-estaduais")
toks = re.findall(
    r'(1º Semestre \d{4}|Jan-Dez/\d{4})|<strong[^>]*>([^<]{3,60})</strong>|href="(https://materiais\.abac\.org\.br/e-book-[^"]+)"',
    html,
)
rows, period, seg = [], None, None
for per, label, href in toks:
    if per:
        period = per
    elif label:
        seg = label.strip()
    elif href:
        assert period and seg, (period, seg, href)
        rows.append((period, seg, href))
        seg = None

print(f"{len(rows)} links em {len(set(r[0] for r in rows))} periodos")
assert len(rows) == 96, len(rows)

Path("ebooks_pdfs").mkdir(exist_ok=True)
dl = []
for per, seg, url in rows:
    slug = url.rstrip("/").split("/")[-1]
    try:
        lp = get(url)
        m = re.search(r'data-asset-action\s*=\s*"([^"]+)"', lp)
        assert m, "sem asset-action"
        asset = base64.b64decode(re.sub(r"\s+", "", m.group(1))).decode().strip()
        fn = asset.split("/")[-1]
        dest = Path("ebooks_pdfs") / f"{slug}__{fn}"
        if not dest.exists():
            req = Request(asset, headers=UA)
            with urlopen(req, timeout=180) as r, open(dest, "wb") as f:
                f.write(r.read())
        dl.append((per, seg, slug, dest.name, asset, "ok"))
        print("OK", dest.name, dest.stat().st_size // 1024, "KB")
    except Exception as e:
        dl.append((per, seg, slug, "", "", f"ERRO: {e}"))
        print("ERRO", slug, e)

with open("ebooks_urls.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["periodo", "segmento", "slug", "arquivo", "asset_url", "status"])
    w.writerows(dl)
print("done:", sum(1 for r in dl if r[5] == "ok"), "/", len(dl))
