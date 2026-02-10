# QUICKSTART — Team AWESOME

## NovaStar Hotels: AI-Powered Post-Stay Engagement System

> This project is **COMPLETE**. All 5 phases + post-pipeline deliverables are done.

---

## Quick Links

| Resource | URL |
|----------|-----|
| **Live Dashboard** | https://sacritom.github.io/novastar-engagement-system/ |
| **GitHub Repository** | https://github.com/SacriTom/novastar-engagement-system |
| **PDF Report** | `outputs/NovaStar_Final_Report.pdf` |

---

## Project Summary

**Team AWESOME** designed and demonstrated a 5-agent sequential workflow to solve NovaStar Hotels' repeat booking crisis. Guests enjoy their stay but never come back (12.1% rebooking rate vs 30-40% benchmark). The team built an AI-powered post-stay engagement system projected to increase rebooking to 32% and generate $12.26M in cumulative incremental value over 2 years.

**Overall Grade: A-** (Morgan's assessment)

---

## Deliverables Map

```
Project Root
├── index.html                    — Standalone interactive dashboard (GitHub Pages)
├── PROJECT_STATE.md              — Planning and progress tracker
├── QUICKSTART.md                 — This file
│
├── agents/
│   ├── 01_researcher.md          — Riley's persona
│   ├── 02_designer.md            — Dana's persona
│   ├── 03_maker.md               — Max's persona
│   ├── 04_communications.md      — Casey's persona
│   └── 05_manager.md             — Morgan's persona
│
└── outputs/
    ├── 01_research_report.md     — Riley: Discovery & landscape analysis
    ├── 02_solution_design.md     — Dana: Solution blueprint & system architecture
    ├── 03_technical_build/
    │   ├── data_models.py        — Max: Database schema (8 dataclasses, 7 enums)
    │   ├── engagement_engine.py  — Max: AI personalisation & trigger engine
    │   ├── guest_journey_simulation.py — Max: 90-day simulation (100 guests)
    │   ├── app.py                — Flask web UI (local dashboard)
    │   ├── dashboard_spec.md     — Max: Analytics dashboard specification
    │   └── implementation_summary.md — Max: Technical overview & build notes
    ├── 04_communications/
    │   ├── launch_strategy.md    — Casey: 3-phase rollout plan
    │   ├── messaging_framework.md — Casey: Tagline, value props, segment messaging
    │   ├── win_back_campaign.md  — Casey: 30-day win-back sequence
    │   ├── on_property_playbook.md — Casey: Front-desk scripts & in-room touchpoints
    │   ├── content_calendar.md   — Casey: 90-day channel plan
    │   └── templates/
    │       ├── email_templates.md    — 4 ready-to-use email templates
    │       ├── push_notifications.md — 10 trigger-based push templates
    │       ├── in_app_messages.md    — 8 contextual in-app messages
    │       └── sms_templates.md      — 6 SMS templates
    ├── 05_manager_report.md      — Morgan: Final review, coherence check, retrospective
    ├── NovaStar_Final_Report.pdf  — PDF version of Morgan's report
    └── generate_report_pdf.py    — Script to regenerate the PDF
```

---

## How to Use This Project

### 1. View the Live Dashboard (No install needed)
Open https://sacritom.github.io/novastar-engagement-system/ in any browser.
- Run simulations with adjustable parameters
- Test the engagement engine for any guest segment
- Browse guest segment data

### 2. Run Python Code Locally
```bash
cd outputs/03_technical_build

# Run data models demo
python data_models.py

# Run engagement engine demo
python engagement_engine.py

# Run 90-day simulation
python guest_journey_simulation.py
```
Requires: Python 3.10+ (standard library only, no pip installs)

### 3. Run Flask Web UI Locally
```bash
cd outputs/03_technical_build
python app.py
# Open http://127.0.0.1:5000
```
Requires: Python 3.10+ and Flask (`pip install flask`)

### 4. Regenerate the PDF Report
```bash
cd outputs
python generate_report_pdf.py
```
Requires: Python 3.10+ and fpdf2 (`pip install fpdf2`)

---

## How to Re-Run Any Agent Phase

Each phase can be independently re-run using the prompt templates in the agent persona files (`agents/0X_*.md`). The sequential dependency is:

```
Phase 1 (Riley) → Phase 2 (Dana) → Phase 3 (Max) → Phase 4 (Casey) → Phase 5 (Morgan)
```

### Phase 1 — Research (Riley)
```
You are Riley the Researcher, Agent 01 of Team AWESOME. Your task is to
conduct a thorough discovery phase for NovaStar Hotels' repeat booking
crisis. The chain has 45 properties and guests enjoy their stay but never
come back — losing repeat bookings to Airbnb. The CEO wants an AI-powered
post-stay engagement system.

Generate synthetic data, analyse it, and produce a comprehensive research
report. Follow the structure and responsibilities defined in your persona file
(agents/01_researcher.md). Write your output to outputs/01_research_report.md
and update PROJECT_STATE.md upon completion.
```

### Phase 2 — Design (Dana)
```
You are Dana the Designer, Agent 02 of Team AWESOME. Read the research report
from Riley (outputs/01_research_report.md) and design a comprehensive AI-powered
post-stay engagement system for NovaStar Hotels.

Transform the research findings into a detailed solution blueprint covering
system architecture, guest journey, app/web features, personalisation mechanics,
and success metrics. Follow the structure defined in your persona file
(agents/02_designer.md). Write your output to outputs/02_solution_design.md
and update PROJECT_STATE.md upon completion.
```

### Phase 3 — Build (Max)
```
You are Max the Maker, Agent 03 of Team AWESOME. Read the solution design
from Dana (outputs/02_solution_design.md) and the research from Riley
(outputs/01_research_report.md), then build the technical implementation.

Create working Python code for the engagement engine, data models, and
guest journey simulation. Produce a dashboard specification and implementation
summary. Follow the structure defined in your persona file
(agents/03_maker.md). Write outputs to outputs/03_technical_build/ and update
PROJECT_STATE.md upon completion.
```

### Phase 4 — Communications (Casey)
```
You are Casey the Communicator, Agent 04 of Team AWESOME. Read the technical
build from Max (outputs/03_technical_build/), the solution design from Dana
(outputs/02_solution_design.md), and the research from Riley
(outputs/01_research_report.md).

Create a comprehensive communications package including launch strategy,
messaging framework, win-back campaigns, communication templates, on-property
playbook, and a 90-day content calendar. Follow the structure defined in your
persona file (agents/04_communications.md). Write outputs to
outputs/04_communications/ and update PROJECT_STATE.md upon completion.
```

### Phase 5 — Manager Review (Morgan)
```
You are Morgan the Manager, Agent 05 of Team AWESOME. Review ALL outputs from
the team: Riley's research (outputs/01_research_report.md), Dana's design
(outputs/02_solution_design.md), Max's build (outputs/03_technical_build/),
and Casey's communications (outputs/04_communications/).

Conduct a quality review, coherence check, and produce the final manager's
report. Assess whether the project tells a consistent story from problem to
solution. Flag any gaps or risks. Follow the structure defined in your persona
file (agents/05_manager.md). Write your report to outputs/05_manager_report.md
and finalise PROJECT_STATE.md.
```

---

## Checkpoint History

| # | Phase | Agent | Status | Timestamp |
|---|-------|-------|--------|-----------|
| 1 | Research | Riley | COMPLETE | 2026-02-10 |
| 2 | Design | Dana | COMPLETE | 2026-02-10 |
| 3 | Build | Max | COMPLETE | 2026-02-10 |
| 4 | Communications | Casey | COMPLETE | 2026-02-10 |
| 5 | Manager Review | Morgan | COMPLETE | 2026-02-10 |
| 6 | Python Verification | Team | COMPLETE | 2026-02-10 |
| 7 | PDF Report Generation | Team | COMPLETE | 2026-02-10 |
| 8 | Flask Web UI | Team | COMPLETE | 2026-02-10 |
| 9 | Standalone HTML Dashboard | Team | COMPLETE | 2026-02-10 |
| 10 | GitHub Repo + Pages | Team | COMPLETE | 2026-02-10 |

---

## Continuation Prompt (if resuming in a new session)

```
We are working on the NovaStar Hotels AI-Powered Post-Stay Engagement System
for Team AWESOME. This is an academic exercise (Week 4 Group Exercise).

The project is COMPLETE with all 5 agent phases done, Python code verified,
PDF report generated, Flask UI built, and a standalone HTML dashboard deployed
to GitHub Pages.

Read PROJECT_STATE.md and QUICKSTART.md for full context. The GitHub repo is at:
https://github.com/SacriTom/novastar-engagement-system
The live dashboard is at:
https://sacritom.github.io/novastar-engagement-system/

[Describe what you'd like to do next]
```

---

**PROJECT STATUS: COMPLETE**
