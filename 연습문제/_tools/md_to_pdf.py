from __future__ import annotations

import html
import re
import textwrap
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    CondPageBreak,
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.doctemplate import LayoutError


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "친절한 SQL 튜닝_전범위_25문항.md"
OUTPUT = ROOT / "친절한 SQL 튜닝_전범위_25문항.pdf"

FONT_REGULAR = Path(r"C:\Windows\Fonts\NotoSansKR-Regular.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\NotoSansKR-Bold.ttf")
FONT_MONO = Path(r"C:\Windows\Fonts\NGULIM.TTF")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("NotoSansKR", str(FONT_REGULAR)))
    pdfmetrics.registerFont(TTFont("NotoSansKR-Bold", str(FONT_BOLD)))
    pdfmetrics.registerFont(TTFont("CodeMono", str(FONT_MONO)))


def make_styles():
    base = getSampleStyleSheet()

    def style(name: str, **kwargs):
        parent = kwargs.pop("parent", base["Normal"])
        return ParagraphStyle(name, parent=parent, **kwargs)

    return {
        "title": style(
            "TitleKR",
            fontName="NotoSansKR-Bold",
            fontSize=19,
            leading=26,
            alignment=TA_CENTER,
            spaceAfter=10,
        ),
        "h1": style(
            "H1KR",
            fontName="NotoSansKR-Bold",
            fontSize=15,
            leading=22,
            textColor=colors.HexColor("#17324d"),
            spaceBefore=12,
            spaceAfter=8,
        ),
        "h2": style(
            "H2KR",
            fontName="NotoSansKR-Bold",
            fontSize=12.5,
            leading=18,
            textColor=colors.HexColor("#22313f"),
            spaceBefore=9,
            spaceAfter=6,
        ),
        "h3": style(
            "H3KR",
            fontName="NotoSansKR-Bold",
            fontSize=10.8,
            leading=16,
            textColor=colors.HexColor("#34495e"),
            spaceBefore=7,
            spaceAfter=4,
        ),
        "body": style(
            "BodyKR",
            fontName="NotoSansKR",
            fontSize=9.4,
            leading=15,
            spaceAfter=5,
        ),
        "bullet": style(
            "BulletKR",
            fontName="NotoSansKR",
            fontSize=9.2,
            leading=14,
            leftIndent=12,
            firstLineIndent=-8,
            spaceAfter=3,
        ),
        "quote": style(
            "QuoteKR",
            fontName="NotoSansKR-Bold",
            fontSize=10,
            leading=15,
            textColor=colors.HexColor("#1f4e79"),
            borderColor=colors.HexColor("#d7e5f0"),
            borderWidth=0.8,
            borderPadding=6,
            backColor=colors.HexColor("#f4f8fb"),
            spaceBefore=4,
            spaceAfter=7,
        ),
        "code": style(
            "CodeKR",
            fontName="CodeMono",
            fontSize=7.0,
            leading=9.2,
            leftIndent=0,
            rightIndent=0,
            backColor=colors.HexColor("#f6f8fa"),
            borderColor=colors.HexColor("#e1e4e8"),
            borderWidth=0.4,
            borderPadding=5,
            spaceBefore=3,
            spaceAfter=7,
        ),
        "cell": style(
            "CellKR",
            fontName="NotoSansKR",
            fontSize=8,
            leading=11,
            alignment=TA_LEFT,
        ),
        "cell_header": style(
            "CellHeaderKR",
            fontName="NotoSansKR-Bold",
            fontSize=8,
            leading=11,
            alignment=TA_CENTER,
            textColor=colors.white,
        ),
}


SQL_KEYWORDS = {
    "SELECT",
    "FROM",
    "WHERE",
    "AND",
    "OR",
    "GROUP",
    "BY",
    "ORDER",
    "CREATE",
    "INDEX",
    "ON",
    "INSERT",
    "INTO",
    "VALUES",
    "JOIN",
    "INNER",
    "LEFT",
    "RIGHT",
    "FULL",
    "OUTER",
    "UNION",
    "ALL",
    "EXISTS",
    "IN",
    "BETWEEN",
    "LIKE",
    "IS",
    "NULL",
    "NOT",
    "AS",
    "DATE",
    "WITH",
    "PARTITION",
    "RANGE",
    "HASH",
    "LIST",
    "LESS",
    "THAN",
}

SQL_FUNCTIONS = {"SUM", "MAX", "MIN", "COUNT", "TO_CHAR", "TRUNC", "NVL", "LPAD", "SUBSTR", "LENGTH"}
JAVA_KEYWORDS = {
    "String",
    "Statement",
    "ResultSet",
    "PreparedStatement",
    "for",
    "new",
    "throws",
    "Exception",
}


def md_inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<font name='NotoSansKR-Bold'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


def code_escape(text: str) -> str:
    return html.escape(text).replace(" ", "&nbsp;")


def color_token(token: str, lang: str) -> str:
    raw = token
    upper = raw.upper()

    if lang == "sql":
        if upper in SQL_KEYWORDS:
            return f"<font color='#005cc5'><b>{raw}</b></font>"
        if upper in SQL_FUNCTIONS:
            return f"<font color='#6f42c1'><b>{raw}</b></font>"
    if lang == "java":
        if raw in JAVA_KEYWORDS:
            return f"<font color='#005cc5'><b>{raw}</b></font>"
        if upper in SQL_KEYWORDS or upper in SQL_FUNCTIONS:
            return f"<font color='#005cc5'><b>{raw}</b></font>"
    if lang == "text":
        if upper in SQL_KEYWORDS or upper in {"NESTED", "LOOPS", "TABLE", "ACCESS", "INDEX", "SCAN", "STATEMENT"}:
            return f"<font color='#005cc5'><b>{raw}</b></font>"
    return code_escape(raw)


def highlight_line(line: str, lang: str) -> str:
    token_re = re.compile(
        r"(--.*$)|(/\*.*?\*/)|('[^']*')|(:[A-Za-z_][A-Za-z0-9_]*)|(\b[A-Za-z_][A-Za-z0-9_$]*\b)|(\b\d+(?:\.\d+)?\b)",
        re.UNICODE,
    )
    out: list[str] = []
    pos = 0
    for match in token_re.finditer(line):
        out.append(code_escape(line[pos : match.start()]))
        token = match.group(0)
        if match.group(1) or match.group(2):
            out.append(f"<font color='#6a737d'>{code_escape(token)}</font>")
        elif match.group(3):
            out.append(f"<font color='#032f62'>{code_escape(token)}</font>")
        elif match.group(4):
            out.append(f"<font color='#e36209'>{code_escape(token)}</font>")
        elif match.group(6):
            out.append(f"<font color='#005cc5'>{code_escape(token)}</font>")
        else:
            out.append(color_token(token, lang))
        pos = match.end()
    out.append(code_escape(line[pos:]))
    return "".join(out)


def highlighted_code_block(code: str, lang: str, styles) -> Table:
    lang = (lang or "text").lower()
    if lang not in {"sql", "java", "text"}:
        lang = "text"
    if lang == "text":
        table = structured_text_table(code, styles)
        if table is not None:
            return table
    lines = code.splitlines() or [""]
    body = "<br/>".join(highlight_line(line.rstrip("\n"), lang) for line in lines)
    para = Paragraph(f"<font name='CodeMono'>{body}</font>", styles["code"])
    table = Table([[para]], colWidths=[A4[0] - 32 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f6f8fa")),
                ("BOX", (0, 0), (-1, -1), 0.45, colors.HexColor("#d0d7de")),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return table


def table_col_widths(headers: list[str], rows: list[list[str]]) -> list[float]:
    page_width = A4[0] - 32 * mm
    normalized = [h.strip().lower() for h in headers]

    if normalized[:3] == ["id", "operation", "name"]:
        base = {
            "id": 12 * mm,
            "operation": 58 * mm,
            "name": 42 * mm,
            "starts": 16 * mm,
            "e-rows": 17 * mm,
            "a-rows": 17 * mm,
            "buffers": 20 * mm,
            "reads": 18 * mm,
        }
        widths = [base.get(h, 18 * mm) for h in normalized]
        scale = min(1, page_width / sum(widths))
        return [w * scale for w in widths]

    if normalized == ["call", "count", "disk", "query", "current", "rows"]:
        return [30 * mm, 22 * mm, 22 * mm, 28 * mm, 28 * mm, 22 * mm]

    weights = []
    for col_idx, header in enumerate(headers):
        content_len = max([len(header)] + [len(row[col_idx]) if col_idx < len(row) else 0 for row in rows])
        weights.append(max(1.0, min(4.0, content_len / 10)))
    total = sum(weights)
    return [page_width * w / total for w in weights]


def make_structured_table(headers: list[str], rows: list[list[str]], styles) -> Table:
    col_count = len(headers)
    normalized_rows = [row + [""] * (col_count - len(row)) for row in rows]
    data = [[Paragraph(md_inline(h), styles["cell_header"]) for h in headers]]
    data.extend([[Paragraph(md_inline(c), styles["cell"]) for c in row[:col_count]] for row in normalized_rows])

    table = Table(data, colWidths=table_col_widths(headers, normalized_rows), repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2f5597")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#ccd7e6")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fbff")]),
            ]
        )
    )
    return table


def parse_pipe_ascii_table(lines: list[str], styles) -> Table | None:
    pipe_lines = [line.strip() for line in lines if "|" in line and not re.fullmatch(r"[-+\s|]+", line.strip())]
    if len(pipe_lines) < 2:
        return None

    parsed = []
    for line in pipe_lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        parsed.append(cells)

    headers = parsed[0]
    rows = parsed[1:]
    if not headers or all(not h for h in headers):
        return None
    return make_structured_table(headers, rows, styles)


def parse_whitespace_ascii_table(lines: list[str], styles) -> Table | None:
    nonempty = [line.rstrip() for line in lines if line.strip()]
    if len(nonempty) < 3:
        return None
    headers = re.split(r"\s{2,}", nonempty[0].strip())
    if headers != ["Call", "Count", "Disk", "Query", "Current", "Rows"]:
        return None
    rows = []
    for line in nonempty[2:]:
        cells = re.split(r"\s+", line.strip())
        if len(cells) == len(headers):
            rows.append(cells)
    if not rows:
        return None
    return make_structured_table(headers, rows, styles)


def structured_text_table(code: str, styles) -> Table | None:
    lines = code.splitlines()
    if any("|" in line for line in lines):
        return parse_pipe_ascii_table(lines, styles)
    return parse_whitespace_ascii_table(lines, styles)


def parse_table(lines: list[str], start: int, styles) -> tuple[Table, int]:
    table_lines = []
    i = start
    while i < len(lines) and lines[i].strip().startswith("|"):
        table_lines.append(lines[i].strip())
        i += 1

    rows = []
    for idx, line in enumerate(table_lines):
        cells = [c.strip() for c in line.strip("|").split("|")]
        if idx == 1 and all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        para_style = styles["cell_header"] if idx == 0 else styles["cell"]
        rows.append([Paragraph(md_inline(c), para_style) for c in cells])

    page_width = A4[0] - 32 * mm
    col_count = max(len(r) for r in rows)
    header_text = [re.sub("<[^>]+>", "", c.getPlainText()) for c in rows[0]]
    if col_count == 2 and header_text[0] == "선택지":
        col_widths = [16 * mm, page_width - 16 * mm]
    elif col_count == 3 and header_text == ["범위", "핵심 내용", "문항"]:
        col_widths = [42 * mm, page_width - 60 * mm, 18 * mm]
    else:
        col_widths = [page_width / col_count] * col_count

    table = Table(rows, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2f5597")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#d9e2f3")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fbfcfe")]),
            ]
        )
    )
    return table, i


def flowable_height(flowable, width: float, max_height: float) -> float:
    try:
        _, height = flowable.wrap(width, max_height)
    except Exception:
        return 0
    return height


def append_question_block(story, block, width: float | None = None, max_height: float | None = None):
    if not block:
        return
    if width and max_height:
        height = sum(flowable_height(flowable, width, max_height) for flowable in block)
        # Ask ReportLab to start a new page only when the whole question cannot
        # fit in the remaining frame. The block itself is not wrapped in
        # KeepTogether, which avoids the overly conservative one-question-per-page
        # behavior.
        story.append(CondPageBreak(min(height * 1.18 + 6 * mm, max_height)))
    story.extend(block)


def build_story(markdown: str, styles, frame_width: float | None = None, frame_height: float | None = None):
    lines = markdown.splitlines()
    story = []
    question_block = None
    i = 0
    in_code = False
    code_lang = "text"
    code_lines: list[str] = []

    def emit(flowable):
        if question_block is not None:
            question_block.append(flowable)
        else:
            story.append(flowable)

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()

        if line.startswith("```"):
            if not in_code:
                in_code = True
                code_lang = line.strip()[3:].strip() or "text"
                code_lines = []
            else:
                code = "\n".join(code_lines)
                emit(highlighted_code_block(code, code_lang, styles))
                emit(Spacer(1, 2 * mm))
                in_code = False
            i += 1
            continue

        if in_code:
            code_lines.append(raw)
            i += 1
            continue

        stripped = line.strip()
        if not stripped:
            emit(Spacer(1, 2.2 * mm))
            i += 1
            continue

        if stripped == "---":
            emit(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#d0d7de")))
            emit(Spacer(1, 2 * mm))
            i += 1
            continue

        if stripped.startswith("|"):
            table, i = parse_table(lines, i, styles)
            emit(table)
            emit(Spacer(1, 4 * mm))
            continue

        if stripped.startswith("# "):
            append_question_block(story, question_block, frame_width, frame_height)
            question_block = None
            text = stripped[2:].strip()
            if text == "문제":
                i += 1
                continue
            if text == "정답 및 해설":
                story.append(PageBreak())
                story.append(Paragraph(md_inline(text), styles["h1"]))
            else:
                if story:
                    story.append(PageBreak())
                story.append(Paragraph(md_inline(text), styles["title"]))
            story.append(Spacer(1, 3 * mm))
        elif stripped.startswith("## "):
            text = stripped[3:].strip()
            is_question = text.startswith("문제 ") and not text.endswith("해설")
            if is_question:
                append_question_block(story, question_block, frame_width, frame_height)
                question_block = []
            elif question_block is not None:
                append_question_block(story, question_block, frame_width, frame_height)
                question_block = None
            block = [Paragraph(md_inline(text), styles["h1"])]
            if is_question:
                block.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e6eef8")))
            emit(KeepTogether(block))
        elif stripped.startswith("### "):
            emit(Paragraph(md_inline(stripped[4:].strip()), styles["h2"]))
        elif stripped.startswith("> "):
            emit(Paragraph(md_inline(stripped[2:].strip()), styles["quote"]))
        elif stripped.startswith("- "):
            emit(Paragraph("• " + md_inline(stripped[2:].strip()), styles["bullet"]))
        else:
            emit(Paragraph(md_inline(stripped), styles["body"]))
        i += 1

    append_question_block(story, question_block, frame_width, frame_height)
    return story


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("NotoSansKR", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawCentredString(A4[0] / 2, 10 * mm, str(doc.page))
    canvas.restoreState()


def main() -> None:
    register_fonts()
    styles = make_styles()
    markdown = INPUT.read_text(encoding="utf-8")
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=15 * mm,
        bottomMargin=16 * mm,
        title="친절한 SQL 튜닝 전범위 25문항",
        author="Codex",
    )
    story = build_story(markdown, styles, doc.width, doc.height)
    try:
        doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    except LayoutError as exc:
        raise SystemExit(
            "PDF layout failed. A question block is taller than one page; split or shorten that question."
        ) from exc
    print(OUTPUT)


if __name__ == "__main__":
    main()
