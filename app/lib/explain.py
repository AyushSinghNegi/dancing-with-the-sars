"""A small drawing of how L-band radar sees water, rough ground, double bounce and coherence."""
from __future__ import annotations

from . import ui

INK, MUTED, WATER, SLIDE, GROUND = ui.INK, ui.MUTED, "#2a78d6", "#eb6834", "#b9a98e"


def _arrow(x1, y1, x2, y2, color=INK, w=2.5, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"{d} '
            f'marker-end="url(#ah-{color.strip("#")})"/>')


def _sat(x, y):
    return (f'<g transform="translate({x},{y})"><rect x="-9" y="-6" width="18" height="12" rx="2" fill="{INK}"/>'
            f'<rect x="-27" y="-4" width="15" height="8" fill="{MUTED}"/><rect x="12" y="-4" width="15" height="8" '
            f'fill="{MUTED}"/></g>')


def svg() -> str:
    tr = ui.tr
    panels = [
        (tr("Calm water looks dark", "शांत पाणी गडद दिसते"),
         tr("A smooth surface reflects the radar away, like a mirror.", "गुळगुळीत पृष्ठभाग रडार आरशासारखा दूर परावर्तित करतो.")),
        (tr("Rough ground looks bright", "खडबडीत जमीन उजळ दिसते"),
         tr("Trees, rock and debris scatter some radar back.", "झाडे, खडक आणि ढिगारा काही रडार परत पाठवतात.")),
        (tr("Water by walls: very bright", "भिंतींजवळचे पाणी: खूप उजळ"),
         tr("Water and a wall or trunk bounce it straight back.", "पाणी आणि भिंत किंवा खोड ते थेट परत पाठवतात.")),
        (tr("Coherence: did it stay put?", "कोहेरन्स: जमीन तशीच राहिली का?"),
         tr("Two passes 12 days apart: a slide scrambles the pattern.", "१२ दिवसांच्या अंतराने दोन निरीक्षणे: भूस्खलन नमुना बिघडवते.")),
    ]
    W, H, PW = 1000, 250, 250
    parts = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="'
             + tr("How NISAR's L-band radar sees water, rough ground, double bounce and coherence",
                  "निसारचे एल-बँड रडार पाणी, खडबडीत जमीन, दुहेरी परावर्तन आणि कोहेरन्स कसे पाहते") + '" '
             'style="max-width:1000px;font-family:IBM Plex Sans, sans-serif">',
             "<defs>" + "".join(
                 f'<marker id="ah-{c.strip("#")}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" '
                 f'markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
                 for c in (INK, WATER, SLIDE, MUTED)) + "</defs>"]
    for k, (title, sub) in enumerate(panels):
        x0 = k * PW
        if k:
            parts.append(f'<line x1="{x0}" y1="18" x2="{x0}" y2="{H - 18}" stroke="#d9dedd"/>')
        parts.append(_sat(x0 + 200, 34))
        gy = 150
        if k == 0:
            parts.append(f'<rect x="{x0 + 20}" y="{gy}" width="210" height="16" rx="3" fill="{WATER}" opacity=".85"/>')
            parts.append(_arrow(x0 + 188, 46, x0 + 120, gy - 4))
            parts.append(_arrow(x0 + 120, gy - 4, x0 + 50, 60, MUTED, 2, "5 4"))
        elif k == 1:
            pts = " ".join(f"{x0 + 20 + i * 15},{gy + (8 if i % 2 else -2) + (i % 3) * 3}" for i in range(15))
            parts.append(f'<polyline points="{pts}" fill="none" stroke="{GROUND}" stroke-width="10" '
                         'stroke-linejoin="round"/>')
            parts.append(_arrow(x0 + 188, 46, x0 + 125, gy - 8))
            for dx, dy in ((-60, -50), (-20, -70), (65, -82), (30, -40)):
                parts.append(_arrow(x0 + 125, gy - 8, x0 + 125 + dx, gy - 8 + dy, INK, 1.8))
        elif k == 2:
            parts.append(f'<rect x="{x0 + 20}" y="{gy}" width="210" height="16" rx="3" fill="{WATER}" opacity=".85"/>')
            parts.append(f'<rect x="{x0 + 70}" y="{gy - 70}" width="22" height="72" fill="#8c979e"/>')
            parts.append(_arrow(x0 + 188, 46, x0 + 130, gy - 4))
            parts.append(_arrow(x0 + 130, gy - 4, x0 + 95, gy - 30))
            parts.append(_arrow(x0 + 95, gy - 30, x0 + 182, 50, INK, 3.5))
        else:
            for row, (yy, lab, scr) in enumerate(((gy - 52, "28 Jun", False), (gy + 6, "10 Jul", True))):
                parts.append(f'<text x="{x0 + 22}" y="{yy + 12}" font-size="12" fill="{MUTED}">{lab}</text>')
                for i in range(8):
                    jit = ((i * 37) % 11 - 5) if (scr and 3 <= i <= 6) else 0
                    h = 6 + ((i * 7) % 9)
                    col = SLIDE if scr and 3 <= i <= 6 else GROUND
                    parts.append(f'<rect x="{x0 + 75 + i * 19}" y="{yy + 14 - h + jit}" width="13" height="{h}" '
                                 f'fill="{col}" rx="2"/>')
        parts.append(f'<text x="{x0 + 18}" y="{H - 58}" font-size="16" font-weight="600" fill="{INK}">{title}</text>')
        words, lines, cur = sub.split(), [], ""
        for w in words:
            if len(cur) + len(w) + 1 > 31:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        for j, ln in enumerate(lines[:3]):
            parts.append(f'<text x="{x0 + 18}" y="{H - 38 + j * 16}" font-size="13.5" fill="{MUTED}">{ln}</text>')
    parts.append("</svg>")
    return "".join(parts)
