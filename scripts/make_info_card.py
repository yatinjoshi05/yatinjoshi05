#!/usr/bin/env python3
"""
make_info_card.py — Hand-authors a neofetch-style terminal info card as an SVG.
"""

def make():
    width = 490
    height = 360

    rows = [
        ("OS", "GTM-Linux x86_64", "#39d353", False, False),
        ("HOST", "Haldwani, Uttarakhand, India", "#e6edf3", False, False),
        ("ROLE", "Entry-Level GTM Engineer", "#58a6ff", True, False),
        ("FOCUS", "Revenue Automation &amp; AI Workflows", "#e6edf3", False, False),
        ("BUILDING", "Revenue Lifecycle Orchestration Engine", "#f0883e", False, False),
        ("STACK", "n8n • Supabase • Clay • HubSpot • JS", "#e6edf3", False, False),
        ("CONCEPTS", "ICP Scoring • Webhooks • Deduplication", "#e6edf3", False, False),
        ("TELEMETRY", "Gated LLM • Error Logging • Sync Status", "#e6edf3", False, False),
        ("MINDSET", "Business Problems → Technical Systems", "#7ee787", False, False),
        ("STATUS", "Available for GTM &amp; RevOps Eng Roles", "#39d353", False, True)
    ]

    start_y = 65
    line_pitch = 27
    lines_svg = []

    for idx, (label, val, color, bold, dot) in enumerate(rows):
        y = start_y + idx * line_pitch
        delay = f"{0.2 + idx * 0.08:.2f}"
        label_x = 25
        val_x = 135
        weight = "font-weight: 600;" if bold else ""
        extra = f'<circle cx="{val_x - 10}" cy="{y - 4}" r="3.5" fill="#39d353" class="status-pulse" />' if dot else ""
        lines_svg.append(f"""    <g class="info-line" style="animation-delay: {delay}s">
      <text x="{label_x}" y="{y}" class="info-label">{label}</text>
      <text x="{val_x - 25}" y="{y}" class="info-colon">:</text>
      {extra}
      <text x="{val_x + 4 if dot else val_x}" y="{y}" class="info-value" style="fill: {color}; {weight}">{val}</text>
    </g>""")

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .card-bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1px; rx: 12px; }}
    .header-text {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 12px; fill: #58a6ff; font-weight: 600; }}
    .info-label {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11.5px; fill: #8b949e; font-weight: 500; }}
    .info-colon {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11.5px; fill: #6e7681; }}
    .info-value {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11.5px; }}
    .btn-red {{ fill: #ff5f56; }}
    .btn-yellow {{ fill: #ffbd2e; }}
    .btn-green {{ fill: #27c93f; }}

    @keyframes fadeInLine {{
      0% {{ opacity: 0; transform: translateY(5px); }}
      100% {{ opacity: 1; transform: translateY(0); }}
    }}

    .info-line {{
      opacity: 0;
      animation: fadeInLine 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}

    @keyframes pulse {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.4; }}
    }}
    .status-pulse {{ animation: pulse 2s infinite; }}

    @media (prefers-reduced-motion: reduce) {{
      .info-line {{ opacity: 1 !important; animation: none !important; }}
      .status-pulse {{ animation: none !important; }}
    }}
  </style>

  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" class="card-bg" />
  <circle cx="20" cy="18" r="4.5" class="btn-red" />
  <circle cx="35" cy="18" r="4.5" class="btn-yellow" />
  <circle cx="50" cy="18" r="4.5" class="btn-green" />
  <text x="75" y="22" class="header-text">yatin@gtm:~$ neofetch --gtm-profile</text>
  <line x1="15" y1="36" x2="{width - 15}" y2="36" stroke="#21262d" stroke-width="1" />

{chr(10).join(lines_svg)}

  <g transform="translate(25, {start_y + len(rows) * line_pitch + 2})">
    <text x="0" y="0" class="header-text" style="fill: #39d353;">yatin@gtm:~$</text>
    <rect x="95" y="-10" width="7" height="12" fill="#58a6ff" class="status-pulse" />
  </g>
</svg>"""

    with open("assets/info-card.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("Saved assets/info-card.svg")

if __name__ == "__main__":
    make()
