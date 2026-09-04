"""Which area each repository belongs to, and how much visual weight it gets.

This is the one editorial file here. Everything else is read from the GitHub
API, so if I ship something new the only thing I have to decide by hand is
which of the five areas it belongs in.

weight: 3 = a flagship I would show first, 2 = substantial, 1 = smaller.
"""
from __future__ import annotations

# ordered: the order the areas appear in the README and the banner
AREAS = [
    ("public-interest AI", (226, 98, 38),
     "Systems for problems that already have victims - crop loss, air quality, "
     "road capacity, misdiagnosis, thin-file credit."),
    ("trust & verification", (72, 146, 180),
     "Deciding whether to believe something: a ring, a face, a claim, a "
     "repository's own README."),
    ("agentic systems", (206, 158, 74),
     "Multi-step pipelines that decide and act, with a human holding the "
     "final switch."),
    ("quant & pipelines", (152, 130, 176),
     "Market behaviour and the reproducible plumbing underneath it."),
    ("foundations", (120, 112, 104),
     "The groundwork - algorithms, tooling, and where I started."),
]

# repo name -> (area, weight)
THEME = {
    # public-interest AI
    "KrishiMitra": ("public-interest AI", 3),
    "VaidyaMitra": ("public-interest AI", 3),
    "Vayu": ("public-interest AI", 3),
    "Kadi": ("public-interest AI", 3),
    "Diabetic-Retinopathy-Detection": ("public-interest AI", 3),
    "MargaDrishti": ("public-interest AI", 2),
    "Medicure-AI": ("public-interest AI", 2),
    "CreditSetu": ("public-interest AI", 2),
    "floodcast-gurugram": ("public-interest AI", 1),

    # trust & verification
    "Orbweaver": ("trust & verification", 3),
    "AGENTIQ": ("trust & verification", 3),          # B.Tech final-year project
    "artifact-repro-triage": ("trust & verification", 2),
    "OpenForensics": ("trust & verification", 2),
    "MedGuardX": ("trust & verification", 2),
    "Specledger": ("trust & verification", 1),
    "Multi-Modal-Evidence-Review": ("trust & verification", 1),
    "Talent-Intelligence-Candidate-Discovery-Platform": ("trust & verification", 1),

    # agentic systems
    "SmartAlloc": ("agentic systems", 2),
    "Inflx": ("agentic systems", 1),
    "Message-Notification-Router": ("agentic systems", 1),
    "Cost-Intel-Intelligence": ("agentic systems", 1),
    "SuiGuard": ("agentic systems", 1),

    # quant & pipelines
    "PrimeTradeML": ("quant & pipelines", 1),
    "PrimeTradeDS": ("quant & pipelines", 1),
    "Flipkart-Gridlock-2.0": ("quant & pipelines", 1),
    "Air-Cargo-Intelligence": ("quant & pipelines", 1),

    # foundations
    "Adaptive-Graph-Search-Suite": ("foundations", 1),
    "LNMIIT-Event-Management-System": ("foundations", 1),
}

# the four repos I learned on, kept out of the counts so they are not padding
LEARNING = {"First-repo", "SecondRepo", "JavaProjects", "PythonProjects"}

# an empty placeholder repository, excluded from every count
SKIP = {"BTP", "demo-repository"}

# short display names where the repo name is too long for a chart label
SHORT = {
    "Talent-Intelligence-Candidate-Discovery-Platform": "Talent-Intelligence",
    "Diabetic-Retinopathy-Detection": "Diabetic-Retinopathy",
    "LNMIIT-Event-Management-System": "LNMIIT-Events",
    "Message-Notification-Router": "Notification-Router",
    "Multi-Modal-Evidence-Review": "Evidence-Review",
    "Cost-Intel-Intelligence": "Cost-Intel",
    "Adaptive-Graph-Search-Suite": "Graph-Search-Suite",
    "Air-Cargo-Intelligence": "Air-Cargo",
    "Flipkart-Gridlock-2.0": "Flipkart-Gridlock",
    "artifact-repro-triage": "artifact-repro-triage",
    "floodcast-gurugram": "floodcast",
}


def short(name: str) -> str:
    return SHORT.get(name, name)


def area_colour(area: str):
    for a, c, _ in AREAS:
        if a == area:
            return c
    return (120, 112, 104)
