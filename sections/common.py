"""Small Streamlit helpers shared by app.py and the sections."""

from urllib.parse import quote

import streamlit as st
from PIL import Image

from media import find_image, load_image, profile_print


def _modified(path: str) -> float | None:
    found = find_image(path)
    return found.stat().st_mtime if found else None


# `modified` is only part of the cache key: adding or swapping a file refreshes it.
@st.cache_data(max_entries=32)
def _picture(path: str, ratio: tuple[int, int], modified: float | None) -> Image.Image | None:
    return load_image(path, ratio, crop=False)


@st.cache_data(max_entries=4)
def _portrait(path: str, ratio: tuple[int, int], name: str, modified: float | None):
    return profile_print(path, ratio, name)


def picture(path: str, ratio: tuple[int, int]) -> Image.Image | None:
    """A project screenshot fitted whole inside its slot, or None (show the project text-only)."""
    return _picture(path, tuple(ratio), _modified(path))


def gmail_url(email: str) -> str:
    """A Gmail compose window addressed to `email` (works without a mail app)."""
    return f"https://mail.google.com/mail/?view=cm&fs=1&to={quote(email)}"


def email_button(email: str, label: str, **button_args) -> None:
    st.link_button(label, gmail_url(email), **button_args)


def portrait(path: str, name: str) -> tuple[Image.Image, bool]:
    """The hero print: (image, True) for a real photo, (image, False) for the stand-in."""
    return _portrait(path, (4, 5), name, _modified(path))
