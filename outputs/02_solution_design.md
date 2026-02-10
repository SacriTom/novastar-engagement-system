# NovaStar Hotels: AI-Powered Post-Stay Engagement System
## Solution Design Document

**Prepared by:** Dana the Designer (Agent 02, Team AWESOME)
**Date:** 10 February 2026
**Classification:** Internal -- Strategic
**Version:** 1.0
**Input:** Riley the Researcher's Discovery Phase Report (01_research_report.md)

---

## Table of Contents

1. [Design Goals & Principles](#1-design-goals--principles)
2. [System Architecture](#2-system-architecture)
3. [Guest Journey Map (To-Be)](#3-guest-journey-map-to-be)
4. [App/Web Feature Specs](#4-appweb-feature-specs)
5. [Personalisation & Retention Mechanics](#5-personalisation--retention-mechanics)
6. [Loyalty Programme Redesign](#6-loyalty-programme-redesign)
7. [Success Metrics & KPI Targets](#7-success-metrics--kpi-targets)
8. [Implementation Priorities (MoSCoW)](#8-implementation-priorities-moscow)

---

## 1. Design Goals & Principles

Every design goal below traces directly to a finding in Riley's research. The format is: **FINDING** (what the research uncovered) -> **GOAL** (what the design must achieve) -> **SOLUTION** (how) -> **METRIC** (how we measure success).

| # | Finding (from Research) | Design Goal | Solution Approach | Success Metric |
|---|---|---|---|---|
| G1 | 57% of guests have no usable contact data; 83% of PMS preference fields are blank (Root Cause #3) | **Capture guest identity at every touchpoint** | Smart digital check-in with value exchange (Wi-Fi upgrade, room selection); OTA de-anonymisation via SMS/WhatsApp room-info flow; progressive profiling across stays | Guest data capture rate: 43% -> 75% within 12 months |
| G2 | All 80,000 guests receive identical emails; personalisation scores 1/10 vs. 8-9/10 for competitors (Root Cause #4) | **Deliver segment- and context-aware communications** | AI Personalisation Engine generating dynamic content per guest based on segment, stay context, season, and behavioural signals | Post-stay email open rate: 18.4% -> 38%; click rate: 2.1% -> 8% |
| G3 | NovaStar Rewards: 11.3% enrolment, 54% points breakage, no tiers, no emotional hook (Root Cause #2) | **Rebuild loyalty around status, recognition, and emotion** | Tiered NovaStar Rewards programme with experiential benefits, surprise-and-delight AI triggers, and visible progression | Loyalty enrolment: 11.3% -> 40%; active member rate: 47% -> 75% |
| G4 | 61% OTA bookings; 59% of repeat guests rebook via OTA; $5.58M annual commission (Root Cause #5) | **Shift bookings from OTA to direct channels** | Best-price guarantee with real-time parity enforcement; direct-only perks; in-stay "book next" conversion moments; loyalty points only on direct bookings | Direct booking share: 27% -> 45%; OTA commission savings: $1.5M/yr |
| G5 | NovaStar scores 1/10 on local experience vs. Airbnb 9/10; 47% of Leisure Couples cite "wanting local" (Root Cause #8) | **Position NovaStar as a local access platform** | "Local Explorer" feature with AI-curated destination content, local partnerships, bookable experiences | Local content engagement: 0% -> 30% of app users; Airbnb consideration among repeat guests: -15pp |
| G6 | Family Vacationers generate 27% of revenue but rebook at only 8.3%; Extended-Stay at 21.8% with highest per-guest value (Insight #5) | **Invest engagement intensity proportional to segment value** | Segment-tiered AI engagement: high-touch for Business Regulars, Families, Extended-Stay; medium for Couples, Groups; light for Budget Solo | Rebooking rate for Families: 8.3% -> 22%; Business Regulars: 19.4% -> 35% |
| G7 | Group/Event guests attribute positive experience to the event, not NovaStar; generic post-stay emails ignore event context (Insight #6) | **Bridge the attribution gap for event guests** | Event-context tagging at check-in; post-stay comms that reference the specific event; individual return offers tied to the destination | Group/Event rebooking: 14.2% -> 25% |

### Overarching Design Principles

1. **Data First, AI Second** -- No AI feature ships without a reliable data pipeline feeding it. (Riley Insight #1)
2. **Personal, Not Programmatic** -- Every guest communication must feel like it was written by a human who remembers them. (Stakeholder quote: "We have amnesia")
3. **Value Exchange at Every Ask** -- Every time we request data from a guest, we give something tangible in return.
4. **Direct Channel Supremacy** -- The direct booking path must always be the best path for the guest. No exceptions.
5. **Segment-Proportional Investment** -- Engineering effort and AI compute follow revenue potential, not guest volume.

---

## 2. System Architecture

### 2.1 Component Overview

| Component | Purpose | Key Integrations | Traces to Finding |
|---|---|---|---|
| **Guest Data Platform (GDP)** | Unified guest profile aggregating PMS, booking engine, loyalty, email, and app data into a single Customer Data Platform | PMS, OTA feeds, booking engine, loyalty DB, email platform, app analytics | Root Cause #3: data capture failure; Insight #1: fix data foundation |
| **AI Personalisation Engine (APE)** | ML models that generate segment-aware, context-aware content, offers, and timing decisions for each guest | GDP (input), Communication Orchestrator (output), Analytics (feedback loop) | Root Cause #4: zero personalisation; Insight #2 |
| **Communication Orchestrator (CO)** | Multi-channel journey builder that executes AI-generated engagement plans across email, SMS, push, WhatsApp, and in-app | APE (decisions), email/SMS/push gateways, guest channel preferences from GDP | Root Cause #1: no post-stay engagement |
| **Loyalty Engine (LE)** | Redesigned NovaStar Rewards: tier management, points ledger, reward fulfilment, surprise-and-delight triggers | GDP (guest status), APE (trigger logic), PMS (benefit delivery), app (display) | Root Cause #2: ineffective loyalty programme |
| **Analytics & Optimisation Dashboard (AOD)** | Real-time KPI tracking, A/B test management, segment performance, funnel visualisation, and ROI attribution | All components feed data; marketing and ops teams consume insights | All root causes -- measurement and continuous improvement |

### 2.2 Architecture Diagram (Text)

```
+----------------------------------------------------------------------+
|                        GUEST TOUCHPOINTS                             |
|  [App/Web]  [Email]  [SMS/WhatsApp]  [Push]  [In-Room Tablet]       |
|  [Front Desk Tablet]  [Digital Check-in Kiosk]  [Chatbot]           |
+------+----------+----------+-----------+----------+---------+--------+
       |          |          |           |          |         |
       v          v          v           v          v         v
+----------------------------------------------------------------------+
|              COMMUNICATION ORCHESTRATOR (CO)                         |
|  - Multi-channel journey execution                                   |
|  - A/B test routing          - Channel preference management         |
|  - Send-time optimisation    - Frequency capping                     |
|  - Template rendering with dynamic AI content                        |
+------+-----------------------------------------------------------+---+
       |                                                           ^
       | triggers & content requests                               | engagement signals
       v                                                           |
+----------------------------------------------------------------------+
|              AI PERSONALISATION ENGINE (APE)                         |
|  +--------------------+  +---------------------+  +---------------+  |
|  | Segment Classifier |  | Content Generator   |  | Timing Model  |  |
|  | (6 segments +      |  | (NLG for emails,    |  | (optimal send |  |
|  |  micro-segments)   |  |  push, SMS)         |  |  windows)     |  |
|  +--------------------+  +---------------------+  +---------------+  |
|  +--------------------+  +---------------------+  +---------------+  |
|  | Offer Selector     |  | Nostalgia Engine    |  | Churn Risk    |  |
|  | (next-best-action  |  | (stay memories,     |  | Predictor     |  |
|  |  optimisation)     |  |  photo prompts)     |  | (early warn)  |  |
|  +--------------------+  +---------------------+  +---------------+  |
+------+-----------------------------------------------------------+---+
       |                                                           ^
       | profile queries & writes                                  | model feedback
       v                                                           |
+----------------------------------------------------------------------+
|              GUEST DATA PLATFORM (GDP)                               |
|  +---------------------+  +--------------------+                     |
|  | Unified Guest       |  | Identity Resolution|                     |
|  | Profile Store       |  | (OTA email -> real  |                     |
|  | (Golden Record)     |  |  guest matching)    |                     |
|  +---------------------+  +--------------------+                     |
|  +---------------------+  +--------------------+                     |
|  | Preference &        |  | Consent &          |                     |
|  | Behaviour History   |  | Privacy Manager    |                     |
|  +---------------------+  +--------------------+                     |
+------+----------+----------+-----------+----------+---------+--------+
       ^          ^          ^           ^          ^         ^
       |          |          |           |          |         |
+------+--+ +----+----+ +---+----+ +----+---+ +---+---+ +---+--------+
|   PMS   | | Booking | | OTA    | | Loyalty| |  App  | | Front-Desk |
|  (Opera/| | Engine  | | Feeds  | | DB     | | Events| | Tablet     |
|  Mews)  | |         | |        | |        | |       | |            |
+---------+ +---------+ +--------+ +--------+ +-------+ +------------+

+----------------------------------------------------------------------+
|              LOYALTY ENGINE (LE)                                      |
|  - Tier management (Explorer/Adventurer/Voyager/Ambassador)          |
|  - Points ledger & earn/burn rules                                   |
|  - Surprise-and-delight trigger execution                            |
|  - Reward catalogue & fulfilment                                     |
|  - Partner integration (airlines, experiences)                       |
+----------------------------------------------------------------------+

+----------------------------------------------------------------------+
|              ANALYTICS & OPTIMISATION DASHBOARD (AOD)                |
|  - Real-time KPI tracking    - Segment funnel analysis               |
|  - A/B test results          - Revenue attribution                   |
|  - Churn prediction alerts   - Campaign ROI                          |
|  - Executive dashboard       - Property-level performance            |
+----------------------------------------------------------------------+
```

### 2.3 Data Flow Summary

1. **Capture:** Guest data enters via PMS, booking engine, OTA feeds, front-desk tablet, app, and digital check-in. Identity Resolution merges duplicate profiles.
2. **Enrich:** APE runs segment classification, churn risk scoring, and preference inference on each unified profile in the GDP.
3. **Decide:** APE selects next-best-action (content, offer, channel, timing) for each guest based on their journey stage, segment, and behaviour.
4. **Execute:** CO delivers the personalised communication via the guest's preferred channel(s).
5. **Learn:** Engagement signals (open, click, book, ignore) feed back to APE models for continuous optimisation.
6. **Measure:** AOD aggregates all data for real-time performance monitoring and strategic reporting.

---

## 3. Guest Journey Map (To-Be)

The redesigned post-stay journey replaces NovaStar's current 3-email generic sequence with a continuous, AI-orchestrated engagement lifecycle across six stages.

### Current State (As-Is) vs. To-Be Comparison

| Dimension | Current (As-Is) | Redesigned (To-Be) |
|---|---|---|
| Touchpoints over 90 days | 3 generic emails | 12-18 personalised multi-channel touches |
| Personalisation | None | Segment, context, preference, and behaviour-driven |
| Channels | Email only | Email, SMS, push, WhatsApp, in-app |
| Data utilised | Name, email (if captured) | Full profile: segment, stay context, preferences, behaviour history |
| Loyalty integration | None | Tier status, points balance, milestone tracking woven into every touch |

### 3.1 Six-Stage To-Be Journey

| Stage | Timeframe | Touchpoints | AI Actions | Channels | Expected Outcome |
|---|---|---|---|---|---|
| **1. Warm Farewell** (Checkout) | Day 0 | Digital checkout confirmation; "Remember Your Stay" recap card with stay highlights; NovaStar Rewards sign-up prompt (if not enrolled); request for direct email/mobile (if OTA guest) | APE generates personalised stay summary (property photos, local weather during stay, amenities used); Offer Selector presents sign-up incentive calibrated to segment | App push, in-room tablet, email, front-desk tablet | Data capture rate +30pp; loyalty sign-up at checkout: 25% of non-members; positive last-impression anchoring |
| **2. Nostalgia Trigger** | Days 3-7 | "Your [City] Memories" email/push with curated stay recap; social sharing prompt; post-stay micro-survey (3 questions, not a full survey) | Nostalgia Engine selects top 3 stay highlights (room view, local attractions visited, dining); Content Generator writes segment-appropriate copy; Timing Model picks optimal send window | Email (primary), push (secondary) | Email open rate: 40%+; survey completion: 20%; social sharing: 8% of recipients; emotional brand anchoring |
| **3. Value Reinforcement** | Days 14-21 | Loyalty points summary ("You earned X points -- here's what you can unlock"); direct-booking benefit reminder; "Your Next Stay" personalised recommendation (sister property or return visit) | Segment Classifier selects recommendation type (same property vs. portfolio exploration); Offer Selector generates segment-specific incentive (family: kids-stay-free; business: late checkout guarantee; couples: seasonal experience package) | Email, app in-app message | Click-through to booking page: 8%+; loyalty programme awareness lift; direct booking intent planted |
| **4. Contextual Re-Engagement** | Days 30-60 | Seasonal/event-based trigger ("Barcelona in autumn: 5 new experiences"); destination content from Local Explorer; price-drop alert if watching a property; event reminder for Group guests | Timing Model identifies optimal re-engagement window based on segment travel patterns; Content Generator creates destination-specific content; Churn Risk Predictor flags at-risk guests for elevated offers | Email, push, SMS (for high-value segments) | Re-engagement email open rate: 25%+; Local Explorer content click-through: 12%; churn risk reduction for flagged guests |
| **5. Conversion Push** | Days 45-75 | Time-limited personalised offer; "Book direct and get [specific perk]" with best-price guarantee; loyalty tier progression nudge ("One more stay to reach Adventurer status") | Offer Selector optimises discount depth vs. margin; APE applies loss-aversion framing ("Your 500 points expire in 30 days"); Churn Risk Predictor escalates offer for high-risk, high-value guests | Email (primary), SMS (high-value), push | Booking conversion rate: 5%+ of recipients; direct booking share of conversions: 70%+; average offer discount: <12% (margin-protected) |
| **6. Ongoing Relationship** | 90+ days | Monthly "NovaStar Insider" digest (new properties, seasonal highlights); birthday/anniversary recognition; annual stay summary; referral programme prompts; re-activation campaign for lapsed guests (180+ days no activity) | APE adjusts frequency based on engagement signals (engaged guests: monthly; disengaged: quarterly with higher-value hook); Content Generator personalises digest to travel history; Churn Risk Predictor triggers re-activation sequence | Email (digest), push (milestones), SMS (re-activation) | Monthly digest open rate: 22%+; annual rebooking rate: 30%+; referral programme participation: 10% of active members |

### 3.2 Channel Selection Logic

The AI selects channels based on guest preference and engagement history:

| Signal | Channel Priority |
|---|---|
| Guest has app installed | Push (primary), email (secondary) |
| Guest provided mobile, no app | SMS/WhatsApp (primary), email (secondary) |
| Email only | Email (primary) |
| High-value guest, time-sensitive offer | SMS + email simultaneously |
| Guest disengaged from email (3+ unopened) | Channel switch to SMS/push; reduce email frequency |
| Guest unsubscribed from email | Push/SMS only (with consent); in-app messages |

---

## 4. App/Web Feature Specs

### 4.1 Feature Overview

| Feature | Purpose | Primary Segments | Traces to Finding |
|---|---|---|---|
| **Remember Your Stay** | Post-stay recap creating emotional anchoring | All segments | Root Cause #1 (no engagement), Insight #2 (personalisation) |
| **Your Next Stay** | AI-powered rebooking recommendations | All segments | Root Cause #1, #4, #7 (brand recall) |
| **NovaStar Rewards Hub** | Loyalty dashboard with tier status, points, rewards | All segments | Root Cause #2 (ineffective loyalty) |
| **Local Explorer** | Curated destination content and bookable experiences | Leisure Couples, Families, Extended-Stay | Root Cause #8 (no local content), Airbnb threat |

### 4.2 Feature: "Remember Your Stay"

**Purpose:** Transform checkout from an ending into a relationship anchor. Combat the 23% unaided brand recall (vs. 61% for Marriott) by creating memorable digital artefacts tied to the stay.

**Screen Flow:**

1. **Stay Summary Card** (auto-generated at checkout)
   - Property hero image with guest's stay dates overlaid
   - Key stats: nights stayed, city, room type, weather during visit
   - "Highlights" section: amenities used, dining, any special occasions noted by staff
   - Points earned on this stay (if loyalty member)
   - Share button (generates a social-friendly image card)

2. **Photo Memories Prompt**
   - "Add your favourite photos from [City]" -- guest can upload 3-5 photos to their NovaStar profile
   - AI suggests captions based on location and dates
   - Creates a personal "travel journal" within the app that grows with each stay

3. **Quick Feedback** (replaces the generic satisfaction survey)
   - 3 taps: "What was the best part of your stay?" (select from emoji-backed options: Room, Location, Staff, Food, Pool/Spa, Event)
   - One free-text field: "Anything we should know for next time?"
   - Feeds directly into GDP guest preference profile

**Design rationale:** Riley's research shows 23% unaided brand recall at 30 days. By creating a shareable, visual stay artefact, we anchor the NovaStar brand to the guest's positive memories. The photo upload creates a personal investment in the platform (endowment effect), increasing switching costs.

### 4.3 Feature: "Your Next Stay"

**Purpose:** AI-generated rebooking recommendations that transform the "generic 10% off" approach into a compelling, personalised travel suggestion.

**Screen Flow:**

1. **Recommendation Card** (appears in app home screen and email)
   - Headline: "Your Next [City] Adventure" or "Discover [New City] with NovaStar"
   - AI selects between same-property return or sister-property exploration based on segment
   - Visual card with property image, price starting-from, and a one-line hook
   - Example (Family): "The kids loved the Austin pool -- wait till they see NovaStar Orlando's waterpark suite. From $159/night."
   - Example (Business): "Your next Chicago trip? Same corner room, express check-in, 2x points. Book direct."

2. **Comparison View** (for guests who browsed Airbnb -- inferred from segment behaviour)
   - Side-by-side: NovaStar vs. "typical alternative" showing total cost including hidden fees, cleaning charges, inconsistency risk
   - Highlight NovaStar advantages: guaranteed cleanliness, 24/7 support, loyalty points, no cleaning fee

3. **One-Tap Booking**
   - Pre-filled with guest preferences (room type, floor, bed config, breakfast inclusion)
   - Best-price guarantee badge prominently displayed
   - "Book direct" incentive shown (e.g., "Save $22 vs. Booking.com + earn 500 NovaStar points")

### 4.4 Feature: "NovaStar Rewards Hub"

**Purpose:** Make the loyalty programme visible, aspirational, and emotionally engaging. Address the current state where "one in twenty guests mentions Rewards at check-in" (front-desk staff interview).

**Screen Flow:**

1. **Tier Dashboard**
   - Visual progress bar showing current tier and progress to next
   - Current points balance with "points are worth $X" translation
   - Next milestone: "2 more nights to reach Adventurer -- unlock free breakfast"

2. **Rewards Catalogue**
   - Browsable catalogue: room upgrades, late checkout, dining credits, local experiences, airline miles
   - "Flash Rewards" section: limited-time, high-value redemptions (e.g., suite upgrade at a new property)
   - Family-specific rewards: kids-eat-free, connecting room guarantee, early pool access

3. **Achievement Timeline**
   - Visual history of stays, points earned, rewards redeemed
   - Milestone celebrations (5th stay, 10th night, 1-year anniversary)
   - Sharable "NovaStar Traveller" badge for social media

### 4.5 Feature: "Local Explorer"

**Purpose:** Compete directly with Airbnb's perception of "local, authentic experiences" (Root Cause #8). 47% of Leisure Couples and 39% of Family Vacationers cite wanting "something more local."

**Screen Flow:**

1. **Destination Hub** (per city/property)
   - AI-curated "Top 5 This Season" experiences based on guest segment and travel dates
   - Categories: Food & Drink, Culture, Outdoors, Family Fun, Nightlife, Hidden Gems
   - Staff picks: "Recommended by [GM Name] at NovaStar [City]" -- personal touch from property staff

2. **Bookable Experiences**
   - Partner-provided local tours, cooking classes, guided walks, etc.
   - Book and pay through NovaStar app; earn loyalty points on experiences
   - Post-experience rating feeds back to AI for future recommendations

3. **Post-Stay Destination Content**
   - After checkout, guest receives seasonal updates about their visited city
   - "Barcelona in Autumn: 5 Experiences You Haven't Tried" (referenced in Riley's Insight #7)
   - Creates an ongoing content relationship that keeps NovaStar top-of-mind between stays

---

## 5. Personalisation & Retention Mechanics

### 5.1 AI Personalisation Logic

The APE uses a layered decision model:

| Layer | Input Data | Decision Output | Update Frequency |
|---|---|---|---|
| **Segment Layer** | Booking channel, trip purpose, length of stay, spend, demographics | Assign to 1 of 6 segments + micro-segments | Per booking |
| **Context Layer** | Property, dates, room type, amenities used, weather, local events | Stay-specific content themes and imagery | Per stay |
| **Preference Layer** | Stated preferences (survey), inferred preferences (behaviour), staff notes | Room configuration, dining, amenities, communication style | Progressive (each interaction) |
| **Behavioural Layer** | Email opens/clicks, app usage, booking page visits, search history | Channel selection, timing, offer intensity | Real-time |
| **Lifecycle Layer** | Total stays, recency, loyalty tier, churn risk score | Engagement intensity, escalation triggers | Daily recalculation |

### 5.2 Psychological Retention Mechanics

Each mechanic is grounded in behavioural science and mapped to Riley's findings.

| Mechanic | Psychological Principle | Implementation | Research Basis |
|---|---|---|---|
| **Nostalgia Triggers** | Peak-end rule; emotional anchoring | "Remember Your Stay" recap at Day 3-7 post-checkout; photo memories; annual stay summary | Riley: guests enjoy stays (NPS 62) but 23% brand recall at 30 days. Nostalgia bridges the satisfaction-loyalty gap. |
| **Loss Aversion** | Prospect theory; losses loom larger than gains | Points expiry warnings; tier demotion alerts ("You're 1 stay from keeping Adventurer status"); direct-booking savings shown as "You'd lose $X booking elsewhere" | Riley: 54% points breakage indicates no perceived loss in disengagement. Make inaction costly. |
| **Social Proof** | Conformity bias; informational influence | "4,200 guests rebooked at NovaStar Austin this year"; segment-specific proof ("Families love our Orlando property -- 94% would return"); staff-curated recommendations | Riley: 78% would recommend to a friend, but recommendation does not convert to action. Social proof activates intent. |
| **Surprise & Delight** | Reciprocity; positive expectation violation | AI-triggered upgrades on milestone stays (5th, 10th); birthday amenity; GM welcome-back note; random "thank you" discount for loyal guests | Riley stakeholder quote: "He switched to Hilton because they 'actually notice I exist.'" Recognition is the cheapest, highest-ROI retention tool. |
| **Endowment Effect** | Ownership bias; sunk-cost awareness | Photo memories stored in app; preference profile that "learns" over stays; tier status that would be lost; "Your NovaStar History" timeline | Riley: no switching costs exist today. Build digital assets the guest "owns" within NovaStar's ecosystem. |
| **Goal Gradient** | Accelerated effort near a goal | Tier progress bar; "2 nights to your next reward"; points-to-next-redemption countdown | Riley: 68% of loyalty members have never redeemed. Make the next reward feel close and tangible. |

### 5.3 Segment-Specific Engagement Strategies

Referencing Riley's 6 segments with tailored approaches:

| Segment | Engagement Intensity | Key Triggers | Content Themes | Primary Offer Type | Unique Mechanic |
|---|---|---|---|---|---|
| **1. Business Regulars** (22%, 17,600) | HIGH | Corporate travel cycle (Mon-Tue booking window); city-specific re-travel patterns; expense report deadlines | Consistency, speed, recognition: "Your room is ready exactly how you like it" | Late checkout guarantee, express check-in, lounge access, 2x points on midweek | **"Business Profile"**: saved preferences sync across all 45 properties; recognised by name at check-in |
| **2. Weekend Leisure Couples** (24%, 19,200) | MEDIUM-HIGH | Seasonal triggers (autumn getaway, Valentine's, anniversary); Instagram trends; new property openings | Novelty, experience, romance: "A new side of [City] you haven't seen" | Seasonal experience package, sister-property discovery, couples' dining credit | **"Portfolio Explorer"**: gamified badge system for visiting multiple NovaStar cities; novelty reframed as NovaStar exploration |
| **3. Family Vacationers** (18%, 14,400) | HIGH | School holiday pre-planning (60-90 days out); summer/winter break; property amenity updates | Value, space, kid-friendliness: "The kids are already asking to go back" | Kids-stay-free, family suite upgrade, breakfast included, early pool access | **"Family Favourites"**: saved child ages/preferences; auto-suggested age-appropriate activities; school-holiday early-access booking window |
| **4. Budget-Conscious Solo** (15%, 12,000) | LOW (standard) / MEDIUM (aspirational sub-segment ~2,400) | Price drops; flash sales; new property in budget range | Price, location, basics: "Great room, great price, great location" | Flash-sale alerts, "nomad pass" co-working access, loyalty points as currency | **"Nomad Membership"**: co-working perks, extended-stay discounts, community board for digital nomads. Light-touch; do not over-invest. |
| **5. Group/Event Attendees** (12%, 9,600) | MEDIUM-HIGH | Event anniversary dates; return-to-city triggers; event organiser re-booking | Event memory, social connection, city affinity: "Remember the Williams-Garcia wedding? Charleston is waiting." | Individual return discount tied to event city; group reunion rate; event photo gallery | **"Event Bridge"**: AI tags event context; post-stay email references specific event; converts group guest to individual relationship |
| **6. Extended-Stay / Relocation** (9%, 7,200) | HIGH | Project/relocation cycle end; new assignment start; referral opportunities | Home comfort, community, recognition: "Welcome back, resident" | Extended-stay rate lock, NovaStar Residents programme, referral bonus | **"NovaStar Residents"**: alumni-style programme; priority booking; staff relationships maintained in profile; referral programme with meaningful incentives |

---

## 6. Loyalty Programme Redesign

### 6.1 Current State Assessment

From Riley's research:
- 11.3% enrolment (benchmark: 35-50%)
- 54% points breakage (unused and expired)
- 68% of members have never redeemed
- No tiers, no status recognition, no emotional connection
- Front-desk staff "forget it exists"

### 6.2 Redesigned Tier Structure: "NovaStar Rewards"

| Tier | Name | Qualification | % of Members (Target) | Key Benefits | Emotional Hook |
|---|---|---|---|---|---|
| 1 | **Explorer** | Sign up (free) | 60% | Earn 10 pts/$ spent; member-only rates (5% off BAR); free Wi-Fi upgrade; digital check-in; Remember Your Stay recap | "Your journey begins" -- immediate tangible value at sign-up |
| 2 | **Adventurer** | 5 nights OR 2 stays in 12 months | 25% | All Explorer + room upgrade (when available); late checkout (2pm); 15 pts/$ earned; breakfast discount (25%); Local Explorer premium content | "We know how you travel" -- personalisation becomes visible |
| 3 | **Voyager** | 15 nights OR 5 stays in 12 months | 12% | All Adventurer + guaranteed upgrade; late checkout (4pm); 20 pts/$ earned; complimentary breakfast; lounge access (where available); surprise welcome amenity; annual milestone gift | "Your NovaStar, your way" -- full recognition and preference memory |
| 4 | **Ambassador** | 30 nights OR 10 stays in 12 months | 3% | All Voyager + suite upgrade (when available); guaranteed connecting room for families; personal travel concierge; airport transfer (select properties); 25 pts/$ earned; invitation to NovaStar Insider events; GM direct line | "You're family" -- exclusive access, personal relationships |

### 6.3 Points Economy

| Action | Points Earned | Notes |
|---|---|---|
| Direct booking (per $1 spent) | 10-25 pts (tier-dependent) | OTA bookings earn 0 points -- strong direct incentive |
| Completing guest profile | 500 pts (one-time) | Incentivises data capture (addresses Root Cause #3) |
| Post-stay survey completion | 200 pts | Replaces generic survey with valued feedback loop |
| Referral (friend completes stay) | 2,000 pts + referred friend gets 1,000 pts | Leverages 78% "would recommend" finding |
| Booking a Local Explorer experience | 5 pts per $1 | Drives engagement with local content feature |
| Social sharing (stay recap) | 100 pts (max 1/stay) | Organic brand awareness |

| Redemption | Points Cost | Value Ratio |
|---|---|---|
| $10 dining credit | 1,000 pts | 1 pt = $0.01 |
| Room upgrade (1 night) | 3,000 pts | ~$30 value |
| Free night (standard room) | 15,000 pts | ~$160 value |
| Local experience (up to $50) | 5,000 pts | $0.01/pt |
| Airline miles transfer (1,000 miles) | 2,000 pts | Competitive with major chains |
| Late checkout (guaranteed) | 1,500 pts | High perceived value, low cost to NovaStar |

**Design decision:** Points never expire for active members (1+ stay per 18 months). This directly addresses the 54% breakage rate and the perception that points are worthless. Inactive members receive a 90-day warning before expiry.

### 6.4 Competitive Edge vs. Airbnb

Airbnb has no loyalty programme (scores 1/10 in Riley's competitive matrix). NovaStar's redesigned Rewards creates switching costs that Airbnb cannot match:

| NovaStar Advantage | Airbnb Equivalent | Why NovaStar Wins |
|---|---|---|
| Tier status with visible perks | None | Guests accumulate status they don't want to lose (loss aversion) |
| Preference memory across 45 properties | Host-specific only; varies wildly | "Your room, your way" at any NovaStar property |
| Points earning on every dollar | Occasional credits | Tangible, growing currency creates ongoing relationship |
| Guaranteed service standards | Variable quality (Airbnb's #1 complaint) | Trust + consistency + rewards > price alone |
| Local Explorer with points earning | Airbnb Experiences (no loyalty tie-in) | Same local experience access, plus rewarded for it |
| Family-specific benefits (kids-free, connecting rooms) | No family programme | Families are habitual; reward the habit |

---

## 7. Success Metrics & KPI Targets

### 7.1 Primary KPIs

| Metric | Current Baseline (Riley's Data) | 6-Month Target | 12-Month Target | 24-Month Target | Benchmark |
|---|---|---|---|---|---|
| **Repeat booking rate** | 12.1% | 18% | 25% | 32% | 30-40% |
| **Guest data capture rate** | 43% | 60% | 75% | 85% | 70-80% |
| **Loyalty programme enrolment** | 11.3% | 22% | 40% | 50% | 35-50% |
| **Direct booking share** | 27% | 33% | 40% | 48% | 40-55% |
| **Post-stay email open rate** | 18.4% | 28% | 38% | 42% | 25-35% |
| **Post-stay email click rate** | 2.1% | 5% | 8% | 10% | 5-10% |
| **OTA commission spend** | $5.58M/yr | $5.0M | $4.2M | $3.5M | -- |

### 7.2 Segment-Level Rebooking Targets

| Segment | Current Rebooking Rate | 12-Month Target | 24-Month Target | Rationale |
|---|---|---|---|---|
| Business Regulars | 19.4% | 30% | 38% | Highest existing intent; corporate loyalty tier + recognition unlocks rapid gains |
| Weekend Leisure Couples | 10.7% | 18% | 25% | Portfolio Explorer + seasonal content converts novelty-seekers; large segment = big volume impact |
| Family Vacationers | 8.3% | 16% | 24% | Family Favourites + kids-free + school holiday early access; habitual segment once locked in |
| Budget-Conscious Solo | 6.1% | 8% | 10% | Minimal investment; Nomad Membership targets aspirational sub-segment only |
| Group/Event Attendees | 14.2% | 22% | 28% | Event Bridge closes attribution gap; individual return offers from event context |
| Extended-Stay / Relocation | 21.8% | 30% | 38% | NovaStar Residents programme; already highest NPS -- need only maintain and formalise relationship |

### 7.3 Financial Impact Projections

| Metric | Year 1 | Year 2 | Cumulative |
|---|---|---|---|
| Incremental repeat guests (vs. current 9,680) | +6,320 | +8,720 | +15,040 |
| Incremental room nights (at 3.71 avg stay) | +23,447 | +32,351 | +55,798 |
| Incremental room revenue (at $159.70 ADR) | $3.75M | $5.17M | $8.92M |
| OTA commission savings (direct shift) | $0.58M | $1.36M | $1.94M |
| Reduced acquisition costs | $0.51M | $0.89M | $1.40M |
| **Total incremental value** | **$4.84M** | **$7.42M** | **$12.26M** |

### 7.4 Operational KPIs

| Metric | Current | 12-Month Target | Owner |
|---|---|---|---|
| PMS preference fields populated | 17% | 60% | Front-desk ops + GDP automation |
| Loyalty active member rate | 47% of enrolled | 75% | Loyalty Engine + APE |
| Points redemption rate (ever redeemed) | 32% of members | 55% | Rewards catalogue + goal gradient UX |
| App install rate (among loyalty members) | ~5% (est.) | 35% | Onboarding flow + value exchange |
| Guest profile completeness score | ~20% (est.) | 55% | Progressive profiling via APE |
| Time to first post-stay contact | 14 days (promo email) | <24 hours (personalised recap) | Communication Orchestrator |
| Brand recall at 30 days (unaided) | 23% | 40% | Nostalgia triggers + ongoing content |

---

## 8. Implementation Priorities (MoSCoW)

### 8.1 MoSCoW Categorisation

| Priority | Initiative | Components Involved | Estimated Effort | Traces to Root Cause | Expected Impact |
|---|---|---|---|---|---|
| **MUST** | Guest Data Platform (unified profiles) | GDP: identity resolution, PMS integration, OTA feed ingestion | 3-4 months | RC #3 (data capture failure) | Foundation for all AI features; no personalisation possible without this |
| **MUST** | Digital check-in with data capture incentives | GDP + front-desk tablet + app | 2-3 months | RC #3 (57% no contact data) | Data capture rate 43% -> 60% in 6 months |
| **MUST** | AI Personalisation Engine (core: segment classifier + content generator) | APE: segment model, basic NLG, offer selector | 3-4 months | RC #4 (zero personalisation) | Enables all personalised communications |
| **MUST** | Communication Orchestrator (email + push) | CO: journey builder, email/push integration, template engine | 2-3 months | RC #1 (no post-stay engagement) | Replaces 3-email generic blast with multi-touch personalised journey |
| **MUST** | Best-price guarantee + rate parity enforcement | Booking engine + rate monitoring | 1-2 months | RC #6 (38% rate disparity) | Eliminates "found cheaper elsewhere" abandonment reason; direct trust |
| **MUST** | Loyalty programme tier structure launch | LE: tier logic, basic earn/burn, front-desk integration | 2-3 months | RC #2 (ineffective loyalty) | Enrolment target: 22% at 6 months; addresses "nothing compelling to say" |
| **SHOULD** | "Remember Your Stay" feature (app + email) | APE (nostalgia engine) + app + CO | 2-3 months | RC #1, #7 (brand recall 23%) | Emotional anchoring; brand recall 23% -> 35% at 30 days |
| **SHOULD** | "Your Next Stay" AI recommendations | APE (offer selector) + app + CO | 2-3 months | RC #1, #4 | Personalised rebooking pathway; click-to-book: 8%+ |
| **SHOULD** | SMS/WhatsApp channel integration | CO + consent management | 1-2 months | RC #1 (email-only limitation) | Reaches guests who don't engage with email; +15% contact rate |
| **SHOULD** | NovaStar Rewards Hub (app feature) | LE + app | 2-3 months | RC #2 | Makes loyalty visible and aspirational; drives app adoption |
| **SHOULD** | Surprise-and-delight automation | APE + LE + PMS | 1-2 months | Stakeholder feedback ("notice I exist") | Milestone recognition; 5th-stay upgrade trigger; GM welcome notes |
| **SHOULD** | Analytics & Optimisation Dashboard | AOD: KPI tracking, A/B framework, segment reporting | 2-3 months | All (measurement) | Enables data-driven iteration on all features |
| **COULD** | "Local Explorer" feature (content + partnerships) | App + partner API + APE content curation | 3-4 months | RC #8 (Airbnb local advantage) | Airbnb differentiation; destination content engagement: 30% of app users |
| **COULD** | Bookable local experiences (marketplace) | App + partner fulfilment + payment | 3-4 months | RC #8 | Revenue diversification; points-earning on experiences |
| **COULD** | Event Bridge (group-to-individual conversion) | APE + CO + GDP event tagging | 2-3 months | Insight #6 (attribution gap) | Group/Event rebooking: 14.2% -> 22% |
| **COULD** | Referral programme | LE + app + CO | 1-2 months | 78% would recommend (untapped) | Leverages existing advocacy; low-cost acquisition channel |
| **COULD** | Nomad Membership (Budget Solo sub-programme) | LE + app | 1 month | Segment 4 aspirational sub-segment | Captures future high-value guests; low investment |
| **WON'T** (this phase) | In-room tablet deployment (hardware) | Hardware + GDP | 6+ months | Nice-to-have data capture point | High capex; defer to Phase 2 after software foundation is proven |
| **WON'T** (this phase) | Airline miles transfer partnerships | LE + partner APIs | 3-4 months (negotiation-heavy) | Competitive feature but not a root-cause fix | Complex commercial negotiation; defer until loyalty base is established |
| **WON'T** (this phase) | AI chatbot for post-stay support | APE + CO + NLP platform | 4-5 months | Enhancement, not core | Build after engagement infrastructure is proven |
| **WON'T** (this phase) | Dynamic pricing AI for direct channel | Booking engine + ML pricing model | 4-6 months | RC #6 (partial) | Rate parity enforcement (MUST) addresses the immediate issue; dynamic pricing is an optimisation layer for later |

### 8.2 Phased Delivery Timeline

```
PHASE 1: FOUNDATION (Months 1-4)         PHASE 2: ENGAGEMENT (Months 3-7)
+-----------------------------------+     +-----------------------------------+
| Guest Data Platform               |     | Remember Your Stay                |
| Digital Check-in + Data Capture   | --> | Your Next Stay Recommendations    |
| AI Personalisation Engine (core)  |     | SMS/WhatsApp Channels             |
| Communication Orchestrator        |     | Surprise & Delight Automation     |
| Rate Parity Enforcement          |     | NovaStar Rewards Hub (App)        |
| Loyalty Tier Structure Launch     |     | Analytics Dashboard               |
+-----------------------------------+     +-----------------------------------+
                                                          |
                                                          v
                                          PHASE 3: DIFFERENTIATION (Months 6-10)
                                          +-----------------------------------+
                                          | Local Explorer (Content)          |
                                          | Bookable Experiences Marketplace  |
                                          | Event Bridge                      |
                                          | Referral Programme                |
                                          | Nomad Membership                  |
                                          +-----------------------------------+
```

**Note:** Phases overlap intentionally. Phase 1 components unblock Phase 2 features; Phase 2 generates the engagement data that makes Phase 3 features effective.

### 8.3 Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| PMS integration delays (legacy systems across 45 properties) | High | High | Start with 5 pilot properties in Americas region; use API middleware for PMS abstraction |
| Low front-desk adoption of data capture process | Medium | High | Gamified staff incentives; KPI shift from "check-in speed" to "check-in completeness"; tablet-based flow reduces friction |
| Guest resistance to data sharing | Medium | Medium | Value exchange at every ask; transparent privacy controls; GDPR/CCPA compliance built into GDP consent manager |
| OTA contractual restrictions on direct-booking promotion | Medium | Medium | Legal review of OTA contracts; focus on post-stay (not in-OTA) conversion; loyalty-only benefits avoid rate parity clause violations |
| AI content quality (inappropriate or generic outputs) | Low | High | Human-in-the-loop review for first 90 days; content quality scoring; fallback to curated templates if AI confidence is low |

---

## Appendix: Design Decision Traceability Matrix

Every major design decision maps to Riley's research:

| Design Decision | Riley Finding / Root Cause | Section in This Document |
|---|---|---|
| Build Guest Data Platform as first priority | RC #3: 57% no contact data; 83% blank PMS fields; Insight #1 | Sections 2.1, 8.1 (MUST) |
| Multi-channel orchestration (not email-only) | RC #1: 18.4% email open rate; single-channel limitation | Sections 2.1, 3.2 |
| Segment-specific content and offers | RC #4: identical comms for all 80,000 guests; Insight #2 | Sections 5.1, 5.3 |
| Tiered loyalty with experiential benefits | RC #2: 11.3% enrolment, no tiers, no emotion; Insight #3 | Section 6.2 |
| Direct-booking incentives (points only on direct) | RC #5: 61% OTA, $5.58M commission; Insight #4 | Sections 6.3, 8.1 |
| Local Explorer feature | RC #8: 1/10 local score, 47% want "more local"; Insight #7 | Section 4.5 |
| Family Favourites saved preferences | Segment 3: 8.3% rebooking despite 27% revenue share; Insight #5 | Section 5.3 |
| Event Bridge context tagging | Segment 5: attribution gap; Insight #6 | Section 5.3 |
| Nostalgia triggers at Days 3-7 | 23% brand recall at 30 days; satisfaction-loyalty gap | Sections 3.1, 5.2 |
| Rate parity enforcement | RC #6: 38% rate disparity; 32% booking abandonment | Section 8.1 (MUST) |
| NovaStar Residents programme | Segment 6: highest NPS (68), highest per-guest value ($1,137) | Section 5.3 |
| Low investment in Budget Solo segment | Segment 4: 15% of guests, 7% of revenue, price-driven | Section 5.3 |

---

*End of Design Document*

*Dana the Designer -- Agent 02, Team AWESOME*
