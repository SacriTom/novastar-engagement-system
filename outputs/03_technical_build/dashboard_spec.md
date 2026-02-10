# NovaStar Hotels -- Analytics & Optimisation Dashboard Specification

**Prepared by:** Max the Maker (Agent 03, Team AWESOME)
**Maps to:** Analytics & Optimisation Dashboard (AOD) in Dana's architecture (Section 2.1)

---

## 1. Executive View (C-Suite / VP Marketing)

| Panel | Metrics | Data Source | Refresh |
|-------|---------|-------------|---------|
| **Rebooking Funnel** | First-stay count, post-stay engaged, active consideration, booking intent, repeat booked (overall + direct vs OTA) | GDP + Booking Engine | Daily |
| **Revenue Impact** | Incremental repeat revenue (MTD/QTD/YTD), OTA commission savings, acquisition cost savings | Booking Engine + Finance | Daily |
| **Headline KPIs** | Repeat booking rate, loyalty enrolment %, direct booking share, guest data capture rate, email open rate | All systems | Daily |
| **Segment Heatmap** | Rebooking rate per segment, colour-coded against 12-month targets (Dana Section 7.2) | GDP + Booking Engine | Daily |
| **ROI Scorecard** | System investment vs incremental revenue, payback timeline, per-segment ROI | Finance + AOD | Weekly |

**Layout:** Single-page dashboard with 5 card panels. Top row: 4 headline KPI tiles with sparklines. Middle: funnel visualisation + revenue chart. Bottom: segment heatmap + ROI.

---

## 2. Operational View (Marketing Team / CRM Manager)

| Panel | Metrics | Data Source | Refresh |
|-------|---------|-------------|---------|
| **Campaign Performance** | Active campaigns, emails/push/SMS sent, open rates, click rates, conversion rates, A/B test winners | Communication Orchestrator | Real-time |
| **Journey Stage Pipeline** | Guest count at each of the 6 stages, stage-to-stage conversion rates, average dwell time per stage | APE + CO | Hourly |
| **Channel Mix** | Volume and engagement by channel (email, push, SMS, WhatsApp, in-app), channel switch events | CO | Hourly |
| **Offer Performance** | Offers generated, redemption rate, average discount depth, margin impact, top-performing perks by segment | APE (Offer Selector) | Daily |
| **Churn Risk Alerts** | High-risk guests count, escalated offers sent, save rate (rebooked after escalation) | APE (Churn Predictor) | Real-time |
| **Content Quality** | AI-generated content confidence scores, fallback-to-template rate, subject-line A/B results | APE (Content Generator) | Daily |

**Layout:** Tabbed interface. Tab 1: Campaign + Journey pipeline. Tab 2: Channel + Offer deep-dive. Tab 3: Churn alerts table with one-click escalation.

---

## 3. Segment Drill-Down View

One sub-page per segment (6 total), each containing:

| Panel | Metrics |
|-------|---------|
| **Segment Profile** | Guest count, % of total, avg spend/night, avg stay length, primary booking channel, NPS |
| **Rebooking Trend** | 12-month rolling rebooking rate vs target, before/after comparison |
| **Engagement Funnel** | Segment-specific funnel (post-stay contacted -> engaged -> considered -> booked) |
| **Top Offers** | Best-performing offer type, discount depth distribution, perk redemption ranking |
| **Channel Preference** | Preferred channel breakdown, email vs push vs SMS engagement rates |
| **Loyalty Distribution** | Tier breakdown within segment, points earned/redeemed, milestone progress |

---

## 4. Loyalty Programme View

| Panel | Metrics | Data Source | Refresh |
|-------|---------|-------------|---------|
| **Tier Pyramid** | Member count per tier (Explorer/Adventurer/Voyager/Ambassador), tier movement (upgrades/downgrades) | Loyalty Engine | Daily |
| **Points Economy** | Points issued, redeemed, expired; breakage rate trend (target: 54% -> 20%) | Loyalty Engine | Daily |
| **Enrolment Funnel** | Non-member -> sign-up prompt shown -> enrolled -> first earn -> first redeem | LE + GDP | Daily |
| **Reward Popularity** | Redemption counts by reward type, points-per-redemption, guest satisfaction post-redeem | LE | Weekly |

---

## 5. Property-Level View

| Panel | Metrics |
|-------|---------|
| **Property Scorecard** | Repeat rate, data capture rate, loyalty enrolment, NPS -- per property |
| **Regional Comparison** | Americas / Europe / APAC aggregate performance with drill-down to individual properties |
| **Staff Adoption** | Front-desk data capture completion rate, digital check-in usage, Rewards mentions at check-in |

---

## 6. Technical Requirements

| Requirement | Specification |
|-------------|---------------|
| **Data warehouse** | Unified data lake fed by GDP, CO, APE, LE, and Booking Engine via event streaming |
| **Refresh cadence** | Real-time for alerts/campaigns; hourly for journey pipeline; daily for KPI rollups |
| **Access control** | Role-based: Exec (read-only headline), Marketing (full operational), Property GM (own property + region), IT Admin (all + config) |
| **Export** | CSV/Excel export on all tables; PDF snapshot of Executive View for board reporting |
| **Alerting** | Slack/email alerts for: churn spike (>20% of segment), campaign underperformance (open rate <50% of target), system error |
| **A/B framework** | Built-in test configuration: split %, duration, auto-winner selection at statistical significance (p<0.05) |
| **Target overlay** | All trend charts show Dana's 6-month and 12-month targets as reference lines |

---

*End of Dashboard Specification*
