"""Layout constants, color palettes, and orientation presets."""

# ─── Layout Constants (pixels) ───────────────────────────────────

HOLE_RADIUS = 3.0
HOLE_PITCH = 14
CENTER_GAP = 28
POWER_GAP = 20
RAIL_GAP = 10

MARGIN_TOP = 52
MARGIN_BOTTOM = 16
MARGIN_LEFT = 80
MARGIN_RIGHT = 80

BOARD_PAD_X = 12
BOARD_PAD_Y = 12

TERMINAL_ROWS = 63

# Power rail holes are aligned to terminal rows in groups of 5, with a 1-row gap.
# 10 groups: [3-7], [9-13], [15-19], [21-25], [27-31], [33-37], [39-43], [45-49], [51-55], [57-61]
POWER_RAIL_ROWS: list[int] = [
    r + i
    for r in range(3, 62, 6)
    for i in range(5)
    if r + i <= 61
]

# Colors
BOARD_FILL = "#e8dcc8"
BOARD_STROKE = "#b8a88a"
HOLE_COLOR = "#2a2a2a"
HOLE_OCCUPIED_COLOR = "#666"
RAIL_RED = "#d32f2f"
RAIL_BLUE = "#1565c0"
CENTER_CHANNEL = "#d4c8b0"
LABEL_COLOR = "#666"
FONT = "system-ui, -apple-system, 'Segoe UI', sans-serif"
FONT_MONO = "'SF Mono', 'Cascadia Code', 'Fira Code', monospace"

# Orientation presets — maps named orientations to rotation degrees.
# The orientation describes which direction the component's natural "top"
# faces when placed on the breadboard.
#   up    → 0°    (natural top faces toward row 1)
#   right → 90°   (natural top faces toward column j)
#   down  → 180°  (natural top faces toward row 63)
#   left  → -90°  (natural top faces toward column a)
ORIENTATION_PRESETS = {
    "up": 0,
    "right": 90,
    "down": 180,
    "left": -90,
}

# Default orientation per component type. Only types that use orientation
# are listed here — most components are symmetric or position-derived.
ORIENTATION_DEFAULTS = {
    "seven_segment": "left",
}

# Resistor band colors
BAND_DIGIT = {
    0: "#000", 1: "#8B4513", 2: "#FF0000", 3: "#FF8C00",
    4: "#FFD700", 5: "#228B22", 6: "#0000FF", 7: "#8B00FF",
    8: "#808080", 9: "#FFF",
}
BAND_MULTIPLIER = {
    1: "#000", 10: "#8B4513", 100: "#FF0000",
    1000: "#FF8C00", 10000: "#FFD700", 100000: "#228B22",
    1000000: "#0000FF",
}
BAND_TOLERANCE_GOLD = "#CFB53B"

LED_PALETTE = {
    "red": ("#ff1744", "#ff8a80"),
    "green": ("#00c853", "#69f0ae"),
    "yellow": ("#ffd600", "#fff59d"),
    "blue": ("#2979ff", "#82b1ff"),
    "white": ("#f5f5f5", "#e0e0e0"),
    "orange": ("#ff6d00", "#ffab91"),
}

BUZZER_PALETTE = {
    "active": ("#333", "#555"),
    "passive": ("#555", "#777"),
}
