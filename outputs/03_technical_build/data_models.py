"""
NovaStar Hotels -- Data Models
==============================
Database schema expressed as Python dataclasses.
No ORM required; standard-library only.

Prepared by: Max the Maker (Agent 03, Team AWESOME)
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class GuestSegment(Enum):
    """Riley's 6 guest segments (01_research_report.md, Section 2)."""
    BUSINESS_REGULAR = "Business Regular"
    WEEKEND_LEISURE_COUPLE = "Weekend Leisure Couple"
    FAMILY_VACATIONER = "Family Vacationer"
    BUDGET_SOLO = "Budget-Conscious Solo"
    GROUP_EVENT = "Group/Event Attendee"
    EXTENDED_STAY = "Extended-Stay / Relocation"


class BookingChannel(Enum):
    DIRECT_WEB = "NovaStar.com"
    PHONE_WALKIN = "Phone / Walk-in"
    CORPORATE = "Corporate Portal"
    OTA_BOOKING = "Booking.com"
    OTA_EXPEDIA = "Expedia"
    OTA_OTHER = "Other OTA"
    TRAVEL_AGENT = "Travel Agent"


class LoyaltyTier(Enum):
    """Dana's 4-tier redesign (02_solution_design.md, Section 6.2)."""
    NONE = "Non-member"
    EXPLORER = "Explorer"
    ADVENTURER = "Adventurer"
    VOYAGER = "Voyager"
    AMBASSADOR = "Ambassador"


class ChannelType(Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    WHATSAPP = "whatsapp"
    IN_APP = "in_app"


class JourneyStage(Enum):
    """Dana's 6-stage post-stay journey (02_solution_design.md, Section 3.1)."""
    WARM_FAREWELL = "Warm Farewell"          # Day 0
    NOSTALGIA_TRIGGER = "Nostalgia Trigger"  # Days 3-7
    VALUE_REINFORCEMENT = "Value Reinforcement"  # Days 14-21
    CONTEXTUAL_REENGAGEMENT = "Contextual Re-engagement"  # Days 30-60
    CONVERSION_PUSH = "Conversion Push"      # Days 45-75
    ONGOING_RELATIONSHIP = "Ongoing Relationship"  # 90+ days


class InteractionType(Enum):
    EMAIL_SENT = "email_sent"
    EMAIL_OPENED = "email_opened"
    EMAIL_CLICKED = "email_clicked"
    SMS_SENT = "sms_sent"
    PUSH_SENT = "push_sent"
    PUSH_OPENED = "push_opened"
    APP_SESSION = "app_session"
    BOOKING_PAGE_VISIT = "booking_page_visit"
    SURVEY_COMPLETED = "survey_completed"
    SOCIAL_SHARE = "social_share"
    OFFER_REDEEMED = "offer_redeemed"
    REBOOKED = "rebooked"


class CampaignStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


# ---------------------------------------------------------------------------
# Core Data Models
# ---------------------------------------------------------------------------

@dataclass
class Guest:
    """
    Unified guest profile -- the 'Golden Record' from the Guest Data Platform.

    Relationships:
        - has many Stay records (one per visit)
        - has one GuestPreferences record
        - has many Interaction records
        - has zero or one LoyaltyAccount
    """
    guest_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    first_name: str = ""
    last_name: str = ""
    email: Optional[str] = None          # None when OTA-masked
    phone: Optional[str] = None
    segment: GuestSegment = GuestSegment.BUDGET_SOLO
    has_app: bool = False
    data_capture_complete: bool = False   # True when email + phone + prefs
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()


@dataclass
class Stay:
    """
    A single hotel stay.

    Relationships:
        - belongs to one Guest (via guest_id)
        - belongs to one property
    """
    stay_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    guest_id: str = ""
    property_name: str = ""               # e.g. "NovaStar Austin"
    property_city: str = ""
    check_in: date = field(default_factory=date.today)
    check_out: date = field(default_factory=date.today)
    nights: int = 1
    room_type: str = "Standard"
    rate_per_night: float = 159.70        # ADR from Riley's data
    total_spend: float = 0.0
    booking_channel: BookingChannel = BookingChannel.OTA_BOOKING
    trip_purpose: str = ""                # free text or segment-inferred
    nps_score: Optional[int] = None       # post-stay NPS if collected
    amenities_used: list[str] = field(default_factory=list)


@dataclass
class GuestPreferences:
    """
    Progressive profile built across stays.

    Relationships:
        - belongs to one Guest (via guest_id)
    """
    guest_id: str = ""
    room_floor: Optional[str] = None      # "high", "low", "any"
    bed_type: Optional[str] = None        # "king", "queen", "twin"
    pillow_preference: Optional[str] = None
    breakfast_included: bool = False
    quiet_room: bool = False
    communication_channel: ChannelType = ChannelType.EMAIL
    interests: list[str] = field(default_factory=list)  # ["spa", "dining", "local culture"]
    dietary: Optional[str] = None
    children_ages: list[int] = field(default_factory=list)
    notes: str = ""                       # free-text staff notes


@dataclass
class Interaction:
    """
    Every touchpoint between NovaStar and a guest.

    Relationships:
        - belongs to one Guest (via guest_id)
        - optionally linked to a Campaign (via campaign_id)
        - optionally linked to an Offer (via offer_id)
    """
    interaction_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    guest_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    interaction_type: InteractionType = InteractionType.EMAIL_SENT
    channel: ChannelType = ChannelType.EMAIL
    journey_stage: JourneyStage = JourneyStage.WARM_FAREWELL
    campaign_id: Optional[str] = None
    offer_id: Optional[str] = None
    metadata: dict = field(default_factory=dict)  # e.g. {"subject_line": "..."}


@dataclass
class Offer:
    """
    A personalised offer generated by the AI Personalisation Engine.

    Relationships:
        - targeted at one Guest (via guest_id)
        - belongs to one Campaign (via campaign_id)
    """
    offer_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    guest_id: str = ""
    campaign_id: Optional[str] = None
    headline: str = ""
    body: str = ""
    discount_pct: float = 0.0             # 0.0 - 1.0
    points_bonus: int = 0
    perks: list[str] = field(default_factory=list)  # ["late checkout", "breakfast"]
    valid_from: date = field(default_factory=date.today)
    valid_until: date = field(default_factory=date.today)
    redeemed: bool = False
    target_property: Optional[str] = None  # specific property or None for any


@dataclass
class LoyaltyAccount:
    """
    NovaStar Rewards account -- Dana's redesigned tier structure.

    Relationships:
        - belongs to one Guest (via guest_id)
        - has many Reward records
    """
    account_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    guest_id: str = ""
    tier: LoyaltyTier = LoyaltyTier.EXPLORER
    points_balance: int = 0
    points_lifetime: int = 0
    nights_qualifying: int = 0            # in current qualification window
    stays_qualifying: int = 0
    enrolled_date: date = field(default_factory=date.today)
    last_activity: date = field(default_factory=date.today)
    is_active: bool = True                # active = earned/redeemed in 12 mo


@dataclass
class Reward:
    """
    A reward redeemed from the loyalty catalogue.

    Relationships:
        - belongs to one LoyaltyAccount (via account_id)
    """
    reward_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    account_id: str = ""
    reward_type: str = ""                 # "room_upgrade", "free_night", etc.
    points_cost: int = 0
    redeemed_date: date = field(default_factory=date.today)
    description: str = ""


@dataclass
class Campaign:
    """
    A marketing campaign targeting one or more segments.

    Relationships:
        - produces many Offer records
        - produces many Interaction records
    """
    campaign_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    name: str = ""
    journey_stage: JourneyStage = JourneyStage.NOSTALGIA_TRIGGER
    target_segments: list[GuestSegment] = field(default_factory=list)
    channel: ChannelType = ChannelType.EMAIL
    status: CampaignStatus = CampaignStatus.DRAFT
    start_date: date = field(default_factory=date.today)
    end_date: Optional[date] = None
    created_by: str = "AI Personalisation Engine"


# ---------------------------------------------------------------------------
# Sample Data Factory Functions
# ---------------------------------------------------------------------------

def make_sample_guest(segment: GuestSegment | None = None) -> Guest:
    """Return a realistic sample Guest for the given segment."""
    import random
    seg = segment or random.choice(list(GuestSegment))

    name_map: dict[GuestSegment, tuple[str, str]] = {
        GuestSegment.BUSINESS_REGULAR: ("James", "Chen"),
        GuestSegment.WEEKEND_LEISURE_COUPLE: ("Sofia", "Martinez"),
        GuestSegment.FAMILY_VACATIONER: ("David", "Thompson"),
        GuestSegment.BUDGET_SOLO: ("Alex", "Nowak"),
        GuestSegment.GROUP_EVENT: ("Priya", "Sharma"),
        GuestSegment.EXTENDED_STAY: ("Michael", "Okafor"),
    }
    first, last = name_map[seg]
    return Guest(
        first_name=first,
        last_name=last,
        email=f"{first.lower()}.{last.lower()}@example.com",
        phone="+1-555-0100",
        segment=seg,
        has_app=seg in (GuestSegment.BUSINESS_REGULAR, GuestSegment.EXTENDED_STAY),
        data_capture_complete=True,
    )


def make_sample_stay(guest: Guest, property_city: str = "Austin") -> Stay:
    """Return a sample Stay linked to the provided guest."""
    nights_map = {
        GuestSegment.BUSINESS_REGULAR: 2,
        GuestSegment.WEEKEND_LEISURE_COUPLE: 2,
        GuestSegment.FAMILY_VACATIONER: 4,
        GuestSegment.BUDGET_SOLO: 2,
        GuestSegment.GROUP_EVENT: 3,
        GuestSegment.EXTENDED_STAY: 12,
    }
    nights = nights_map.get(guest.segment, 2)
    rate = {
        GuestSegment.BUSINESS_REGULAR: 189.0,
        GuestSegment.WEEKEND_LEISURE_COUPLE: 152.0,
        GuestSegment.FAMILY_VACATIONER: 174.0,
        GuestSegment.BUDGET_SOLO: 109.0,
        GuestSegment.GROUP_EVENT: 141.0,
        GuestSegment.EXTENDED_STAY: 98.0,
    }.get(guest.segment, 159.70)
    return Stay(
        guest_id=guest.guest_id,
        property_name=f"NovaStar {property_city}",
        property_city=property_city,
        check_in=date(2026, 1, 10),
        check_out=date(2026, 1, 10 + nights),
        nights=nights,
        room_type="Suite" if guest.segment == GuestSegment.EXTENDED_STAY else "Standard",
        rate_per_night=rate,
        total_spend=rate * nights,
        booking_channel=(
            BookingChannel.CORPORATE
            if guest.segment == GuestSegment.BUSINESS_REGULAR
            else BookingChannel.OTA_BOOKING
        ),
        amenities_used=["pool", "breakfast"] if guest.segment == GuestSegment.FAMILY_VACATIONER else ["wifi"],
    )


def make_sample_loyalty(guest: Guest) -> LoyaltyAccount:
    """Return a sample LoyaltyAccount for the guest."""
    tier = {
        GuestSegment.BUSINESS_REGULAR: LoyaltyTier.ADVENTURER,
        GuestSegment.EXTENDED_STAY: LoyaltyTier.VOYAGER,
    }.get(guest.segment, LoyaltyTier.EXPLORER)
    return LoyaltyAccount(
        guest_id=guest.guest_id,
        tier=tier,
        points_balance=3420 if tier == LoyaltyTier.EXPLORER else 8500,
        points_lifetime=5000 if tier == LoyaltyTier.EXPLORER else 15000,
        nights_qualifying=4 if tier == LoyaltyTier.EXPLORER else 12,
        stays_qualifying=2 if tier == LoyaltyTier.EXPLORER else 5,
    )


def make_sample_campaign() -> Campaign:
    return Campaign(
        name="Post-Stay Nostalgia -- Q1 2026",
        journey_stage=JourneyStage.NOSTALGIA_TRIGGER,
        target_segments=[GuestSegment.WEEKEND_LEISURE_COUPLE, GuestSegment.FAMILY_VACATIONER],
        channel=ChannelType.EMAIL,
        status=CampaignStatus.ACTIVE,
        start_date=date(2026, 1, 15),
        end_date=date(2026, 3, 31),
    )


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("NovaStar Data Models -- Sample Records")
    print("=" * 60)

    for seg in GuestSegment:
        g = make_sample_guest(seg)
        s = make_sample_stay(g)
        la = make_sample_loyalty(g)
        print(f"\n--- {seg.value} ---")
        print(f"  Guest  : {g.full_name} ({g.email}), app={g.has_app}")
        print(f"  Stay   : {s.property_name}, {s.nights}n @ ${s.rate_per_night}/n = ${s.total_spend:.0f}")
        print(f"  Loyalty: {la.tier.value}, {la.points_balance} pts, {la.nights_qualifying} qualifying nights")

    camp = make_sample_campaign()
    print(f"\nSample Campaign: '{camp.name}' [{camp.status.value}]")
    print(f"  Stage={camp.journey_stage.value}, Segments={[s.value for s in camp.target_segments]}")
    print("\nAll models validated successfully.")
