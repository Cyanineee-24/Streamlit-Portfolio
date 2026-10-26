"""Projects tab."""

import re

import streamlit as st

import content
from portfolio import content_problems, filter_projects, used_categories
from sections.common import picture

STATUS_COLORS = {"Completed": "green", "In progress": "orange"}  # everything else is gray
NARROW_IMAGE_WIDTH = 280  # px, for portrait/square images (phone screens, logos)


def slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def project_text(p: dict) -> None:
    st.subheader(p["title"], anchor=False)
    if p["status"]:
        st.badge(p["status"], color=STATUS_COLORS.get(p["status"], "gray"))
    st.write(p["desc"])
    st.markdown(
        f"**My role:** {p['role']}  \n"
        f"**Tools:** {', '.join(p['tech'])}  \n"
        f"**Outcome:** {p['outcome']}"
    )
    if p["link"]:
        st.link_button("View project", p["link"], icon=":material/open_in_new:")


def project_block(p: dict) -> None:
    """One project: text beside its screenshot, or text-only if there's no screenshot."""
    image = picture(p["image"], p["image_ratio"])
    with st.container(key=f"project-{slug(p['title'])}"):
        if image is None:
            project_text(p)
        else:
            text_col, image_col = st.columns([7, 5], gap="large", vertical_alignment="center")
            with text_col:
                project_text(p)
            with image_col:
                width = "stretch" if image.width > image.height else NARROW_IMAGE_WIDTH
                st.image(image, width=width, caption=p.get("caption"),
                         alt=f"Screenshot of {p['title']}")


def render() -> None:
    st.header("Projects", anchor=False)
    for problem in content_problems():
        st.warning(problem)

    picked = st.multiselect(
        "Filter by category", used_categories(), placeholder="All categories",
        key="project_categories",
    )
    shown = filter_projects(content.PROJECTS, picked)
    st.caption(f"Showing {len(shown)} of {len(content.PROJECTS)} projects")
    for i, p in enumerate(shown):
        if i:
            st.divider()
        project_block(p)
