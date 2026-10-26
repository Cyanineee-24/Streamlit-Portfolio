"""Contact tab: one feedback form; submissions are kept in session state."""

import datetime as dt
import re

import pandas as pd
import streamlit as st

from content import CONTACT_SENTENCE, EMAIL
from sections.common import gmail_url

REASONS = ["Internship / job", "Collaboration", "Feedback on this portfolio", "Just saying hi", "Other"]
FOUND_VIA = ["LinkedIn", "GitHub", "A classmate or teacher", "Other"]
EMAIL_PATTERN = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")

# Form fields and the values they reset to after a successful submit.
FIELDS = {
    "contact_name": "",
    "contact_email": "",
    "contact_reason": REASONS[0],
    "contact_found": FOUND_VIA[0],
    "contact_rating": 8,
    "contact_message": "",
    "contact_robot": False,
}


def problems(state) -> list[str]:
    found = []
    if not state.contact_name.strip():
        found.append("your name")
    if not EMAIL_PATTERN.fullmatch(state.contact_email.strip()):
        found.append("a valid email")
    if not state.contact_message.strip():
        found.append("a message")
    return found


def submit() -> None:
    """Form callback: validate, store the submission, then reset the fields."""
    state = st.session_state
    missing = problems(state)
    if missing:
        state.contact_feedback = ("error", "Please add " + ", ".join(missing) + ".")
        return
    if not state.contact_robot:
        state.contact_feedback = ("warning", "Please tick “I'm not a robot”.")
        return
    state.submissions.append(
        {
            "Time": dt.datetime.now().strftime("%H:%M"),
            "Name": state.contact_name.strip(),
            "Email": state.contact_email.strip(),
            "Reason": state.contact_reason,
            "Found via": state.contact_found,
            "Rating": state.contact_rating,
            "Message": state.contact_message.strip(),
        }
    )
    state.contact_feedback = (
        "success",
        f"Thanks, {state.contact_name.strip()}! Your message was received.",
    )
    for key, value in FIELDS.items():
        state[key] = value


def clear_submissions() -> None:
    st.session_state.submissions = []
    st.session_state.contact_feedback = None


def render() -> None:
    state = st.session_state
    state.setdefault("submissions", [])
    state.setdefault("contact_feedback", None)
    for key, value in FIELDS.items():
        state.setdefault(key, value)

    st.header("Contact", anchor=False)
    st.write(CONTACT_SENTENCE)
    st.markdown(f"**Email:** [{EMAIL}]({gmail_url(EMAIL)})")

    with st.form("contact_form"):
        st.subheader("Contact & feedback", anchor=False)
        left, right = st.columns(2, gap="medium")
        left.text_input("Your name", key="contact_name")
        right.text_input("Your email", key="contact_email")
        st.selectbox("Reason", REASONS, key="contact_reason")
        st.radio("How did you find my portfolio?", FOUND_VIA, key="contact_found", horizontal=True)
        st.slider("Rate this portfolio", 1, 10, key="contact_rating")
        st.text_area("Message", height=140, key="contact_message")
        st.checkbox("I'm not a robot", key="contact_robot")
        st.form_submit_button("Send message", type="primary", on_click=submit)

    if state.contact_feedback:
        kind, text = state.contact_feedback
        {"success": st.success, "warning": st.warning, "error": st.error}[kind](text)

    if state.submissions:
        st.subheader("Submissions this session", anchor=False)
        st.table(pd.DataFrame(state.submissions))
        st.button("Clear submissions", on_click=clear_submissions)
