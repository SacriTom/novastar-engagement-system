"""
NovaStar Hotels -- AI-Powered Post-Stay Engagement Engine
==========================================================
Core logic for guest profiling, personalised offer generation,
and multi-channel trigger orchestration.

Maps to Dana's System Architecture (02_solution_design.md):
  - AI Personalisation Engine (APE)
  - Communication Orchestrator (CO)
  - Loyalty Engine (LE) basics

Prepared by: Max the Maker (Agent 03, Team AWESOME)

Runnable with Python 3.10+ standard library only.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Optional

from data_models import (
    BookingChannel,
    ChannelType,
    Guest,
    GuestPreferences,
    GuestSegment,
    InteractionType,
    JourneyStage,
    LoyaltyAccount,
    LoyaltyTier,
    Offer,
    Stay,
)


# ===================================================================
# 1. GUEST PROFILER -- Segment Classifier + Churn Risk
# ===================================================================

# Engagement intensity per segment (Dana, Section 5.3)
SEGMENT_INTENSITY: dict[GuestSegment, str] = {
    GuestSegment.BUSINESS_REGULAR: "HIGH",
    GuestSegment.WEEKEND_LEISURE_COUPLE: "MEDIUM-HIGH",
    GuestSegment.FAMILY_VACATIONER: "HIGH",
    GuestSegment.BUDGET_SOLO: "LOW",
    GuestSegment.GROUP_EVENT: "MEDIUM-HIGH",
    GuestSegment.EXTENDED_STAY: "HIGH",
}

# Baseline rebooking probability per segment (Riley, Section 2.1)
SEGMENT_BASE_REBOOK: dict[GuestSegment, float] = {
    GuestSegment.BUSINESS_REGULAR: 0.194,
    GuestSegment.WEEKEND_LEISURE_COUPLE: 0.107,
    GuestSegment.FAMILY_VACATIONER: 0.083,
    GuestSegment.BUDGET_SOLO: 0.061,
    GuestSegment.GROUP_EVENT: 0.142,
    GuestSegment.EXTENDED_STAY: 0.218,
}


@dataclass
class GuestProfile:
    """Enriched profile produced by the AI Personalisation Engine."""
    guest: Guest
    stay: Stay
    preferences: GuestPreferences
    loyalty: Optional[LoyaltyAccount] = None
    churn_risk: float = 0.5               # 0 = safe, 1 = certain churn
    engagement_score: float = 0.0         # running engagement metric
    days_since_checkout: int = 0
    journey_stage: JourneyStage = JourneyStage.WARM_FAREWELL
    interactions: list[dict] = field(default_factory=list)


def classify_segment(stay: Stay) -> GuestSegment:
    """
    Assign a guest to one of Riley's 6 segments based on stay attributes.
    In production this would be an ML model; here we use heuristic rules.
    """
    if stay.booking_channel == BookingChannel.CORPORATE:
        return GuestSegment.BUSINESS_REGULAR
    if stay.nights >= 7:
        return GuestSegment.EXTENDED_STAY
    if "event" in stay.trip_purpose.lower() or "wedding" in stay.trip_purpose.lower():
        return GuestSegment.GROUP_EVENT
    if stay.rate_per_night < 120 and stay.nights <= 2:
        return GuestSegment.BUDGET_SOLO
    if any(a in stay.amenities_used for a in ("kids_club", "pool", "connecting_room")):
        return GuestSegment.FAMILY_VACATIONER
    # Default for leisure short-stays
    return GuestSegment.WEEKEND_LEISURE_COUPLE


def calculate_churn_risk(profile: GuestProfile) -> float:
    """
    Churn risk predictor.  High risk = closer to 1.0.

    Factors (from Dana's APE spec, Section 5.1 Behavioural + Lifecycle layers):
      - days since checkout (recency)
      - engagement score (behavioural signals)
      - loyalty tier (lifecycle)
      - booking channel (OTA guests churn more)
    """
    risk = 0.5

    # Recency decay
    if profile.days_since_checkout > 60:
        risk += 0.15
    elif profile.days_since_checkout > 30:
        risk += 0.08

    # Low engagement increases risk
    if profile.engagement_score < 0.2:
        risk += 0.15
    elif profile.engagement_score < 0.5:
        risk += 0.05

    # OTA guests churn more (Riley, Root Cause #5)
    if profile.stay.booking_channel in (
        BookingChannel.OTA_BOOKING,
        BookingChannel.OTA_EXPEDIA,
        BookingChannel.OTA_OTHER,
    ):
        risk += 0.10

    # Loyalty cushions churn
    if profile.loyalty and profile.loyalty.tier in (LoyaltyTier.VOYAGER, LoyaltyTier.AMBASSADOR):
        risk -= 0.20
    elif profile.loyalty and profile.loyalty.tier == LoyaltyTier.ADVENTURER:
        risk -= 0.10

    return max(0.0, min(1.0, risk))


def determine_journey_stage(days_since_checkout: int) -> JourneyStage:
    """Map days-since-checkout to Dana's 6 journey stages."""
    if days_since_checkout <= 0:
        return JourneyStage.WARM_FAREWELL
    if days_since_checkout <= 7:
        return JourneyStage.NOSTALGIA_TRIGGER
    if days_since_checkout <= 21:
        return JourneyStage.VALUE_REINFORCEMENT
    if days_since_checkout <= 60:
        return JourneyStage.CONTEXTUAL_REENGAGEMENT
    if days_since_checkout <= 75:
        return JourneyStage.CONVERSION_PUSH
    return JourneyStage.ONGOING_RELATIONSHIP


# ===================================================================
# 2. AI PERSONALISATION LOGIC -- Content + Offer Generation
# ===================================================================

@dataclass
class PersonalisedMessage:
    """Output of the Content Generator sub-engine."""
    subject_line: str = ""
    body: str = ""
    channel: ChannelType = ChannelType.EMAIL
    offer: Optional[Offer] = None
    journey_stage: JourneyStage = JourneyStage.WARM_FAREWELL
    send_at: Optional[datetime] = None


# -- Content templates per segment x stage (subset to keep code concise) --

_TEMPLATES: dict[GuestSegment, dict[JourneyStage, dict[str, str]]] = {
    GuestSegment.BUSINESS_REGULAR: {
        JourneyStage.WARM_FAREWELL: {
            "subject": "Thanks for staying with us, {name} -- your stay recap is ready",
            "body": (
                "Hi {name},\n\n"
                "Your {nights}-night stay at {property} is wrapped up. "
                "You earned {points} NovaStar Rewards points.\n"
                "Your Business Profile is saved -- next time, express check-in "
                "and your preferred room await.\n\n"
                "Safe travels,\nNovaStar Hotels"
            ),
        },
        JourneyStage.NOSTALGIA_TRIGGER: {
            "subject": "Your {city} trip highlights",
            "body": (
                "Hi {name},\n\n"
                "Quick recap of your recent {city} stay: {nights} nights, "
                "{room_type} room. We hope the meetings went well.\n"
                "Your preferences are locked in for next time.\n\n"
                "-- NovaStar Hotels"
            ),
        },
        JourneyStage.VALUE_REINFORCEMENT: {
            "subject": "{name}, you're {nights_to_next} nights from Adventurer status",
            "body": (
                "Hi {name},\n\n"
                "You have {points} points and are just {nights_to_next} qualifying nights "
                "from unlocking Adventurer tier -- free room upgrades, guaranteed late checkout, "
                "and 15 pts per dollar.\n\n"
                "Book your next stay direct at NovaStar.com for 2x points.\n\n"
                "-- NovaStar Hotels"
            ),
        },
        JourneyStage.CONVERSION_PUSH: {
            "subject": "Your {city} room is waiting, {name}",
            "body": (
                "Hi {name},\n\n"
                "Heading back to {city}? Your corner room and express check-in "
                "are one tap away. Book direct and earn double points this month.\n\n"
                "{offer_text}\n\n-- NovaStar Hotels"
            ),
        },
    },
    GuestSegment.WEEKEND_LEISURE_COUPLE: {
        JourneyStage.WARM_FAREWELL: {
            "subject": "Your {city} memories are ready, {name}",
            "body": (
                "Hi {name},\n\n"
                "What a {nights}-night getaway! Here is your stay recap from "
                "{property}. Share your favourite moment with friends.\n\n"
                "Already dreaming of your next escape? Check out our sister "
                "properties -- new cities, same NovaStar quality.\n\n"
                "-- NovaStar Hotels"
            ),
        },
        JourneyStage.NOSTALGIA_TRIGGER: {
            "subject": "Missing {city}? We have photos",
            "body": (
                "Hi {name},\n\n"
                "Your {city} highlights: the rooftop view, the local food scene, "
                "and {nights} nights of relaxation. Add your own photos to your "
                "NovaStar travel journal.\n\n"
                "-- NovaStar Hotels"
            ),
        },
        JourneyStage.CONTEXTUAL_REENGAGEMENT: {
            "subject": "{city} in a new season -- 5 experiences you haven't tried",
            "body": (
                "Hi {name},\n\n"
                "{city} has a whole new personality this time of year. "
                "Here are 5 experiences our Local Explorer team hand-picked for you.\n\n"
                "{offer_text}\n\n-- NovaStar Hotels"
            ),
        },
        JourneyStage.CONVERSION_PUSH: {
            "subject": "A new NovaStar city awaits, {name}",
            "body": (
                "Hi {name},\n\n"
                "You loved {city}. How about discovering {alt_city} next? "
                "Same NovaStar comfort, completely new adventure.\n\n"
                "{offer_text}\n\n-- NovaStar Hotels"
            ),
        },
    },
    GuestSegment.FAMILY_VACATIONER: {
        JourneyStage.WARM_FAREWELL: {
            "subject": "The {last_name} family's stay recap is ready!",
            "body": (
                "Hi {name},\n\n"
                "We loved having your family for {nights} nights at {property}! "
                "The kids enjoyed the {amenities}. Your Family Favourites profile "
                "is saved for next time.\n\n"
                "You earned {points} NovaStar Rewards points.\n\n"
                "-- NovaStar Hotels"
            ),
        },
        JourneyStage.NOSTALGIA_TRIGGER: {
            "subject": "The kids are already asking to go back to {city}",
            "body": (
                "Hi {name},\n\n"
                "Remember the {amenities} at {property}? "
                "Your family trip highlights are in the NovaStar app. "
                "Share them or save them for the fridge!\n\n"
                "-- NovaStar Hotels"
            ),
        },
        JourneyStage.VALUE_REINFORCEMENT: {
            "subject": "School holidays sorted -- kids stay free at NovaStar",
            "body": (
                "Hi {name},\n\n"
                "Planning the next family trip? Book direct and get kids-stay-free, "
                "breakfast included, and early pool access.\n\n"
                "{offer_text}\n\n-- NovaStar Hotels"
            ),
        },
        JourneyStage.CONVERSION_PUSH: {
            "subject": "Wait till the kids see NovaStar {alt_city}",
            "body": (
                "Hi {name},\n\n"
                "Your family loved {city}. NovaStar {alt_city} has a "
                "waterpark suite and kids' adventure club starting at $159/night.\n\n"
                "{offer_text}\n\n-- NovaStar Hotels"
            ),
        },
    },
    GuestSegment.BUDGET_SOLO: {
        JourneyStage.WARM_FAREWELL: {
            "subject": "Thanks for staying at NovaStar, {name}",
            "body": (
                "Hi {name},\n\n"
                "Hope you enjoyed your stay at {property}. "
                "Join NovaStar Rewards (free) and get member-only rates next time.\n\n"
                "-- NovaStar Hotels"
            ),
        },
        JourneyStage.CONVERSION_PUSH: {
            "subject": "Flash deal: {city} from $89/night",
            "body": (
                "Hi {name},\n\nGreat room, great price, great location.\n"
                "{offer_text}\n\n-- NovaStar Hotels"
            ),
        },
    },
    GuestSegment.GROUP_EVENT: {
        JourneyStage.WARM_FAREWELL: {
            "subject": "We hope the event in {city} was a hit, {name}",
            "body": (
                "Hi {name},\n\n"
                "We loved hosting your group at {property}. "
                "Your event photos and stay highlights are in the app.\n\n"
                "-- NovaStar Hotels"
            ),
        },
        JourneyStage.NOSTALGIA_TRIGGER: {
            "subject": "Remember {city}? Your personal return offer is inside",
            "body": (
                "Hi {name},\n\n"
                "The event may be over, but {city} has so much more to offer. "
                "Next time, come back on your own terms.\n\n"
                "{offer_text}\n\n-- NovaStar Hotels"
            ),
        },
        JourneyStage.CONVERSION_PUSH: {
            "subject": "Your {city} room is waiting, {name}",
            "body": (
                "Hi {name},\n\n"
                "Return to {city} with a special individual rate -- "
                "no group needed.\n\n"
                "{offer_text}\n\n-- NovaStar Hotels"
            ),
        },
    },
    GuestSegment.EXTENDED_STAY: {
        JourneyStage.WARM_FAREWELL: {
            "subject": "Welcome to NovaStar Residents, {name}",
            "body": (
                "Hi {name},\n\n"
                "After {nights} nights you are practically family. "
                "Your NovaStar Residents profile keeps your preferences "
                "and staff notes for your next assignment.\n\n"
                "You earned {points} NovaStar Rewards points.\n\n"
                "-- NovaStar Hotels"
            ),
        },
        JourneyStage.VALUE_REINFORCEMENT: {
            "subject": "Your next project? NovaStar has you covered",
            "body": (
                "Hi {name},\n\n"
                "Wherever your next assignment takes you, your NovaStar "
                "Residents rate and priority booking are ready.\n\n"
                "Refer a colleague and you both earn 2,000 bonus points.\n\n"
                "-- NovaStar Hotels"
            ),
        },
        JourneyStage.CONVERSION_PUSH: {
            "subject": "Welcome back, resident -- {city} misses you",
            "body": (
                "Hi {name},\n\n"
                "Your extended-stay rate is locked. Book direct for "
                "priority room selection and 2x points.\n\n"
                "{offer_text}\n\n-- NovaStar Hotels"
            ),
        },
    },
}


# Sister-city suggestions for "portfolio explorer" messaging
_SISTER_CITIES: dict[str, str] = {
    "Austin": "Orlando",
    "Orlando": "Austin",
    "Chicago": "Denver",
    "Denver": "Chicago",
    "Barcelona": "Lisbon",
    "Lisbon": "Barcelona",
    "London": "Amsterdam",
    "Amsterdam": "London",
    "Osaka": "Singapore",
    "Singapore": "Osaka",
}


def _pick_channel(guest: Guest, stage: JourneyStage) -> ChannelType:
    """
    Channel selection logic per Dana's table (Section 3.2).
    """
    if guest.has_app:
        # Push primary for app users; email for conversion-heavy stages
        if stage in (JourneyStage.CONVERSION_PUSH, JourneyStage.VALUE_REINFORCEMENT):
            return ChannelType.EMAIL
        return ChannelType.PUSH
    if guest.phone and not guest.email:
        return ChannelType.SMS
    return ChannelType.EMAIL


def _generate_offer(profile: GuestProfile) -> Offer:
    """
    Offer Selector: next-best-action offer calibrated to segment and risk.
    Discount depth is margin-protected (Dana, Section 3.1 Stage 5: avg < 12%).
    """
    seg = profile.guest.segment
    risk = profile.churn_risk

    # Base discount by segment
    base_discount = {
        GuestSegment.BUSINESS_REGULAR: 0.0,
        GuestSegment.WEEKEND_LEISURE_COUPLE: 0.08,
        GuestSegment.FAMILY_VACATIONER: 0.10,
        GuestSegment.BUDGET_SOLO: 0.12,
        GuestSegment.GROUP_EVENT: 0.10,
        GuestSegment.EXTENDED_STAY: 0.05,
    }.get(seg, 0.08)

    # Escalate for high-churn-risk, high-value guests
    if risk > 0.7 and SEGMENT_INTENSITY.get(seg, "LOW") != "LOW":
        base_discount = min(base_discount + 0.05, 0.15)

    # Segment-specific perks (Dana, Section 5.3)
    perks: list[str] = []
    match seg:
        case GuestSegment.BUSINESS_REGULAR:
            perks = ["late checkout guaranteed", "express check-in", "2x points"]
        case GuestSegment.WEEKEND_LEISURE_COUPLE:
            perks = ["couples dining credit", "room upgrade when available"]
        case GuestSegment.FAMILY_VACATIONER:
            perks = ["kids stay free", "breakfast included", "early pool access"]
        case GuestSegment.BUDGET_SOLO:
            perks = ["flash-sale rate"]
        case GuestSegment.GROUP_EVENT:
            perks = ["individual return discount"]
        case GuestSegment.EXTENDED_STAY:
            perks = ["rate lock", "priority room selection"]

    points_bonus = 500 if risk > 0.6 else 0

    alt_city = _SISTER_CITIES.get(profile.stay.property_city, "Miami")
    target = alt_city if profile.journey_stage == JourneyStage.CONVERSION_PUSH else profile.stay.property_city

    headline = f"{'Save ' + str(int(base_discount*100)) + '% + ' if base_discount else ''}{' & '.join(perks[:2])}"

    return Offer(
        guest_id=profile.guest.guest_id,
        headline=headline,
        body=f"Book direct at NovaStar.com for {target}.",
        discount_pct=base_discount,
        points_bonus=points_bonus,
        perks=perks,
        valid_from=date.today(),
        valid_until=date.today() + timedelta(days=30),
        target_property=f"NovaStar {target}",
    )


def generate_message(profile: GuestProfile) -> PersonalisedMessage:
    """
    Top-level content generator.
    Selects the right template, fills dynamic fields, attaches an offer
    when appropriate, and decides channel + timing.
    """
    seg = profile.guest.segment
    stage = profile.journey_stage
    templates = _TEMPLATES.get(seg, {})
    tmpl = templates.get(stage)

    # Fallback: if no template for this exact combo, use WARM_FAREWELL
    if tmpl is None:
        tmpl = templates.get(JourneyStage.WARM_FAREWELL, {
            "subject": "A note from NovaStar Hotels",
            "body": "Hi {name},\n\nThank you for choosing NovaStar.\n\n-- NovaStar Hotels",
        })

    # Build offer for conversion-oriented stages
    offer: Optional[Offer] = None
    offer_text = ""
    if stage in (
        JourneyStage.CONVERSION_PUSH,
        JourneyStage.CONTEXTUAL_REENGAGEMENT,
        JourneyStage.VALUE_REINFORCEMENT,
    ):
        offer = _generate_offer(profile)
        perk_str = ", ".join(offer.perks) if offer.perks else "special perks"
        discount_str = f"{int(offer.discount_pct * 100)}% off + " if offer.discount_pct else ""
        offer_text = (
            f"YOUR OFFER: {discount_str}{perk_str}. "
            f"{'Plus ' + str(offer.points_bonus) + ' bonus points! ' if offer.points_bonus else ''}"
            f"Valid until {offer.valid_until.isoformat()}. Book at NovaStar.com."
        )

    # Resolve variables
    alt_city = _SISTER_CITIES.get(profile.stay.property_city, "Miami")
    nights_to_next = max(0, 5 - (profile.loyalty.nights_qualifying if profile.loyalty else 0))
    pts = profile.loyalty.points_balance if profile.loyalty else 0
    amenities_str = ", ".join(profile.stay.amenities_used) if profile.stay.amenities_used else "our amenities"

    fill = {
        "name": profile.guest.first_name,
        "last_name": profile.guest.last_name,
        "city": profile.stay.property_city,
        "property": profile.stay.property_name,
        "nights": str(profile.stay.nights),
        "room_type": profile.stay.room_type,
        "points": str(pts),
        "nights_to_next": str(nights_to_next),
        "alt_city": alt_city,
        "offer_text": offer_text,
        "amenities": amenities_str,
    }

    subject = tmpl["subject"]
    body = tmpl["body"]
    for k, v in fill.items():
        subject = subject.replace("{" + k + "}", v)
        body = body.replace("{" + k + "}", v)

    channel = _pick_channel(profile.guest, stage)

    # Timing model: simple optimal-window heuristic
    send_hour = 9 if seg == GuestSegment.BUSINESS_REGULAR else 18
    send_at = datetime.now().replace(hour=send_hour, minute=0, second=0, microsecond=0)

    return PersonalisedMessage(
        subject_line=subject,
        body=body,
        channel=channel,
        offer=offer,
        journey_stage=stage,
        send_at=send_at,
    )


# ===================================================================
# 3. TRIGGER SYSTEM -- What / When / Which Channel
# ===================================================================

@dataclass
class Trigger:
    """A scheduled action produced by the Communication Orchestrator."""
    guest_id: str
    action: str               # e.g. "send_email", "send_push"
    journey_stage: JourneyStage
    channel: ChannelType
    day_offset: int           # days post-checkout
    message: Optional[PersonalisedMessage] = None


# Trigger schedule aligned to Dana's 6 stages (Section 3.1)
_TRIGGER_SCHEDULE: list[dict] = [
    {"stage": JourneyStage.WARM_FAREWELL,           "day": 0},
    {"stage": JourneyStage.NOSTALGIA_TRIGGER,       "day": 5},
    {"stage": JourneyStage.VALUE_REINFORCEMENT,      "day": 17},
    {"stage": JourneyStage.CONTEXTUAL_REENGAGEMENT,  "day": 40},
    {"stage": JourneyStage.CONVERSION_PUSH,          "day": 60},
    {"stage": JourneyStage.ONGOING_RELATIONSHIP,     "day": 90},
]


def build_trigger_plan(profile: GuestProfile) -> list[Trigger]:
    """
    Build the full post-stay trigger plan for a guest.
    Budget Solo guests get fewer touches (Dana, Section 5.3: LOW intensity).
    """
    intensity = SEGMENT_INTENSITY.get(profile.guest.segment, "LOW")
    schedule = _TRIGGER_SCHEDULE[:]

    # LOW-intensity segments skip mid-funnel stages
    if intensity == "LOW":
        schedule = [t for t in schedule if t["stage"] in (
            JourneyStage.WARM_FAREWELL,
            JourneyStage.CONVERSION_PUSH,
        )]

    triggers: list[Trigger] = []
    for entry in schedule:
        stage = entry["stage"]
        profile.journey_stage = stage
        profile.days_since_checkout = entry["day"]
        profile.churn_risk = calculate_churn_risk(profile)
        msg = generate_message(profile)
        channel = msg.channel

        triggers.append(Trigger(
            guest_id=profile.guest.guest_id,
            action=f"send_{channel.value}",
            journey_stage=stage,
            channel=channel,
            day_offset=entry["day"],
            message=msg,
        ))

    return triggers


# ===================================================================
# 4. DEMO
# ===================================================================

def _print_divider(label: str) -> None:
    print(f"\n{'=' * 64}")
    print(f"  {label}")
    print("=" * 64)


if __name__ == "__main__":
    from data_models import make_sample_guest, make_sample_stay, make_sample_loyalty

    _print_divider("NovaStar Engagement Engine -- Full Demo")

    # --- Create a sample Family Vacationer guest ---
    guest = make_sample_guest(GuestSegment.FAMILY_VACATIONER)
    stay = make_sample_stay(guest, property_city="Austin")
    prefs = GuestPreferences(
        guest_id=guest.guest_id,
        bed_type="king",
        breakfast_included=True,
        children_ages=[6, 9],
        interests=["pool", "local attractions"],
    )
    loyalty = make_sample_loyalty(guest)

    print(f"\nGuest   : {guest.full_name} ({guest.segment.value})")
    print(f"Stay    : {stay.property_name}, {stay.nights} nights, ${stay.total_spend:.0f}")
    print(f"Loyalty : {loyalty.tier.value}, {loyalty.points_balance} pts")

    # --- Classify segment from stay data ---
    inferred = classify_segment(stay)
    print(f"Inferred segment: {inferred.value}")

    # --- Build full trigger plan ---
    profile = GuestProfile(
        guest=guest,
        stay=stay,
        preferences=prefs,
        loyalty=loyalty,
    )

    triggers = build_trigger_plan(profile)
    _print_divider(f"Trigger Plan for {guest.full_name} ({len(triggers)} touches)")

    for i, t in enumerate(triggers, 1):
        msg = t.message
        print(f"\n--- Touch {i}: Day {t.day_offset} | {t.journey_stage.value} | {t.channel.value} ---")
        print(f"  Subject : {msg.subject_line if msg else 'N/A'}")
        if msg and msg.offer:
            print(f"  Offer   : {msg.offer.headline}")
            print(f"  Discount: {msg.offer.discount_pct*100:.0f}%  |  Bonus pts: {msg.offer.points_bonus}")
            print(f"  Perks   : {', '.join(msg.offer.perks)}")
        print(f"  Churn risk at this stage: {profile.churn_risk:.2f}")

    # --- Show message body for the nostalgia trigger ---
    nostalgia = [t for t in triggers if t.journey_stage == JourneyStage.NOSTALGIA_TRIGGER]
    if nostalgia:
        _print_divider("Sample Email Body -- Nostalgia Trigger (Day 5)")
        print(nostalgia[0].message.body if nostalgia[0].message else "(no body)")

    # --- Quick run for every segment ---
    _print_divider("Trigger Plans Across All 6 Segments")
    for seg in GuestSegment:
        g = make_sample_guest(seg)
        s = make_sample_stay(g, "Barcelona")
        la = make_sample_loyalty(g)
        p = GuestProfile(guest=g, stay=s, preferences=GuestPreferences(guest_id=g.guest_id), loyalty=la)
        plan = build_trigger_plan(p)
        touch_stages = [t.journey_stage.value for t in plan]
        print(f"  {seg.value:32s} -> {len(plan)} touches: {touch_stages}")

    print("\nEngine demo complete. All segments processed successfully.")
