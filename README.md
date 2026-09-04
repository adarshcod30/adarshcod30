<div align="center">

<img src="assets/banner.png" alt="Adarsh Dwivedi — measured, explainable ML for problems that matter in India. A graph of 26 projects clustered into public-interest AI, trust and verification, agentic systems, quant and pipelines, and foundations." width="100%">

**[Orbweaver](https://github.com/adarshcod30/Orbweaver)** ·
**[KrishiMitra](https://github.com/adarshcod30/KrishiMitra)** ·
**[Vayu](https://github.com/adarshcod30/Vayu)** ·
**[Kadi](https://github.com/adarshcod30/Kadi)** ·
**[MargaDrishti](https://github.com/adarshcod30/MargaDrishti)** ·
**[every project →](PROJECTS.md)**

</div>

---

I build machine-learning systems for problems that already have victims — crop
loss, air quality, road capacity, fraud rings, misdiagnosis — and I try to build
them so that a sceptical reader can check every claim I make.

Three habits run through nearly all of it.

**Every number is reproducible.** One command regenerates the tables and the
figures from raw data. If a number appears in a README, a script put it there —
including the ones on this page.

**Every model says how sure it is, and is allowed to refuse.** Calibrated
confidence and selective abstention beat a confident guess on problems where
being wrong costs somebody something. Medicure-AI refuses when the evidence is
thin. Specledger abstains rather than inventing a spec. Orbweaver prints the
real customers it would wrongly sweep up next to every detection rate.

**Every limit is written down.** The negative results stay in the repository
next to the positive ones. MargaDrishti ships an audit of enforcement bias in
its own training data. The retinopathy work says on its front page that it is a
research prototype and not a medical device, because that is what it is.

<div align="center">

<img src="assets/timeline.png" alt="Timeline of 26 projects from October 2025 to September 2026, coloured by area, with the four early learning repositories marked in grey." width="100%">

</div>

## Selected work

### Public-interest AI

| Project | What it does |
|---|---|
| **[KrishiMitra](https://github.com/adarshcod30/KrishiMitra)** | Crop intelligence for Indian smallholders. CatBoost recommendations cross-checked against five years of government district returns, leaf-disease detection at 93.75% over 10,162 images, FAO-56 irrigation advisory, Soil Health Card baselines from 13.35M tests. 12 languages, deployed free |
| **[Vayu](https://github.com/adarshcod30/Vayu)** | National air-quality platform: LightGBM + CNN-LSTM forecasting, a 15,360-cell satellite grid, Gaussian-plume ROI ranking, and difference-in-differences verification that an intervention actually worked |
| **[Kadi](https://github.com/adarshcod30/Kadi)** | 59,985 siloed FIRs joined into one explainable link graph for the Karnataka State Police — entity resolution, 8 benchmarked models, evidence OCR, and a grounded bilingual (English / ಕನ್ನಡ) assistant |
| **[MargaDrishti](https://github.com/adarshcod30/MargaDrishti)** | Bengaluru road-capacity loss on one H3 × hourly substrate: 298k parking violations, 8k events, 8 model families — and a published audit of enforcement bias in the data itself |
| **[Diabetic-Retinopathy-Detection](https://github.com/adarshcod30/Diabetic-Retinopathy-Detection)** | Quality-aware retinopathy screening for rural India, with measured Grad-CAM localisation and a district programme simulation |
| **[Medicure-AI](https://github.com/adarshcod30/Medicure-AI)** | Photograph a medicine strip: composition, NPPA price check, Jan Aushadhi generic and interaction warnings — each with a calibrated confidence, and an honest refusal when the evidence is thin |

### Trust and verification

| Project | What it does |
|---|---|
| **[Orbweaver](https://github.com/adarshcod30/Orbweaver)** | Coordinated abuse rings are invisible order by order. Densest-subgraph extraction over a 35.7M-edge account graph finds them at 0.7292 precision against a 0.2242 base rate — and reports the cost in real customers, every time |
| **[artifact-repro-triage](https://github.com/adarshcod30/artifact-repro-triage)** | Checks whether a paper's repository contains what its README promises. 0% → 100% detection of fabricated file claims, across 742 artifacts |
| **[OpenForensics](https://github.com/adarshcod30/OpenForensics)** | Deepfake detection with a three-backbone ensemble, calibrated confidence and per-backbone Grad-CAM — the dashboard shows the evidence, not just the verdict |
| **[MedGuardX](https://github.com/adarshcod30/MedGuardX)** | Context-aware PII/PHI detection and masking for healthcare data: an engine on PyPI, a hardened FastAPI service, and an app on top |

### Agentic systems, quant and foundations

| Project | What it does |
|---|---|
| **[SmartAlloc](https://github.com/adarshcod30/SmartAlloc)** | A 7-agent LangGraph pipeline over linear programming that finds compute waste and predicts SLA bottlenecks before they land |
| **[Talent-Intelligence](https://github.com/adarshcod30/Talent-Intelligence-Candidate-Discovery-Platform)** | Ranks 100,000 candidates in under 18 seconds on CPU only, filters honeypots and fake profiles, and justifies every ranking factually |
| **[PrimeTradeDS](https://github.com/adarshcod30/PrimeTradeDS)** | 211K Hyperliquid trades against Bitcoin Fear/Greed sentiment — what actually moves trader behaviour, and what does not |
| **[Adaptive-Graph-Search-Suite](https://github.com/adarshcod30/Adaptive-Graph-Search-Suite)** | Graph traversal on realistic map topologies, built to be watched while it runs |

**[The full index, grouped by area →](PROJECTS.md)**

## How I work

```
Python · PyTorch · XGBoost / LightGBM / CatBoost · scikit-learn · igraph
FastAPI · Streamlit · Next.js / TypeScript · Docker · GitHub Actions
Google Cloud Run · Vercel · pandas / PyArrow · LangGraph
```

The stack matters less than the discipline around it: a temporal split that a
test enforces, a held-out set nothing touches, the false-positive cost printed
next to the detection rate, and a `FAILURES.md` recording what I got wrong on
the way there.

## This repository

The banner, the timeline and [PROJECTS.md](PROJECTS.md) are all generated from
the GitHub API, so none of them can quietly fall behind what I have actually
shipped:

```bash
make refresh    # pull the current repository list
make assets     # redraw the banner and the timeline
make index      # rewrite PROJECTS.md
make            # all three
```

It seemed dishonest to claim everything I build is reproducible and then
hand-maintain my own profile.

## Elsewhere

Computer science at **LNMIIT Jaipur**. Most of what I build ends up deployed
somewhere free, because a model nobody can open is a claim nobody can check.

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-adarshcod30-1c1c1c?logo=github)](https://github.com/adarshcod30)
[![Email](https://img.shields.io/badge/email-23ucs509%40lnmiit.ac.in-c2410c)](mailto:23ucs509@lnmiit.ac.in)

</div>
