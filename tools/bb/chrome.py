"""Board chrome — background, power rails, holes, labels, row connections."""

from bb.board import Board
from bb.constants import (
    BOARD_FILL,
    BOARD_STROKE,
    CENTER_CHANNEL,
    FONT,
    FONT_MONO,
    HOLE_COLOR,
    HOLE_OCCUPIED_COLOR,
    HOLE_PITCH,
    HOLE_RADIUS,
    LABEL_COLOR,
    RAIL_BLUE,
    RAIL_RED,
)
from bb.geometry import _extract_row
from bb.svg import _circle, _line, _rect, _text


def render_background(board: Board) -> list[str]:
    bw = board.board_right - board.board_left
    bh = board.board_bottom - board.board_top
    els = []

    # Shadow
    els.append(_rect(board.board_left + 2, board.board_top + 2, bw, bh,
                     rx="8", fill="#00000015"))
    # Body
    els.append(_rect(board.board_left, board.board_top, bw, bh,
                     rx="8", fill=BOARD_FILL, stroke=BOARD_STROKE, stroke_width="1.2"))
    # Center channel
    cx1 = board._col_x["e"] + HOLE_PITCH * 0.5
    cx2 = board._col_x["f"] - HOLE_PITCH * 0.5
    els.append(_rect(cx1, board.board_top + 4, cx2 - cx1, bh - 8,
                     rx="2", fill=CENTER_CHANNEL, stroke="#c4b898", stroke_width="0.4"))

    return els


def render_power_rails(board: Board) -> list[str]:
    els = []
    y_top = board.board_top + 4
    y_bot = board.board_bottom - 4
    for col, c in [("+L", RAIL_RED), ("-L", RAIL_BLUE),
                   ("+R", RAIL_RED), ("-R", RAIL_BLUE)]:
        x = board._col_x[col]
        els.append(_line(x, y_top, x, y_bot,
                         stroke=c, stroke_width="1.2", opacity="0.2",
                         stroke_dasharray="3,5"))
    return els


def render_holes(board: Board) -> list[str]:
    els = []
    for col in "abcdefghij":
        for row in range(board.row_lo, board.row_hi + 1):
            x = board._col_x[col]
            y = board._terminal_row_y(row)
            hid = f"{col}{row}"
            fill = HOLE_OCCUPIED_COLOR if board.is_occupied(hid) else HOLE_COLOR
            els.append(_circle(x, y, HOLE_RADIUS, fill=fill))

    for col in ("+L", "-L", "+R", "-R"):
        for r in board._power_rows_in_view():
            x = board._col_x[col]
            y = board._power_row_y(r)
            els.append(_circle(x, y, HOLE_RADIUS - 0.5, fill=HOLE_COLOR))

    return els


def render_labels(board: Board) -> list[str]:
    els = []

    # Column letters
    for col in "abcdefghij":
        x = board._col_x[col]
        els.append(_text(x, board.board_top - 4, col,
                         font_size="9", fill=LABEL_COLOR,
                         text_anchor="middle", font_family=FONT_MONO))

    # Rail symbols
    for col, sym in [("+L", "+"), ("-L", "\u2013"), ("+R", "+"), ("-R", "\u2013")]:
        x = board._col_x[col]
        c = RAIL_RED if "+" in col else RAIL_BLUE
        els.append(_text(x, board.board_top - 4, sym,
                         font_size="10", fill=c, font_weight="bold",
                         text_anchor="middle", font_family=FONT))

    # Row numbers — every row in the visible range
    for row in range(board.row_lo, board.row_hi + 1):
        y = board._terminal_row_y(row) + 3.5
        # Only label every row if few visible, or every 5th + endpoints
        if board.visible_rows <= 25 or row == board.row_lo or row == board.row_hi or row % 5 == 0:
            lx = (board._col_x["-L"] + board._col_x["a"]) / 2
            els.append(_text(lx, y, str(row),
                             font_size="8", fill=LABEL_COLOR,
                             text_anchor="middle", font_family=FONT_MONO))
            rx = (board._col_x["j"] + board._col_x["+R"]) / 2
            els.append(_text(rx, y, str(row),
                             font_size="8", fill=LABEL_COLOR,
                             text_anchor="middle", font_family=FONT_MONO))

    return els


def render_row_connections(board: Board) -> list[str]:
    """Draw subtle highlight bars behind rows that have occupied holes,
    showing which holes are electrically connected."""
    els = []
    occupied_rows = set()
    for hid in board.occupied:
        r = _extract_row(hid)
        if r:
            occupied_rows.add(r)

    for row in sorted(occupied_rows):
        if row < board.row_lo or row > board.row_hi:
            continue
        y = board._terminal_row_y(row)
        # Left bank (a-e)
        x_start = board._col_x["a"] - 5
        x_end = board._col_x["e"] + 5
        els.append(_rect(x_start, y - 5, x_end - x_start, 10,
                         rx="3", fill="#ffeaa7", opacity="0.25"))
        # Right bank (f-j)
        x_start = board._col_x["f"] - 5
        x_end = board._col_x["j"] + 5
        els.append(_rect(x_start, y - 5, x_end - x_start, 10,
                         rx="3", fill="#ffeaa7", opacity="0.25"))

    return els
