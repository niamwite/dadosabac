import csv, html as ihtml, re, zipfile
from pathlib import Path
from urllib.request import Request, urlopen

UA = {"User-Agent": "Mozilla/5.0"}


def get(url, binary=False):
    req = Request(url, headers=UA)
    with urlopen(req, timeout=120) as r:
        data = r.read()
        return data if binary else data.decode("utf-8", "replace")


NEED = [
    # (periodo, segmento, sitemap-slug)
    *[(f"Jan-Dez/2023", s, f"e-books-{s}-jan-dez-2023") for s in
      ["sistema-em-geral", "veiculos-leves", "veiculos-pesados", "motocicletas", "imoveis", "servicos", "eletroeletronicos", "baixar-todos"]],
    *[(f"Jan-Dez/2022", s, f"e-books-{s}-jan-dez-2022") for s in
      ["veiculos-leves", "veiculos-pesados", "motocicletas", "servicos", "eletroeletronicos", "baixar-todos"]],
    *[(f"1o-Sem/2022", s, f"e-books-{s}-1o-semestre-2022") for s in
      ["sistema-em-geral", "veiculos-leves", "veiculos-pesados", "motocicletas", "imoveis", "servicos", "eletroeletronicos"]],
    *[(f"Jan-Dez/2021", s, f"e-books-{s}-jan-dez-2021") for s in
      ["sistema-de-geral", "veiculos-leves", "veiculos-pesados", "motocicletas", "imoveis", "servicos", "eletroeletronicos", "baixar-todos"]],
    *[(f"1o-Sem/2021", s, f"e-books-{s}-1o-semestre-2021") for s in
      ["sistema-em-geral", "veiculos-leves", "veiculos-pesados", "motocicletas", "imoveis", "servicos", "baixar-todos"]],
]

Path("ebooks_pdfs").mkdir(exist_ok=True)
dl = []
for per, seg, slug in NEED:
    try:
        page = get(f"https://abac.org.br/sistema-downloads/{slug}/")
        m = re.search(r"\?wpdmdl=\d+[^\"'\s]*", page)
        assert m, "sem link wpdmdl"
        link = ihtml.unescape("https://abac.org.br/sistema-downloads/" + slug + "/" + m.group(0))
        fn = re.search(r"filename=([^&]+)", link).group(1)
        dest = Path("ebooks_pdfs") / f"abac-{slug}__{fn}"
        if not dest.exists():
            dest.write_bytes(get(link, binary=True))
        if dest.suffix == ".zip":
            with zipfile.ZipFile(dest) as z:
                z.extractall("ebooks_pdfs")
            inner = ", ".join(z.namelist())
        else:
            inner = ""
        dl.append((per, seg, slug, dest.name, link, "ok", inner))
        print("OK", dest.name, dest.stat().st_size // 1024, "KB", inner[:80])
    except Exception as e:
        dl.append((per, seg, slug, "", "", f"ERRO: {e}", ""))
        print("ERRO", slug, str(e)[:120])

with open("ebooks_urls2.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["periodo", "segmento", "slug", "arquivo", "asset_url", "status", "zip_inner"])
    w.writerows(dl)
print("done:", sum(1 for r in dl if r[5] == "ok"), "/", len(dl))
