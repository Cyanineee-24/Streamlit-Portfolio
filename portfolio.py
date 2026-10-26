"""
Plain helper functions that derive views from content.py.
No Streamlit code here, so everything is easy to test on its own.
"""

import pandas as pd

from content import PROJECT_CATEGORIES, PROJECT_STATUSES, PROJECTS, SKILLS

UNCATEGORIZED = "Uncategorized"
NON_TOOL_CATEGORIES = {"Areas & Practices"}  # not counted as "languages & tools"


def project_tech() -> list[str]:
    """Every tech tag used by any project, in first-seen order."""
    seen = []
    for p in PROJECTS:
        for tech in p["tech"]:
            if tech not in seen:
                seen.append(tech)
    return seen


def skills_by_category() -> dict[str, dict[str, int | None]]:
    """SKILLS plus any project tech missing from it (as Uncategorized, unrated)."""
    merged = {category: dict(skills) for category, skills in SKILLS.items()}
    known = {skill for skills in SKILLS.values() for skill in skills}
    missing = [tech for tech in project_tech() if tech not in known]
    if missing:
        merged[UNCATEGORIZED] = {tech: None for tech in missing}
    return merged


def skills_table() -> pd.DataFrame:
    """One row per skill: Skill, Category, Level (1-5, or None if unrated)."""
    rows = [
        {"Skill": skill, "Category": category, "Level": level}
        for category, skills in skills_by_category().items()
        for skill, level in skills.items()
    ]
    return pd.DataFrame(rows)


def count_languages_and_tools() -> int:
    return sum(
        len(skills)
        for category, skills in skills_by_category().items()
        if category not in NON_TOOL_CATEGORIES
    )


def content_problems() -> list[str]:
    """Typos in content.py that would break the filter or cards."""
    problems = []
    for p in PROJECTS:
        if p["category"] not in PROJECT_CATEGORIES:
            problems.append(f"{p['title']}: unknown category '{p['category']}'")
        if p["status"] is not None and p["status"] not in PROJECT_STATUSES:
            problems.append(f"{p['title']}: unknown status '{p['status']}'")
        for field in ("role", "outcome"):
            if not p.get(field):
                problems.append(f"{p['title']}: '{field}' is empty")
    return problems


def used_categories() -> list[str]:
    return [c for c in PROJECT_CATEGORIES if any(p["category"] == c for p in PROJECTS)]


def filter_projects(projects: list[dict], categories: list[str]) -> list[dict]:
    """Projects in any of `categories`, in content order; all of them if none are picked."""
    return [p for p in projects if not categories or p["category"] in categories]
