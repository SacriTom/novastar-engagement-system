"""
NovaStar Hotels -- Guest Journey Simulation
=============================================
Simulates 100 guests over 90 days post-stay.
Models Dana's 6-stage journey, tracks engagement metrics,
and compares "before" (current 12.1% rebooking) vs "after"
(with the AI engagement system).

Uses random module with fixed seed for reproducibility.
Standard-library only; Python 3.10+.

Prepared by: Max the Maker (Agent 03, Team AWESOME)
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum

# ---------------------------------------------------------------------------
# Configuration & Constants
# ---------------------------------------------------------------------------

SEED = 42
NUM_GUESTS = 100
SIM_DAYS = 90

# Riley's 6 segments with their proportions (Section 2.1)
SEGMENT_DIST: list[tuple[str, float]] = [
    ("Business Regular",         0.22),
    ("Weekend Leisure Couple",   0.24),
    ("Family Vacationer",        0.18),
    ("Budget-Conscious Solo",    0.15),
    ("Group/Event Attendee",     0.12),
    ("Extended-Stay/Relocation", 0.09),
]

# Current (before) rebooking rates -- Riley Section 2.1
BEFORE_REBOOK: dict[str, float] = {
    "Business Regular":         0.194,
    "Weekend Leisure Couple":   0.107,
    "Family Vacationer":        0.083,
    "Budget-Conscious Solo":    0.061,
    "Group/Event Attendee":     0.142,
    "Extended-Stay/Relocation": 0.218,
}

# Target (after) 12-month rebooking rates -- Dana Section 7.2
AFTER_REBOOK: dict[str, float] = {
    "Business Regular":         0.30,
    "Weekend Leisure Couple":   0.18,
    "Family Vacationer":        0.16,
    "Budget-Conscious Solo":    0.08,
    "Group/Event Attendee":     0.22,
    "Extended-Stay/Relocation": 0.30,
}

# Email engagement probabilities -- BEFORE (Riley Section 6.4)
BEFORE_EMAIL_OPEN = 0.184
BEFORE_EMAIL_CLICK = 0.021  # per email (unconditional)

# After: improved by AI personalisation (Dana Section 7.1 targets)
AFTER_EMAIL_OPEN = 0.38
AFTER_EMAIL_CLICK = 0.08

# Dana's 6 journey stages (Section 3.1)
class Stage(Enum):
    WARM_FAREWELL = 0            # Day 0
    NOSTALGIA_TRIGGER = 5        # Days 3-7 (midpoint 5)
    VALUE_REINFORCEMENT = 17     # Days 14-21
    CONTEXTUAL_REENGAGEMENT = 40 # Days 30-60
    CONVERSION_PUSH = 60         # Days 45-75
    ONGOING_RELATIONSHIP = 90    # 90+


# How many emails each approach sends per stage
BEFORE_EMAILS_PER_STAGE = {
    Stage.WARM_FAREWELL: 1,       # generic survey
    Stage.NOSTALGIA_TRIGGER: 0,
    Stage.VALUE_REINFORCEMENT: 1, # "book again" promo
    Stage.CONTEXTUAL_REENGAGEMENT: 1,  # re-engagement
    Stage.CONVERSION_PUSH: 0,
    Stage.ONGOING_RELATIONSHIP: 0,
}  # Total: 3 emails -- matches Riley's current state

AFTER_EMAILS_PER_STAGE = {
    Stage.WARM_FAREWELL: 1,
    Stage.NOSTALGIA_TRIGGER: 1,
    Stage.VALUE_REINFORCEMENT: 1,
    Stage.CONTEXTUAL_REENGAGEMENT: 1,
    Stage.CONVERSION_PUSH: 1,
    Stage.ONGOING_RELATIONSHIP: 1,
}  # Total: 6 personalised emails


# Engagement intensity multiplier by segment (Dana Section 5.3)
INTENSITY: dict[str, float] = {
    "Business Regular":         1.2,
    "Weekend Leisure Couple":   1.0,
    "Family Vacationer":        1.2,
    "Budget-Conscious Solo":    0.6,
    "Group/Event Attendee":     1.0,
    "Extended-Stay/Relocation": 1.2,
}


# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass
class GuestSim:
    """A guest being simulated over the 90-day post-stay window."""
    guest_id: int
    segment: str
    has_email: bool = True
    has_app: bool = False
    # Tracking counters
    emails_sent: int = 0
    emails_opened: int = 0
    emails_clicked: int = 0
    push_sent: int = 0
    push_opened: int = 0
    app_sessions: int = 0
    rebooked: bool = False
    rebook_day: int = -1
    stages_reached: list[str] = field(default_factory=list)


@dataclass
class SimResult:
    """Aggregate results for one scenario (before or after)."""
    label: str
    total_guests: int = 0
    guests_with_email: int = 0
    total_emails_sent: int = 0
    total_emails_opened: int = 0
    total_emails_clicked: int = 0
    total_push_sent: int = 0
    total_push_opened: int = 0
    total_app_sessions: int = 0
    total_rebooked: int = 0
    rebook_by_segment: dict[str, tuple[int, int]] = field(default_factory=dict)
    # (segment -> (rebooked_count, total_count))


# ---------------------------------------------------------------------------
# Simulation Engine
# ---------------------------------------------------------------------------

def _assign_segments(rng: random.Random, n: int) -> list[str]:
    """Assign segments to n guests following Riley's distribution."""
    segments: list[str] = []
    for seg_name, pct in SEGMENT_DIST:
        count = round(pct * n)
        segments.extend([seg_name] * count)
    # Fix rounding so we hit exactly n
    while len(segments) < n:
        segments.append(SEGMENT_DIST[0][0])
    while len(segments) > n:
        segments.pop()
    rng.shuffle(segments)
    return segments


def simulate(
    label: str,
    rng: random.Random,
    email_open_rate: float,
    email_click_rate: float,
    rebook_rates: dict[str, float],
    emails_per_stage: dict[Stage, int],
    use_push: bool = False,
    use_app: bool = False,
) -> SimResult:
    """Run the 90-day simulation for one scenario."""

    segments = _assign_segments(rng, NUM_GUESTS)
    guests: list[GuestSim] = []

    for i, seg in enumerate(segments):
        # Data capture rate: 43% currently (Riley), 75% with engagement system
        capture_rate = 0.75 if label == "AFTER" else 0.43
        has_email = rng.random() < capture_rate

        has_app_flag = False
        if use_app and has_email:
            # App install among loyalty members ~35% target (Dana, Section 7.4)
            has_app_flag = rng.random() < 0.30

        guests.append(GuestSim(
            guest_id=i,
            segment=seg,
            has_email=has_email,
            has_app=has_app_flag,
        ))

    # Walk each guest through the 90-day journey
    for guest in guests:
        if not guest.has_email and not guest.has_app:
            # Guest is unreachable -- mirrors the 57% data-void problem
            continue

        intensity = INTENSITY.get(guest.segment, 1.0)
        cumulative_engagement = 0.0

        for stage in Stage:
            day = stage.value
            if day > SIM_DAYS:
                break

            guest.stages_reached.append(stage.name)

            # --- Emails ---
            n_emails = emails_per_stage.get(stage, 0)
            for _ in range(n_emails):
                if guest.has_email:
                    guest.emails_sent += 1
                    if rng.random() < email_open_rate * intensity:
                        guest.emails_opened += 1
                        cumulative_engagement += 0.15
                        if rng.random() < (email_click_rate / email_open_rate):
                            guest.emails_clicked += 1
                            cumulative_engagement += 0.25

            # --- Push notifications (after system only) ---
            if use_push and guest.has_app and stage not in (
                Stage.WARM_FAREWELL,
                Stage.ONGOING_RELATIONSHIP,
            ):
                guest.push_sent += 1
                if rng.random() < 0.35 * intensity:  # push open ~35%
                    guest.push_opened += 1
                    cumulative_engagement += 0.10

            # --- App sessions (organic, after system only) ---
            if use_app and guest.has_app:
                if rng.random() < 0.20 * intensity:
                    guest.app_sessions += 1
                    cumulative_engagement += 0.10

        # --- Rebooking decision ---
        base_rate = rebook_rates.get(guest.segment, 0.12)

        # Engagement lift: each unit of cumulative engagement nudges rebooking
        engagement_boost = min(cumulative_engagement * 0.08, 0.10)
        final_prob = min(base_rate + engagement_boost, 0.60)

        if rng.random() < final_prob:
            guest.rebooked = True
            # Estimate rebook day (weighted toward later stages)
            guest.rebook_day = rng.randint(30, SIM_DAYS)

    # --- Aggregate ---
    result = SimResult(label=label, total_guests=NUM_GUESTS)
    seg_counts: dict[str, list[int]] = {s: [0, 0] for s, _ in SEGMENT_DIST}

    for g in guests:
        if g.has_email:
            result.guests_with_email += 1
        result.total_emails_sent += g.emails_sent
        result.total_emails_opened += g.emails_opened
        result.total_emails_clicked += g.emails_clicked
        result.total_push_sent += g.push_sent
        result.total_push_opened += g.push_opened
        result.total_app_sessions += g.app_sessions
        if g.rebooked:
            result.total_rebooked += 1
        seg_counts[g.segment][1] += 1
        if g.rebooked:
            seg_counts[g.segment][0] += 1

    result.rebook_by_segment = {s: (v[0], v[1]) for s, v in seg_counts.items()}
    return result


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_report(before: SimResult, after: SimResult) -> None:
    """Pretty-print comparative results."""

    def pct(n: int, d: int) -> str:
        return f"{n/d*100:.1f}%" if d > 0 else "N/A"

    w = 72
    print("=" * w)
    print("  NovaStar Hotels -- 90-Day Post-Stay Journey Simulation")
    print(f"  {NUM_GUESTS} guests, {SIM_DAYS} days, seed={SEED}")
    print("=" * w)

    print(f"\n{'Metric':<40} {'BEFORE':>12} {'AFTER':>12}  {'Delta':>8}")
    print("-" * w)

    rows = [
        ("Guests reachable (have email/app)",
         f"{before.guests_with_email}",
         f"{after.guests_with_email}",
         f"+{after.guests_with_email - before.guests_with_email}"),

        ("Emails sent",
         str(before.total_emails_sent),
         str(after.total_emails_sent),
         f"+{after.total_emails_sent - before.total_emails_sent}"),

        ("Emails opened",
         f"{before.total_emails_opened} ({pct(before.total_emails_opened, before.total_emails_sent)})",
         f"{after.total_emails_opened} ({pct(after.total_emails_opened, after.total_emails_sent)})",
         f"+{after.total_emails_opened - before.total_emails_opened}"),

        ("Emails clicked",
         f"{before.total_emails_clicked} ({pct(before.total_emails_clicked, before.total_emails_sent)})",
         f"{after.total_emails_clicked} ({pct(after.total_emails_clicked, after.total_emails_sent)})",
         f"+{after.total_emails_clicked - before.total_emails_clicked}"),

        ("Push notifications sent",
         str(before.total_push_sent),
         str(after.total_push_sent),
         f"+{after.total_push_sent - before.total_push_sent}"),

        ("Push opened",
         str(before.total_push_opened),
         str(after.total_push_opened),
         f"+{after.total_push_opened - before.total_push_opened}"),

        ("App sessions (organic)",
         str(before.total_app_sessions),
         str(after.total_app_sessions),
         f"+{after.total_app_sessions - before.total_app_sessions}"),

        ("REBOOKED (total)",
         f"{before.total_rebooked} ({pct(before.total_rebooked, NUM_GUESTS)})",
         f"{after.total_rebooked} ({pct(after.total_rebooked, NUM_GUESTS)})",
         f"+{after.total_rebooked - before.total_rebooked}"),
    ]

    for label, b, a, d in rows:
        print(f"  {label:<38} {b:>12} {a:>12}  {d:>8}")

    # Segment breakdown
    print(f"\n{'Rebooking by Segment':<40} {'BEFORE':>12} {'AFTER':>12}  {'Delta':>8}")
    print("-" * w)
    for seg, _ in SEGMENT_DIST:
        b_rebook, b_total = before.rebook_by_segment.get(seg, (0, 0))
        a_rebook, a_total = after.rebook_by_segment.get(seg, (0, 0))
        b_str = f"{b_rebook}/{b_total} ({pct(b_rebook, b_total)})"
        a_str = f"{a_rebook}/{a_total} ({pct(a_rebook, a_total)})"
        delta = a_rebook - b_rebook
        print(f"  {seg:<38} {b_str:>12} {a_str:>12}  {'+' if delta >= 0 else ''}{delta:>7}")

    # Financial projections (scaled to 80,000 guests)
    scale = 80_000 / NUM_GUESTS
    b_repeat_80k = int(before.total_rebooked * scale)
    a_repeat_80k = int(after.total_rebooked * scale)
    incremental = a_repeat_80k - b_repeat_80k
    avg_stay_nights = 3.71
    adr = 159.70
    incremental_revenue = incremental * avg_stay_nights * adr

    print(f"\n{'Financial Projection (scaled to 80k guests)':<40}")
    print("-" * w)
    print(f"  {'Repeat guests (before, scaled)':<38} {b_repeat_80k:>12,}")
    print(f"  {'Repeat guests (after, scaled)':<38} {a_repeat_80k:>12,}")
    print(f"  {'Incremental repeat guests':<38} {'+':>1}{incremental:>11,}")
    print(f"  {'Incremental room nights':<38} {'+':>1}{int(incremental * avg_stay_nights):>11,}")
    print(f"  {'Incremental revenue (est.)':<38} {'$':>1}{incremental_revenue:>11,.0f}")
    print(f"  {'OTA savings (10pp shift to direct)':<38} {'$':>1}{560_000:>11,}")
    print()
    print("=" * w)
    print("  Simulation complete.")
    print("=" * w)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    rng_before = random.Random(SEED)
    before = simulate(
        label="BEFORE",
        rng=rng_before,
        email_open_rate=BEFORE_EMAIL_OPEN,
        email_click_rate=BEFORE_EMAIL_CLICK,
        rebook_rates=BEFORE_REBOOK,
        emails_per_stage=BEFORE_EMAILS_PER_STAGE,
        use_push=False,
        use_app=False,
    )

    rng_after = random.Random(SEED)
    after = simulate(
        label="AFTER",
        rng=rng_after,
        email_open_rate=AFTER_EMAIL_OPEN,
        email_click_rate=AFTER_EMAIL_CLICK,
        rebook_rates=AFTER_REBOOK,
        emails_per_stage=AFTER_EMAILS_PER_STAGE,
        use_push=True,
        use_app=True,
    )

    print_report(before, after)
