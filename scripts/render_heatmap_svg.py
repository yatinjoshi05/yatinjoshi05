#!/usr/bin/env python3
"""
render_heatmap_svg.py — Renders the real GitHub contribution heatmap as a self-typing/staggered SVG.
Used by both local environment and GitHub Actions daily refresh.
"""

import json
from datetime import datetime

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

def render():
    with open("data/contributions.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total = data.get("total_contributions", 3)

    width = 860
    height = 185
    cell_size = 10
    cell_radius = 2.5
    cell_pitch = 13.5
    grid_start_x = 65
    grid_start_y = 45

    weeks = []
    current_week = []

    first_date = datetime.strptime(days[0]["date"], "%Y-%m-%d")
    start_day = (first_date.weekday() + 1) % 7 # 0 is Sunday

    for _ in range(start_day):
        current_week.append(None)

    for d in days:
        current_week.append(d)
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []
    if current_week:
        while len(current_week) < 7:
            current_week.append(None)
        weeks.append(current_week)

    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_labels = []
    last_month = -1

    for w_idx, wk in enumerate(weeks):
        first_valid = next((d for d in wk if d is not None), None)
        if first_valid:
            m = datetime.strptime(first_valid["date"], "%Y-%m-%d").month - 1
            if m != last_month and w_idx < 50:
                last_month = m
                x_pos = grid_start_x + w_idx * cell_pitch
                month_labels.append(f'<text x="{x_pos}" y="{grid_start_y - 10}" class="month-label">{month_names[m]}</text>')

    cells = []
    for w_idx, wk in enumerate(weeks):
        for d_idx, day in enumerate(wk):
            if not day:
                continue
            x = grid_start_x + w_idx * cell_pitch
            y = grid_start_y + d_idx * cell_pitch
            color = PALETTE[day.get("level", 0)]
            delay = f"{(w_idx * 7 + d_idx) * 0.003:.3f}"
            cnt = day.get("count", 0)
            title = f"{cnt} contribution{'s' if cnt != 1 else ''} on {day.get('date')}"
            cells.append(
                f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="{cell_radius}" fill="{color}" style="animation-delay: {delay}s" class="contrib-box">'
                f'<title>{title}</title>'
                f'</rect>'
            )

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .terminal-bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1px; rx: 12px; }}
    .header-text {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 12px; fill: #58a6ff; font-weight: 600; }}
    .month-label {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 9.5px; fill: #7d8590; }}
    .day-label {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 9.5px; fill: #7d8590; text-anchor: end; }}
    .legend-text {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 10px; fill: #7d8590; }}
    .footer-stat {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11px; fill: #e6edf3; font-weight: 500; }}
    .footer-accent {{ fill: #39d353; font-weight: 600; }}
    .btn-red {{ fill: #ff5f56; }}
    .btn-yellow {{ fill: #ffbd2e; }}
    .btn-green {{ fill: #27c93f; }}

    @keyframes slideIn {{
      0% {{ opacity: 0; transform: translateY(4px); }}
      100% {{ opacity: 1; transform: translateY(0); }}
    }}

    .contrib-box {{
      opacity: 0;
      animation: slideIn 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}

    @media (prefers-reduced-motion: reduce) {{
      .contrib-box {{ opacity: 1 !important; animation: none !important; }}
    }}
  </style>

  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" class="terminal-bg" />
  <circle cx="20" cy="18" r="4.5" class="btn-red" />
  <circle cx="35" cy="18" r="4.5" class="btn-yellow" />
  <circle cx="50" cy="18" r="4.5" class="btn-green" />
  <text x="75" y="22" class="header-text">yatin@gtm:~$ ./contributions.sh --summary</text>

  {''.join(month_labels)}

  <text x="{grid_start_x - 8}" y="{grid_start_y + 1 * cell_pitch + 8}" class="day-label">Mon</text>
  <text x="{grid_start_x - 8}" y="{grid_start_y + 3 * cell_pitch + 8}" class="day-label">Wed</text>
  <text x="{grid_start_x - 8}" y="{grid_start_y + 5 * cell_pitch + 8}" class="day-label">Fri</text>

  <g id="heatmap-grid">
  {''.join(cells)}
  </g>

  <g transform="translate({grid_start_x}, {height - 18})">
    <text x="0" y="0" class="footer-stat">
      <tspan class="footer-accent">{total} contributions</tspan> in the last year
    </text>

    <g transform="translate({width - grid_start_x - 190}, -8)">
      <text x="-32" y="8" class="legend-text">Less</text>
      <rect x="0" y="0" width="10" height="10" rx="2" fill="{PALETTE[0]}" />
      <rect x="13.5" y="0" width="10" height="10" rx="2" fill="{PALETTE[1]}" />
      <rect x="27" y="0" width="10" height="10" rx="2" fill="{PALETTE[2]}" />
      <rect x="40.5" y="0" width="10" height="10" rx="2" fill="{PALETTE[3]}" />
      <rect x="54" y="0" width="10" height="10" rx="2" fill="{PALETTE[4]}" />
      <text x="70" y="8" class="legend-text">More</text>
    </g>
  </g>
</svg>"""

    with open("assets/contribution-heatmap.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("Saved assets/contribution-heatmap.svg")

if __name__ == "__main__":
    render()
