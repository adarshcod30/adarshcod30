<div align="center">

<img src="assets/banner.png" alt="Adarsh Dwivedi: ML, deep learning and generative and agentic AI, built to be checked. A radial map of 32 projects across five areas: public-interest AI, trust and verification, agentic systems, quant and pipelines, and foundations." width="100%">

### [Orbweaver](https://github.com/adarshcod30/Orbweaver) · [Kadi](https://github.com/adarshcod30/Kadi) · [KrishiMitra](https://github.com/adarshcod30/KrishiMitra) · [Vayu](https://github.com/adarshcod30/Vayu) · [MargaDrishti](https://github.com/adarshcod30/MargaDrishti) · [VaidyaMitra](https://github.com/VaidyaMitra/VaidyaMitra) · [AGENTIQ](https://github.com/adarshcod30/AGENTIQ)

**[Every project, grouped →](PROJECTS.md)**

</div>

---

I build AI systems for problems that already have victims: crop loss, air
quality, road capacity, fraud rings, misdiagnosis, thin-file credit. And I
build them so a sceptical reader can check every claim I make.

I work across the whole range rather than one corner of it:

| | What I reach for | Where it shows up |
|---|---|---|
| **Classical ML** | XGBoost · LightGBM · CatBoost · scikit-learn · igraph | Orbweaver's account scorer, KrishiMitra's crop model, CreditSetu's risk tiering |
| **Deep learning** | PyTorch · ResNet50 / VGG16 / EfficientNetV2 · CNN-LSTM · GraphSAGE · Grad-CAM | OpenForensics' three-backbone ensemble, the retinopathy grader, Vayu's forecaster |
| **Generative AI** | Gemini · Amazon Bedrock (Nova Pro) · RAG · vision OCR | VaidyaMitra reads strips and reports, Kadi's grounded bilingual assistant, Specledger's extraction |
| **Agentic systems** | LangGraph · MCP tool layers · planner + executor splits | SmartAlloc's 7-agent pipeline, AGENTIQ's permission-checked tool layer, Inflx |

The thing that stays constant across all four is not the technique.

## The shape almost everything I build takes

A model is allowed to *propose*. Something deterministic, a threshold, a
knapsack, a peeling objective, an assertion evaluator, is what *decides*. That
separation is the single design decision I repeat most, because it is what
makes "why did this happen?" answerable by a person.

```mermaid
flowchart LR
    E["evidence in"] --> D["deterministic<br/>parse · validate · features"]
    D --> M["<b>the model proposes</b><br/>XGBoost · CNN · LLM · agent"]
    M --> G{"calibrated,<br/>enough evidence?"}
    G -->|no| A["<b>abstain</b><br/>route to a human"]
    G -->|yes| DEC["<b>deterministic decides</b><br/>peeling · knapsack · assertions"]
    DEC --> O["output + what it cost<br/>evidence · ₹ · false positives"]

    classDef learned fill:#151B2E,stroke:#818CF8,stroke-width:2px,color:#EDF4FF
    classDef proved fill:#0E2230,stroke:#22D3EE,stroke-width:2px,color:#EDF4FF
    classDef plain fill:#0F1422,stroke:#64748B,color:#EDF4FF
    classDef soft fill:#101A2B,stroke:#38A8FF,color:#EDF4FF
    class M learned
    class DEC proved
    class E,D,O plain
    class A,G soft
```

**Why it is worth the extra work.** Ring membership in Orbweaver comes from a
peeling objective with a proved ½-approximation bound, so "why is this account
in this ring?" is checkable arithmetic rather than a model's opinion. AGENTIQ
generates test assertions with an LLM and then evaluates them with a tool,
because a model grading its own output is not evidence. Specledger's extraction
works with the LLM switched off entirely. The model adds recall, it is not
load-bearing.

<div align="center">

<img src="assets/timeline.png" alt="Running total of 32 projects from June 2025 to September 2026, coloured by area, with the four early learning repositories in grey." width="100%">

</div>

## Selected work

### Public-interest AI: *problems that already have victims*

| Project | The hard part |
|---|---|
| **[KrishiMitra](https://github.com/adarshcod30/KrishiMitra)** | CatBoost crop recommendations cross-checked against **five years of government district returns**, leaf disease at **93.75%** over 10,162 images, FAO-56 irrigation advisory, Soil Health Card baselines from **13.35M** tests. 12 languages, deployed free |
| **[Vayu](https://github.com/adarshcod30/Vayu)** | LightGBM + CNN-LSTM forecasting over a **15,360-cell** satellite grid, Gaussian-plume ROI ranking, and **difference-in-differences** verification that an intervention actually worked, never a guessed AQI |
| **[Kadi](https://github.com/adarshcod30/Kadi)** | **59,985** siloed FIRs into one explainable link graph across **31 districts** and **298 stations**. Shared modus operandi ranks as a *hypothesis*, never as a name. The translator refuses to touch FIR numbers, dates and identifiers |
| **[VaidyaMitra](https://github.com/VaidyaMitra/VaidyaMitra)** ⟨org⟩ | Every identifier is masked **before** it reaches the model. Jan Aushadhi generic matching with substitution-safety warnings, vision OCR, ten Indian languages, on Amazon Bedrock |
| **[MargaDrishti](https://github.com/adarshcod30/MargaDrishti)** | Bengaluru road-capacity loss on one H3 × hourly substrate: **298k** violations, 8 model families, and a published audit of enforcement bias *in its own training data* |
| **[Floodcast-Gurugram](https://github.com/adarshcod30/Floodcast-Gurugram)** | Will *this route* flood, and when. Live rainfall matched against **73** researched flood points, rather than a city-wide alert nobody can act on. Provenance is a first-class field: **39 of 73** points carry a named source and every row has a confidence value |
| **[Diabetic-Retinopathy-Detection](https://github.com/adarshcod30/Diabetic-Retinopathy-Detection)** | Temperature-scaled confidence with reliability diagrams and ECE; low-confidence cases escalate to a human grader. Front page says *not a medical device*, because it is not |
| **[Medicure-AI](https://github.com/adarshcod30/Medicure-AI)** | Photograph a strip → composition, NPPA price, Jan Aushadhi generic, interaction warnings, each with a calibrated confidence and an honest refusal when evidence is thin |
| **[CreditSetu](https://github.com/adarshcod30/CreditSetu)** | `pip install creditsetu`. Validated against **150,000 real borrowers** with real default outcomes: **0.82 AUC using only 7 of 14 features**, to close the circularity gap of testing on its own synthetic data |

### Trust and verification: *deciding whether to believe something*

| Project | The hard part |
|---|---|
| **[Orbweaver](https://github.com/adarshcod30/Orbweaver)** | Densest-subgraph extraction over a **35.7M-edge** account graph: **0.7292** ring precision against a **0.2242** base rate, always reported with the **0.371** real customers swept in per fraudster caught. 36 dated failures published alongside |
| **[AGENTIQ](https://github.com/adarshcod30/AGENTIQ)** | B.Tech final-year project. **Eight** vulnerability families mapped to the OWASP API Security Top 10, probed by **baseline differential**, so a finding needs a material deviation rather than a suspicious-looking string. Every outbound request passes a permission-checked, SSRF-guarded, audited tool layer |
| **[artifact-repro-triage](https://github.com/adarshcod30/artifact-repro-triage)** | Checks whether a paper's repository contains what its README promises. **0% → 100%** detection of fabricated file claims across **742** artifacts |
| **[OpenForensics](https://github.com/adarshcod30/OpenForensics)** | Three-backbone deepfake ensemble with calibrated confidence and per-backbone Grad-CAM. The dashboard shows the evidence, not just the verdict |
| **[Specledger](https://github.com/adarshcod30/Specledger)** | A logistic calibrator over **11 evidence features** picks an auto-publish threshold hitting a measured precision floor on held-out data, instead of trusting an LLM's self-reported confidence |
| **[MedGuardX](https://github.com/adarshcod30/MedGuardX)** | Context-aware PII/PHI masking: an engine on PyPI, a hardened FastAPI service with JWT RBAC, and an app on top |

### Agentic systems · quant · foundations

| Project | The hard part |
|---|---|
| **[SmartAlloc](https://github.com/adarshcod30/SmartAlloc)** | A 7-agent LangGraph pipeline over linear programming that finds compute waste and predicts SLA bottlenecks before they land |
| **[Talent-Intelligence](https://github.com/adarshcod30/Talent-Intelligence-Candidate-Discovery-Platform)** | **100,000** candidates ranked in under **18 seconds**, CPU only, with honeypot and fake-profile filtering |
| **[CacheLLM](https://github.com/adarshcod30/CacheLLM)** | `pip install cachellm-proxy`. A drop-in proxy keeping the OpenAI request and response shape *including streaming*, verified against the official Python and Node SDKs. Exact hash, then a cosine tier whose safe threshold is **measured per embedding model**. **77%** hit rate, **78%** lower cost, zero wrong answers on genuinely new questions |
| **[Adaptive-Graph-Search-Suite](https://github.com/adarshcod30/Adaptive-Graph-Search-Suite)** | Graph traversal on realistic map topologies, built to be watched while it runs |

## Receipts for "every limit is written down"

The claim is cheap; these are the times it cost me something.

| Where | What I published anyway |
|---|---|
| **MargaDrishti** | A target of PR-AUC ≥ 0.45 was set assuming ~10% prevalence. The real label rate is **0.291%**, so the goal was unreachable *by construction*. Reported as a **46.9× lift** over base rate with the original goal marked wrong, not as a 3× shortfall |
| **MargaDrishti** | Seven model families all returned PR-AUC **0.9999** on one task. That is the signature of a recovered business rule, not a hard problem, so it is reported as a *recovered rule*, because presenting it as modelling performance would mislead |
| **MargaDrishti** | The review process changed regime mid-window, so every model on that task is miscalibrated. Reported as **not-yet-answerable** rather than as a weak result |
| **Orbweaver** | Four of thirteen investigations came back negative and are published beside the nine that worked, including one where the hypothesis was exactly backwards |
| **CreditSetu** | The live demo runs on synthetic data, and the README says so *above* the numbers rather than below them |

## Where this has been measured against other people

| | |
|---|---|
| **HackerRank Orchestrate** | 24-hour agentic AI challenges: **#12** (Sep 2026), **#290** with a bronze medal, top 15% (Aug 2026), **#427**, top 25% (Jun 2026). Each submission is public: [Buy or Wait](https://github.com/adarshcod30/buy-or-wait-financial-agent), [Message Notification Router](https://github.com/adarshcod30/Message-Notification-Router), [Multi-Modal Evidence Review](https://github.com/adarshcod30/Multi-Modal-Evidence-Review) |
| **KSP Datathon 2026** | Reached **Level 2** with [Kadi](https://github.com/adarshcod30/Kadi), built end to end over 50 days and deployed for the Karnataka State Police |
| **Hacksplosion 2026** (Deloitte India) | Cleared **Levels 1, 2 and 3** |
| **SWITCH Energy-X** | **11th of 93** on the private leaderboard, recovering a hidden physical law from 500,000 unlabeled, 26%-missing sensor rows |
| **micro1 Frontier Engineering** | [artifact-repro-triage](https://github.com/adarshcod30/artifact-repro-triage), measured across **742** repositories |
| **PyPI** | Three packages published and documented: [cachellm-proxy](https://pypi.org/project/cachellm-proxy/), [creditsetu](https://pypi.org/project/creditsetu/), [medguardx-core](https://pypi.org/project/medguardx-core/) |

10+ national hackathons and datathons, each shipping something that runs.

## How I work

Shipped on FastAPI, Streamlit and Next.js; deployed to Cloud Run, Vercel,
Render and AWS; packaged to PyPI where it makes sense. But the stack matters
less than the discipline around it: a temporal split a test enforces, a
held-out set nothing touches, the false-positive cost printed next to the
detection rate, and a `FAILURES.md` recording what I got wrong on the way.

## This repository builds itself

The banner, the timeline and [PROJECTS.md](PROJECTS.md) are generated from the
GitHub API, my own repositories and both organisations, so none of them can
quietly fall behind what I have actually shipped. The three avatars (mine and
the two organisations') are drawn by the same scripts, in one visual language:

```bash
make refresh    # pull the current repository list
make assets     # redraw the banner and the timeline
make index      # rewrite PROJECTS.md
make            # the last two
```

Claiming reproducibility on 32 projects and then hand-maintaining my own
profile would have made this the one dishonest page on the account.

## Elsewhere

Final-year computer science at **LNMIIT Jaipur**. I build under two
organisations, [VaidyaMitra](https://github.com/VaidyaMitra) for clinical
work and [B-TechProject](https://github.com/B-TechProject) for my final-year
project. Most of what I build ends up deployed somewhere free, because a model
nobody can open is a claim nobody can check.

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-adarshcod30-0A0E1A?logo=github)](https://github.com/adarshcod30)
[![Email](https://img.shields.io/badge/email-23ucs509%40lnmiit.ac.in-1D76DB)](mailto:23ucs509@lnmiit.ac.in)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-adarshdwivedi30-0369a1?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/adarshdwivedi30/)

</div>
