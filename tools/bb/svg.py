"""SVG primitive helpers and resistor band computation."""

from xml.sax.saxutils import escape

from bb.constants import BAND_DIGIT, BAND_MULTIPLIER, BAND_TOLERANCE_GOLD


def _attr(**kw) -> str:
    return " ".join(
        f'{k.replace("_", "-")}="{escape(str(v))}"'
        for k, v in kw.items() if v is not None
    )


def _circle(cx, cy, r, **kw) -> str:
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" {_attr(**kw)}/>'


def _rect(x, y, w, h, **kw) -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" {_attr(**kw)}/>'


def _line(x1, y1, x2, y2, **kw) -> str:
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" {_attr(**kw)}/>'


def _text(x, y, content, **kw) -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" {_attr(**kw)}>{escape(str(content))}</text>'


def resistor_bands(ohms: int) -> list[str]:
    if ohms <= 0:
        return ["#000"] * 4
    sig, mult = ohms, 1
    while sig >= 100:
        sig //= 10
        mult *= 10
    return [
        BAND_DIGIT.get(sig // 10, "#000"),
        BAND_DIGIT.get(sig % 10, "#000"),
        BAND_MULTIPLIER.get(mult, "#000"),
        BAND_TOLERANCE_GOLD,
    ]
