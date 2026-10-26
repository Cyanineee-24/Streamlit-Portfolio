"""Skills tab: a text summary and one bar chart of rated skills."""

import altair as alt
import streamlit as st

from content import SKILL_SCALE
from portfolio import skills_by_category, skills_table

SAGE = "#8fa37a"  # keep in sync with .streamlit/config.toml
INK = "#1f1f1f"
CHART_TITLE = "Skills by self-rated proficiency"


def level_axis_labels() -> str:
    """Vega expression that shows each tick (1-5) as its scale name."""
    cases = " : ".join(f"datum.value == {n} ? '{label}'" for n, label in SKILL_SCALE.items())
    return f"{cases} : ''"


def render() -> None:
    st.header("Skills", anchor=False)
    st.write("These are the languages, frameworks and practices I work with.")
    for category, items in skills_by_category().items():
        st.markdown(f"**{category}:** {', '.join(items)}")

    st.subheader(CHART_TITLE, anchor=False)
    rated = skills_table().dropna(subset=["Level"])
    if rated.empty:
        st.info("No skills are rated yet. Add 1–5 levels to SKILLS in content.py.")
        return
    rated = rated.assign(Rating=[SKILL_SCALE[int(v)] for v in rated["Level"]])
    chart = (
        alt.Chart(rated)
        .mark_bar(color=SAGE, size=26)
        .encode(
            x=alt.X(
                "Level:Q",
                scale=alt.Scale(domain=[0, 5]),
                axis=alt.Axis(values=list(SKILL_SCALE), labelExpr=level_axis_labels(),
                              labelFontSize=14, labelColor=INK),
                title=None,
            ),
            y=alt.Y(
                "Skill:N",
                sort=alt.EncodingSortField(field="Level", order="descending"),
                axis=alt.Axis(labelLimit=0, labelFontSize=14, labelColor=INK, labelPadding=8),
                title=None,
            ),
            tooltip=["Skill", "Category", "Rating"],
        )
        .properties(height=max(140, 48 * len(rated)))
    )
    st.altair_chart(chart, width="stretch", alt=f"{CHART_TITLE}, horizontal bar chart")
    st.caption("Self-assessed on a 1–5 scale.")
