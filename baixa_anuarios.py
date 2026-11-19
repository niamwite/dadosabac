import base64, csv, re
from pathlib import Path
from urllib.request import Request, urlopen

UA = {"User-Agent": "Mozilla/5.0"}
BASE = "https://materiais.abac.org.br"


def get(url, binary=False):
    req = Request(url, headers=UA)
    with urlopen(req, timeout=60) as r:
        d = r.read()
        return d if binary else d.decode("utf-8", "replace")


SLUGS = [
    ("2026", "anuario-do-sistema-de-consorcios-2026"),
    ("2025", "lp-anuario-do-sistema-de-consorcios-2025"),
    ("2024", "lp-anuario-do-sistema-de-consorcios-2024"),
    ("2023", "lp-anuario-do-sistema-de-consorcios-2023"),
    ("2022", "anuario-do-sistema-de-consorcios-2022"),
    ("2021", "anuario-2021-sistema-de-consorcios"),
    ("2020", "anuario-sistema-de-consorcios-2020"),
    ("2019", "anuario-sistema-de-consorcios-2019"),
    ("2018", "anuario-sistema-consorcios-2017"),
    ("2017", "anuario-sistema-consorcios-2016"),
    ("2016", "anuario-sistema-consorcios-2015"),
    ("2015", "anuario-sistema-consorcios-2014"),
]

Path("anuarios_pdfs").mkdir(exist_ok=True)
dl = []
for ano, slug in SLUGS:
    try:
        lp = get(BASE + "/" + slug)
        m = re.search(r'data-asset-action\s*=\s*"([^"]+)"', lp)
        assert m and m.group(1).strip(), "sem asset-action"
        asset = base64.b64decode(re.sub(r"\s+", "", m.group(1))).decode().strip()
        fn = asset.split("/")[-1]
        dest = Path("anuarios_pdfs") / f"anuario-{ano}__{fn}"
        if not dest.exists():
            req = Request(asset, headers=UA)
            with urlopen(req, timeout=180) as r, open(dest, "wb") as f:
                f.write(r.read())
        dl.append((ano, slug, dest.name, asset, "ok"))
        print("OK", ano, dest.name, dest.stat().st_size // 1024, "KB")
    except Exception as e:
        dl.append((ano, slug, "", "", f"ERRO: {e}"))
        print("ERRO", ano, slug, str(e)[:100])

with open("anuarios_urls.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["ano", "slug", "arquivo", "asset_url", "status"])
    w.writerows(dl)
print("done:", sum(1 for r in dl if r[4] == "ok"), "/", len(dl))
