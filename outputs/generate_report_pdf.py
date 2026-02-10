#!/usr/bin/env python3
"""
generate_report_pdf.py

Reads outputs/05_manager_report.md and produces a professionally formatted PDF
at outputs/05_manager_report.pdf using fpdf2.

Run from the outputs directory:
    python generate_report_pdf.py
"""

import os
import re
import sys
from fpdf import FPDF
from fpdf.enums import XPos, YPos


# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------
DARK_BLUE = (26, 54, 93)       # #1a365d  -- headings, title page
ACCENT_BLUE = (44, 82, 130)    # #2c5282  -- table headers
LIGHT_GREY = (245, 247, 250)   # #f5f7fa  -- alternating table rows
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MEDIUM_GREY = (100, 100, 100)
RULE_GREY = (200, 200, 210)
BODY_TEXT = (30, 30, 30)


# ---------------------------------------------------------------------------
# Text sanitiser -- replace Unicode chars that Helvetica (latin-1) cannot
# render with safe ASCII/latin-1 equivalents.
# ---------------------------------------------------------------------------
_UNICODE_MAP = {
    "\u2019": "'",   # right single quote
    "\u2018": "'",   # left single quote
    "\u201c": '"',   # left double quote
    "\u201d": '"',   # right double quote
    "\u2014": " -- ",  # em dash
    "\u2013": " - ",   # en dash
    "\u2026": "...",   # ellipsis
    "\u2022": "-",     # bullet
    "\u2611": "[x]",   # checked checkbox
    "\u2610": "[ ]",   # unchecked checkbox
    "\u2192": "->",    # right arrow
    "\u00a0": " ",     # non-breaking space
}


def _sanitize(text: str) -> str:
    """Replace problematic Unicode characters with latin-1 safe alternatives."""
    for uchar, replacement in _UNICODE_MAP.items():
        text = text.replace(uchar, replacement)
    # Fallback: replace anything still outside latin-1
    try:
        text.encode("latin-1")
    except UnicodeEncodeError:
        cleaned = []
        for ch in text:
            try:
                ch.encode("latin-1")
                cleaned.append(ch)
            except UnicodeEncodeError:
                cleaned.append("?")
        text = "".join(cleaned)
    return text


# ---------------------------------------------------------------------------
# Custom PDF class
# ---------------------------------------------------------------------------
class ReportPDF(FPDF):
    """A4 PDF with header stripe and page-numbered footer."""

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=25)
        self._is_title_page = False

    # -- footer with page number -------------------------------------------
    def footer(self):
        if self._is_title_page:
            return
        self.set_y(-18)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*MEDIUM_GREY)
        self.cell(
            0, 10,
            _sanitize(f"NovaStar Hotels -- Final Manager's Report    |    Page {self.page_no()}/{{nb}}"),
            new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C",
        )

    # -- header accent line -------------------------------------------------
    def header(self):
        if self._is_title_page:
            return
        self.set_fill_color(*DARK_BLUE)
        self.rect(10, 8, self.w - 20, 1.2, "F")

    # -- title page ---------------------------------------------------------
    def add_title_page(self):
        self._is_title_page = True
        self.add_page()

        # Background bar
        self.set_fill_color(*DARK_BLUE)
        self.rect(0, 0, self.w, 110, "F")

        # Title text
        self.set_y(32)
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(*WHITE)
        self.cell(0, 14, "NovaStar Hotels",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.set_font("Helvetica", "", 16)
        self.cell(0, 10, "Final Manager's Report",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

        self.ln(8)
        self.set_draw_color(*WHITE)
        self.set_line_width(0.4)
        self.line(60, self.get_y(), self.w - 60, self.get_y())
        self.ln(8)

        self.set_font("Helvetica", "B", 14)
        self.cell(0, 9, "Team AWESOME",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.set_font("Helvetica", "", 11)
        self.cell(0, 7, "Project Review & Consolidated Assessment",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

        # Meta block below the blue area
        self.set_y(125)
        self.set_text_color(*DARK_BLUE)
        meta_lines = [
            ("Prepared by:", "Morgan the Manager (Agent 05, Team AWESOME)"),
            ("Date:", "10 February 2026"),
            ("Classification:", "Internal -- Strategic"),
            ("Version:", "1.0"),
        ]
        for label, value in meta_lines:
            self.set_x(45)
            self.set_font("Helvetica", "B", 11)
            self.cell(35, 8, label)
            self.set_font("Helvetica", "", 11)
            self.cell(0, 8, value,
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self._is_title_page = False


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_ITALIC_RE = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")
_CHECKBOX_CHECKED = re.compile(r"^\s*-\s*\[x\]\s*", re.IGNORECASE)
_CHECKBOX_UNCHECKED = re.compile(r"^\s*-\s*\[\s*\]\s*")
_BULLET_RE = re.compile(r"^\s*[-*]\s+")
_NUMBERED_RE = re.compile(r"^\s*(\d+)\.\s+")
_TABLE_SEP = re.compile(r"^\|[\s\-:|]+\|$")


def _is_table_line(line: str) -> bool:
    return line.strip().startswith("|") and line.strip().endswith("|")


def _parse_table_row(line: str) -> list[str]:
    """Return cell contents for a table row."""
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def _write_rich_text(pdf: FPDF, text: str, default_style: str = "",
                     default_size: float = 10.5, line_height: float = 5.5):
    """Write *text* handling **bold** and *italic* spans via pdf.write()."""
    text = _sanitize(text)

    # Tokenise into segments: (style_flag, content)
    tokens: list[tuple[str, str]] = []
    pos = 0
    combined = re.compile(r"(\*\*(.+?)\*\*|\*(.+?)\*)")
    for m in combined.finditer(text):
        if m.start() > pos:
            tokens.append((default_style, text[pos:m.start()]))
        if m.group(2) is not None:
            tokens.append(("B", m.group(2)))
        elif m.group(3) is not None:
            tokens.append(("I", m.group(3)))
        pos = m.end()
    if pos < len(text):
        tokens.append((default_style, text[pos:]))

    for style, content in tokens:
        pdf.set_font("Helvetica", style, default_size)
        pdf.write(line_height, content)


# ---------------------------------------------------------------------------
# Table renderer
# ---------------------------------------------------------------------------
def _calc_cell_height(pdf: FPDF, text: str, col_w: float,
                      font_style: str, font_size: float,
                      line_h: float) -> float:
    """Return the height needed to render *text* inside a cell of *col_w* mm."""
    pdf.set_font("Helvetica", font_style, font_size)
    # Subtract a small padding from width for the leading space
    effective_w = col_w - 2
    if effective_w <= 0:
        effective_w = col_w
    text = _sanitize(text)
    # Use get_string_width to estimate number of lines
    words = text.split(" ")
    lines = 1
    current_line = ""
    for word in words:
        test = current_line + (" " if current_line else "") + word
        if pdf.get_string_width(test) > effective_w and current_line:
            lines += 1
            current_line = word
        else:
            current_line = test
    return max(lines * line_h, line_h)


def _render_table(pdf: ReportPDF, header_cells: list[str],
                  data_rows: list[list[str]]):
    """Draw a table that fits within the printable width, with word-wrapping."""
    usable_w = pdf.w - pdf.l_margin - pdf.r_margin
    n_cols = len(header_cells)
    line_h = 5.0  # line height inside cells
    min_row_h = 7.5  # minimum row height

    # -- Determine column widths -------------------------------------------
    # For tables with many columns (>4) and long content, use a smarter
    # allocation that gives more space to text-heavy columns.
    col_max_chars = []
    for i in range(n_cols):
        max_len = len(header_cells[i])
        for row in data_rows:
            if i < len(row):
                max_len = max(max_len, len(row[i]))
        col_max_chars.append(max(max_len, 3))

    total_chars = sum(col_max_chars)
    col_widths = [(c / total_chars) * usable_w for c in col_max_chars]

    # Enforce a minimum column width of 12mm so short columns stay readable
    MIN_COL_W = 12.0
    for i in range(n_cols):
        if col_widths[i] < MIN_COL_W:
            col_widths[i] = MIN_COL_W
    # Re-normalise so columns still sum to usable_w
    cw_total = sum(col_widths)
    col_widths = [(w / cw_total) * usable_w for w in col_widths]

    # Ensure space for at least header + 2 rows; otherwise new page
    needed = min_row_h * (min(len(data_rows), 3) + 1) + 4
    if pdf.get_y() + needed > pdf.h - 30:
        pdf.add_page()

    # -- Helper to draw one row (header or data) ---------------------------
    def _draw_row(cells: list[str], is_header: bool, fill_color: tuple):
        font_size = 9.5 if is_header else 9

        # First pass: compute the maximum cell height for this row
        row_h = min_row_h
        cell_styles: list[tuple[str, str]] = []  # (style, clean_text)
        for i in range(n_cols):
            raw = cells[i] if i < len(cells) else ""
            clean = _BOLD_RE.sub(r"\1", raw)
            is_bold = is_header or _BOLD_RE.search(raw) is not None
            style = "B" if is_bold else ""
            cell_styles.append((style, clean))
            h = _calc_cell_height(pdf, clean, col_widths[i],
                                  style, font_size, line_h)
            row_h = max(row_h, h)

        # Page break if this row won't fit
        if pdf.get_y() + row_h > pdf.h - 25:
            pdf.add_page()

        y_start = pdf.get_y()
        x_start = pdf.l_margin

        # Second pass: draw each cell
        for i, (style, clean) in enumerate(cell_styles):
            x = x_start + sum(col_widths[:i])
            pdf.set_xy(x, y_start)

            # Draw the filled rectangle + border first
            pdf.set_fill_color(*fill_color)
            if is_header:
                pdf.set_draw_color(*ACCENT_BLUE)
            else:
                pdf.set_draw_color(*RULE_GREY)
            pdf.rect(x, y_start, col_widths[i], row_h, "FD")

            # Now draw the text inside
            if is_header:
                pdf.set_text_color(*WHITE)
            else:
                pdf.set_text_color(*BODY_TEXT)
            pdf.set_font("Helvetica", style, font_size)
            pdf.set_xy(x + 1, y_start + 0.5)
            pdf.multi_cell(col_widths[i] - 2, line_h,
                           _sanitize(clean), border=0, fill=False)

        # Move cursor below the row
        pdf.set_y(y_start + row_h)

    # -- Draw header row ---------------------------------------------------
    _draw_row(header_cells, is_header=True, fill_color=ACCENT_BLUE)

    # -- Draw data rows ----------------------------------------------------
    for r_idx, row in enumerate(data_rows):
        fill = LIGHT_GREY if r_idx % 2 == 0 else WHITE
        _draw_row(row, is_header=False, fill_color=fill)

    pdf.ln(3)


# ---------------------------------------------------------------------------
# Main document builder
# ---------------------------------------------------------------------------
def build_pdf(md_path: str, out_path: str):
    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.set_title("NovaStar Hotels: Final Manager's Report")
    pdf.set_author("Morgan the Manager -- Team AWESOME")

    # -- Title page --------------------------------------------------------
    pdf.add_title_page()

    # -- Content pages -----------------------------------------------------
    pdf.add_page()

    with open(md_path, "r", encoding="utf-8") as fh:
        raw_lines = fh.readlines()

    lines = [l.rstrip("\n") for l in raw_lines]
    i = 0

    # Skip lines up to and including the first "---" (already on title page)
    first_rule = None
    for idx, l in enumerate(lines):
        if l.strip() == "---":
            first_rule = idx
            break

    if first_rule is not None:
        i = first_rule + 1
    else:
        i = 0

    # Table accumulator
    table_header: list[str] | None = None
    table_rows: list[list[str]] = []
    in_table = False

    def _flush_table():
        nonlocal table_header, table_rows, in_table
        if table_header:
            _render_table(pdf, table_header, table_rows)
        table_header = None
        table_rows = []
        in_table = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # -- Blank line -----------------------------------------------------
        if stripped == "":
            if in_table:
                _flush_table()
            pdf.ln(3)
            i += 1
            continue

        # -- Horizontal rule ------------------------------------------------
        if stripped == "---":
            if in_table:
                _flush_table()
            y = pdf.get_y() + 3
            if y > pdf.h - 25:
                pdf.add_page()
                y = pdf.get_y() + 3
            pdf.set_draw_color(*RULE_GREY)
            pdf.set_line_width(0.3)
            pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
            pdf.set_y(y + 5)
            i += 1
            continue

        # -- Table lines ----------------------------------------------------
        if _is_table_line(stripped):
            if _TABLE_SEP.match(stripped):
                i += 1
                continue  # skip separator
            cells = _parse_table_row(stripped)
            if not in_table:
                table_header = cells
                in_table = True
            else:
                table_rows.append(cells)
            i += 1
            continue
        else:
            if in_table:
                _flush_table()

        # -- H1 header (skip -- already on title page) ---------------------
        if stripped.startswith("# ") and not stripped.startswith("## "):
            i += 1
            continue

        # -- H2 header ------------------------------------------------------
        if stripped.startswith("## "):
            heading = _sanitize(stripped[3:].strip())
            if pdf.get_y() > pdf.h - 50:
                pdf.add_page()
            pdf.ln(5)
            pdf.set_font("Helvetica", "B", 16)
            pdf.set_text_color(*DARK_BLUE)
            pdf.cell(0, 10, heading,
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            # Decorative underline
            y = pdf.get_y()
            pdf.set_draw_color(*DARK_BLUE)
            pdf.set_line_width(0.5)
            pdf.line(pdf.l_margin, y, pdf.l_margin + 60, y)
            pdf.ln(4)
            i += 1
            continue

        # -- H3 header ------------------------------------------------------
        if stripped.startswith("### "):
            heading = _sanitize(stripped[4:].strip())
            if pdf.get_y() > pdf.h - 40:
                pdf.add_page()
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 13)
            pdf.set_text_color(*ACCENT_BLUE)
            pdf.cell(0, 8, heading,
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(2)
            i += 1
            continue

        # -- Checkbox bullet  - [x] ... ------------------------------------
        m_check = _CHECKBOX_CHECKED.match(stripped)
        m_uncheck = _CHECKBOX_UNCHECKED.match(stripped)
        if m_check or m_uncheck:
            marker = "[x] " if m_check else "[ ] "
            content = (stripped[m_check.end():] if m_check
                       else stripped[m_uncheck.end():])
            if pdf.get_y() > pdf.h - 20:
                pdf.add_page()
            pdf.set_text_color(*BODY_TEXT)
            pdf.set_font("Helvetica", "B", 10.5)
            x_indent = pdf.l_margin + 6
            pdf.set_x(x_indent)
            pdf.cell(9, 5.5, marker)
            _write_rich_text(pdf, content, default_size=10.5)
            pdf.ln(6)
            i += 1
            continue

        # -- Bullet point ---------------------------------------------------
        m_bullet = _BULLET_RE.match(stripped)
        if m_bullet:
            content = stripped[m_bullet.end():]
            if pdf.get_y() > pdf.h - 20:
                pdf.add_page()
            pdf.set_text_color(*BODY_TEXT)
            x_indent = pdf.l_margin + 6
            pdf.set_x(x_indent)
            pdf.set_font("Helvetica", "", 10.5)
            pdf.cell(5, 5.5, "- ")
            _write_rich_text(pdf, content, default_size=10.5)
            pdf.ln(6)
            i += 1
            continue

        # -- Numbered list --------------------------------------------------
        m_num = _NUMBERED_RE.match(stripped)
        if m_num:
            num = m_num.group(1)
            content = stripped[m_num.end():]
            if pdf.get_y() > pdf.h - 20:
                pdf.add_page()
            pdf.set_text_color(*BODY_TEXT)
            x_indent = pdf.l_margin + 6
            pdf.set_x(x_indent)
            pdf.set_font("Helvetica", "B", 10.5)
            pdf.cell(7, 5.5, f"{num}.")
            _write_rich_text(pdf, content, default_size=10.5)
            pdf.ln(6)

            # Continuation lines (indented paragraphs under the number)
            while i + 1 < len(lines):
                next_line = lines[i + 1]
                if (next_line.startswith("   ")
                        and not _NUMBERED_RE.match(next_line.strip())
                        and not _BULLET_RE.match(next_line.strip())
                        and not next_line.strip().startswith("#")
                        and not next_line.strip().startswith("|")
                        and next_line.strip() != ""
                        and next_line.strip() != "---"):
                    i += 1
                    pdf.set_x(x_indent + 7)
                    _write_rich_text(pdf, next_line.strip(), default_size=10.5)
                    pdf.ln(6)
                else:
                    break
            i += 1
            continue

        # -- Italic-only line (closing signature) ---------------------------
        if (stripped.startswith("*") and stripped.endswith("*")
                and not stripped.startswith("**")):
            content = _sanitize(stripped.strip("*").strip())
            pdf.set_font("Helvetica", "I", 10.5)
            pdf.set_text_color(*MEDIUM_GREY)
            pdf.cell(0, 6, content,
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            i += 1
            continue

        # -- Regular paragraph text -----------------------------------------
        if pdf.get_y() > pdf.h - 20:
            pdf.add_page()
        pdf.set_text_color(*BODY_TEXT)
        pdf.set_x(pdf.l_margin)
        _write_rich_text(pdf, stripped, default_size=10.5)
        pdf.ln(6)
        i += 1

    # Flush any remaining table
    if in_table:
        _flush_table()

    # -- Save ---------------------------------------------------------------
    pdf.output(out_path)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    md_path = os.path.join(script_dir, "05_manager_report.md")
    if not os.path.exists(md_path):
        md_path = os.path.join(project_root, "outputs", "05_manager_report.md")
    if not os.path.exists(md_path):
        print(f"ERROR: Cannot find 05_manager_report.md. Looked in:\n"
              f"  {os.path.join(script_dir, '05_manager_report.md')}\n"
              f"  {os.path.join(project_root, 'outputs', '05_manager_report.md')}")
        sys.exit(1)

    out_path = os.path.join(script_dir, "NovaStar_Final_Report.pdf")

    print(f"Reading markdown : {md_path}")
    print(f"Generating PDF   : {out_path}")
    build_pdf(md_path, out_path)
    print(f"\nDone. PDF saved to:\n  {out_path}")


if __name__ == "__main__":
    main()
