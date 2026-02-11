#!/usr/bin/env python3
"""
Generate a per-character heatmap for the Miscellaneous Technical Unicode block
(U+2300..U+23FF), colored by character frequency in English web text.

Frequency data source:
    FineFreq dataset (https://github.com/Bin-2/FineFreq)
    Derived from FineWeb v1.4.0 — 48.58 TB of English web text from Common Crawl,
    covering 2013–2025 (81+ trillion characters).

Usage:
    python generate_misc_technical_heatmap.py [--output heatmap.html] [--csv-cache /tmp/eng_freq.csv]
"""

import argparse
import csv
import html as html_mod
import math
import os
import unicodedata
import urllib.request

# ---------------------------------------------------------------------------
# Block boundaries
# ---------------------------------------------------------------------------

BLOCK_START = 0x2300
BLOCK_END = 0x23FF
BLOCK_NAME = "Miscellaneous Technical"

# ---------------------------------------------------------------------------
# Download / cache the FineFreq English CSV
# ---------------------------------------------------------------------------

FINEFREQ_URL = (
    "https://raw.githubusercontent.com/Bin-2/FineFreq/main/csv/eng_Latn.csv"
)


def ensure_csv(path):
    """Download the FineFreq English CSV if it does not already exist at *path*."""
    if os.path.exists(path):
        print(f"Using cached CSV: {path}")
        return
    print(f"Downloading FineFreq English CSV to {path} ...")
    urllib.request.urlretrieve(FINEFREQ_URL, path)
    print("Download complete.")


# ---------------------------------------------------------------------------
# Read per-character frequencies for our block
# ---------------------------------------------------------------------------


def read_char_frequencies(csv_path):
    """Return a dict mapping codepoint -> frequency for U+2300..U+23FF."""
    freqs = {}
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            char = row["character"]
            if not char:
                continue
            cp = ord(char[0])
            if BLOCK_START <= cp <= BLOCK_END:
                freqs[cp] = int(row["total_frequency_all_time"])
    return freqs


# ---------------------------------------------------------------------------
# Colour mapping  (log-scale heat)
# ---------------------------------------------------------------------------

GRADIENT = [
    (0.0, (20, 24, 46)),       # near-black navy
    (0.15, (32, 52, 102)),     # dark blue
    (0.30, (44, 90, 140)),     # steel blue
    (0.45, (60, 140, 120)),    # teal
    (0.55, (100, 170, 70)),    # olive-green
    (0.65, (180, 180, 40)),    # yellow
    (0.75, (220, 150, 30)),    # amber
    (0.85, (210, 90, 20)),     # orange
    (0.95, (180, 30, 20)),     # crimson
    (1.0, (130, 10, 10)),      # deep dark red
]


def lerp(a, b, t):
    return a + (b - a) * t


def freq_to_rgb(freq, max_log):
    """Map a frequency (may be 0) to an (r, g, b) tuple."""
    if freq <= 0:
        return GRADIENT[0][1]
    t = math.log10(freq + 1) / max_log
    t = max(0.0, min(1.0, t))
    for i in range(len(GRADIENT) - 1):
        t0, c0 = GRADIENT[i]
        t1, c1 = GRADIENT[i + 1]
        if t0 <= t <= t1:
            local_t = (t - t0) / (t1 - t0) if t1 != t0 else 0
            r = int(lerp(c0[0], c1[0], local_t))
            g = int(lerp(c0[1], c1[1], local_t))
            b = int(lerp(c0[2], c1[2], local_t))
            return (r, g, b)
    return GRADIENT[-1][1]


def luminance(r, g, b):
    """Relative luminance (simplified)."""
    return 0.299 * r + 0.587 * g + 0.114 * b


# ---------------------------------------------------------------------------
# Human-readable numbers
# ---------------------------------------------------------------------------


def _human_number(n):
    """Format large numbers with SI suffix."""
    if n >= 1e15:
        return f"{n/1e15:.1f} P"
    if n >= 1e12:
        return f"{n/1e12:.1f} T"
    if n >= 1e9:
        return f"{n/1e9:.1f} B"
    if n >= 1e6:
        return f"{n/1e6:.1f} M"
    if n >= 1e3:
        return f"{n/1e3:.1f} K"
    return str(n)


# ---------------------------------------------------------------------------
# HTML generation
# ---------------------------------------------------------------------------

COLUMNS = 16  # 16 columns = one row per 16 codepoints


def generate_html(freqs, output_path):
    """Write the per-character heatmap as a standalone HTML file."""
    max_freq = max(freqs.values()) if freqs else 1
    max_log = math.log10(max_freq + 1)

    cells = []
    for cp in range(BLOCK_START, BLOCK_END + 1):
        freq = freqs.get(cp, 0)
        r, g, b = freq_to_rgb(freq, max_log)
        fg = "#f0f0f0" if luminance(r, g, b) < 140 else "#111"
        bg = f"rgb({r},{g},{b})"

        char = chr(cp)
        safe_char = html_mod.escape(char)
        char_name = unicodedata.name(char, "")
        freq_label = _human_number(freq)

        # Show the character prominently, its codepoint, and the frequency
        cell = (
            f'<div class="char-cell" style="background:{bg};color:{fg}" '
            f'data-cp="U+{cp:04X}" data-name="{html_mod.escape(char_name)}">'
            f'<div class="char-display">{safe_char}</div>'
            f'<div class="char-code">U+{cp:04X}</div>'
            f'<div class="char-freq">{freq_label}</div>'
            f'</div>'
        )
        cells.append(cell)

    grid = "\n".join(cells)

    # Legend stops
    legend_stops = []
    num_legend = 12
    for li in range(num_legend + 1):
        t = li / num_legend
        log_val = t * max_log
        freq_val = 10 ** log_val - 1
        r, g, b = freq_to_rgb(freq_val, max_log)
        legend_stops.append(f"rgb({r},{g},{b})")
    gradient_css = ", ".join(legend_stops)

    page = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Miscellaneous Technical (U+2300..U+23FF) — Per-Character Frequency Heatmap</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
  background: #111;
  color: #eee;
  padding: 24px;
}}
h1 {{ text-align: center; margin-bottom: 6px; font-size: 1.5rem; }}
.subtitle {{ text-align: center; margin-bottom: 20px; font-size: 0.85rem;
             color: #aaa; max-width: 800px; margin-left: auto; margin-right: auto; }}
.legend {{
  display: flex; align-items: center; justify-content: center;
  gap: 10px; margin-bottom: 20px; font-size: 0.8rem;
}}
.legend-bar {{
  width: 320px; height: 18px; border-radius: 4px;
  background: linear-gradient(to right, {gradient_css});
}}
.grid {{
  display: grid;
  grid-template-columns: repeat({COLUMNS}, 1fr);
  gap: 3px;
}}
.char-cell {{
  position: relative;
  padding: 6px 4px;
  border-radius: 4px;
  min-height: 72px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  transition: transform 0.15s;
  cursor: default;
}}
.char-cell:hover {{ transform: scale(1.08); z-index: 2; box-shadow: 0 0 8px rgba(255,255,255,0.3); }}
.char-check {{ position: absolute; top: 3px; right: 3px; width: 14px; height: 14px; cursor: pointer; accent-color: #7af; }}
.char-display {{ font-size: 1.4rem; line-height: 1.3; }}
.char-code {{ font-size: 0.55rem; opacity: 0.8; font-family: monospace; margin-top: 2px; }}
.char-freq {{ font-size: 0.5rem; opacity: 0.7; font-family: monospace; margin-top: 1px; }}
.tooltip {{
  display: none;
  position: absolute;
  bottom: calc(100% + 6px);
  left: 50%;
  transform: translateX(-50%);
  background: #222;
  color: #eee;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 6px 10px;
  font-size: 0.7rem;
  white-space: nowrap;
  z-index: 10;
  pointer-events: none;
}}
.char-cell:hover .tooltip {{ display: block; }}
.source {{ text-align: center; margin-top: 24px; font-size: 0.75rem; color: #888; }}
.source a {{ color: #7af; }}
@media (max-width: 1100px) {{ .grid {{ grid-template-columns: repeat(8, 1fr); }} }}
@media (max-width: 600px)  {{ .grid {{ grid-template-columns: repeat(4, 1fr); }} }}
</style>
</head>
<body>

<h1>{BLOCK_NAME} — Per-Character Heatmap</h1>
<p class="subtitle">
  All 256 characters in the {BLOCK_NAME} block (U+2300..U+23FF), in code-point order.
  Background colour shows character frequency in English web text (log scale).
  Hover for Unicode name. Check tiles and click Export to copy selections.
</p>

<div class="legend">
  <span>0 occurrences</span>
  <div class="legend-bar"></div>
  <span>{_human_number(max_freq)}</span>
  <button id="export-btn" style="margin-left:16px; padding:4px 12px; border-radius:4px; border:1px solid #888; background:#222; color:#7af; cursor:pointer; font-size:0.8rem;">Export selections</button>
</div>

<div class="grid">
{grid}
</div>

<div class="source">
  Frequency data: <a href="https://github.com/Bin-2/FineFreq">FineFreq</a>
  (FineWeb v1.4.0 &mdash; 81 T English web characters, 2013&ndash;2025) &middot;
  Block: <a href="https://www.unicode.org/charts/PDF/U2300.pdf">{BLOCK_NAME}</a> (Unicode 16.0) &middot;
  Paper: <a href="https://arxiv.org/html/2512.09701">arXiv:2512.09701</a>
</div>

<script>
// Add checkboxes and tooltips to every cell
document.querySelectorAll('.char-cell').forEach(cell => {{
  // Checkbox
  const cb = document.createElement('input');
  cb.type = 'checkbox';
  cb.className = 'char-check';
  cb.title = 'Select this character';
  cell.insertBefore(cb, cell.firstChild);

  // Tooltip with Unicode name
  const name = cell.dataset.name || '(unassigned)';
  const tip = document.createElement('div');
  tip.className = 'tooltip';
  tip.textContent = cell.dataset.cp + '  ' + name;
  cell.appendChild(tip);
}});

// Export button
document.getElementById('export-btn').addEventListener('click', () => {{
  const checked = [...document.querySelectorAll('.char-cell')].filter(
    cell => cell.querySelector('.char-check').checked
  );
  if (checked.length === 0) {{
    alert('No characters selected. Check some tiles first.');
    return;
  }}
  const lines = checked.map(cell => {{
    const cp = cell.dataset.cp;
    const name = cell.dataset.name || '(unassigned)';
    const charDisp = cell.querySelector('.char-display').textContent;
    return charDisp + '  ' + cp + '  ' + name;
  }});
  const text = checked.length + ' character(s) selected:\\n\\n' + lines.join('\\n');
  navigator.clipboard.writeText(text).then(() => {{
    alert('Copied ' + checked.length + ' selected character(s) to clipboard.');
  }});
}});
</script>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"Heatmap written to {output_path}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Generate a per-character heatmap for the Miscellaneous Technical block."
    )
    parser.add_argument(
        "--output",
        default="misc_technical_heatmap.html",
        help="Output HTML file path (default: misc_technical_heatmap.html)",
    )
    parser.add_argument(
        "--csv-cache",
        default="/tmp/eng_freq.csv",
        help="Path to cache the FineFreq English CSV (default: /tmp/eng_freq.csv)",
    )
    args = parser.parse_args()

    ensure_csv(args.csv_cache)
    print("Reading character frequencies for Miscellaneous Technical block ...")
    freqs = read_char_frequencies(args.csv_cache)
    print(f"Found frequency data for {len(freqs)} characters in the block.")

    generate_html(freqs, args.output)


if __name__ == "__main__":
    main()
