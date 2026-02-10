# PROJECT STATE — Team AWESOME

## NovaStar Hotels: AI-Powered Post-Stay Engagement System

---

## Project Brief

**Client:** NovaStar Hotels (hypothetical mid-range hotel chain)
**Problem:** Guests enjoy their stay but never come back. Repeat bookings are being lost to Airbnb.
**Goal:** Design and demonstrate an AI-powered post-stay engagement system that turns one-time guests into loyal repeat customers.
**Team:** Team AWESOME (5-agent sequential workflow)
**Repository:** https://github.com/SacriTom/novastar-engagement-system
**Live Dashboard:** https://sacritom.github.io/novastar-engagement-system/

---

## Team Roster

| # | Agent | Name | Role | Status |
|---|-------|------|------|--------|
| 1 | Researcher | Riley | Discovery & Landscape Analyst | COMPLETE |
| 2 | Designer | Dana | Solution Architect & Experience Designer | COMPLETE |
| 3 | Maker | Max | Builder & Technical Implementer | COMPLETE |
| 4 | Communications | Casey | Marketing Strategist & Guest Engagement Specialist | COMPLETE |
| 5 | Manager | Morgan | Project Orchestrator & Quality Gatekeeper | COMPLETE |

---

## Workflow

```
Riley (Research) → Dana (Design) → Max (Build) → Casey (Comms) → Morgan (Review)
```

Each agent's output becomes the next agent's input. Sequential pipeline.

---

## Phase Tracker

### Phase 1: Research (Riley)
- **Status:** COMPLETE
- **Output:** `outputs/01_research_report.md`
- **Key deliverables:** Guest segmentation, churn funnel, competitive landscape, root cause analysis
- **Started:** 2026-02-10
- **Completed:** 2026-02-10
- **Key findings:** 12.1% rebooking rate vs 30-40% industry benchmark; 6 guest segments identified; 57% data capture failure at checkout is biggest leak; NPS 62 but loyalty disconnect; $34.2M estimated annual revenue impact; Airbnb wins on local experience and price flexibility; 8 root causes ranked by impact

### Phase 2: Design (Dana)
- **Status:** COMPLETE
- **Output:** `outputs/02_solution_design.md`
- **Key deliverables:** System architecture, guest journey map, feature specs, success metrics
- **Started:** 2026-02-10
- **Completed:** 2026-02-10
- **Key decisions:** 5-component system architecture; 4-tier loyalty programme (Explorer→Ambassador); 6-stage post-stay journey; rebooking target 12.1%→32% at 24 months; MoSCoW prioritisation across 20 initiatives; $12.26M projected incremental value

### Phase 3: Build (Max)
- **Status:** COMPLETE
- **Output:** `outputs/03_technical_build/`
- **Key deliverables:** Engagement engine, data models, guest journey simulation, dashboard spec
- **Started:** 2026-02-10
- **Completed:** 2026-02-10
- **Technical notes:** 3 runnable Python files (std lib only); 8 dataclasses, 7 enums; segment classifier, churn predictor, content generator, trigger planner; 100-guest simulation shows rebooking 4%→17%; projected +10,400 repeat guests and ~$6.2M incremental revenue at scale

### Phase 4: Communications (Casey)
- **Status:** COMPLETE
- **Output:** `outputs/04_communications/`
- **Key deliverables:** Launch strategy, messaging framework, templates, content calendar
- **Started:** 2026-02-10
- **Completed:** 2026-02-10
- **Campaign notes:** 9 files delivered; master tagline "We Remember. You Return."; 3-phase rollout; win-back campaign targeting ~30K lapsed guests projecting ~1,100 rebookings ($566K revenue); 4 email templates, 10 push notifications, 8 in-app messages, 6 SMS templates; on-property playbook with checkout scripts; 90-day content calendar

### Phase 5: Manager Review (Morgan)
- **Status:** COMPLETE
- **Output:** `outputs/05_manager_report.md`
- **Key deliverables:** Quality review, coherence check, final report, retrospective
- **Started:** 2026-02-10
- **Completed:** 2026-02-10
- **Review notes:** All 4 phases rated "Strong"; overall grade A-; 4 coherence traces validated; 3 chain breaks flagged (missing docs, privacy gap, price parity); 8 risks registered; recommended $775K-$1.5M Year 1 budget; 14-month phased timeline; ready for CEO presentation with caveats

---

## Post-Pipeline Deliverables

### Python Verification
- **Status:** COMPLETE
- **Date:** 2026-02-10
- **Result:** All 3 Python files (`data_models.py`, `engagement_engine.py`, `guest_journey_simulation.py`) run successfully with Python 3.14, standard library only. Simulation output verified: rebooking 4%→17%, financial projections consistent with design targets.

### PDF Report
- **Status:** COMPLETE
- **Output:** `outputs/NovaStar_Final_Report.pdf`
- **Generator:** `outputs/generate_report_pdf.py` (uses fpdf2)
- **Details:** Professional formatted PDF of Morgan's full report — title page, styled headings, tables with alternating rows, bullet points, page numbers, dark blue (#1a365d) colour scheme

### Flask Web UI (Local)
- **Status:** COMPLETE
- **Output:** `outputs/03_technical_build/app.py`
- **How to run:** `cd outputs/03_technical_build && python app.py` → http://127.0.0.1:5000
- **Pages:** Dashboard Home (`/`), Simulation (`/simulation`), Engagement Engine (`/engine`), Guest Segments (`/segments`)
- **Details:** Interactive dashboard with adjustable simulation parameters, engagement engine demo with form inputs, segment overview. Requires Flask.

### Standalone HTML Dashboard (GitHub Pages)
- **Status:** COMPLETE
- **Output:** `index.html`
- **Live URL:** https://sacritom.github.io/novastar-engagement-system/
- **Details:** Single-file HTML/CSS/JS with all simulation and engagement engine logic ported to JavaScript. Zero dependencies. Works for anyone with the link — no server or installation needed. Includes: Dashboard, Simulation (adjustable params), Engagement Engine (interactive), Guest Segments.

### GitHub Repository
- **Status:** COMPLETE
- **URL:** https://github.com/SacriTom/novastar-engagement-system
- **Visibility:** Public
- **GitHub Pages:** Enabled (serves index.html from main branch)

---

## Decisions Log

| # | Decision | Made By | Date | Rationale |
|---|----------|---------|------|-----------|
| 1 | Adapted agent personas from NorthSouth Coffee to NovaStar Hotels | Team + User | 2026-02-10 | Reuse proven team structure for new domain |
| 2 | All Python code uses standard library only (no pip installs) | Max | 2026-02-10 | Maximum portability for academic demo |
| 3 | PDF generated with fpdf2 (already installed) | Team | 2026-02-10 | Lightweight PDF generation without heavy dependencies |
| 4 | Flask for local UI, standalone HTML for GitHub Pages | Team + User | 2026-02-10 | Flask for rich local experience; pure HTML/JS for universal web access |
| 5 | GitHub Pages enabled on main branch root | Team + User | 2026-02-10 | Anyone with the link can interact with the project |

---

## Blockers & Risks

| # | Issue | Status | Owner | Resolution |
|---|-------|--------|-------|------------|
| 1 | OneDrive file lock on initial PDF generation | RESOLVED | Team | Used alternative filename `NovaStar_Final_Report.pdf` |
| 2 | Git identity not configured on machine | RESOLVED | User | Configured with GitHub username SacriTom |

---

## Project Timeline

- **Project Start:** 2026-02-10
- **Phase 1-5 Complete:** 2026-02-10
- **Verification, PDF, UI, GitHub:** 2026-02-10
- **Current Status:** ALL DELIVERABLES COMPLETE
- **Total files produced:** 31 (5 agent personas, 14 phase outputs, 1 PDF, 1 PDF generator, 1 Flask app, 1 standalone HTML, 3 project tracking files, 1 .gitignore)

---

## Key Metrics Summary

| Metric | Current State | Projected (12-Month) | Projected (24-Month) |
|--------|--------------|---------------------|---------------------|
| Repeat booking rate | 12.1% | 25% | 32% |
| Guest data capture | 43% | 75% | 85% |
| Loyalty enrolment | 11.3% | 40% | 50% |
| Direct booking share | 27% | 40% | 50% |
| Post-stay email open rate | 18.4% | 38% | 42% |
| Incremental annual revenue | — | +$4.84M | +$7.42M |
| Cumulative incremental value | — | $4.84M | $12.26M |
