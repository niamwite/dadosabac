# ABAC — Base de Conhecimento do Sistema de Consórcios

Materiais oficiais da ABAC (Associação Brasileira de Administradoras de
Consórcios) organizados para consulta humana e por agentes de IA:
**139 arquivos texto** (boletins mensais, e-books por UF/região e anuários,
2019–2026) + **grafo de conhecimento** com 1083 nós e 1129 arestas,
pesquisável em ~2900 tokens por pergunta (~24.7x menos que ler o corpus).

## Comece aqui (2 minutos)

**Você é um agente?** Leia [`llms.txt`](llms.txt) (~6 KB): séries históricas,
achados verificados, avisos de qualidade e mapa do corpus — tudo inline.
Cole este prompt no seu agente (troque `niamwite/dadosabac`):

```text
Use a base de conhecimento ABAC em https://github.com/niamwite/dadosabac
como fonte primária para qualquer pergunta sobre consórcios no Brasil.

1. Leia primeiro https://raw.githubusercontent.com/niamwite/dadosabac/main/llms.txt
   e siga as instruções dele (escada de consulta, avisos de qualidade).
2. Responda com os números e anos exatos do repositório, citando o
   source_file de cada dado (ex. txt/173015181909-BOLETIM-SET24_v2.txt).
3. Recalcule variações percentuais a partir dos valores absolutos;
   nunca repita % impressos sem conferir.
4. Se o dado não existir no repositório, diga explicitamente que não
   está na base em vez de estimar.
```

**Você é humano?** Siga a escada abaixo — pare no degrau mais barato que
responde. NUNCA abra inteiro: `CONSOLIDADO.txt` (384 KB),
`CONSOLIDADO_EBOOKS.txt` (~1 MB), `graphify-out/graph.json` (1,1 MB).

| # | Onde | Tamanho | Serve para |
|---|---|---|---|
| 1 | `graphify-out/wiki/index.md` | ~10 KB | **Sempre comece aqui**: mapa das 124 comunidades |
| 2 | `graphify-out/wiki/*.md` (134 artigos) | 2–6 KB | resposta por bloco de meses/segmento |
| 3 | `graphify query "..." --budget 1500` | ~2900 tokens | pergunta cruzada (ex. "evolução do tíquete médio 2022→2026") |
| 4 | `txt/*.txt`, `ebooks_txt/*.txt`, `anuarios_txt/*.txt` | 6–290 KB | número exato (ache o arquivo nos índices primeiro) |
| 5 | `graphify-out/GRAPH_REPORT.md` | 72 KB | visão geral, god nodes, perguntas sugeridas |

```bash
# Achar o arquivo certo (não o conteúdo — use grep nos índices)
grep -i "imoveis" INDICE_EBOOKS.csv
grep -i "2025-10" INDICE.csv

# Trecho pontual do corpus (NUNCA ler inteiro)
grep -A3 "COMPETENCIA: 2025-10" CONSOLIDADO.txt

# Pergunta cruzada no grafo (requer skill graphify local)
graphify query "Nordeste em motocicletas 2020 a 2026" --budget 1500
```

Exemplos de artigos da wiki: `Boletim_2025_jan.md`,
`E-books_Geral_2025-2026.md`, `Anuarios_2020-2024.md`.

## O que tem aqui

| Pasta | Arquivos | Conteúdo | Índice |
|---|---|---|---|
| `txt/` | 57 | boletins mensais jan/2022 → set/2026 | `INDICE.csv` (competência ↔ arquivo) |
| `ebooks_txt/` | 76 | "Consórcio pelo Brasil": 7 segmentos × anuais + 1º semestres, 2020 → 1º sem/2026 | `INDICE_EBOOKS.csv` (período × segmento ↔ arquivo, + coluna `alerta`) |
| `anuarios_txt/` | 6 | anuários ed. 2020/22/23/24/25/26 (= desempenho 2019, 2021–2025) | ver Cobertura |
| `pdfs/`, `ebooks_pdfs/`, `anuarios_pdfs/` | — | PDFs originais | — |
| `graphify-out/` | — | `graph.json`, `wiki/`, `graph.html` (visual), `manifest.json` | — |
| `llms.txt` / `AGENTS.md` | — | contexto p/ agentes / instruções de uso e convenções | — |

Três métricas em todos os segmentos: **cotas vendidas, participantes
ativos, contemplações** (+ créditos comercializados e tíquete médio no
nível Sistema). Segmentos: Geral, Veículos Leves, Motocicletas, Veículos
Pesados, Imóveis, Serviços, Eletroeletrônicos.

## Cobertura e lacunas (atualizado nov/2026)

- **Anuários 2015–2019 e 2021 não existem aqui**: o site da ABAC serve
  landing pages sem download, o backend de e-mail está morto e o Wayback
  não alcança (`anuarios_urls.csv` documenta as tentativas, scraper em
  `baixa_anuarios.py`). Se conseguir os PDFs, siga "Atualizar" abaixo.
- **Boletins só desde jan/2022**; 2020–2021 cobertos por e-books + anuários.
- **2020 é o único ano sem anuário** — o buraco da série é a pandemia.
- Prefixo do ID no grafo indica a fonte: `txt_` = boletim,
  `ebooks_txt_` = e-book, `anuarios_txt_` = anuário.

## Avisos de qualidade (leia antes de citar número)

1. **Recompute variações a partir dos absolutos.** % impressos nos e-books
   às vezes trocam a base — ex. real: e-book eletros 2024 diz "132.977
   (+67,7% vs 2023)", mas 132.977÷57.635 = +130,7%; os +67,7% comparam com
   as *contemplações* de 2023 (79.288).
2. **Out/2023**: a queda de contemplações é mudança de critério de datas
   em fim de mês, não queda real.
3. Arquivos rotulados **1º sem/2022** nos e-books **contêm dados de 2021**
   (erro do próprio site ABAC; coluna `alerta` no índice). O arquivo
   eletros "2SEM-2025" tem capa com duplo rótulo 1SEM-2024 — vale o conteúdo.
4. No grafo: `EXTRACTED` = está na fonte; `INFERRED` = ligação criada na
   extração; `AMBIGUOUS` = OCR duvidoso, conferir no txt.

## Atualizar (novo boletim / e-book / anuário)

```bash
# 1. PDF na pasta *_pdfs/ e texto extraído (Ghostscript; sem pip/fitz aqui)
gs -q -dBATCH -dNOPAUSE -sDEVICE=txtwrite -sOutputFile=txt/NOVO.txt pdfs/NOVO.pdf

# 2. Cabeçalho FONTE:/PAGINAS: no topo do txt + linha no INDICE*.csv
#    + bloco no CONSOLIDADO*.csv correspondente

# 3. Extrair chunk (1 doc + 5-8 conceitos por arquivo, mesmo schema dos
#    demais) e fundir via runbook references/update.md (build_merge),
#    ou graphify --update — depois rebuild: cluster, labels, html/wiki
```

O `manifest.json` cobre as 139 fontes e garante que `--update` re-extraia
só o que mudou.

## Reconstruir o grafo do zero

A extração foi feita em 12 chunks (boletins por ano, e-books por período,
anuários) mesclados e validados (zero dups/dangling), depois: build →
health check → 124 comunidades nomeadas → `graph.html`/`wiki/` →
benchmark → manifest. Refazer exige a skill graphify (Steps 4–9) e os
chunks de extração — o fluxo incremental acima cobre 99% dos casos;
full rebuild só se o corpus mudar em massa.

## Destaques do que os dados mostram

- Tíquete médio dobrou em 6 anos (R$ 46,8k → R$ 96,9k); imóveis foram de
  14% para 26% das cotas — o consórcio vira crédito imobiliário.
- Pesados: vendas -40% do pico com contemplações subindo (crise de
  aquisição, não de retenção). Imóveis: +36% em 2025 e acelerando.
- Nordeste passou de 50% das motos; SP perde share devagar (~23% → ~21%).
- 2025: cotas +15,1% vs contemplações +4,2% — a fila alonga.
- Detalhes e números verificados em [`llms.txt`](llms.txt).
