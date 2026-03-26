"""Board class — maps breadboard hole addresses to pixel coordinates."""

from bb.constants import (
    BOARD_PAD_X,
    BOARD_PAD_Y,
    CENTER_GAP,
    HOLE_PITCH,
    MARGIN_BOTTOM,
    MARGIN_LEFT,
    MARGIN_RIGHT,
    MARGIN_TOP,
    POWER_GAP,
    POWER_RAIL_ROWS,
    RAIL_GAP,
    TERMINAL_ROWS,
)


class Board:
    """Maps breadboard hole addresses to pixel coordinates.

    Supports rendering a subset of rows (row_lo to row_hi) for focused diagrams.
    """

    def __init__(self, row_lo: int = 1, row_hi: int = TERMINAL_ROWS,
                 margin_left: float = MARGIN_LEFT,
                 margin_right: float = MARGIN_RIGHT):
        self.row_lo = row_lo
        self.row_hi = row_hi
        self.visible_rows = row_hi - row_lo + 1
        self.margin_left = margin_left
        self.margin_right = margin_right
        self._col_x: dict[str, float] = {}
        self._setup_columns()
        self.occupied: set[str] = set()
        self.specs: dict = {}  # populated by generate() from component-specs.yaml

    def _setup_columns(self):
        x = self.margin_left
        self._col_x["+L"] = x
        x += RAIL_GAP
        self._col_x["-L"] = x
        x += POWER_GAP
        for col in "abcde":
            self._col_x[col] = x
            x += HOLE_PITCH
        x = self._col_x["e"] + CENTER_GAP
        for col in "fghij":
            self._col_x[col] = x
            x += HOLE_PITCH
        x = self._col_x["j"] + POWER_GAP
        self._col_x["+R"] = x
        x += RAIL_GAP
        self._col_x["-R"] = x

    def hole_xy(self, hole_id: str) -> tuple[float, float]:
        hole_id = hole_id.strip()

        if hole_id[0] in "+-":
            sign = hole_id[0]
            rest = hole_id[1:]
            if rest and rest[0] in "LR":
                side, idx = rest[0], int(rest[1:])
            else:
                side, idx = "L", int(rest)
            # idx is 1-based into POWER_RAIL_ROWS
            if idx < 1 or idx > len(POWER_RAIL_ROWS):
                raise ValueError(f"Power rail index {idx} out of range 1–{len(POWER_RAIL_ROWS)}")
            terminal_row = POWER_RAIL_ROWS[idx - 1]
            return self._col_x[f"{sign}{side}"], self._power_row_y(terminal_row)

        col = hole_id[0].lower()
        row = int(hole_id[1:])
        return self._col_x[col], self._terminal_row_y(row)

    def _terminal_row_y(self, row: int) -> float:
        return MARGIN_TOP + (row - self.row_lo) * HOLE_PITCH

    def _power_row_y(self, terminal_row: int) -> float:
        """Power rail holes sit at the same y as their aligned terminal row."""
        return self._terminal_row_y(terminal_row)

    def _power_rows_in_view(self) -> list[int]:
        """Return the terminal row numbers of power rail holes within the visible range."""
        return [r for r in POWER_RAIL_ROWS if self.row_lo <= r <= self.row_hi]

    @property
    def board_left(self) -> float:
        return self._col_x["+L"] - BOARD_PAD_X

    @property
    def board_right(self) -> float:
        return self._col_x["-R"] + BOARD_PAD_X

    @property
    def board_top(self) -> float:
        return MARGIN_TOP - BOARD_PAD_Y

    @property
    def board_bottom(self) -> float:
        return MARGIN_TOP + (self.visible_rows - 1) * HOLE_PITCH + BOARD_PAD_Y

    @property
    def svg_width(self) -> float:
        return self.board_right + self.margin_right

    @property
    def svg_height(self) -> float:
        return self.board_bottom + MARGIN_BOTTOM

    def mark_occupied(self, *holes: str):
        for h in holes:
            self.occupied.add(h.strip().lower())

    def is_occupied(self, hole_id: str) -> bool:
        return hole_id.strip().lower() in self.occupied
