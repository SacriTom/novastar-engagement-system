# NovaStar Hotels -- Technical Implementation Summary

**Prepared by:** Max the Maker (Agent 03, Team AWESOME)
**Date:** 10 February 2026

---

## 1. What Was Built

This package contains a working prototype of NovaStar's AI-Powered Post-Stay Engagement System, implemented as four runnable Python modules and a dashboard specification.

| File | Purpose | Maps to (Dana's Architecture) |
|------|---------|-------------------------------|
| `data_models.py` | Database schema: 8 core models, enumerations, sample data factories | Guest Data Platform (GDP) |
| `engagement_engine.py` | Segment classifier, churn risk predictor, personalised content/offer generator, trigger planner | AI Personalisation Engine (APE) + Communication Orchestrator (CO) |
| `guest_journey_simulation.py` | 100-guest, 90-day Monte Carlo simulation comparing before vs after engagement | Analytics & Optimisation Dashboard (AOD) data validation |
| `dashboard_spec.md` | Dashboard panels, metrics, refresh rates, access control | Analytics & Optimisation Dashboard (AOD) |

---

## 2. Architecture Decisions

| Decision | Rationale |
|----------|-----------|
| **Pure Python, standard library only** | Zero-dependency prototype that any team member can run without environment setup. Validates logic before committing to a tech stack. |
| **Dataclasses over ORM** | Keeps the schema readable and portable. Production migration to SQLAlchemy/Django ORM is straightforward -- field types and relationships are documented in comments. |
| **Template-based content generation** | Simulates AI-generated copy with segment x stage templates. In production, this layer would call an LLM API (e.g., Claude) for dynamic natural-language generation. |
| **Heuristic segment classifier** | Rule-based classification mirrors the logic an ML model would learn. Easy to validate against Riley's segment definitions before investing in model training. |
| **Fixed random seed in simulation** | Reproducible results for stakeholder review. Seed can be changed or removed for stochastic analysis. |
| **Engagement-boosted rebooking model** | Rebooking probability = base rate (from Riley's data) + engagement lift (capped). This reflects the core thesis: more touchpoints at higher quality raise return probability. |

---

## 3. How Code Maps to Dana's Design

| Dana's Component | Code Implementation |
|------------------|---------------------|
| **6 Guest Segments** (Section 2.1, 5.3) | `GuestSegment` enum + `classify_segment()` in `engagement_engine.py`; segment distribution in simulation |
| **6-Stage Journey** (Section 3.1) | `JourneyStage` enum + `determine_journey_stage()` + `_TRIGGER_SCHEDULE` |
| **Channel Selection Logic** (Section 3.2) | `_pick_channel()` function with app/SMS/email priority rules |
| **AI Personalisation Layers** (Section 5.1) | `GuestProfile` dataclass aggregating segment, context, preference, behavioural, and lifecycle layers |
| **Segment-Specific Offers** (Section 5.3) | `_generate_offer()` with match-statement routing per segment; perks from Dana's table |
| **Churn Risk Predictor** (Section 2.1) | `calculate_churn_risk()` using recency, engagement, channel, and loyalty factors |
| **Loyalty Tiers** (Section 6.2) | `LoyaltyTier` enum (Explorer/Adventurer/Voyager/Ambassador) + `LoyaltyAccount` model |
| **Psychological Mechanics** (Section 5.2) | Loss-aversion framing in conversion-push templates; goal-gradient in tier-progress messaging; nostalgia triggers at Day 5 |
| **KPI Targets** (Section 7.1-7.2) | Simulation compares Riley's baselines against Dana's 12-month targets |
| **MoSCoW Priorities** (Section 8.1) | MUST-have components (GDP, APE core, CO, Loyalty tiers) are all implemented in this package |

---

## 4. What Would Need to Change for Production

| Area | Prototype State | Production Requirement |
|------|-----------------|------------------------|
| **Data storage** | In-memory dataclasses | PostgreSQL/DynamoDB with the schema from `data_models.py`; event-sourced interaction log |
| **Content generation** | String templates with variable substitution | LLM API calls (Claude/GPT) with segment-aware system prompts; A/B test variants; human-in-the-loop review queue |
| **Segment classifier** | Rule-based heuristics | ML model (gradient-boosted trees or neural network) trained on historical booking + behaviour data |
| **Churn predictor** | Weighted-factor score | Survival model or gradient-boosted classifier with time-series features |
| **Communication delivery** | Console print | Integration with SendGrid (email), Twilio (SMS/WhatsApp), Firebase (push), Braze or Iterable (orchestration) |
| **Trigger scheduling** | Synchronous loop | Celery/Airflow task queue with cron-based stage evaluation per guest |
| **Dashboard** | Markdown specification | Looker, Tableau, or Metabase connected to the analytics data warehouse |
| **Identity resolution** | Single guest object | Probabilistic matching engine (e.g., Amperity, Segment) to merge OTA-masked emails with real profiles |
| **Privacy & consent** | Not implemented | GDPR/CCPA consent manager integrated into GDP; opt-out propagation across all channels |
| **Scale** | 100 simulated guests | 80,000+ guests with real-time event streaming (Kafka/Kinesis) feeding the APE |
| **Testing** | Manual demo run | pytest suite with unit tests for classifier, churn model, offer logic; integration tests for the full trigger pipeline |

---

## 5. How to Run

All three Python files are independently runnable with Python 3.10+, no pip installs needed.

```bash
# Run from the 03_technical_build directory
python data_models.py               # prints sample records for all 6 segments
python engagement_engine.py         # full demo: Family Vacationer through all 6 journey stages
python guest_journey_simulation.py  # 100-guest simulation with before/after comparison
```

The engagement engine imports from `data_models.py`, so both files must be in the same directory (or on `PYTHONPATH`).

---

*End of Implementation Summary*

*Max the Maker -- Agent 03, Team AWESOME*
