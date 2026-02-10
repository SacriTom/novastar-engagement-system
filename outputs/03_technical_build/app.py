"""
NovaStar Hotels -- AI Post-Stay Engagement System Dashboard
============================================================
Flask web application for Team AWESOME's Week 4 Group Exercise.

Run from the 03_technical_build directory:
    python app.py

Then visit http://127.0.0.1:5000 in your browser.

Prepared by: Team AWESOME
"""

from __future__ import annotations

import os
import sys
import random
import traceback
from datetime import date

# ---------------------------------------------------------------------------
# Ensure sibling modules are importable regardless of how the app is launched
# ---------------------------------------------------------------------------
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

from flask import Flask, render_template_string, request, jsonify

# --- Project modules ---
from data_models import (
    Guest, Stay, GuestPreferences, LoyaltyAccount, LoyaltyTier,
    GuestSegment, BookingChannel, ChannelType,
    make_sample_guest, make_sample_stay, make_sample_loyalty,
)
from engagement_engine import (
    GuestProfile, build_trigger_plan, SEGMENT_INTENSITY, SEGMENT_BASE_REBOOK,
)
import guest_journey_simulation as sim

# ---------------------------------------------------------------------------
# Flask application
# ---------------------------------------------------------------------------
app = Flask(__name__)

# ===================================================================
# SHARED CSS & LAYOUT
# ===================================================================
BASE_CSS = """
:root {
    --primary: #1a365d;
    --primary-light: #2a4a7f;
    --accent: #0d9488;
    --accent-light: #14b8a6;
    --bg: #f1f5f9;
    --card-bg: #ffffff;
    --text: #1e293b;
    --text-light: #64748b;
    --border: #e2e8f0;
    --success: #16a34a;
    --warning: #d97706;
    --danger: #dc2626;
    --shadow: 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06);
    --shadow-md: 0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.06);
    --shadow-lg: 0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05);
    --radius: 8px;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    min-height: 100vh;
}
.topbar {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    color: #fff;
    padding: 0;
    box-shadow: var(--shadow-md);
    position: sticky;
    top: 0;
    z-index: 100;
}
.topbar-inner {
    max-width: 1280px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
    height: 64px;
}
.topbar .brand {
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
    color: #fff;
}
.brand-star {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    background: var(--accent);
    border-radius: 6px;
    font-weight: 900;
    font-size: 1.1rem;
}
.topbar nav {
    display: flex;
    gap: 4px;
}
.topbar nav a {
    color: rgba(255,255,255,0.8);
    text-decoration: none;
    padding: 8px 16px;
    border-radius: 6px;
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.2s;
}
.topbar nav a:hover, .topbar nav a.active {
    color: #fff;
    background: rgba(255,255,255,0.15);
}
.container {
    max-width: 1280px;
    margin: 0 auto;
    padding: 32px 24px;
}
h1 { font-size: 1.75rem; font-weight: 700; color: var(--primary); margin-bottom: 8px; }
h2 { font-size: 1.35rem; font-weight: 700; color: var(--primary); margin-bottom: 12px; }
h3 { font-size: 1.1rem; font-weight: 600; color: var(--primary); margin-bottom: 8px; }
.subtitle { color: var(--text-light); font-size: 0.95rem; margin-bottom: 24px; }

.card {
    background: var(--card-bg);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 24px;
    margin-bottom: 20px;
    border: 1px solid var(--border);
}
.card-header {
    font-weight: 700;
    font-size: 1.05rem;
    color: var(--primary);
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 2px solid var(--bg);
}

/* Stat cards grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    margin-bottom: 28px;
}
.stat-card {
    background: var(--card-bg);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 20px 24px;
    border: 1px solid var(--border);
    border-top: 3px solid var(--accent);
}
.stat-card .stat-label {
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-light);
    margin-bottom: 4px;
}
.stat-card .stat-value {
    font-size: 1.9rem;
    font-weight: 800;
    color: var(--primary);
    line-height: 1.2;
}
.stat-card .stat-sub {
    font-size: 0.8rem;
    color: var(--text-light);
    margin-top: 4px;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
}
th {
    background: var(--primary);
    color: #fff;
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}
th:first-child { border-radius: 6px 0 0 0; }
th:last-child { border-radius: 0 6px 0 0; }
td {
    padding: 10px 14px;
    border-bottom: 1px solid var(--border);
}
tr:hover td { background: #f8fafc; }

/* Buttons */
.btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 10px 22px;
    border: none;
    border-radius: 6px;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    text-decoration: none;
}
.btn-primary {
    background: var(--accent);
    color: #fff;
}
.btn-primary:hover {
    background: var(--accent-light);
    box-shadow: var(--shadow-md);
}
.btn-secondary {
    background: var(--primary);
    color: #fff;
}
.btn-secondary:hover {
    background: var(--primary-light);
}

/* Forms */
.form-group {
    margin-bottom: 16px;
}
.form-group label {
    display: block;
    font-weight: 600;
    font-size: 0.85rem;
    color: var(--text);
    margin-bottom: 4px;
}
.form-group select, .form-group input[type="number"], .form-group input[type="text"] {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid var(--border);
    border-radius: 6px;
    font-size: 0.9rem;
    color: var(--text);
    background: #fff;
}
.form-group input[type="range"] {
    width: 100%;
    accent-color: var(--accent);
}
.range-value {
    display: inline-block;
    background: var(--accent);
    color: #fff;
    font-weight: 700;
    font-size: 0.8rem;
    padding: 2px 10px;
    border-radius: 12px;
    margin-left: 8px;
}

.form-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
}

/* Badges */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}
.badge-high { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
.badge-medium-high { background: #fff7ed; color: #d97706; border: 1px solid #fed7aa; }
.badge-medium { background: #fefce8; color: #a16207; border: 1px solid #fde68a; }
.badge-low { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }

/* Message display */
.msg-block {
    background: #f8fafc;
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: 0 6px 6px 0;
    padding: 16px 20px;
    margin: 12px 0;
    font-size: 0.9rem;
    white-space: pre-wrap;
    font-family: 'Segoe UI', sans-serif;
    line-height: 1.7;
}
.offer-block {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    border-left: 4px solid var(--success);
    border-radius: 0 6px 6px 0;
    padding: 16px 20px;
    margin: 12px 0;
}
.offer-block strong { color: #065f46; }

/* Comparison table highlight */
.delta-positive { color: var(--success); font-weight: 700; }
.delta-negative { color: var(--danger); font-weight: 700; }

/* Touch card */
.touch-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    margin-bottom: 16px;
    overflow: hidden;
}
.touch-header {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    color: #fff;
    padding: 12px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.9rem;
}
.touch-header .touch-num {
    background: rgba(255,255,255,0.2);
    padding: 2px 10px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 0.8rem;
}
.touch-body { padding: 20px; }
.touch-meta {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
    margin-bottom: 12px;
    font-size: 0.85rem;
}
.touch-meta span {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    color: var(--text-light);
}
.touch-meta strong { color: var(--text); }

.hero-section {
    background: linear-gradient(135deg, var(--primary) 0%, #1e40af 100%);
    color: #fff;
    border-radius: var(--radius);
    padding: 40px;
    margin-bottom: 28px;
    box-shadow: var(--shadow-lg);
}
.hero-section h1 { color: #fff; font-size: 2rem; margin-bottom: 4px; }
.hero-section .subtitle { color: rgba(255,255,255,0.75); }
.team-badge {
    display: inline-block;
    background: var(--accent);
    color: #fff;
    font-weight: 700;
    padding: 4px 14px;
    border-radius: 14px;
    font-size: 0.8rem;
    letter-spacing: 0.5px;
    margin-top: 8px;
}

/* Loading state */
.loading { opacity: 0.6; pointer-events: none; }

/* Footer */
.footer {
    text-align: center;
    padding: 24px;
    font-size: 0.8rem;
    color: var(--text-light);
    border-top: 1px solid var(--border);
    margin-top: 40px;
}

/* Error block */
.error-block {
    background: #fef2f2;
    border: 1px solid #fecaca;
    border-left: 4px solid #dc2626;
    border-radius: 0 6px 6px 0;
    padding: 16px 20px;
    color: #991b1b;
    margin: 16px 0;
    font-size: 0.9rem;
    white-space: pre-wrap;
}

@media (max-width: 768px) {
    .topbar-inner { flex-direction: column; height: auto; padding: 12px; gap: 8px; }
    .topbar nav { flex-wrap: wrap; justify-content: center; }
    .hero-section { padding: 24px; }
    .hero-section h1 { font-size: 1.5rem; }
    .stats-grid { grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); }
}
"""

LAYOUT_TOP = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ title }} | NovaStar Hotels</title>
<style>""" + BASE_CSS + """</style>
</head>
<body>
<div class="topbar">
    <div class="topbar-inner">
        <a href="/" class="brand">
            <span class="brand-star">N</span>
            NovaStar Hotels
        </a>
        <nav>
            <a href="/" class="{{ 'active' if active == 'home' else '' }}">Dashboard</a>
            <a href="/simulation" class="{{ 'active' if active == 'simulation' else '' }}">Simulation</a>
            <a href="/engine" class="{{ 'active' if active == 'engine' else '' }}">Engagement Engine</a>
            <a href="/segments" class="{{ 'active' if active == 'segments' else '' }}">Guest Segments</a>
        </nav>
    </div>
</div>
<div class="container">
"""

LAYOUT_BOTTOM = """
</div>
<div class="footer">
    NovaStar Hotels &mdash; AI Post-Stay Engagement System &bull; Team AWESOME &bull; CE Masters AI Agent Teams
</div>
</body>
</html>
"""


# ===================================================================
# HELPER: wrap page content in layout
# ===================================================================
def _page(title: str, active: str, body: str) -> str:
    return render_template_string(
        LAYOUT_TOP + body + LAYOUT_BOTTOM,
        title=title,
        active=active,
    )


# ===================================================================
# PAGE 1 -- Dashboard Home
# ===================================================================
HOME_BODY = """
<div class="hero-section">
    <h1>AI-Powered Post-Stay Engagement System</h1>
    <p class="subtitle">Transforming 80,000 one-time guests into loyal NovaStar advocates through personalised, data-driven post-stay journeys.</p>
    <span class="team-badge">TEAM AWESOME</span>
</div>

<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-label">Properties</div>
        <div class="stat-value">45</div>
        <div class="stat-sub">Across 3 continents</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Annual Guests</div>
        <div class="stat-value">80K</div>
        <div class="stat-sub">Unique stays per year</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Current Rebooking</div>
        <div class="stat-value">12.1%</div>
        <div class="stat-sub">vs. 40% industry benchmark</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Revenue Gap</div>
        <div class="stat-value">$34.2M</div>
        <div class="stat-sub">Annual opportunity cost</div>
    </div>
</div>

<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap:20px;">
    <div class="card">
        <div class="card-header">The Problem</div>
        <p style="font-size:0.9rem; color:var(--text-light); margin-bottom:12px;">
            NovaStar currently loses 87.9% of first-time guests. Post-stay engagement is limited to a single
            generic survey email. 57% of guests leave without recoverable contact information.
        </p>
        <ul style="font-size:0.9rem; color:var(--text-light); padding-left:18px;">
            <li>No personalised follow-up after checkout</li>
            <li>18.4% email open rate (industry avg: 38%)</li>
            <li>Loyalty programme enrolment at 14% (target: 45%)</li>
            <li>OTA dependency: 62% of bookings through third parties</li>
        </ul>
    </div>
    <div class="card">
        <div class="card-header">Our Solution</div>
        <p style="font-size:0.9rem; color:var(--text-light); margin-bottom:12px;">
            A 6-stage AI-powered post-stay engagement journey tailored to 6 guest segments,
            delivered through the right channel at the right time.
        </p>
        <div style="margin-top:16px; display:flex; flex-wrap:wrap; gap:8px;">
            <a href="/simulation" class="btn btn-primary">Run Simulation</a>
            <a href="/engine" class="btn btn-secondary">Try Engagement Engine</a>
            <a href="/segments" class="btn btn-secondary">View Segments</a>
        </div>
    </div>
</div>

<div class="card" style="margin-top:8px;">
    <div class="card-header">Dana's 6-Stage Post-Stay Journey</div>
    <table>
        <tr>
            <th>Stage</th><th>Timing</th><th>Purpose</th>
        </tr>
        <tr><td><strong>1. Warm Farewell</strong></td><td>Day 0</td><td>Thank-you, stay recap, loyalty enrolment prompt</td></tr>
        <tr><td><strong>2. Nostalgia Trigger</strong></td><td>Days 3-7</td><td>Photo highlights, travel journal, social sharing</td></tr>
        <tr><td><strong>3. Value Reinforcement</strong></td><td>Days 14-21</td><td>Loyalty progress, tier benefits preview, points incentive</td></tr>
        <tr><td><strong>4. Contextual Re-engagement</strong></td><td>Days 30-60</td><td>Seasonal content, local experiences, sister-city discovery</td></tr>
        <tr><td><strong>5. Conversion Push</strong></td><td>Days 45-75</td><td>Personalised offer, urgency driver, direct booking incentive</td></tr>
        <tr><td><strong>6. Ongoing Relationship</strong></td><td>90+ days</td><td>Anniversary, birthday, portfolio explorer nudges</td></tr>
    </table>
</div>
"""


@app.route("/")
def home():
    return _page("Dashboard", "home", HOME_BODY)


# ===================================================================
# PAGE 2 -- Simulation
# ===================================================================
SIMULATION_BODY = """
<h1>Guest Journey Simulation</h1>
<p class="subtitle">Run the 90-day post-stay simulation to compare BEFORE (current state) vs AFTER (AI engagement system).</p>

<div class="card">
    <div class="card-header">Simulation Parameters</div>
    <form method="POST" action="/simulation">
        <div class="form-row">
            <div class="form-group">
                <label for="num_guests">Number of Guests: <span class="range-value" id="ng_val">{{ num_guests }}</span></label>
                <input type="range" id="num_guests" name="num_guests" min="50" max="500" step="10" value="{{ num_guests }}"
                       oninput="document.getElementById('ng_val').textContent=this.value">
            </div>
            <div class="form-group">
                <label for="seed">Random Seed</label>
                <input type="number" id="seed" name="seed" value="{{ seed }}" min="1" max="99999">
            </div>
        </div>
        <button type="submit" class="btn btn-primary">Run Simulation</button>
    </form>
</div>

{% if results %}
<div class="card">
    <div class="card-header">BEFORE vs AFTER Comparison &mdash; {{ results.num_guests }} guests, seed={{ results.seed }}</div>
    <table>
        <tr>
            <th style="width:40%;">Metric</th>
            <th style="width:20%; text-align:right;">BEFORE</th>
            <th style="width:20%; text-align:right;">AFTER</th>
            <th style="width:20%; text-align:right;">Delta</th>
        </tr>
        {% for row in results.comparison %}
        <tr>
            <td><strong>{{ row.label }}</strong></td>
            <td style="text-align:right;">{{ row.before }}</td>
            <td style="text-align:right;">{{ row.after }}</td>
            <td style="text-align:right;" class="{{ 'delta-positive' if row.delta_num >= 0 else 'delta-negative' }}">{{ row.delta }}</td>
        </tr>
        {% endfor %}
    </table>
</div>

<div class="card">
    <div class="card-header">Rebooking by Segment</div>
    <table>
        <tr>
            <th>Segment</th>
            <th style="text-align:right;">BEFORE</th>
            <th style="text-align:right;">AFTER</th>
            <th style="text-align:right;">Delta</th>
        </tr>
        {% for row in results.segment_rows %}
        <tr>
            <td><strong>{{ row.segment }}</strong></td>
            <td style="text-align:right;">{{ row.before }}</td>
            <td style="text-align:right;">{{ row.after }}</td>
            <td style="text-align:right;" class="delta-positive">{{ row.delta }}</td>
        </tr>
        {% endfor %}
    </table>
</div>

<div class="card">
    <div class="card-header">Financial Projections (Scaled to 80,000 Guests)</div>
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-label">Repeat Guests (Before)</div>
            <div class="stat-value">{{ "{:,}".format(results.fin.b_repeat) }}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Repeat Guests (After)</div>
            <div class="stat-value">{{ "{:,}".format(results.fin.a_repeat) }}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Incremental Guests</div>
            <div class="stat-value" style="color:var(--success);">+{{ "{:,}".format(results.fin.incremental) }}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Incremental Revenue</div>
            <div class="stat-value" style="color:var(--success);">${{ "{:,.0f}".format(results.fin.revenue) }}</div>
            <div class="stat-sub">+$560,000 OTA savings</div>
        </div>
    </div>
</div>
{% endif %}
"""


def _pct(n, d):
    return f"{n/d*100:.1f}%" if d > 0 else "N/A"


def _run_simulation(num_guests, seed):
    """Run BEFORE and AFTER simulations and return structured results."""
    # Temporarily override the module-level constant
    original_num = sim.NUM_GUESTS
    original_seed = sim.SEED
    sim.NUM_GUESTS = num_guests
    sim.SEED = seed

    try:
        rng_before = random.Random(seed)
        before = sim.simulate(
            label="BEFORE",
            rng=rng_before,
            email_open_rate=sim.BEFORE_EMAIL_OPEN,
            email_click_rate=sim.BEFORE_EMAIL_CLICK,
            rebook_rates=sim.BEFORE_REBOOK,
            emails_per_stage=sim.BEFORE_EMAILS_PER_STAGE,
            use_push=False,
            use_app=False,
        )

        rng_after = random.Random(seed)
        after = sim.simulate(
            label="AFTER",
            rng=rng_after,
            email_open_rate=sim.AFTER_EMAIL_OPEN,
            email_click_rate=sim.AFTER_EMAIL_CLICK,
            rebook_rates=sim.AFTER_REBOOK,
            emails_per_stage=sim.AFTER_EMAILS_PER_STAGE,
            use_push=True,
            use_app=True,
        )
    finally:
        sim.NUM_GUESTS = original_num
        sim.SEED = original_seed

    # Build comparison rows
    comparison = []

    def add_row(label, b_val, a_val, b_str=None, a_str=None):
        delta_num = a_val - b_val
        d_sign = "+" if delta_num >= 0 else ""
        comparison.append({
            "label": label,
            "before": b_str or str(b_val),
            "after": a_str or str(a_val),
            "delta": f"{d_sign}{delta_num}",
            "delta_num": delta_num,
        })

    add_row("Guests reachable (email/app)", before.guests_with_email, after.guests_with_email)
    add_row("Emails sent", before.total_emails_sent, after.total_emails_sent)
    add_row("Emails opened", before.total_emails_opened, after.total_emails_opened,
            f"{before.total_emails_opened} ({_pct(before.total_emails_opened, before.total_emails_sent)})",
            f"{after.total_emails_opened} ({_pct(after.total_emails_opened, after.total_emails_sent)})")
    add_row("Emails clicked", before.total_emails_clicked, after.total_emails_clicked,
            f"{before.total_emails_clicked} ({_pct(before.total_emails_clicked, before.total_emails_sent)})",
            f"{after.total_emails_clicked} ({_pct(after.total_emails_clicked, after.total_emails_sent)})")
    add_row("Push notifications sent", before.total_push_sent, after.total_push_sent)
    add_row("Push opened", before.total_push_opened, after.total_push_opened)
    add_row("App sessions (organic)", before.total_app_sessions, after.total_app_sessions)
    add_row("REBOOKED (total)", before.total_rebooked, after.total_rebooked,
            f"{before.total_rebooked} ({_pct(before.total_rebooked, num_guests)})",
            f"{after.total_rebooked} ({_pct(after.total_rebooked, num_guests)})")

    # Segment breakdown
    segment_rows = []
    for seg_name, _ in sim.SEGMENT_DIST:
        b_rebook, b_total = before.rebook_by_segment.get(seg_name, (0, 0))
        a_rebook, a_total = after.rebook_by_segment.get(seg_name, (0, 0))
        delta = a_rebook - b_rebook
        segment_rows.append({
            "segment": seg_name,
            "before": f"{b_rebook}/{b_total} ({_pct(b_rebook, b_total)})",
            "after": f"{a_rebook}/{a_total} ({_pct(a_rebook, a_total)})",
            "delta": f"+{delta}" if delta >= 0 else str(delta),
        })

    # Financial projections
    scale = 80_000 / num_guests
    b_repeat = int(before.total_rebooked * scale)
    a_repeat = int(after.total_rebooked * scale)
    incremental = a_repeat - b_repeat
    revenue = incremental * 3.71 * 159.70

    class Fin:
        pass
    fin = Fin()
    fin.b_repeat = b_repeat
    fin.a_repeat = a_repeat
    fin.incremental = incremental
    fin.revenue = revenue

    class Results:
        pass
    results = Results()
    results.num_guests = num_guests
    results.seed = seed
    results.comparison = comparison
    results.segment_rows = segment_rows
    results.fin = fin

    return results


@app.route("/simulation", methods=["GET", "POST"])
def simulation():
    num_guests = 100
    seed = 42
    results = None

    if request.method == "POST":
        try:
            num_guests = int(request.form.get("num_guests", 100))
            seed = int(request.form.get("seed", 42))
            num_guests = max(50, min(500, num_guests))
            results = _run_simulation(num_guests, seed)
        except Exception as e:
            error_html = f'<div class="error-block">Simulation error:\n{traceback.format_exc()}</div>'
            return _page("Simulation", "simulation", render_template_string(
                SIMULATION_BODY + error_html,
                num_guests=num_guests, seed=seed, results=None,
            ))

    return render_template_string(
        LAYOUT_TOP + SIMULATION_BODY + LAYOUT_BOTTOM,
        title="Simulation", active="simulation",
        num_guests=num_guests, seed=seed, results=results,
    )


# ===================================================================
# PAGE 3 -- Engagement Engine Demo
# ===================================================================
ENGINE_BODY = """
<h1>Engagement Engine Demo</h1>
<p class="subtitle">Configure a guest profile and see the full personalised trigger plan generated by the AI Personalisation Engine.</p>

<div class="card">
    <div class="card-header">Guest Profile Configuration</div>
    <form method="POST" action="/engine">
        <div class="form-row">
            <div class="form-group">
                <label for="segment">Guest Segment</label>
                <select id="segment" name="segment">
                    {% for seg in segments %}
                    <option value="{{ seg.name }}" {{ 'selected' if seg.name == selected_segment else '' }}>{{ seg.value }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label for="city">Property City</label>
                <select id="city" name="city">
                    {% for c in cities %}
                    <option value="{{ c }}" {{ 'selected' if c == selected_city else '' }}>{{ c }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label for="nights">Number of Nights: <span class="range-value" id="nv">{{ selected_nights }}</span></label>
                <input type="range" id="nights" name="nights" min="1" max="14" value="{{ selected_nights }}"
                       oninput="document.getElementById('nv').textContent=this.value">
            </div>
        </div>
        <button type="submit" class="btn btn-primary">Generate Trigger Plan</button>
    </form>
</div>

{% if guest_info %}
<div class="card">
    <div class="card-header">Guest Profile Summary</div>
    <div class="form-row" style="gap:32px;">
        <div>
            <p><strong>Name:</strong> {{ guest_info.name }}</p>
            <p><strong>Segment:</strong> {{ guest_info.segment }}</p>
            <p><strong>Email:</strong> {{ guest_info.email }}</p>
        </div>
        <div>
            <p><strong>Property:</strong> {{ guest_info.property }}</p>
            <p><strong>Nights:</strong> {{ guest_info.nights }}</p>
            <p><strong>Total Spend:</strong> ${{ guest_info.total_spend }}</p>
        </div>
        <div>
            <p><strong>Loyalty Tier:</strong> {{ guest_info.tier }}</p>
            <p><strong>Points Balance:</strong> {{ "{:,}".format(guest_info.points) }}</p>
            <p><strong>Engagement Intensity:</strong>
                <span class="badge badge-{{ guest_info.intensity_class }}">{{ guest_info.intensity }}</span>
            </p>
        </div>
    </div>
</div>

<h2>Trigger Plan ({{ triggers|length }} Touches)</h2>

{% for t in triggers %}
<div class="touch-card">
    <div class="touch-header">
        <div>
            <span class="touch-num">Touch {{ loop.index }}</span>
            &nbsp;&nbsp;{{ t.stage }}
        </div>
        <div>Day {{ t.day }}</div>
    </div>
    <div class="touch-body">
        <div class="touch-meta">
            <span>Channel: <strong>{{ t.channel }}</strong></span>
            <span>Action: <strong>{{ t.action }}</strong></span>
            <span>Churn Risk: <strong>{{ t.churn_risk }}</strong></span>
        </div>
        <h3>{{ t.subject }}</h3>
        <div class="msg-block">{{ t.body }}</div>
        {% if t.has_offer %}
        <div class="offer-block">
            <strong>OFFER: {{ t.offer_headline }}</strong><br>
            Discount: {{ t.offer_discount }}% &bull;
            Bonus Points: {{ t.offer_points }} &bull;
            Target: {{ t.offer_target }}<br>
            Perks: {{ t.offer_perks }}<br>
            Valid until: {{ t.offer_valid_until }}
        </div>
        {% endif %}
    </div>
</div>
{% endfor %}
{% endif %}
"""

CITIES = ["Austin", "Orlando", "Chicago", "Denver", "Barcelona", "London"]


def _segment_enum_from_name(name: str) -> GuestSegment:
    """Resolve a GuestSegment enum member from its .name string."""
    return GuestSegment[name]


def _run_engine(segment_name: str, city: str, nights: int):
    """Build a guest profile and run the engagement engine, returning template-friendly data."""
    seg = _segment_enum_from_name(segment_name)
    guest = make_sample_guest(seg)
    stay = make_sample_stay(guest, property_city=city)
    # Override nights and recalculate spend
    stay.nights = nights
    stay.total_spend = stay.rate_per_night * nights
    stay.check_out = date(2026, 1, 10 + nights)
    if nights >= 7:
        stay.room_type = "Suite"

    loyalty = make_sample_loyalty(guest)
    prefs = GuestPreferences(guest_id=guest.guest_id)

    profile = GuestProfile(
        guest=guest,
        stay=stay,
        preferences=prefs,
        loyalty=loyalty,
    )

    triggers = build_trigger_plan(profile)

    intensity = SEGMENT_INTENSITY.get(seg, "LOW")
    intensity_class = {
        "HIGH": "high",
        "MEDIUM-HIGH": "medium-high",
        "MEDIUM": "medium",
        "LOW": "low",
    }.get(intensity, "low")

    guest_info = {
        "name": guest.full_name,
        "segment": seg.value,
        "email": guest.email,
        "property": stay.property_name,
        "nights": stay.nights,
        "total_spend": f"{stay.total_spend:,.0f}",
        "tier": loyalty.tier.value,
        "points": loyalty.points_balance,
        "intensity": intensity,
        "intensity_class": intensity_class,
    }

    trigger_data = []
    for t in triggers:
        msg = t.message
        entry = {
            "stage": t.journey_stage.value,
            "day": t.day_offset,
            "channel": t.channel.value,
            "action": t.action,
            "churn_risk": f"{profile.churn_risk:.2f}",
            "subject": msg.subject_line if msg else "N/A",
            "body": msg.body if msg else "",
            "has_offer": bool(msg and msg.offer),
            "offer_headline": "",
            "offer_discount": 0,
            "offer_points": 0,
            "offer_perks": "",
            "offer_target": "",
            "offer_valid_until": "",
        }
        if msg and msg.offer:
            o = msg.offer
            entry["offer_headline"] = o.headline
            entry["offer_discount"] = int(o.discount_pct * 100)
            entry["offer_points"] = o.points_bonus
            entry["offer_perks"] = ", ".join(o.perks) if o.perks else "None"
            entry["offer_target"] = o.target_property or "Any NovaStar property"
            entry["offer_valid_until"] = o.valid_until.isoformat()
        trigger_data.append(entry)

    return guest_info, trigger_data


@app.route("/engine", methods=["GET", "POST"])
def engine():
    segments = list(GuestSegment)
    selected_segment = "FAMILY_VACATIONER"
    selected_city = "Austin"
    selected_nights = 4
    guest_info = None
    triggers = []

    if request.method == "POST":
        try:
            selected_segment = request.form.get("segment", "FAMILY_VACATIONER")
            selected_city = request.form.get("city", "Austin")
            selected_nights = int(request.form.get("nights", 4))
            selected_nights = max(1, min(14, selected_nights))
            guest_info, triggers = _run_engine(selected_segment, selected_city, selected_nights)
        except Exception:
            error_html = f'<div class="error-block">Engine error:\n{traceback.format_exc()}</div>'
            return render_template_string(
                LAYOUT_TOP + ENGINE_BODY + error_html + LAYOUT_BOTTOM,
                title="Engagement Engine", active="engine",
                segments=segments, cities=CITIES,
                selected_segment=selected_segment, selected_city=selected_city,
                selected_nights=selected_nights, guest_info=None, triggers=[],
            )

    return render_template_string(
        LAYOUT_TOP + ENGINE_BODY + LAYOUT_BOTTOM,
        title="Engagement Engine", active="engine",
        segments=segments, cities=CITIES,
        selected_segment=selected_segment, selected_city=selected_city,
        selected_nights=selected_nights, guest_info=guest_info, triggers=triggers,
    )


# ===================================================================
# PAGE 4 -- Guest Segments
# ===================================================================
SEGMENTS_BODY = """
<h1>Guest Segments</h1>
<p class="subtitle">Riley's research identified 6 distinct guest segments with unique behaviours, rebooking rates, and engagement strategies.</p>

<div class="card">
    <div class="card-header">Segment Overview</div>
    <div style="overflow-x:auto;">
    <table>
        <tr>
            <th>Segment</th>
            <th style="text-align:right;">% of Guests</th>
            <th style="text-align:right;">Avg Spend/Stay</th>
            <th style="text-align:right;">Current Rebook</th>
            <th style="text-align:right;">Target Rebook</th>
            <th style="text-align:center;">Engagement Intensity</th>
        </tr>
        {% for s in segment_data %}
        <tr>
            <td><strong>{{ s.name }}</strong></td>
            <td style="text-align:right;">{{ s.pct }}%</td>
            <td style="text-align:right;">${{ s.avg_spend }}</td>
            <td style="text-align:right;">{{ s.current_rebook }}%</td>
            <td style="text-align:right;">{{ s.target_rebook }}%</td>
            <td style="text-align:center;">
                <span class="badge badge-{{ s.intensity_class }}">{{ s.intensity }}</span>
            </td>
        </tr>
        {% endfor %}
    </table>
    </div>
</div>

<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap:20px;">
    {% for s in segment_data %}
    <div class="card">
        <div class="card-header" style="display:flex; justify-content:space-between; align-items:center;">
            {{ s.name }}
            <span class="badge badge-{{ s.intensity_class }}">{{ s.intensity }}</span>
        </div>
        <div style="font-size:0.88rem; color:var(--text-light);">
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:12px;">
                <div><strong>Share:</strong> {{ s.pct }}% of guests</div>
                <div><strong>Avg Spend:</strong> ${{ s.avg_spend }}</div>
                <div><strong>Current Rebook:</strong> {{ s.current_rebook }}%</div>
                <div><strong>Target Rebook:</strong> {{ s.target_rebook }}%</div>
                <div><strong>Avg Nights:</strong> {{ s.avg_nights }}</div>
                <div><strong>ADR:</strong> ${{ s.adr }}</div>
            </div>
            <p><strong>Key Traits:</strong> {{ s.traits }}</p>
            <div style="margin-top:10px;">
                <div style="background:var(--bg); border-radius:4px; height:8px; overflow:hidden;">
                    <div style="background: var(--accent); width:{{ s.target_rebook_bar }}%; height:100%; border-radius:4px; position:relative;">
                    </div>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:0.75rem; margin-top:2px;">
                    <span>Current: {{ s.current_rebook }}%</span>
                    <span>Target: {{ s.target_rebook }}%</span>
                </div>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
"""

SEGMENT_DETAILS = [
    {
        "name": "Business Regular",
        "pct": 22,
        "avg_spend": "378",
        "current_rebook": 19.4,
        "target_rebook": 30.0,
        "intensity": "HIGH",
        "intensity_class": "high",
        "avg_nights": 2,
        "adr": "189",
        "traits": "Corporate bookings, express check-in, loyalty-sensitive, weekday travel, consistent preferences.",
        "target_rebook_bar": 30,
    },
    {
        "name": "Weekend Leisure Couple",
        "pct": 24,
        "avg_spend": "304",
        "current_rebook": 10.7,
        "target_rebook": 18.0,
        "intensity": "MEDIUM-HIGH",
        "intensity_class": "medium-high",
        "avg_nights": 2,
        "adr": "152",
        "traits": "Weekend getaways, experience-driven, social media active, responsive to sister-city suggestions.",
        "target_rebook_bar": 18,
    },
    {
        "name": "Family Vacationer",
        "pct": 18,
        "avg_spend": "696",
        "current_rebook": 8.3,
        "target_rebook": 16.0,
        "intensity": "HIGH",
        "intensity_class": "high",
        "avg_nights": 4,
        "adr": "174",
        "traits": "School holiday travel, kids amenities, pool & breakfast usage, high total spend, long planning horizon.",
        "target_rebook_bar": 16,
    },
    {
        "name": "Budget-Conscious Solo",
        "pct": 15,
        "avg_spend": "218",
        "current_rebook": 6.1,
        "target_rebook": 8.0,
        "intensity": "LOW",
        "intensity_class": "low",
        "avg_nights": 2,
        "adr": "109",
        "traits": "Price-sensitive, OTA-dominant, minimal engagement, respond to flash deals and value pricing.",
        "target_rebook_bar": 8,
    },
    {
        "name": "Group/Event Attendee",
        "pct": 12,
        "avg_spend": "423",
        "current_rebook": 14.2,
        "target_rebook": 22.0,
        "intensity": "MEDIUM-HIGH",
        "intensity_class": "medium-high",
        "avg_nights": 3,
        "adr": "141",
        "traits": "Conference/wedding guests, individual return potential, social proof responsive, group-to-solo conversion.",
        "target_rebook_bar": 22,
    },
    {
        "name": "Extended-Stay / Relocation",
        "pct": 9,
        "avg_spend": "1,176",
        "current_rebook": 21.8,
        "target_rebook": 30.0,
        "intensity": "HIGH",
        "intensity_class": "high",
        "avg_nights": 12,
        "adr": "98",
        "traits": "Long-term project assignments, highest lifetime value, residents programme, referral potential, loyalty-driven.",
        "target_rebook_bar": 30,
    },
]


@app.route("/segments")
def segments():
    return render_template_string(
        LAYOUT_TOP + SEGMENTS_BODY + LAYOUT_BOTTOM,
        title="Guest Segments", active="segments",
        segment_data=SEGMENT_DETAILS,
    )


# ===================================================================
# MAIN
# ===================================================================
if __name__ == "__main__":
    print()
    print("=" * 60)
    print("  NovaStar Hotels -- AI Post-Stay Engagement Dashboard")
    print("  Team AWESOME")
    print("=" * 60)
    print()
    print("  Starting Flask development server...")
    print("  Open your browser to: http://127.0.0.1:5000")
    print()
    print("=" * 60)
    print()
    app.run(host="127.0.0.1", port=5000, debug=True)
