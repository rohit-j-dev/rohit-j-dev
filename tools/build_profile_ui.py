"""Generate the inert SVG assets used by the profile README.

Run from the repository root:  python tools/build_profile_ui.py
It rewrites assets/ui/*.svg and README.md.
Every asset has a desktop (1200px wide) and a mobile (800px wide) variant.
The SVGs contain no scripts, links, external fonts, or external resources.
"""

from __future__ import annotations

import math
import random
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "ui"

SANS = "'Segoe UI', 'Inter', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'SFMono-Regular', 'Cascadia Code', Consolas, 'Liberation Mono', monospace"

INK = "#070914"
CARD_TOP = "#0D1230"
CARD_BOTTOM = "#090C1E"
TEXT = "#EEF1FF"
MUTED = "#A3ACCF"
DIM = "#6B7499"
CYAN = "#22D3EE"
VIOLET = "#8B5CF6"
PINK = "#F472B6"
AMBER = "#FBBF24"
ACCENTS = (CYAN, VIOLET, PINK, AMBER)

STYLE = f"""
.sans{{font-family:{SANS}}}
.mono{{font-family:{MONO}}}
.twinkle{{animation:twinkle 4s ease-in-out infinite}}
.aurora{{animation:aurora 16s ease-in-out infinite alternate}}
.aurora.b{{animation-duration:21s;animation-direction:alternate-reverse}}
.bob{{transform-box:fill-box;transform-origin:50% 90%;animation:bob 6s ease-in-out infinite}}
.shimmer{{animation:shimmer 3.2s ease-in-out infinite}}
.glow{{animation:glow 7s ease-in-out infinite}}
.cursor{{animation:blink 1.1s steps(1) infinite}}
.petal{{animation:fall linear infinite}}
.sweep{{animation:sweep 9s ease-in-out infinite}}
.wave{{animation:wave 14s linear infinite}}
.wave.b{{animation-duration:22s;animation-direction:reverse}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2.4s ease-in-out infinite}}
@keyframes twinkle{{0%,100%{{opacity:.2}}50%{{opacity:1}}}}
@keyframes aurora{{from{{transform:translate(-40px,0)}}to{{transform:translate(60px,18px)}}}}
@keyframes bob{{0%,100%{{transform:translateY(0) rotate(-1.2deg)}}50%{{transform:translateY(5px) rotate(1.2deg)}}}}
@keyframes shimmer{{0%,100%{{opacity:.25}}50%{{opacity:.85}}}}
@keyframes glow{{0%,100%{{opacity:.55}}50%{{opacity:.9}}}}
@keyframes blink{{0%{{opacity:1}}50%{{opacity:0}}}}
@keyframes fall{{from{{transform:translate(0,-40px) rotate(0deg)}}to{{transform:translate(-260px,620px) rotate(540deg)}}}}
@keyframes sweep{{0%{{transform:translateX(-30%)}}100%{{transform:translateX(130%)}}}}
@keyframes wave{{from{{transform:translateX(0)}}to{{transform:translateX(-600px)}}}}
@keyframes pulse{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.45;transform:scale(.8)}}}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}
"""


def char_width(size: float, mono: bool = False, bold: bool = False, caps: bool = False) -> float:
    if mono:
        return size * 0.61
    if caps:
        return size * (0.7 if bold else 0.64)
    return size * (0.56 if bold else 0.52)


def text_width(text: str, size: float, **kw) -> float:
    return len(text) * char_width(size, **kw)


def wrap(text: str, size: float, max_width: float, **kw) -> list[str]:
    lines, line = [], ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if line and text_width(candidate, size, **kw) > max_width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def t(x, y, text, size, fill=TEXT, cls="sans", weight=400, anchor="start", spacing=0, extra=""):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}"{ls}{extra}>{escape(text)}</text>'
    )


def svg(width: int, height: int, title: str, body: str, defs: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">\n'
        f"<title id=\"title\">{escape(title)}</title>\n"
        f"<style>{STYLE}</style>\n"
        f"<defs>{COMMON_DEFS}{defs}</defs>\n{body}\n</svg>\n"
    )


COMMON_DEFS = f"""
<linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#FFFFFF"/><stop offset=".55" stop-color="#D8CCFF"/><stop offset="1" stop-color="{CYAN}"/>
</linearGradient>
<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/>
</linearGradient>
<linearGradient id="card" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{CARD_TOP}"/><stop offset="1" stop-color="{CARD_BOTTOM}"/>
</linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{CYAN}" stop-opacity=".55"/><stop offset=".45" stop-color="{VIOLET}" stop-opacity=".25"/>
  <stop offset="1" stop-color="{PINK}" stop-opacity=".45"/>
</linearGradient>
<linearGradient id="tile" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#141A3D"/><stop offset="1" stop-color="#0E1230"/>
</linearGradient>
<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity=".07"/>
  <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
</linearGradient>
<radialGradient id="glowCyan"><stop offset="0" stop-color="{CYAN}" stop-opacity=".5"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<radialGradient id="glowViolet"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".55"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
<radialGradient id="glowPink"><stop offset="0" stop-color="{PINK}" stop-opacity=".4"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/></radialGradient>
"""


# ---------------------------------------------------------------- primitives

def card_frame(w, h, number, label, title, title_size=34, pad=56, beam=True, label_size=16):
    parts = [
        f'<clipPath id="clip"><rect width="{w}" height="{h}" rx="28"/></clipPath>',
        '<g clip-path="url(#clip)">',
        f'<rect width="{w}" height="{h}" fill="url(#card)"/>',
        f'<ellipse cx="{w * 0.9:.0f}" cy="0" rx="{w * 0.35:.0f}" ry="{h * 0.45:.0f}" fill="url(#glowViolet)" opacity=".55"/>',
        f'<ellipse cx="0" cy="{h:.0f}" rx="{w * 0.3:.0f}" ry="{h * 0.35:.0f}" fill="url(#glowCyan)" opacity=".35"/>',
    ]
    if beam:
        parts.append(f'<rect class="sweep" x="0" y="0" width="{w * 0.35:.0f}" height="{h}" fill="url(#beam)"/>')
    parts += [
        "</g>",
        f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="27.5" fill="none" stroke="url(#edge)" stroke-width="1.5"/>',
        f'<rect x="{pad}" y="0" width="120" height="3" rx="1.5" fill="url(#accent)"/>',
        t(pad, 72, f"{number} // {label}", label_size, CYAN, "mono", 600, spacing=4),
        t(pad, 72 + title_size + 16, title, title_size, TEXT, "sans", 700),
    ]
    return "\n".join(parts)


def chip(x, y, label, color, size=14, height=32, filled=False):
    width = text_width(label, size, mono=True) + 34
    fill = color if filled else "none"
    text_fill = INK if filled else color
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height}" rx="{height / 2}" fill="{fill}" '
        f'fill-opacity="{1 if filled else 0}" stroke="{color}" stroke-opacity=".6"/>'
        + f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height}" rx="{height / 2}" fill="{color}" fill-opacity=".1"/>'
        + t(x + width / 2, y + height / 2 + size * 0.36, label, size, text_fill, "mono", 600, "middle", 1)
    ), width


def chips_row(labels, x, y, max_width, size=14, height=32, gap=10, center=False):
    rows, row, row_w = [], [], 0.0
    for i, label in enumerate(labels):
        w = text_width(label, size, mono=True) + 34
        if row and row_w + gap + w > max_width:
            rows.append((row, row_w))
            row, row_w = [], 0.0
        row_w = row_w + (gap if row else 0) + w
        row.append((label, ACCENTS[i % len(ACCENTS)]))
    if row:
        rows.append((row, row_w))
    out = []
    for r, (items, total) in enumerate(rows):
        cx = x + (max_width - total) / 2 if center else x
        for label, color in items:
            s, w = chip(cx, y + r * (height + gap), label, color, size, height)
            out.append(s)
            cx += w + gap
    return "\n".join(out), len(rows) * (height + gap) - gap


def icon(kind, x, y, size, color):
    """Small line icons drawn on a 24-unit grid."""
    paths = {
        "agent": '<circle cx="12" cy="5" r="2.6"/><circle cx="5" cy="18" r="2.6"/><circle cx="19" cy="18" r="2.6"/>'
                 '<path d="M10.7 7.3 6.3 15.7M13.3 7.3l4.4 8.4M7.6 18h8.8"/>',
        "cloud": '<path d="M7 18.5h10.2a4.3 4.3 0 0 0 .6-8.6A6 6 0 0 0 6.4 9.4 4.6 4.6 0 0 0 7 18.5Z"/><path d="M12 12v4M10 14h4"/>',
        "cube": '<path d="M12 2.8 20 7.3v9.4l-8 4.5-8-4.5V7.3Z"/><path d="M4 7.3l8 4.5 8-4.5M12 11.8v9.4"/>',
        "spark": '<path d="M12 2.5c.8 5.1 3.4 7.7 8.5 8.5-5.1.8-7.7 3.4-8.5 8.5-.8-5.1-3.4-7.7-8.5-8.5 5.1-.8 7.7-3.4 8.5-8.5Z"/>'
                 '<path d="M19 17.5v4M17 19.5h4"/>',
        "petal": '<path d="M12 3c3.8 3 4.6 7.3 0 12.5C7.4 10.3 8.2 6 12 3Z"/><path d="M4.2 13.3c4.8-.6 7.4 1.6 7.8 6.8-5 .7-7.7-1.5-7.8-6.8ZM19.8 13.3c-4.8-.6-7.4 1.6-7.8 6.8 5 .7 7.7-1.5 7.8-6.8Z"/>',
        "station": '<path d="M3 20.5h18M5 20.5V9.5l7-5 7 5v11"/><path d="M9 20.5v-6h6v6M8.5 10.5h7"/>',
        "bolt": '<path d="M13.5 2.5 5 13.5h6l-1 8 8.5-11h-6Z"/>',
    }
    scale = size / 24
    return (
        f'<g transform="translate({x:.1f} {y:.1f}) scale({scale:.3f})" fill="none" stroke="{color}" '
        f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{paths[kind]}</g>'
    )


def icon_tile(kind, x, y, size, color):
    return (
        f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size * 0.28:.1f}" fill="{color}" fill-opacity=".1" '
        f'stroke="{color}" stroke-opacity=".45"/>' + icon(kind, x + size * 0.22, y + size * 0.22, size * 0.56, color)
    )


# ---------------------------------------------------------------- hero

def stars(w, h, count, seed, max_y_ratio=0.72, avoid=None):
    rnd = random.Random(seed)
    out = []
    for i in range(count):
        x, y = rnd.uniform(10, w - 10), rnd.uniform(8, h * max_y_ratio)
        if avoid and avoid[0] <= x <= avoid[2] and avoid[1] <= y <= avoid[3]:
            continue
        r = rnd.choice((0.7, 0.9, 1.1, 1.4, 1.8))
        if i % 3 == 0:
            delay = rnd.uniform(-4, 0)
            out.append(f'<circle class="twinkle" style="animation-delay:{delay:.2f}s" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#FFFFFF"/>')
        else:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#FFFFFF" opacity="{rnd.uniform(.25, .7):.2f}"/>')
    return "\n".join(out)


def petals(w, count, seed, top=-20, start=0.25):
    rnd = random.Random(seed)
    out = []
    for _ in range(count):
        x = rnd.uniform(w * start, w + 160)
        dur = rnd.uniform(13, 22)
        delay = -rnd.uniform(0, dur)
        size = rnd.uniform(4, 7)
        out.append(
            f'<g transform="translate({x:.0f} {top})"><ellipse class="petal" style="animation-duration:{dur:.1f}s;'
            f'animation-delay:{delay:.1f}s" rx="{size:.1f}" ry="{size * 0.55:.1f}" fill="{PINK}" opacity=".75"/></g>'
        )
    return "\n".join(out)


def ship(x, y, scale):
    """An original, stylised sailing ship silhouette (not a copy of any franchise design)."""
    return f"""
<g transform="translate({x} {y}) scale({scale})">
 <g class="bob">
  <path d="M85 -2V84M40 30v54M132 26v56" stroke="#05060F" stroke-width="3.2"/>
  <path d="M85 -2v-16l21 5-21 5" fill="{PINK}"/>
  <path d="M60 8q25-8 50 0 11 32 0 64-25-7-50 0-11-32 0-64Z" fill="#0A0C1E" stroke="#C4B5FD" stroke-opacity=".55" stroke-width="1.4"/>
  <path d="M24 34q16-6 32 0 7 19 0 38-16-5-32 0-7-19 0-38Z" fill="#0A0C1E" stroke="#C4B5FD" stroke-opacity=".45" stroke-width="1.2"/>
  <path d="M134 28 166 76H134Z" fill="#0A0C1E" stroke="#C4B5FD" stroke-opacity=".45" stroke-width="1.2"/>
  <path d="M0 80q85 26 176 0l-12 22q-76 18-152 0Z" fill="#05060F" stroke="{CYAN}" stroke-opacity=".5" stroke-width="1.4"/>
  <circle cx="176" cy="76" r="8" fill="{AMBER}" opacity=".9"/>
  <circle cx="176" cy="76" r="14" fill="none" stroke="{AMBER}" stroke-opacity=".5" stroke-dasharray="3 3"/>
  <circle cx="30" cy="88" r="2.2" fill="{AMBER}"/><circle cx="55" cy="92" r="2.2" fill="{AMBER}"/>
 </g>
</g>"""


def moon_scene(w, h, horizon, moon_x, moon_y, moon_r, ship_x, ship_y, ship_scale):
    reflections = []
    for i in range(7):
        ry = horizon + 14 + i * 16
        rw = moon_r * (1.5 - i * 0.17)
        delay = -i * 0.45
        reflections.append(
            f'<rect class="shimmer" style="animation-delay:{delay:.2f}s" x="{moon_x - rw / 2:.0f}" y="{ry:.0f}" '
            f'width="{rw:.0f}" height="3" rx="1.5" fill="#E9D5FF" opacity=".5"/>'
        )
    hills = (
        f'<path d="M0 {horizon} q{w * 0.08:.0f} -38 {w * 0.17:.0f} -14 q{w * 0.07:.0f} -26 {w * 0.15:.0f} 14 Z" fill="#0B0F2A"/>'
        f'<path d="M{w * 0.66:.0f} {horizon} q{w * 0.1:.0f} -30 {w * 0.2:.0f} -8 q{w * 0.08:.0f} -22 {w * 0.14:.0f} 8 Z" fill="#0B0F2A"/>'
    )
    return f"""
<circle class="glow" cx="{moon_x}" cy="{moon_y}" r="{moon_r * 2.1:.0f}" fill="url(#moonHalo)"/>
<circle cx="{moon_x}" cy="{moon_y}" r="{moon_r}" fill="url(#moon)"/>
<circle cx="{moon_x - moon_r * 0.35:.0f}" cy="{moon_y - moon_r * 0.2:.0f}" r="{moon_r * 0.16:.0f}" fill="#C4B5FD" opacity=".25"/>
<circle cx="{moon_x + moon_r * 0.3:.0f}" cy="{moon_y + moon_r * 0.28:.0f}" r="{moon_r * 0.1:.0f}" fill="#C4B5FD" opacity=".25"/>
<circle cx="{moon_x + moon_r * 0.4:.0f}" cy="{moon_y - moon_r * 0.4:.0f}" r="{moon_r * 0.07:.0f}" fill="#C4B5FD" opacity=".2"/>
{hills}
<rect x="0" y="{horizon}" width="{w}" height="{h - horizon}" fill="url(#sea)"/>
<rect x="0" y="{horizon}" width="{w}" height="1.5" fill="{CYAN}" opacity=".35"/>
{''.join(reflections)}
{ship(ship_x, ship_y, ship_scale)}
"""


HERO_DEFS = f"""
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#05060F"/><stop offset=".55" stop-color="#0C0F2E"/><stop offset="1" stop-color="#1B1040"/>
</linearGradient>
<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#151A45"/><stop offset="1" stop-color="#05060F"/>
</linearGradient>
<radialGradient id="moon" cx=".4" cy=".35" r=".75">
  <stop offset="0" stop-color="#FFF7ED"/><stop offset=".55" stop-color="#F5D0FE"/><stop offset="1" stop-color="#A78BFA"/>
</radialGradient>
<radialGradient id="moonHalo"><stop offset=".45" stop-color="#E9D5FF" stop-opacity=".35"/><stop offset="1" stop-color="#8B5CF6" stop-opacity="0"/></radialGradient>
"""

TAGLINE = "AI agents · Developer automation · Digital twins"
HERO_CHIPS = ["FULL STACK & AI", "CLOUD · CI/CD", "OMNIVERSE · ISAAC SIM"]
HERO_ALT = "ROHIT JAGADALE — AI agents, developer automation and digital twins. A moonlit sea with a small sailing ship."


def hero_desktop():
    w, h = 1200, 520
    body = f"""
<clipPath id="clip"><rect width="{w}" height="{h}" rx="28"/></clipPath>
<g clip-path="url(#clip)">
<rect width="{w}" height="{h}" fill="url(#sky)"/>
<ellipse class="aurora" cx="330" cy="120" rx="460" ry="170" fill="url(#glowCyan)" opacity=".55"/>
<ellipse class="aurora b" cx="760" cy="60" rx="420" ry="160" fill="url(#glowViolet)"/>
<ellipse class="aurora" cx="160" cy="470" rx="380" ry="140" fill="url(#glowPink)" opacity=".6"/>
{stars(w, h, 110, 7, avoid=(40, 90, 790, 460))}
{moon_scene(w, h, 380, 940, 236, 112, 830, 262, 1.3)}
{petals(w, 8, 3, start=0.72)}
<rect class="sweep" x="0" y="0" width="420" height="{h}" fill="url(#beam)"/>
</g>
<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="27.5" fill="none" stroke="url(#edge)" stroke-width="1.5"/>
{t(w - 40, 52, "github.com/rohit-j-dev", 15, DIM, "mono", 500, "end", 2)}
<circle class="pulse" cx="72" cy="47" r="5" fill="#34D399"/>
{t(88, 52, "ONLINE · BUILDING THE NEXT LEVEL", 14, "#6EE7B7", "mono", 600, spacing=3)}
{t(72, 168, "HELLO, WORLD — I'M", 18, CYAN, "mono", 600, spacing=6)}
<text x="68" y="252" class="sans" font-size="76" font-weight="800" fill="url(#name)" textLength="690" lengthAdjust="spacing">ROHIT JAGADALE</text>
<rect x="72" y="278" width="140" height="4" rx="2" fill="url(#accent)"/>
{t(72, 330, TAGLINE, 27, "#D4DAF7", "sans", 500)}
{t(72, 372, "> automate the boring stuff. ship useful things.", 18, MUTED, "mono", 500)}
<rect class="cursor" x="{72 + text_width('> automate the boring stuff. ship useful things.', 18, mono=True) + 6:.0f}" y="357" width="10" height="20" fill="{CYAN}"/>
{chips_row(HERO_CHIPS, 72, 412, 700, 14, 34)[0]}
"""
    return svg(w, h, HERO_ALT, body, HERO_DEFS)


def hero_mobile():
    w, h = 800, 1060
    body = f"""
<clipPath id="clip"><rect width="{w}" height="{h}" rx="32"/></clipPath>
<g clip-path="url(#clip)">
<rect width="{w}" height="{h}" fill="url(#sky)"/>
<ellipse class="aurora" cx="200" cy="140" rx="380" ry="190" fill="url(#glowCyan)" opacity=".55"/>
<ellipse class="aurora b" cx="600" cy="80" rx="360" ry="170" fill="url(#glowViolet)"/>
<ellipse class="aurora" cx="400" cy="900" rx="420" ry="180" fill="url(#glowPink)" opacity=".5"/>
{stars(w, h, 80, 11, 0.42, avoid=(0, 0, 200, 100))}
{moon_scene(w, 470, 400, 480, 230, 128, 300, 266, 1.55)}
<rect x="0" y="470" width="{w}" height="{h - 470}" fill="#05060F" opacity=".55"/>
{petals(w, 8, 5)}
</g>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="31" fill="none" stroke="url(#edge)" stroke-width="2"/>
<circle class="pulse" cx="56" cy="62" r="7" fill="#34D399"/>
{t(76, 70, "ONLINE", 24, "#6EE7B7", "mono", 600, spacing=4)}
{t(w / 2, 560, "HELLO, WORLD — I'M", 26, CYAN, "mono", 600, "middle", 6)}
<text x="{w / 2}" y="664" class="sans" font-size="104" font-weight="800" fill="url(#name)" text-anchor="middle">ROHIT</text>
<text x="{w / 2}" y="772" class="sans" font-size="104" font-weight="800" fill="url(#name)" text-anchor="middle" textLength="640" lengthAdjust="spacing">JAGADALE</text>
<rect x="{w / 2 - 80}" y="800" width="160" height="5" rx="2.5" fill="url(#accent)"/>
{t(w / 2, 856, "AI agents · Developer automation", 34, "#D4DAF7", "sans", 500, "middle")}
{t(w / 2, 900, "Digital twins", 34, "#D4DAF7", "sans", 500, "middle")}
{chips_row(HERO_CHIPS, 40, 936, w - 80, 22, 48, 14, center=True)[0]}
"""
    return svg(w, h, HERO_ALT, body, HERO_DEFS)


# ---------------------------------------------------------------- about

ABOUT_TITLE = "Turning complicated problems into useful software."
ABOUT_ITEMS = [
    ("agent", "AI AGENTS", "MCP servers, LLM agents and developer automation", CYAN),
    ("cloud", "CLOUD", "AWS, CI/CD, Python and modern web technologies", VIOLET),
    ("cube", "DIGITAL TWINS", "NVIDIA Omniverse and Isaac Sim simulation workflows", PINK),
    ("spark", "GENAI", "LLMs, retrieval, embeddings and practical GenAI", AMBER),
    ("petal", "OFF THE CLOCK", "Anime, games and stories where the underdog becomes overpowered", CYAN),
]
TERMINAL = [
    ("$ cat mindset.txt", DIM),
    ("→ automate the boring stuff", TEXT),
    ("→ ship useful things", TEXT),
    ("→ keep learning", TEXT),
    ("", TEXT),
    ("$ echo $MOTTO", DIM),
    ("ship code. level up. repeat.", PINK),
]
ABOUT_ALT = (
    "About Rohit: " + ABOUT_TITLE + " "
    + " ".join(f"{label}: {text}." for _, label, text, _ in ABOUT_ITEMS)
    + " Mindset: automate the boring stuff, ship useful things, keep learning."
)


def terminal(x, y, w, size, line_h):
    h = 70 + len(TERMINAL) * line_h + 10
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#060818" stroke="#2A3366"/>',
        f'<path d="M{x} {y + 46}h{w}" stroke="#2A3366"/>',
    ]
    for i, c in enumerate(("#FB7185", AMBER, "#34D399")):
        parts.append(f'<circle cx="{x + 26 + i * 22}" cy="{y + 23}" r="6.5" fill="{c}"/>')
    parts.append(t(x + w - 22, y + 28, "rohit@github: ~", size * 0.78, DIM, "mono", 500, "end"))
    for i, (line, color) in enumerate(TERMINAL):
        if line:
            parts.append(t(x + 26, y + 84 + i * line_h, line, size, color, "mono", 500))
    last_w = text_width(TERMINAL[-1][0], size, mono=True)
    yl = y + 84 + (len(TERMINAL) - 1) * line_h
    parts.append(f'<rect class="cursor" x="{x + 32 + last_w:.0f}" y="{yl - size * 0.85:.0f}" width="{size * 0.55:.0f}" height="{size * 1.05:.0f}" fill="{PINK}"/>')
    return "\n".join(parts), h


def about_rows(x, y, width, label_size, text_size, tile, gap):
    parts, cy = [], y
    for kind, label, text, color in ABOUT_ITEMS:
        lines = wrap(text, text_size, width - tile - 24)
        parts.append(icon_tile(kind, x, cy, tile, color))
        parts.append(t(x + tile + 22, cy + label_size + 2, label, label_size, color, "mono", 700, spacing=3))
        for j, line in enumerate(lines):
            parts.append(t(x + tile + 22, cy + label_size + 10 + text_size * 1.05 + j * text_size * 1.3, line, text_size, "#D4DAF7"))
        row_h = max(tile, label_size + 14 + len(lines) * text_size * 1.3)
        cy += row_h + gap
    return "\n".join(parts), cy - gap - y


def about_desktop():
    w = 1200
    rows, rows_h = about_rows(56, 160, 640, 14, 21, 52, 22)
    term, term_h = terminal(752, 160, 392, 18, 32)
    h = int(160 + max(rows_h, term_h) + 52)
    body = card_frame(w, h, "01", "WHOAMI", ABOUT_TITLE, 32) + rows + term
    return svg(w, h, ABOUT_ALT, body)


def about_mobile():
    w = 800
    title = wrap(ABOUT_TITLE, 44, w - 96, bold=True)
    top = 72 + 44 + 16 + (len(title) - 1) * 54 + 48
    rows, rows_h = about_rows(48, top, w - 96, 20, 30, 72, 30)
    term, term_h = terminal(48, top + rows_h + 44, w - 96, 26, 44)
    h = int(top + rows_h + 44 + term_h + 48)
    frame = card_frame(w, h, "01", "WHOAMI", title[0], 44, pad=48, label_size=22)
    extra = "".join(t(48, 72 + 44 + 16 + i * 54, line, 44, TEXT, "sans", 700) for i, line in enumerate(title[1:], 1))
    return svg(w, h, ABOUT_ALT, frame + extra + rows + term)


# ---------------------------------------------------------------- missions

MISSIONS = [
    ("agent", "AI & Developer Automation", "MCP SERVERS · LLM AGENTS · CI/CD",
     "Python MCP servers for issue workflows, pipeline automation that drafts fixes and merge requests, and AI-assisted codebase exploration.",
     ["Python", "MCP", "GitLab CI/CD", "LLMs"], CYAN),
    ("cube", "Virtual Lab & Digital Twin", "NVIDIA OMNIVERSE · ISAAC SIM",
     "Cloud-hosted virtual lab for elevator and robotics digital-twin workflows: Nucleus collaboration, USD scenes and robot simulation.",
     ["Omniverse", "Isaac Sim", "USD", "AWS"], VIOLET),
    ("station", "Station Twin", "DIGITAL TWIN PLATFORM",
     "Building digital-twin experiences that connect real-world systems with their virtual representations.",
     ["Digital Twins", "Cloud", "3D Workflows"], PINK),
    ("bolt", "Hackathons & Experiments", "DATA · AI · RAPID PROTOTYPING",
     "Service-conversation mining, multilingual text, topic discovery and practical AI workflows.",
     ["Databricks", "Python", "GenAI"], AMBER),
]
MISSIONS_ALT = "What I build: " + " ".join(f"{m[1]} ({m[2]}): {m[3]}" for m in MISSIONS)


def mission_tile(x, y, w, m, s):
    """s: scale dict with font sizes."""
    kind, title, sub, desc, tags, color = m
    pad = s["pad"]
    lines = wrap(desc, s["desc"], w - pad * 2)
    tags_svg, tags_h = chips_row(tags, x + pad, 0, w - pad * 2, s["chip"], s["chip_h"], 8)
    head = s["tile"]
    desc_y = y + pad + head + s["desc"] * 1.6
    tags_y = desc_y + (len(lines) - 1) * s["desc"] * 1.4 + s["desc"] * 0.9
    h = tags_y - y + tags_h + pad
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h:.0f}" rx="20" fill="url(#tile)" stroke="{color}" stroke-opacity=".28"/>',
        f'<rect x="{x + 24}" y="{y}" width="{w * 0.35:.0f}" height="2" fill="{color}" opacity=".8"/>',
        icon_tile(kind, x + pad, y + pad, head, color),
        t(x + pad + head + 18, y + pad + head * 0.45, title, s["title"], TEXT, "sans", 700),
        t(x + pad + head + 18, y + pad + head * 0.45 + s["sub"] + 12, sub, s["sub"], color, "mono", 600, spacing=2),
    ]
    for j, line in enumerate(lines):
        parts.append(t(x + pad, desc_y + j * s["desc"] * 1.4, line, s["desc"], "#C9D0F0"))
    parts.append(f'<g transform="translate(0 {tags_y:.0f})">{tags_svg}</g>')
    return "\n".join(parts), h


def missions(w, cols, pad, gap, title_size, s):
    top = 72 + title_size + 16 + 40
    tile_w = (w - pad * 2 - gap * (cols - 1)) / cols
    tiles, y = [], top
    for r in range(0, len(MISSIONS), cols):
        row = MISSIONS[r:r + cols]
        rendered = [mission_tile(pad + c * (tile_w + gap), y, tile_w, m, s) for c, m in enumerate(row)]
        row_h = max(h for _, h in rendered)
        # Equalise tile heights within a row.
        for svg_part, h in rendered:
            tiles.append(svg_part.replace(f'height="{h:.0f}" rx="20"', f'height="{row_h:.0f}" rx="20"', 1))
        y += row_h + gap
    h = int(y - gap + pad * 0.85)
    return svg(w, h, MISSIONS_ALT, card_frame(w, h, "02", "MISSION LOG", "What I build", title_size, pad, label_size=16 if w > 1000 else 22) + "\n".join(tiles))


# ---------------------------------------------------------------- loadout

LOADOUT = [
    ("AI & LLMS", ["Python", "LLMs", "MCP", "LangChain", "Embeddings", "Retrieval"], CYAN),
    ("CLOUD & DEVOPS", ["AWS", "Docker", "GitLab CI/CD", "Linux"], VIOLET),
    ("WEB", ["TypeScript", "React", "GraphQL"], PINK),
    ("SIMULATION", ["NVIDIA Omniverse", "Isaac Sim", "USD"], AMBER),
    ("DATA", ["Databricks"], CYAN),
]
LOADOUT_ALT = "Loadout: " + "; ".join(f"{cat}: {', '.join(items)}" for cat, items, _ in LOADOUT)


def pill(x, y, label, color, size, h):
    w = text_width(label, size) + h * 0.9 + 26
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="url(#tile)" stroke="{color}" stroke-opacity=".4"/>'
        f'<circle cx="{x + h * 0.55:.1f}" cy="{y + h / 2:.1f}" r="{h * 0.14:.1f}" fill="{color}"/>'
        + t(x + h * 0.55 + h * 0.35, y + h / 2 + size * 0.36, label, size, TEXT, "sans", 600)
    ), w


def loadout(w, pad, title_size, stacked, label_size, size, h_pill, gap_row):
    y = 72 + title_size + 16 + 40
    parts = []
    label_w = 0 if stacked else 230
    for cat, items, color in LOADOUT:
        if stacked:
            parts.append(t(pad, y + label_size, cat, label_size, color, "mono", 700, spacing=3))
            y += label_size + 16
        else:
            parts.append(t(pad, y + h_pill / 2 + label_size * 0.36, cat, label_size, color, "mono", 700, spacing=3))
        x, row_y = pad + label_w, y
        for label in items:
            _, pw = pill(0, 0, label, color, size, h_pill)
            if x + pw > w - pad:
                x, row_y = pad + label_w, row_y + h_pill + 12
            s, pw = pill(x, row_y, label, color, size, h_pill)
            parts.append(s)
            x += pw + 12
        y = row_y + h_pill + gap_row
        if not stacked:
            parts.append(f'<path d="M{pad} {y - gap_row / 2:.0f}h{w - pad * 2}" stroke="#FFFFFF" stroke-opacity=".05"/>')
    h = int(y - gap_row + pad * 0.85)
    return svg(w, h, LOADOUT_ALT, card_frame(w, h, "03", "LOADOUT", "Tools of the trade", title_size, pad, label_size=16 if w > 1000 else 22) + "\n".join(parts))


# ---------------------------------------------------------------- snake header & footer

SNAKE_ALT = "04 // Contribution trail — public contributions, eaten by a snake."


def snake_header(w, pad, title_size, sub_size):
    h = 72 + title_size + 16 + sub_size + 46
    body = card_frame(w, h, "04", "CONTRIBUTION TRAIL", "Every commit feeds the snake", title_size, pad, beam=False, label_size=16 if w > 1000 else 22)
    body += t(pad, 72 + title_size + 16 + sub_size + 18, "Public contributions · refreshed daily", sub_size, MUTED, "sans", 500)
    return svg(w, int(h), SNAKE_ALT, body)


QUOTE = "Dreams don't run away — it's we who run away from them."
FOOTER_ALT = QUOTE + " github.com/rohit-j-dev — ship code, level up, repeat."


def footer(w, h, quote_size, meta_size, meta):
    lines = wrap(QUOTE, quote_size, w - 120)
    waves = []
    for i, (color, op, amp, base, cls) in enumerate(
        ((CYAN, 0.18, 18, h - 70, "wave"), (VIOLET, 0.22, 24, h - 50, "wave b"), (PINK, 0.16, 14, h - 30, "wave"))
    ):
        d = f"M0 {base}"
        for k in range(0, int(w / 150) + 6):
            d += f" q75 {-amp if k % 2 == 0 else amp} 150 0"
        d += f" V{h} H0Z"
        waves.append(f'<path class="{cls}" d="{d}" fill="{color}" opacity="{op}"/>')
    start = h * 0.4 - (len(lines) - 1) * quote_size * 0.65
    quote = "".join(
        t(w / 2, start + i * quote_size * 1.3, line, quote_size, TEXT, "sans", 500, "middle", extra=' font-style="italic"')
        for i, line in enumerate(lines)
    )
    meta_y = start + (len(lines) - 1) * quote_size * 1.3 + meta_size + 30
    body = f"""
<clipPath id="clip"><rect width="{w}" height="{h}" rx="28"/></clipPath>
<g clip-path="url(#clip)">
<rect width="{w}" height="{h}" fill="url(#card)"/>
<ellipse cx="{w / 2}" cy="{h}" rx="{w * 0.45}" ry="{h * 0.7}" fill="url(#glowViolet)" opacity=".7"/>
{stars(w, h, 40, 21, 0.5)}
{''.join(waves)}
</g>
<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="27.5" fill="none" stroke="url(#edge)" stroke-width="1.5"/>
{quote}
{t(w / 2, meta_y, meta, meta_size, CYAN, "mono", 600, "middle", 2)}
"""
    return svg(w, h, FOOTER_ALT, body)


# ---------------------------------------------------------------- build

DESKTOP_MISSION = dict(pad=30, tile=54, title=25, sub=14, desc=19, chip=13, chip_h=30)
MOBILE_MISSION = dict(pad=36, tile=72, title=34, sub=20, desc=28, chip=21, chip_h=46)

ASSETS = {
    "hero.svg": hero_desktop,
    "hero-mobile.svg": hero_mobile,
    "about.svg": about_desktop,
    "about-mobile.svg": about_mobile,
    "missions.svg": lambda: missions(1200, 2, 56, 24, 34, DESKTOP_MISSION),
    "missions-mobile.svg": lambda: missions(800, 1, 48, 28, 46, MOBILE_MISSION),
    "loadout.svg": lambda: loadout(1200, 56, 34, False, 15, 18, 42, 22),
    "loadout-mobile.svg": lambda: loadout(800, 48, 46, True, 21, 27, 60, 34),
    "snake-header.svg": lambda: snake_header(1200, 56, 34, 19),
    "snake-header-mobile.svg": lambda: snake_header(800, 48, 46, 28),
    "footer.svg": lambda: footer(1200, 240, 28, 16, "github.com/rohit-j-dev  ·  ship code · level up · repeat"),
    "footer-mobile.svg": lambda: footer(800, 340, 38, 24, "ship code · level up · repeat"),
}


RAW = "https://raw.githubusercontent.com/rohit-j-dev/rohit-j-dev"


def responsive(name, alt):
    return (
        f'<picture>\n  <source media="(max-width: 700px)" srcset="{RAW}/main/assets/ui/{name}-mobile.svg">\n'
        f'  <img src="assets/ui/{name}.svg" width="100%" alt="{escape(alt)}">\n</picture>'
    )


def readme():
    snake = (
        f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{RAW}/output/github-snake-dark.svg">\n'
        f'  <img src="{RAW}/output/github-snake.svg" width="100%" alt="Contribution snake eating the public contribution grid">\n</picture>'
    )
    parts = [
        "<!-- Generated by tools/build_profile_ui.py; edit that script, then re-run it. -->",
        '<div align="center">',
        responsive("hero", HERO_ALT),
        responsive("about", ABOUT_ALT),
        responsive("missions", MISSIONS_ALT),
        responsive("loadout", LOADOUT_ALT),
        responsive("snake-header", SNAKE_ALT),
        snake,
        responsive("footer", FOOTER_ALT),
        "</div>",
    ]
    return "\n\n".join(parts) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in ASSETS.items():
        (OUT / name).write_text(build(), encoding="utf-8", newline="\n")
        print("wrote", (OUT / name).relative_to(OUT.parent.parent))
    (OUT.parent.parent / "README.md").write_text(readme(), encoding="utf-8", newline="\n")
    print("wrote README.md")


if __name__ == "__main__":
    main()
