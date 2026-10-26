"""
Builds a one-page résumé PDF from content.py (fpdf2 only, no Streamlit).
Used when assets/resume.pdf isn't there, so the download is always a PDF.
"""

from fpdf import FPDF

import content
from portfolio import skills_by_category

SAGE_DEEP = (95, 115, 80)  # #5f7350, the theme's deep sage
INK = (31, 31, 31)
MUTED = (85, 83, 78)

# The built-in PDF fonts only cover Latin-1; swap the few characters outside it.
REPLACEMENTS = {"–": "-", "—": "-", "‘": "'", "’": "'", "“": '"', "”": '"', "…": "..."}


def clean(text: str) -> str:
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    return text.encode("latin-1", "replace").decode("latin-1")


def filled(value: str) -> bool:
    """False for blanks and TODO placeholders, which stay off the résumé."""
    return bool(value) and not value.strip().upper().startswith("TODO")


class Resume(FPDF):
    def heading(self, text: str) -> None:
        self.ln(2)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*SAGE_DEEP)
        self.cell(0, 7, clean(text), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*SAGE_DEEP)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)

    def para(self, text: str, size: float = 9.5, style: str = "", color=INK) -> None:
        self.set_font("Helvetica", style, size)
        self.set_text_color(*color)
        self.multi_cell(0, size * 0.5, clean(text), align="L", new_x="LMARGIN", new_y="NEXT")

    def bullet(self, text: str) -> None:
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*INK)
        self.set_x(self.l_margin + 3)
        self.multi_cell(0, 5, clean(f"- {text}"), align="L", new_x="LMARGIN", new_y="NEXT")


def build_resume() -> bytes:
    pdf = Resume(format="A4")
    pdf.set_margins(18, 14, 18)
    pdf.set_auto_page_break(True, margin=12)
    pdf.add_page()

    pdf.para(content.NAME, size=22, style="B")
    pdf.ln(1)
    pdf.para(f"{content.PROGRAM} · {content.YEAR_LEVEL} · {content.SCHOOL}", color=SAGE_DEEP)
    pdf.para(f"{content.LOCATION} · {content.EMAIL}", color=MUTED)
    pdf.para(f"{content.LINKEDIN} · {content.GITHUB}", size=9, color=MUTED)

    pdf.heading("Summary")
    pdf.para(content.ABOUT[-1])  # the paragraph about current work and the internship goal

    pdf.heading("Education")
    for school, program, years in content.EDUCATION:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*INK)
        pdf.write(5, clean(school))
        pdf.set_font("Helvetica", "", 10)
        pdf.write(5, clean(f" · {program} · {years}"))
        pdf.ln(5)

    pdf.heading("Skills")
    for category, items in skills_by_category().items():
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*INK)
        pdf.write(5, clean(f"{category}: "))
        pdf.set_font("Helvetica", "", 10)
        pdf.write(5, clean(", ".join(items)))
        pdf.ln(5.2)

    pdf.heading("Projects")
    for p in content.PROJECTS:
        title = p["title"] + (f" ({p['status']})" if p["status"] else "")
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*INK)
        pdf.write(5, clean(title))
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*MUTED)
        pdf.write(5, clean(f"   {', '.join(p['tech'])}"))
        pdf.ln(5)
        # Role and outcome say more on a résumé than the website blurb; the blurb is only a fallback.
        details = [f"{label}: {p[key]}" for key, label in (("role", "Role"), ("outcome", "Outcome"))
                   if filled(p[key])]
        if p["link"]:
            details.append(p["link"])
        for line in details or [p["desc"]]:
            pdf.para(line)
        pdf.ln(1.5)

    pdf.heading("Certifications")
    pdf.para("; ".join(f"{c['name']} ({c['issuer']})" for c in content.CERTIFICATIONS))

    pdf.heading("Milestones")
    for label, items in content.MILESTONES:  # one line per year group keeps it to one page
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*INK)
        pdf.write(5, clean(f"{label}: "))
        pdf.set_font("Helvetica", "", 10)
        pdf.write(5, clean("; ".join(items)))
        pdf.ln(5.2)

    return bytes(pdf.output())
