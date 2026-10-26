"""
Charles Daragosa — Autobiography & Portfolio
Built with Streamlit.  Run with:  streamlit run app.py
Edit content.py to personalize everything. Look and feel: .streamlit/config.toml
(theme) and assets/style.css (the few details the theme can't express).
"""

import datetime as dt
from pathlib import Path

import pandas as pd
import streamlit as st

from content import (
    ABOUT,
    BACKGROUND,
    CERTIFICATES_DIR,
    CERTIFICATIONS,
    EDUCATION,
    EMAIL,
    GITHUB,
    HERO_SENTENCE,
    INTERESTS,
    LINKEDIN,
    MILESTONES,
    NAME,
    PROFILE_IMAGE,
    PROGRAM,
    PROJECTS,
    RESUME_DOWNLOAD_NAME,
    RESUME_PDF,
    SECTION,
    SHORT_NAME,
    START_YEAR,
    YEAR_LEVEL,
)
from media import stand_in_label
from portfolio import count_languages_and_tools
from resume import build_resume
from sections import contact, projects, skills
from sections.common import email_button, portrait

ROOT = Path(__file__).parent
STYLE = ROOT / "assets" / "style.css"
TABS = ["About", "Skills", "Projects", "Contact"]

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG (must be the first Streamlit call)
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=f"{SHORT_NAME} | Portfolio",
    page_icon=":material/menu_book:",
    layout="wide",
    initial_sidebar_state="auto",  # open on desktop, collapsed on phones
)
st.html(STYLE)

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
def file_label(path: Path) -> str:
    """'C-Programming_Certificate.pdf' -> 'C Programming Certificate'."""
    return path.stem.replace("_", " ").replace("-", " ")


with st.sidebar:
    st.header("Quick Access", anchor=False)

    st.subheader("Profiles", anchor=False)
    st.link_button("LinkedIn", LINKEDIN, width="stretch", icon=":material/person:")
    st.link_button("GitHub", GITHUB, width="stretch", icon=":material/code:")
    email_button(EMAIL, "Email", width="stretch", icon=":material/mail:")

    st.subheader("Downloads", anchor=False)
    resume = ROOT / RESUME_PDF
    # Your own PDF if it's there; otherwise one built from content.py. Either way it's a PDF.
    st.download_button(
        "Résumé (PDF)", resume.read_bytes() if resume.is_file() else build_resume(),
        file_name=RESUME_DOWNLOAD_NAME, mime="application/pdf",
        width="stretch", type="primary", icon=":material/download:",
    )
    for certificate in sorted((ROOT / CERTIFICATES_DIR).glob("*.pdf")):
        st.download_button(
            file_label(certificate), certificate.read_bytes(), file_name=certificate.name,
            mime="application/pdf", width="stretch", icon=":material/workspace_premium:",
        )

# ─────────────────────────────────────────────────────────────
# HERO — text left, the portrait "print" right
# ─────────────────────────────────────────────────────────────
def show_projects() -> None:
    st.session_state.tab = "Projects"


photo, is_real_photo = portrait(PROFILE_IMAGE, SHORT_NAME)
with st.container(key="hero"):
    text_col, photo_col = st.columns([7, 5], gap="large", vertical_alignment="center")
    with text_col:
        st.markdown('<p class="eyebrow">Hello, I\'m</p>', unsafe_allow_html=True)
        st.title(NAME, anchor=False)
        st.markdown(f'<p class="hero-line">{PROGRAM} · {YEAR_LEVEL} · Section {SECTION}</p>',
                    unsafe_allow_html=True)
        st.write(HERO_SENTENCE)
        with st.container(horizontal=True, gap="small"):
            email_button(EMAIL, "Email me", type="primary")
            st.button("View projects", on_click=show_projects)
    with photo_col:
        label = f"Portrait of {NAME}" if is_real_photo else stand_in_label(SHORT_NAME)
        st.image(photo, width="stretch", alt=label)  # the stand-in carries its label in the picture

with st.container(key="metrics"):
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Projects", len(PROJECTS))
    m2.metric("Languages & tools", count_languages_and_tools())
    m3.metric("Certifications", len(CERTIFICATIONS))
    m4.metric("CS student since", START_YEAR)

# ─────────────────────────────────────────────────────────────
# TABS — the active tab lives in st.session_state.tab (and the URL)
# ─────────────────────────────────────────────────────────────
tab_about, tab_skills, tab_projects, tab_contact = st.tabs(TABS, key="tab", bind="query-params")

with tab_about:
    st.header("About me", anchor=False)
    for paragraph in ABOUT:
        st.write(paragraph)

    st.header("My story", anchor=False)
    st.subheader("Background", anchor=False)
    for paragraph in BACKGROUND:
        st.write(paragraph)

    left, right = st.columns(2, gap="large")
    with left:
        st.subheader("Education", anchor=False)
        st.table(pd.DataFrame(EDUCATION, columns=["School", "Level", "Years"]), hide_index=True)
    with right:
        st.subheader("Interests", anchor=False)
        st.markdown("\n".join(f"- {interest}" for interest in INTERESTS))

    st.subheader("Milestones", anchor=False)
    with st.container(key="timeline"):
        for label, items in MILESTONES:
            when, what = st.columns([1, 3], gap="large")
            when.markdown(f'<p class="when">{label}</p>', unsafe_allow_html=True)
            what.markdown("\n".join(f"- {item}" for item in items))

    st.subheader("Certifications", anchor=False)
    st.markdown("\n".join(f"- {c['name']} ({c['issuer']})" for c in CERTIFICATIONS))

with tab_skills:
    skills.render()

with tab_projects:
    projects.render()

with tab_contact:
    contact.render()

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.divider()
st.caption(f"© {dt.date.today().year} {NAME} · Section {SECTION} · Built with Streamlit")
