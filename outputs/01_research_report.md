# NovaStar Hotels: Repeat Booking Crisis
## Discovery Phase Research Report

**Prepared by:** Riley the Researcher (Agent 01, Team AWESOME)
**Date:** 10 February 2026
**Classification:** Internal -- Strategic
**Version:** 1.0

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Guest Segmentation Analysis](#2-guest-segmentation-analysis)
3. [Churn Funnel Breakdown](#3-churn-funnel-breakdown)
4. [Competitive Landscape Matrix](#4-competitive-landscape-matrix)
5. [Root Cause Analysis](#5-root-cause-analysis)
6. [Synthetic Data Summary](#6-synthetic-data-summary)
7. [Stakeholder Interview Themes](#7-stakeholder-interview-themes)
8. [Key Insights & Recommendations for the Designer](#8-key-insights--recommendations-for-the-designer)

---

## 1. Executive Summary

NovaStar Hotels operates 45 mid-range properties across three regions (Americas: 20 properties, Europe: 15 properties, Asia-Pacific: 10 properties) and served approximately 80,000 unique guests in the trailing twelve months. The chain enjoys strong in-stay satisfaction -- a Net Promoter Score of 62 and an average post-stay satisfaction rating of 4.3 out of 5 -- yet its repeat booking rate sits at a critically low **12.1%**. Industry benchmarks for comparable mid-range chains range from 30% to 40%.

### Headline Statistics

| Metric | NovaStar (Actual) | Mid-Range Benchmark | Gap |
|---|---|---|---|
| Repeat booking rate | 12.1% | 30--40% | -18 to -28 pp |
| Net Promoter Score | 62 | 55--65 | On par |
| Post-stay email open rate | 18.4% | 25--35% | -7 to -17 pp |
| Loyalty programme enrolment | 11.3% | 35--50% | -24 to -39 pp |
| Direct booking share | 27% | 40--55% | -13 to -28 pp |
| Guest data capture rate (email + preferences) | 43% | 70--80% | -27 to -37 pp |
| Estimated annual revenue lost to non-return | $34.2M | -- | -- |

The paradox is clear: guests enjoy their stays but see no compelling reason to return to NovaStar specifically. The chain is effectively a commodity -- interchangeable with any other mid-range option surfaced by an OTA or displaced by an Airbnb listing. This report identifies the structural causes of that commoditisation and provides a data foundation for designing an AI-powered post-stay engagement system to close the gap.

---

## 2. Guest Segmentation Analysis

Analysis of 80,000 guest records from the past 12 months reveals six distinct behavioural segments. Segmentation was derived from booking channel, trip purpose, length of stay, spend per night, geographic origin, and post-stay engagement signals.

### 2.1 Segment Overview Table

| # | Segment Name | % of Guests | Est. Guests (12 mo) | Avg. Spend / Night | Avg. Length of Stay | Current Rebooking Rate | Primary Booking Channel | NPS (Segment) |
|---|---|---|---|---|---|---|---|---|
| 1 | **Business Regulars** | 22% | 17,600 | $189 | 2.1 nights | 19.4% | Corporate portal / Direct | 58 |
| 2 | **Weekend Leisure Couples** | 24% | 19,200 | $152 | 2.4 nights | 10.7% | OTA (Booking.com, Expedia) | 66 |
| 3 | **Family Vacationers** | 18% | 14,400 | $174 | 4.2 nights | 8.3% | OTA / Airbnb comparison | 60 |
| 4 | **Budget-Conscious Solo Travellers** | 15% | 12,000 | $109 | 1.8 nights | 6.1% | OTA (price-sorted) | 55 |
| 5 | **Group/Event Attendees** | 12% | 9,600 | $141 | 2.7 nights | 14.2% | Event block / Direct | 64 |
| 6 | **Extended-Stay / Relocation** | 9% | 7,200 | $98 | 11.6 nights | 21.8% | Direct / Corporate | 68 |

### 2.2 Detailed Segment Profiles

#### Segment 1: Business Regulars (22% -- 17,600 guests)

- **Demographics:** 30--55 years old, predominantly male (64%), mid-to-senior professionals.
- **Behaviour:** Book mid-week (Tue--Thu), value fast Wi-Fi, late checkout, and proximity to business districts. Often have corporate travel policies dictating hotel choice.
- **Motivation:** Convenience, consistency, expenseable pricing. Not emotionally attached to any brand -- loyalty follows the corporate travel management tool.
- **Why they lapse:** Corporate travel policies rotate preferred vendors; NovaStar lacks a compelling corporate loyalty tier; no personalised recognition upon return.
- **Opportunity:** Highest rebooking rate of the transient segments (19.4%), yet still well below potential. These guests already have repeat intent -- they need structural reasons (loyalty points, corporate perks, recognition) to choose NovaStar over competitors.

#### Segment 2: Weekend Leisure Couples (24% -- 19,200 guests)

- **Demographics:** 25--45 years old, dual-income, no or few children. Skew slightly female decision-maker (58%).
- **Behaviour:** Book Friday--Sunday, drawn by location and photography-friendly aesthetics. Heavy social media users. Comparison-shop across OTAs and Airbnb.
- **Motivation:** Experience, novelty, Instagram-worthy moments. They want each trip to feel different.
- **Why they lapse:** NovaStar offers no "reason to return" narrative. Couples seek novelty; without seasonal packages, local-experience tie-ins, or evolving property features, the same hotel feels like a repeat rather than a new experience.
- **Opportunity:** Large segment with high satisfaction (NPS 66) but very low rebooking (10.7%). Personalised post-stay content showcasing new local experiences, seasonal offers, or sister-property suggestions could convert the novelty desire into a NovaStar portfolio exploration journey.

#### Segment 3: Family Vacationers (18% -- 14,400 guests)

- **Demographics:** 32--50 years old, 1--3 children, household income $75K--$150K. Planning-intensive; book 30--90 days in advance.
- **Behaviour:** Longest average stay among transient segments (4.2 nights). Price-sensitive but willing to pay for family-friendly amenities (connecting rooms, breakfast included, pool). Actively compare NovaStar room rates against Airbnb entire-home listings.
- **Motivation:** Value for money, space, child-friendly facilities, proximity to attractions.
- **Why they lapse:** Airbnb's whole-home listings offer more space at a comparable or lower per-night rate for families. NovaStar's post-stay communication is generic and does not address the family-specific value proposition. No kids' loyalty program or family return incentive.
- **Opportunity:** Families are habitual -- once they find a property that works, they return. The 8.3% rebooking rate is a failure of engagement, not of product. Targeted family packages, early-access booking for school holidays, and a "family favourites" saved-preferences feature could dramatically lift return rates.

#### Segment 4: Budget-Conscious Solo Travellers (15% -- 12,000 guests)

- **Demographics:** 20--35 years old, freelancers, backpackers upgrading, digital nomads. Skew male (57%).
- **Behaviour:** Shortest stays (1.8 nights), lowest spend ($109/night). Sort OTA results by price. Rarely engage with hotel brand at all -- the hotel is a place to sleep, not an experience.
- **Motivation:** Lowest acceptable price for a clean, safe, well-located room.
- **Why they lapse:** Pure price-driven behaviour. NovaStar will only win these guests when it is the cheapest option on the OTA, which is margin-destructive.
- **Opportunity:** Lowest-priority segment for re-engagement investment. However, a subset (~20% of this segment, approx. 2,400 guests) are "aspirational upgraders" -- digital nomads who will spend more as their income grows. Light-touch engagement (e.g., "nomad membership" with co-working perks) can capture future value.

#### Segment 5: Group/Event Attendees (12% -- 9,600 guests)

- **Demographics:** Mixed, defined by event (conferences, weddings, sports events). Wide age range.
- **Behaviour:** Booking driven by event organiser or block reservation. Limited individual brand interaction during stay. Moderate satisfaction -- they associate the positive experience with the event, not the hotel.
- **Motivation:** Proximity to event venue, group rate, social belonging.
- **Why they lapse:** Attribution gap -- positive memories are tagged to the event, not NovaStar. Post-stay emails are generic and do not reference the event context. No mechanism to convert a group attendee into an individual guest.
- **Opportunity:** With a 14.2% rebooking rate, this segment shows latent loyalty. Post-event follow-up referencing the specific event, combined with a "return to [city]" individual offer, can bridge the attribution gap.

#### Segment 6: Extended-Stay / Relocation (9% -- 7,200 guests)

- **Demographics:** 28--50 years old, project-based workers, relocating professionals, insurance-placed guests. Higher proportion of corporate-billed stays.
- **Behaviour:** Longest stays (11.6 nights average), lowest per-night spend ($98) due to extended-stay discounts. High engagement with on-site facilities (laundry, kitchenette, gym). Build relationships with staff.
- **Motivation:** Home-like comfort, predictable costs, proximity to work site.
- **Why they lapse:** Project or relocation ends. NovaStar does not maintain the relationship for the guest's next relocation or project assignment. No "welcome back" pathway.
- **Opportunity:** Highest rebooking rate (21.8%) already, and highest NPS (68). These guests are natural advocates. A lightweight alumni programme ("NovaStar Residents") could turn them into repeat guests and referral sources.

### 2.3 Segment Revenue Contribution

| Segment | % of Guests | % of Room Nights | % of Revenue | Revenue / Guest |
|---|---|---|---|---|
| Business Regulars | 22% | 18% | 23% | $397 |
| Weekend Leisure Couples | 24% | 22% | 21% | $365 |
| Family Vacationers | 18% | 29% | 27% | $731 |
| Budget-Conscious Solo | 15% | 10% | 7% | $196 |
| Group/Event Attendees | 12% | 12% | 11% | $381 |
| Extended-Stay / Relocation | 9% | 9% | 11% | $1,137 |

Family Vacationers and Extended-Stay guests punch well above their weight in revenue contribution due to longer stays. These are high-value segments where improved retention yields disproportionate revenue impact.

---

## 3. Churn Funnel Breakdown

The guest lifecycle from first stay to repeat booking follows a five-stage funnel. At each stage, NovaStar haemorrhages potential repeat guests. The data below synthesises booking records, email engagement metrics, and website analytics for the 80,000 guests over the trailing 12-month period.

### 3.1 Funnel Stages and Drop-off Rates

```
Stage 1: FIRST STAY COMPLETED
  80,000 guests (100%)
      |
      |  Drop-off: 57% never receive meaningful post-stay contact
      |  (email not captured, opt-out, incorrect address, generic blast ignored)
      v
Stage 2: POST-STAY CONTACT ENGAGED
  34,400 guests (43%)
      |
      |  Drop-off: 62% of contacted guests do not engage
      |  (email unopened, no click-through, unsubscribe)
      v
Stage 3: ACTIVE CONSIDERATION
  13,072 guests (16.3% of original)
      |
      |  Drop-off: 56% consider but do not convert
      |  (price comparison lost, chose Airbnb, chose competitor, trip not taken)
      v
Stage 4: BOOKING INTENT (visit booking page or call)
  5,752 guests (7.2% of original)
      |
      |  Drop-off: 32% abandon at booking stage
      |  (price shock on direct site, better OTA deal found, trip cancelled)
      v
Stage 5: REPEAT BOOKING CONFIRMED
  3,920 guests (4.9% direct repeat*)
      |
      |  * Additional 5,760 rebook via OTA without NovaStar attribution
      |  Total effective rebooking: ~9,680 guests (12.1%)
      v
```

### 3.2 Funnel Visualisation (Text)

```
FIRST STAY              |==================================================| 80,000  (100.0%)
                        |                                                  |
POST-STAY ENGAGED       |=====================                             | 34,400  ( 43.0%)
                        |                                                  |
ACTIVE CONSIDERATION    |========                                          | 13,072  ( 16.3%)
                        |                                                  |
BOOKING INTENT          |====                                              |  5,752  (  7.2%)
                        |                                                  |
REPEAT BOOKED (Direct)  |==                                                |  3,920  (  4.9%)
                        |                                                  |
REPEAT BOOKED (All)     |=====                                             |  9,680  ( 12.1%)
```

### 3.3 Key Funnel Observations

1. **The biggest single leak is at Stage 1 to Stage 2** (57% drop-off). NovaStar fails to capture usable guest contact data for more than half its guests. Guests who book via OTAs often have their email masked by the OTA, and front-desk check-in does not systematically collect direct email or communication preferences.

2. **Post-stay email engagement (Stage 2 to 3) is critically weak.** Of the 34,400 guests who do receive post-stay email, only 38% engage. The current post-stay email sequence is:
   - Day 1 post-checkout: Generic satisfaction survey (open rate: 22.1%, completion rate: 8.7%)
   - Day 14: Promotional blast -- "Book again and save 10%" (open rate: 14.2%, click rate: 2.1%)
   - Day 60: Re-engagement email (open rate: 11.8%, click rate: 1.4%)
   - No further contact unless guest opts into marketing newsletter

3. **The hidden OTA re-booking problem.** Approximately 5,760 guests (7.2%) do rebook at a NovaStar property but do so through an OTA, meaning NovaStar pays 15--22% commission and has no ability to build a direct relationship. These are guests who chose NovaStar again but were not given a compelling reason to book direct.

4. **Booking-page abandonment (Stage 4 to 5) at 32%** indicates pricing or UX friction on the direct booking path. Competitor rate-matching or best-price guarantees are not prominently displayed, and the NovaStar direct site lacks parity with OTA pricing in 38% of sampled rate checks.

### 3.4 Funnel by Segment

| Stage | Business Regulars | Leisure Couples | Family Vacationers | Budget Solo | Group/Event | Extended-Stay |
|---|---|---|---|---|---|---|
| First Stay | 100% | 100% | 100% | 100% | 100% | 100% |
| Post-Stay Engaged | 54% | 38% | 41% | 29% | 47% | 62% |
| Active Consideration | 24% | 13% | 15% | 7% | 18% | 31% |
| Booking Intent | 12% | 5% | 4% | 2% | 8% | 16% |
| Repeat Booked (All) | 19.4% | 10.7% | 8.3% | 6.1% | 14.2% | 21.8% |

Note: "Repeat Booked (All)" exceeds "Booking Intent" in some segments because some guests rebook via OTA or corporate portal without visiting NovaStar's direct booking page, bypassing the tracked funnel.

---

## 4. Competitive Landscape Matrix

### 4.1 Primary Competitor Comparison

| Dimension | NovaStar Hotels | Marriott Bonvoy | Hilton Honors | IHG One Rewards | Airbnb | Booking.com | Expedia |
|---|---|---|---|---|---|---|---|
| **Post-Stay Engagement** | Generic survey + 2 promo emails over 60 days | Multi-touch personalised journey; app push notifications; status-based offers | Personalised email series; Hilton Honors app with stay summaries; milestone celebrations | Targeted email + app engagement; point-expiry reminders | Host-sent thank-you messages; Airbnb algorithm re-surfaces similar listings | Genius loyalty emails; "You looked at [city]" retargeting | Retargeting ads; reward point reminders |
| **Quality Score** | 2/10 | 8/10 | 8/10 | 7/10 | 6/10 | 7/10 | 6/10 |
| | | | | | | | |
| **Personalisation** | None -- all guests receive identical communications | Deep: room preference memory, welcome amenity by tier, AI-suggested destinations | Strong: Digital Key, room selection, connected room for families | Moderate: milestone rewards, room preferences | Host-driven; varies wildly; platform suggests "based on your trips" | Moderate: Genius-tier pricing, smart recommendations | Moderate: member pricing, trip boards |
| **Quality Score** | 1/10 | 9/10 | 8/10 | 6/10 | 7/10 (variable) | 6/10 | 5/10 |
| | | | | | | | |
| **Loyalty Programme** | "NovaStar Rewards" exists on paper; <12% enrolment; earn-and-burn points with no aspirational tiers | Gold/Platinum/Titanium/Ambassador tiers; points never expire with activity; 30+ airline transfer partners | Silver/Gold/Diamond tiers; 5th-night-free reward; points + money flexibility | Club/Gold/Platinum/Diamond; milestone bonuses; PointBreaks value deals | No formal loyalty; Airbnb credits occasionally offered | Genius Levels 1/2/3; automatic enrolment; instant discounts | Silver/Gold tiers; member-only pricing; one-key rewards |
| **Quality Score** | 2/10 | 10/10 | 9/10 | 7/10 | 1/10 | 7/10 | 6/10 |
| | | | | | | | |
| **Pricing Flexibility** | Rigid rack rates; 10% direct-booking discount poorly promoted; no dynamic member pricing | Best-rate guarantee; PointSavers; dynamic member pricing; flexible cancellation | Price match guarantee; Points + Money combos; flexible dates tool | Best-price guarantee; PointBreaks; flexible member rates | Dynamic host pricing; long-stay discounts; negotiable on some listings | Genius discounts (10--20%); Secret Deals; free cancellation as standard | Member pricing; bundled flight+hotel deals; flexible date search |
| **Quality Score** | 3/10 | 8/10 | 8/10 | 7/10 | 8/10 | 8/10 | 8/10 |
| | | | | | | | |
| **Local Experience Integration** | No integration; generic area guide PDF in room | Bonvoy Moments (bookable experiences); Marriott EDITION curated local guides | Hilton Experiences; property-specific local partnerships | Limited; some properties offer local tours via concierge | Airbnb Experiences deeply integrated; local hosts as guides | Booking.com Experiences marketplace; Things to Do tab | Expedia Local Expert desk; activities marketplace |
| **Quality Score** | 1/10 | 7/10 | 6/10 | 4/10 | 9/10 | 7/10 | 6/10 |

### 4.2 Competitive Position Summary

```
                    Post-Stay    Personalisation    Loyalty    Pricing    Local Exp.    TOTAL
                    Engagement                      Programme  Flexibility Integration  (/50)
NovaStar            2            1                  2          3          1             9
Marriott Bonvoy     8            9                  10         8          7             42
Hilton Honors       8            8                  9          8          6             39
IHG One Rewards     7            6                  7          7          4             31
Airbnb              6            7                  1          8          9             31
Booking.com         7            6                  7          8          7             35
Expedia             6            5                  6          8          6             31
```

**NovaStar scores 9 out of 50 -- dead last** against every meaningful competitor. The gap is not in the in-stay product (which scores competitively on guest satisfaction) but in every dimension of the pre-and-post-stay relationship.

### 4.3 The Airbnb Threat: Specific Analysis

Airbnb is NovaStar's most dangerous competitor for the Family Vacationer and Weekend Leisure Couples segments. Key comparative data:

| Factor | NovaStar (Mid-Range) | Airbnb (Comparable Listing) |
|---|---|---|
| Avg. nightly rate (family, 2BR equivalent) | $174 (room) + $89 (adjoining) = $263 | $195 (entire home) |
| Space per guest | ~350 sq ft (standard room) | ~900 sq ft (avg. 2BR listing) |
| Kitchen access | Limited (minibar, microwave) | Full kitchen (89% of listings) |
| Check-in flexibility | 3pm check-in / 11am checkout | Flexible, often self-check-in |
| Local feel | Standardised hotel experience | Neighbourhood immersion |
| Post-stay relationship | With brand (NovaStar) | With host (personal) |
| Repeat booking friction | High (re-search on OTA) | Low (message host directly) |

For a family of four on a 4-night stay, Airbnb saves approximately **$272** while providing nearly triple the living space and a full kitchen. NovaStar cannot win on price or space -- it must win on trust, consistency, convenience, and loyalty rewards.

---

## 5. Root Cause Analysis

The following root causes are ranked by estimated impact on the repeat-booking gap. Impact is calculated as the estimated percentage-point lift in rebooking rate if the cause were fully addressed.

### 5.1 Ranked Root Causes

| Rank | Root Cause | Impact | Est. Rebooking Lift | Supporting Data |
|---|---|---|---|---|
| 1 | **No meaningful post-stay engagement** | HIGH | +6--8 pp | Only 43% of guests receive any post-stay contact; those who do get generic, untargeted emails with 18.4% open rate (vs. 30%+ benchmark). 57% of guests vanish into a data void after checkout. |
| 2 | **Absent or ineffective loyalty programme** | HIGH | +5--7 pp | NovaStar Rewards has 11.3% enrolment vs. 35--50% benchmark. Programme offers only basic earn-and-burn points with no status tiers, no aspirational benefits, and no emotional hook. 68% of enrolled members have never redeemed a single point. |
| 3 | **Failure to capture guest data at booking/check-in** | HIGH | +4--6 pp | 57% of guests have no usable direct email on file. OTA bookings (61% of total) come with masked email addresses. Front-desk staff report no training or incentive to capture direct contact information. PMS (property management system) data fields for guest preferences are blank for 83% of records. |
| 4 | **Zero personalisation in guest communications** | MEDIUM-HIGH | +3--5 pp | All 80,000 guests receive identical email templates regardless of segment, stay purpose, or behaviour. No dynamic content. No trip-context awareness. A family who stayed for a week at a beach property receives the same email as a solo business traveller who stayed one night in a city centre. |
| 5 | **OTA dependency eroding direct relationship** | MEDIUM-HIGH | +3--4 pp | 61% of bookings come through OTAs. NovaStar pays 15--22% commission on these. Critically, 5,760 repeat guests (59% of all repeat bookings) rebook via OTA rather than direct, meaning NovaStar has no attribution and pays commission even on its most loyal guests. |
| 6 | **No price parity between direct site and OTAs** | MEDIUM | +2--3 pp | In 38% of sampled rate checks, OTA prices undercut NovaStar's own website. This makes "book direct" messaging actively counterproductive and erodes trust. Booking-page abandonment rate is 32%, with exit surveys citing "found a better price elsewhere" as the #1 reason (41% of respondents). |
| 7 | **Generic, non-differentiated brand positioning** | MEDIUM | +2--3 pp | NovaStar's brand promise ("Comfortable stays, great value") is indistinguishable from any mid-range chain. Guest post-stay surveys show only 23% can recall the NovaStar brand name unprompted one month after their stay, compared to 61% for Marriott and 54% for Hilton. |
| 8 | **No local experience or destination content** | MEDIUM | +1--3 pp | Airbnb's competitive advantage is not just price -- it is the perception of local, authentic experiences. NovaStar provides a generic area guide PDF and no curated local experiences. 47% of Leisure Couples and 39% of Family Vacationers cite "wanting something more local" as a reason they consider Airbnb over hotels for their next trip. |

### 5.2 Root Cause Interdependency Map

Many causes are interconnected:

```
Data Capture Failure (#3)
    |
    +--> No Post-Stay Engagement (#1)
    |        |
    |        +--> No Personalisation (#4)
    |        |        |
    |        |        +--> Weak Loyalty Programme (#2)
    |        |                 |
    |        |                 +--> Low Rebooking Rate
    |        |
    |        +--> Low Brand Recall (#7)
    |                 |
    |                 +--> OTA Dependency (#5)
    |                          |
    |                          +--> Price Parity Issues (#6)
    |                                   |
    |                                   +--> Booking Abandonment
    |
    +--> No Local Content (#8)
             |
             +--> Airbnb Preference
```

The root of the problem is fundamentally a **data and engagement infrastructure failure**. NovaStar checks guests in, provides a good stay, checks them out, and then loses them forever because it has no mechanism to maintain the relationship.

---

## 6. Synthetic Data Summary

### 6.1 Core Metrics (Trailing 12 Months)

| Metric | Value |
|---|---|
| Total unique guests | 80,000 |
| Total room nights sold | 296,800 |
| Average length of stay | 3.71 nights |
| Total revenue (rooms) | $47.4M |
| Average revenue per guest | $592.50 |
| Average daily rate (ADR) | $159.70 |
| Occupancy rate (chain-wide) | 71.3% |
| RevPAR (Revenue per Available Room) | $113.85 |
| Total properties | 45 |
| Regions | Americas (20), Europe (15), APAC (10) |

### 6.2 Booking Channel Distribution

| Channel | % of Bookings | # of Bookings | Commission Rate | Est. Commission Paid |
|---|---|---|---|---|
| Booking.com | 28% | 22,400 | 17% avg | $2.27M |
| Expedia Group | 19% | 15,200 | 20% avg | $1.81M |
| Other OTAs | 14% | 11,200 | 18% avg | $1.20M |
| **Total OTA** | **61%** | **48,800** | -- | **$5.28M** |
| NovaStar.com (Direct Web) | 16% | 12,800 | 0% | $0 |
| Phone / Walk-in | 7% | 5,600 | 0% | $0 |
| Corporate / Group Block | 12% | 9,600 | 2% avg (GDS) | $0.11M |
| Travel Agent | 4% | 3,200 | 10% avg | $0.19M |
| **Total Direct + Other** | **39%** | **31,200** | -- | **$0.30M** |
| | | | **Total Commission** | **$5.58M** |

NovaStar pays **$5.58M annually** in distribution costs, representing 11.8% of room revenue. Shifting just 10% of OTA bookings to direct would save approximately $560K per year.

### 6.3 Guest Satisfaction Metrics

| Metric | Score |
|---|---|
| Net Promoter Score (NPS) | 62 |
| Overall satisfaction (post-stay survey, 1--5) | 4.3 |
| Room cleanliness (1--5) | 4.5 |
| Staff friendliness (1--5) | 4.4 |
| Value for money (1--5) | 3.9 |
| Check-in experience (1--5) | 4.1 |
| Facilities & amenities (1--5) | 3.8 |
| Would recommend to a friend (% yes) | 78% |
| Post-stay survey response rate | 8.7% (of guests contacted) |

### 6.4 Post-Stay Email Engagement

| Email | Send Volume | Open Rate | Click Rate | Conversion Rate |
|---|---|---|---|---|
| Day 1: Satisfaction survey | 34,400 | 22.1% | 8.7% (complete survey) | n/a |
| Day 14: "Book again" promo | 32,100* | 14.2% | 2.1% | 0.3% |
| Day 60: Re-engagement | 29,800* | 11.8% | 1.4% | 0.2% |

*Volume decreases due to unsubscribes and bounces.

**Composite post-stay email engagement rate: 18.4%** (% of recipients who opened at least one email in the sequence).

### 6.5 Repeat Booking Analysis

| Metric | Value |
|---|---|
| Guests who booked 2+ times in 12 months | 9,680 (12.1%) |
| - Of which, booked direct on return | 3,920 (4.9%) |
| - Of which, booked via OTA on return | 5,760 (7.2%) |
| Average time between stays (repeaters) | 4.8 months |
| Repeat guests who booked same property | 62% |
| Repeat guests who booked different NovaStar property | 38% |

### 6.6 Loyalty Programme Metrics

| Metric | Value |
|---|---|
| NovaStar Rewards members | 9,040 (11.3% of guests) |
| Active members (earned or redeemed in 12 mo) | 4,250 (47% of members) |
| Members who have ever redeemed | 2,893 (32% of members) |
| Average points balance (unredeemed) | 3,420 points (~$34 value) |
| Points breakage rate (expired unused) | 54% |

### 6.7 Revenue Impact of Lost Repeat Bookings

If NovaStar achieved the mid-range benchmark of 35% repeat booking rate:

| Scenario | Current | Benchmark Target | Difference |
|---|---|---|---|
| Repeat guests | 9,680 | 28,000 | +18,320 |
| Incremental room nights (3.71 avg stay) | -- | 67,968 | +67,968 |
| Incremental revenue (at $159.70 ADR) | -- | $10.86M | +$10.86M |
| Reduced OTA commission (50% shift to direct) | -- | -- | +$1.40M |
| Reduced acquisition cost (repeat vs. new) | -- | -- | +$2.74M* |
| **Total estimated annual revenue impact** | -- | -- | **+$15.0M** |

*Acquiring a new guest costs an estimated $38 (marketing + OTA commission allocated), while retaining a repeat guest costs approximately $8. For 18,320 incremental repeat guests, the saving is (38-8) x 18,320 x a blended factor for guests who would have been acquired anyway = ~$2.74M.

Conservative estimate of **$34.2M in total revenue opportunity** when factoring in lifetime value over 3 years, referral effects, and higher ancillary spend from loyal guests ($34.2M = $15.0M direct annual impact x 2.28 LTV multiplier).

---

## 7. Stakeholder Interview Themes

Simulated interviews were conducted with key stakeholder groups across NovaStar's operations. Below are the synthesised themes and representative quotes.

### 7.1 Hotel General Managers (8 interviews across 3 regions)

**Theme 1: Awareness of the problem, powerlessness to act**

> "I know we're losing guests. I can see it in the numbers. But I have no tools to do anything about it. After checkout, the guest belongs to corporate marketing -- and corporate sends them a generic email that has nothing to do with their stay at my property."
> -- *GM, NovaStar Austin (Americas)*

> "We had a family stay with us for a full week last summer. Amazing guests, loved the property, left a glowing review. They came back to Austin six months later and booked an Airbnb. I only know because the front-desk manager ran into them at a coffee shop. When I asked why they didn't return, they said they 'didn't even think of us.' That's the problem in a nutshell."
> -- *GM, NovaStar Austin (Americas)*

**Theme 2: Data captured at property level is not used**

> "My team makes notes about guest preferences -- extra pillows, room-temperature preference, anniversary celebrations. It goes into the PMS. But when that guest books at another NovaStar property, or even comes back to ours, none of that information surfaces. It's like we have amnesia."
> -- *GM, NovaStar Barcelona (Europe)*

**Theme 3: Loyalty programme is an afterthought**

> "Honestly, I forget NovaStar Rewards exists. My front-desk team doesn't mention it because there's nothing compelling to say. 'Earn points towards a free night' -- every chain says that. There's no tier status, no recognition, nothing that makes a guest feel special."
> -- *GM, NovaStar Osaka (APAC)*

### 7.2 Front-Desk Staff (12 interviews)

**Theme 1: No incentive or training to capture guest data**

> "We're measured on check-in speed. If I take an extra two minutes to get a guest's email, preferences, and sign them up for Rewards, my queue backs up and I get flagged. So I don't."
> -- *Front Desk Associate, NovaStar Chicago (Americas)*

> "The OTA bookings come in with a weird relay email address. We know we should ask for the real one, but most guests are tired from travel and just want their room key. It feels intrusive to ask."
> -- *Front Desk Supervisor, NovaStar London (Europe)*

**Theme 2: Guests don't know about NovaStar Rewards**

> "I'd say maybe one in twenty guests mentions Rewards at check-in. Most have no idea it exists. Even when they're enrolled, they don't know their points balance or what they can do with them."
> -- *Front Desk Associate, NovaStar Miami (Americas)*

**Theme 3: Repeat guests get no recognition**

> "We had a gentleman who stayed with us every month for six months -- corporate travel. He never got so much as an upgraded room or a welcome note. He eventually told me he switched to Hilton because they 'actually notice I exist.' That stuck with me."
> -- *Front Desk Associate, NovaStar Singapore (APAC)*

### 7.3 Marketing Team (6 interviews -- HQ and Regional)

**Theme 1: Working with insufficient data**

> "I can't personalise what I can't see. Fifty-seven percent of our guests are effectively ghosts -- no email, no preferences, no history. For the ones I do have, the data is so thin that the best I can do is 'Dear Guest, we hope you enjoyed your stay.' It's embarrassing."
> -- *Director of CRM, NovaStar HQ*

**Theme 2: No technology for journey orchestration**

> "We use a basic email platform. No CDP, no journey builder, no AI, no real-time triggers. I write three emails that go to everyone on the same schedule. I've proposed a customer data platform twice and been told it's 'not in the budget.' Meanwhile, we're spending $5.5 million a year on OTA commissions."
> -- *Head of Digital Marketing, NovaStar HQ*

> "The irony is that we have enough data to be smart -- stay dates, room type, property, spend -- but it's locked in the PMS, the booking engine, and the Rewards database, and none of them talk to each other. I'd need an engineer and six months just to build a unified guest profile."
> -- *Regional Marketing Manager, NovaStar Europe*

**Theme 3: Desire for AI-driven engagement**

> "What I want is simple: know who the guest is, know why they stayed, know what would bring them back, and send the right message at the right time. That's it. An AI system that can do that would transform our numbers overnight."
> -- *Director of CRM, NovaStar HQ*

> "Marriott is sending personalised push notifications based on a guest's destination preferences before the guest even knows they want to travel. We're sending a flat-rate '10% off your next stay' email 14 days after checkout. The gap is not 10% -- it's 10 years."
> -- *Head of Digital Marketing, NovaStar HQ*

### 7.4 Cross-Cutting Theme: The "Satisfaction-Loyalty Gap"

Every stakeholder group articulated the same fundamental paradox: guests are satisfied with their stay, but satisfaction does not translate to loyalty. The organisation delivers a good product but has no post-stay relationship infrastructure. As one GM summarised:

> "We're a great one-night stand. Guests enjoy us, but they don't call back. And honestly, we don't call them either."
> -- *GM, NovaStar Denver (Americas)*

---

## 8. Key Insights & Recommendations for the Designer

Based on the full discovery phase, the following insights should directly inform the design of the AI-powered post-stay engagement system.

### Insight 1: Fix the Data Foundation Before Building the AI

**Finding:** 57% of guests have no usable direct contact information. Guest preference data is blank for 83% of PMS records. Systems (PMS, booking engine, loyalty database) are siloed.

**Implication for design:** The AI system must include a **data capture layer** -- not just a communication layer. This means:
- A smart check-in flow (digital or in-person) that incentivises guests to share their email and preferences in exchange for a tangible benefit (e.g., room selection, early checkout notification, Wi-Fi upgrade)
- Integration middleware that unifies PMS, booking engine, and loyalty data into a single guest profile
- OTA email de-anonymisation strategies (e.g., "text us to get your room details" as a way to capture mobile numbers)

### Insight 2: Personalisation is the Single Highest-Leverage Intervention

**Finding:** All 80,000 guests receive identical communications. The competitive gap on personalisation is 1/10 vs. 8--9/10 for major chains.

**Implication for design:** The AI engine must segment and personalise at the individual level, not the campaign level. Design for:
- **Segment-aware messaging** (a family should receive family content, a business traveller should receive business content)
- **Context-aware timing** (a leisure couple who stayed in Barcelona in June should receive a "Barcelona in autumn" message in September, not a generic "book again" blast in July)
- **Progressive profiling** (each interaction teaches the system more about the guest, enriching the profile over time)

### Insight 3: The Loyalty Programme Needs to Be Rebuilt Around Emotional, Not Transactional, Value

**Finding:** NovaStar Rewards has 11.3% enrolment and 54% points breakage. The programme offers no status recognition, no aspirational tiers, and no emotional connection.

**Implication for design:** Do not simply layer AI on top of the existing Rewards programme. Redesign the loyalty concept:
- **Introduce status tiers** with visible, experiential benefits (room upgrade, late checkout, welcome amenity) rather than purely points-based rewards
- **Use AI to create "surprise and delight" moments** -- the system identifies a guest's 5th stay and triggers a complimentary upgrade or a personalised thank-you from the GM
- **Make loyalty feel personal**, not programmatic. A message that says "Welcome back, Sarah -- we've set up your room with extra pillows, just the way you like it" is worth more than 1,000 points

### Insight 4: Recapture OTA Guests Into the Direct Relationship

**Finding:** 61% of bookings come through OTAs ($5.58M in annual commission). Even 59% of repeat guests rebook via OTA.

**Implication for design:** The AI system must include a **direct-booking conversion pathway**:
- During stay: Digital touchpoints (e.g., in-app chat, in-room tablet) that surface "book your next stay direct and save" offers at moments of high satisfaction
- Post stay: AI-generated offers that are exclusively available through direct booking, creating a genuine reason to bypass the OTA
- Price parity enforcement: The system should flag rate disparities in real time and ensure the direct channel is never more expensive

### Insight 5: Segment Investment Strategically -- Not All Guests Are Equal

**Finding:** Family Vacationers (18% of guests) generate 27% of revenue. Extended-Stay guests (9%) generate 11% of revenue with the highest per-guest value ($1,137). Budget Solo travellers (15%) generate only 7% of revenue.

**Implication for design:** The AI system should allocate engagement intensity based on segment value:
- **High-touch AI engagement:** Business Regulars, Family Vacationers, Extended-Stay (high value, improvable rebooking rates)
- **Medium-touch AI engagement:** Weekend Leisure Couples, Group/Event Attendees (high volume, moderate value)
- **Light-touch AI engagement:** Budget-Conscious Solo Travellers (low margin, low rebooking potential -- focus only on the "aspirational upgrader" subsegment)

### Insight 6: Bridge the "Attribution Gap" for Event and Group Guests

**Finding:** Group/Event attendees (12% of guests) associate their positive experience with the event, not the hotel. Post-stay emails make no reference to the event context.

**Implication for design:** The AI system should:
- Tag guests with event context at check-in
- Send post-stay messages that reference the event ("We hope the Williams-Garcia wedding was wonderful -- next time you're in Charleston, your NovaStar room is waiting")
- Offer individual return incentives that build on the group experience

### Insight 7: Build for Local Experiences as a Differentiator Against Airbnb

**Finding:** NovaStar scores 1/10 on local experience integration vs. 9/10 for Airbnb. 47% of Leisure Couples and 39% of Family Vacationers cite "wanting something more local" as a reason to consider Airbnb.

**Implication for design:** The AI system should curate and deliver **hyper-local content** as part of the post-stay engagement:
- "Your next visit to Barcelona: 5 experiences you haven't tried" (AI-curated based on the guest's previous activities and season of travel)
- Partnerships with local experience providers, bookable through the NovaStar app
- Position NovaStar not as a hotel chain but as a "local access platform" -- you get Airbnb's local flavour with hotel-grade consistency

---

## Appendices

### Appendix A: Methodology Notes

All data in this report is synthetic, created for an academic exercise exploring AI agent team collaboration. The data was designed to be internally consistent and realistic relative to publicly available hospitality industry benchmarks. Sources informing the realism of the synthetic data include:

- STR Global hotel performance benchmarks (ADR, occupancy, RevPAR ranges)
- Phocuswright research on OTA market share and commission structures
- McKinsey & Company hospitality loyalty programme studies
- Cornell Hospitality Quarterly research on repeat booking drivers
- Public investor presentations from Marriott International, Hilton Worldwide, and IHG

### Appendix B: Definitions

| Term | Definition |
|---|---|
| ADR | Average Daily Rate -- total room revenue divided by rooms sold |
| RevPAR | Revenue Per Available Room -- ADR multiplied by occupancy rate |
| NPS | Net Promoter Score -- % Promoters minus % Detractors (scale -100 to +100) |
| OTA | Online Travel Agency (e.g., Booking.com, Expedia) |
| PMS | Property Management System -- hotel operations software |
| CDP | Customer Data Platform -- unified guest data repository |
| pp | Percentage points |
| LTV | Lifetime Value -- total projected revenue from a guest over the relationship |

### Appendix C: Segment-Level Data Tables

Full segment-level breakdowns are embedded in Section 2. Additional cross-tabulations available on request.

---

*End of Report*

*Riley the Researcher -- Agent 01, Team AWESOME*
