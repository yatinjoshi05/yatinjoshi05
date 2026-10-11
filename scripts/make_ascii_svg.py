#!/usr/bin/env python3
"""
make_ascii_svg.py — Converts prepped portrait into an animated monochrome ASCII SVG.
"""

from PIL import Image

RAMP = " .`:-=+*cs#%@"

def escape_xml(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def generate():
    img = Image.open("source-prepped.png").convert("L")
    cols = 68
    rows = 44
    resized = img.resize((cols, rows), Image.Resampling.LANCZOS)

    lines = []
    for y in range(rows):
        line = ""
        for x in range(cols):
            val = resized.getpixel((x, y))
            if val > 232:
                line += " "
            else:
                norm = 1.0 - (val / 232.0)
                idx = min(len(RAMP) - 1, int(norm * len(RAMP)))
                line += RAMP[idx]
        lines.append(line)

    width = 370
    height = 360
    start_y = 54
    line_height = 6.8

    row_elements = []
    for idx, l in enumerate(lines):
        y = start_y + idx * line_height
        delay = f"{0.05 + idx * 0.04:.3f}"
        escaped = escape_xml(l)
        row_elements.append(f"""    <g class="ascii-row" style="animation-delay: {delay}s">
      <text x="20" y="{y:.1f}" class="ascii-text" xml:space="preserve">{escaped}</text>
    </g>""")

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .terminal-bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1px; rx: 12px; }}
    .header-text {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 12px; fill: #58a6ff; font-weight: 600; }}
    .ascii-text {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 6.8px;
      letter-spacing: 0.1px;
      fill: #e6edf3;
      white-space: pre;
    }}
    .btn-red {{ fill: #ff5f56; }}
    .btn-yellow {{ fill: #ffbd2e; }}
    .btn-green {{ fill: #27c93f; }}

    @keyframes printRow {{
      0% {{ opacity: 0; clip-path: inset(0 100% 0 0); }}
      100% {{ opacity: 1; clip-path: inset(0 0 0 0); }}
    }}

    .ascii-row {{
      opacity: 0;
      animation: printRow 0.12s steps(10, end) forwards;
    }}

    @media (prefers-reduced-motion: reduce) {{
      .ascii-row {{ opacity: 1 !important; clip-path: none !important; animation: none !important; }}
    }}
  </style>

  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" class="terminal-bg" />
  <circle cx="20" cy="18" r="4.5" class="btn-red" />
  <circle cx="35" cy="18" r="4.5" class="btn-yellow" />
  <circle cx="50" cy="18" r="4.5" class="btn-green" />
  <text x="75" y="22" class="header-text">yatin@gtm:~$ ./portrait.sh</text>
  <line x1="15" y1="36" x2="{width - 15}" y2="36" stroke="#21262d" stroke-width="1" />

  <g id="ascii-canvas">
{chr(10).join(row_elements)}
  </g>
</svg>"""

    with open("assets/profile-ascii.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("Saved assets/profile-ascii.svg")

if __name__ == "__main__":
    generate()
