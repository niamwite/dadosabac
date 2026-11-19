# ABAC — Base de Conhecimento (boletins 2022-01 → 2026-09 + e-books + anuários)

139 arquivos: 57 boletins mensais (`txt/`, índice `INDICE.csv`,
tudo junto em `CONSOLIDADO.txt`) + 76 e-books por UF/região
(`ebooks_txt/`, índice `INDICE_EBOOKS.csv`, tudo junto em
`CONSOLIDADO_EBOOKS.txt` ~1 MB) + 6 anuários (`anuarios_txt/`:
2020, 2022, 2023, 2024, 2025 e 2026 = desempenho 2019, 2021–2025;
faltam 2015–2019 e 2021 — ver seção Anuários).

## Regra de ouro

NUNCA abra `CONSOLIDADO.txt` (384 KB), `CONSOLIDADO_EBOOKS.txt`
(~1 MB) nem `graphify-out/graph.json` (1,1 MB) inteiros. Siga a
escada abaixo — pare no degrau mais barato que responde.

## Escada de consulta (barato → caro)

1. `graphify-out/wiki/index.md` (~10 KB) — mapa das 124 comunidades + god nodes.
   Serve para: achar ONDE está o assunto (qual período/segmento/fonte).
2. Um artigo da wiki (~2–6 KB cada, 134 no total) — ex. `Boletim_2025_jan.md`,
   `E-books_Geral_2025-2026.md`, `Anuarios_2020-2024.md`.
   Serve para: valores mensais + variações MoM/YoY de um bloco.
3. `graphify query "<pergunta>" --budget 1500` — busca no grafo
   (1083 nós, 1129 arestas; ~2900 tokens/resposta, 24.7x mais barato
   que ler o corpus). Serve para: perguntas cruzadas
   ("quando X bateu recorde?", "evolução do tíquete médio 2022→2026",
   "Nordeste em motos 2020→2026").
4. Um `txt/<arquivo>.txt` (~6 KB) — localize via `INDICE.csv`
   (competência → arquivo); e-books via `INDICE_EBOOKS.csv`
   (período × segmento → arquivo em `ebooks_txt/`). Serve para: número
   exato de um mês/período específico.
5. `graphify-out/GRAPH_REPORT.md` (72 KB) — god nodes, conexões
   surpreendentes, perguntas sugeridas. Serve para: visão geral/auditoria.

## Mapa dos arquivos

| Arquivo | Tamanho | Quando usar |
|---|---|---|
| `graphify-out/wiki/index.md` | ~10 KB | SEMPRE comece aqui |
| `graphify-out/wiki/*.md` (134) | 2–6 KB | resposta por bloco de meses/segmento |
| `txt/*.txt` (57) | ~6 KB cada | mês específico (via `INDICE.csv`) |
| `ebooks_txt/*.txt` (76) | ~6–14 KB cada | período×segmento (via `INDICE_EBOOKS.csv`) |
| `anuarios_txt/*.txt` (6) | ~100–290 KB cada | anuário (edição 2020/22/23/24/25/26) |
| `INDICE.csv` | 2 KB | mapear competência ↔ arquivo |
| `INDICE_EBOOKS.csv` | ~10 KB | mapear período×segmento ↔ arquivo (+`alerta`) |
| `graphify-out/GRAPH_REPORT.md` | 72 KB | panorama + perguntas prontas |
| `graphify-out/graph.html` | — | só para humanos (navegação visual) |
| `CONSOLIDADO.txt` | 384 KB | PROIBIDO ler inteiro; `grep` pontual ok |
| `pdfs/*.pdf` (57) | 12 MB | só se o txt parecer corrompido |

## Convenções dos dados

- Nós do grafo carregam valores no `label`: ex.
  `"Cotas comercializadas SET/25: 507.141 (MoM +15,6%; YoY +29,6%)"`.
- `source_file` = prova. Cite o arquivo ao afirmar um número.
- Confiança: `EXTRACTED` = está na fonte; `INFERRED` = ligação temporal/
  similaridade criada na extração; `AMBIGUOUS` = OCR duvidoso — confira
  no txt antes de usar.
- Série histórica 2026 vem com acumulados no label
  (ex. `"acumulado Jan-Set 4.372.215 (+14,3% vs 2025)"`).
- Recordes: wiki `Recordes_historicos_transversal.md` + hiperarcos
  `recorde_*` no grafo (por ano + marcos mensais).
- Furo conhecido: Out/2023 tem queda de contemplações por mudança de
  critério de datas em fim de mês (não é queda real) — ver hiperarco
  `170128703310_boletim_out23_queda_metodologica`.

## Comandos

```bash
graphify query "evolução das contemplações 2022 a 2026" --budget 1500
graphify query "recorde de cotas por ano" --budget 1000
grep -i "imoveis" INDICE.csv            # achar meses (não o conteúdo)
grep -A3 "COMPETENCIA: 2025-10" CONSOLIDADO.txt   # trecho pontual ok
```

## E-books "Consórcio pelo Brasil" (2020 → 1º sem 2026)

76 arquivos únicos com dados por UF/região (`ebooks_txt/`, índice
`INDICE_EBOOKS.csv`, tudo junto em `CONSOLIDADO_EBOOKS.txt` ~1 MB).
Períodos: anuais (Jan-Dez) + 1º semestres, 7 segmentos cada.

- Achar arquivo: `grep -i "imoveis" INDICE_EBOOKS.csv`
- Coluna `alerta`: inconsistências do próprio site ABAC. Principais:
  - arquivos rotulados `1o-Sem/2022` CONTÊM DADOS DE 2021 (site serve o
    arquivo errado; os e-books de 1º sem/2022 não existem de verdade);
  - "Baixar Todos" de vários períodos apontam para o bundle errado.
- `CONSOLIDADO_EBOOKS.txt` também é PROIBIDO ler inteiro (1 MB);
  `grep -A3 "PERIODO: Jan-Dez/2023"` para trecho pontual.
- E-books ESTÃO no grafo (comunidades `E-books *`, nós `ebooks_txt_*`).
  Prefixo do ID indica a fonte: `txt_` = boletim, `ebooks_txt_` = e-book,
  `anuarios_txt_*` = anuário.

## Anuários (6 no grafo; 2015–2019 e 2021 pendentes)

`anuarios_txt/` tem 6 arquivos — edições 2020, 2022, 2023, 2024, 2025,
2026 (anos de referência 2019, 2021, 2022, 2023, 2024, 2025),
comunidades `Anuarios 2020-2024` + `Anuarios 2025-2026` no grafo.
Faltam 2015–2019 e 2021 (landing pages sem `data-asset-action`,
backend de e-mail morto, Wayback inalcançável; URLs em
`anuarios_urls.csv`, scraper em `baixa_anuarios.py`). Extração de PDF:
`gs -sDEVICE=txtwrite` + cabeçalho `FONTE:/PAGINAS:` (sem pip/fitz
neste ambiente). Se o usuário fornecer os PDFs: extrair para
`anuarios_txt/`, extrair chunk e fundir via `references/update.md`
(build_merge) ou `graphify --update`.

## Ao atualizar (novos boletins/e-books/anuários)

1. Baixe o PDF em `pdfs/` (ou `ebooks_pdfs/`), extraia para `txt/`
   (ou `ebooks_txt/`) no mesmo padrão de nome.
2. Adicione a linha em `INDICE.csv` (ou `INDICE_EBOOKS.csv`) e o bloco
   no consolidado correspondente.
3. Rode `graphify --update` na raiz (re-extrai só o novo; manifest em
   `graphify-out/manifest.json` cobre as 139 fontes).
