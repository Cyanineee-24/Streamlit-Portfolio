"""
Headless smoke test for the whole app (no browser needed).
Run from the project folder:  venv\\Scripts\\python tests\\smoke_test.py

Image scenarios point content.py's image paths at a temporary folder, so your
real files in assets/images/ are never read, moved or overwritten.
"""

import datetime as dt
import re
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from PIL import Image  # noqa: E402
from streamlit.testing.v1 import AppTest  # noqa: E402

import content  # noqa: E402
from content import CERTIFICATIONS, NAME, PROJECT_CATEGORIES, PROJECTS, SECTION, SKILLS  # noqa: E402
from media import find_image, load_image, profile_print, slot_size  # noqa: E402
from portfolio import project_tech, skills_by_category, skills_table  # noqa: E402
from resume import build_resume  # noqa: E402

TIMEOUT = 20
EXPECTED_ORDER = ["ResiboReportAI", "VizuaLearn", "AutoLease", "LuxWatch"]
checks = 0


def ok(label: str) -> None:
    global checks
    checks += 1
    print(f"  ok  {label}")


def check(at: AppTest, label: str) -> None:
    assert not at.exception, f"{label}: {[e.value for e in at.exception]}"
    ok(label)


def card_titles(at: AppTest) -> list[str]:
    titles = {p["title"] for p in PROJECTS}
    return [h.value for h in at.subheader if h.value in titles]


def image_count(at: AppTest) -> int:
    return len(at.get("image"))


def all_text(at: AppTest) -> str:
    return " ".join(e.value for e in [*at.markdown, *at.caption, *at.title, *at.header, *at.subheader])


def button(at: AppTest, label: str):
    return next(b for b in at.button if b.label == label)


def download_labels(at: AppTest) -> list[str]:
    return [d.proto.label for d in at.sidebar.get("download_button")]


def fresh_app() -> AppTest:
    return AppTest.from_file(str(ROOT / "app.py"), default_timeout=TIMEOUT).run()


# Content checks
print("Content")
known = {s for skills in SKILLS.values() for s in skills}
missing = [t for t in project_tech() if t not in known]
assert not missing, f"project tech missing from SKILLS: {missing}"
assert "Uncategorized" not in skills_by_category()
ok("every project tech is in SKILLS")

assert [p["title"] for p in PROJECTS] == EXPECTED_ORDER
assert all("featured" not in p for p in PROJECTS)
ok(f"projects in content order, no featured flag: {EXPECTED_ORDER}")
for p in PROJECTS:
    assert p.get("role") and p.get("outcome"), p["title"]
    assert "TODO" not in p["role"] + p["outcome"], p["title"]
ok("every project has a real role and outcome (no TODO)")
statuses = [p["status"] for p in PROJECTS]
assert statuses == ["Completed", "Completed", "In progress", "In progress"], statuses
ok("completed projects first, then in progress")
assert "Hardware / Maker" not in PROJECT_CATEGORIES and "Product Design" not in known
ok("'Hardware / Maker' category and 'Product Design' skill removed")

source_files = [ROOT / "app.py", ROOT / "content.py", ROOT / "portfolio.py", ROOT / "media.py",
                ROOT / "assets" / "style.css", *(ROOT / "sections").glob("*.py")]
for path in source_files:
    text = path.read_text(encoding="utf-8").lower()
    for word in ("piyesa", "bill of materials", "hardware"):
        assert word not in text, f"'{word}' still in {path.name}"
ok("no Piyesa / hardware mentions in the app's source")

# Image scenarios
print("\nImages")
tmp = Path(tempfile.mkdtemp(prefix="portfolio-test-"))
real_profile = content.PROFILE_IMAGE
real_project_images = [p["image"] for p in PROJECTS]
content.PROFILE_IMAGE = str(tmp / "profile.jpg")
for p in PROJECTS:
    p["image"] = str(tmp / Path(p["image"]).name)

# No profile.jpg: the stand-in fills the frame.
_, is_photo = profile_print(content.PROFILE_IMAGE, (4, 5), "Charles Daragosa")
assert not is_photo
at = fresh_app()
check(at, "no profile.jpg: app runs")
assert image_count(at) == 1, image_count(at)
check(at, "  -> hero shows the labelled stand-in; projects text-only")

# With profile.jpg: the photo in full colour, with the sage block behind it.
Image.new("RGB", (900, 1200), "#c0392b").save(tmp / "profile.jpg")
framed, is_photo = profile_print(content.PROFILE_IMAGE, (4, 5), "Charles Daragosa")
r, g, b, _ = framed.getpixel((10, 10))
assert is_photo and r - b > 100, (r, g, b)  # still red, not gray
assert framed.getpixel((framed.width - 5, framed.height - 5))[:3] == (0x8F, 0xA3, 0x7A)
ok("profile.jpg -> colour photo with sage offset block")
at = fresh_app()
check(at, "profile.jpg present: app runs")
assert image_count(at) == 1
check(at, "  -> one image (the portrait)")

Image.new("RGB", (1200, 800), "#888888").save(tmp / Path(PROJECTS[3]["image"]).name)
at = fresh_app()
check(at, "one project screenshot present: app runs")
assert image_count(at) == 2
check(at, "  -> portrait + LuxWatch screenshot; others text-only")

# A wide screenshot is fitted whole inside its 3:2 slot (mat above and below), not cropped.
Image.new("RGB", (2000, 900), "#c0392b").save(tmp / "wide.png")
fitted = load_image(str(tmp / "wide.png"), (3, 2), crop=False)
assert fitted.size == slot_size((3, 2))
assert fitted.getpixel((fitted.width // 2, 2)) == (0xEA, 0xE8, 0xE1)  # mat
assert fitted.getpixel((2, fitted.height // 2))[0] > 150  # left edge of the screenshot kept
ok("wide screenshot fitted inside its slot, nothing cropped or stretched")

(tmp / Path(PROJECTS[2]["image"]).name).write_bytes(b"not really a png")
at = fresh_app()
check(at, "corrupt project image: falls back instead of crashing")
assert image_count(at) == 2

content.PROFILE_IMAGE = real_profile
for p, image in zip(PROJECTS, real_project_images):
    p["image"] = image

# Download scenarios (temp folder again; your real PDFs are never touched)
print("\nDownloads")
real_resume, real_certificates = content.RESUME_PDF, content.CERTIFICATES_DIR
content.RESUME_PDF = str(tmp / "resume.pdf")
content.CERTIFICATES_DIR = str(tmp / "certificates")

built = build_resume()
assert built.startswith(b"%PDF") and len(re.findall(rb"/Type /Page[^s]", built)) == 1
ok("build_resume() makes a one-page PDF from content.py")
at = fresh_app()
check(at, "no resume.pdf, no certificates folder: app runs")
assert download_labels(at) == ["Résumé (PDF)"], download_labels(at)
check(at, "  -> still offers a PDF résumé (built from content.py)")

(tmp / "resume.pdf").write_bytes(b"%PDF-1.4 test")
(tmp / "certificates").mkdir()
(tmp / "certificates" / "Java-OOP-Certificate.pdf").write_bytes(b"%PDF-1.4 test")
(tmp / "certificates" / "C_Programming_Certificate.pdf").write_bytes(b"%PDF-1.4 test")
at = fresh_app()
check(at, "resume.pdf + two certificate PDFs: app runs")
labels = download_labels(at)
assert labels == ["Résumé (PDF)", "C Programming Certificate", "Java OOP Certificate"], labels
check(at, f"  -> {labels}")

content.RESUME_PDF, content.CERTIFICATES_DIR = real_resume, real_certificates

# App checks (with whatever images are really in assets/images)
print("\nApp")
at = fresh_app()
check(at, "initial run")
assert [t.label for t in at.tabs] == ["About", "Skills", "Projects", "Contact"]
check(at, "tabs: About · Skills · Projects · Contact")

metrics = {m.label: m.value for m in at.metric}
expected_tools = sum(len(s) for c, s in SKILLS.items() if c != "Areas & Practices")
assert metrics == {
    "Projects": "4",
    "Languages & tools": str(expected_tools),
    "Certifications": str(len(CERTIFICATIONS)),
    "CS student since": "2024",
}, metrics
check(at, f"metrics: Projects = 4, tools = {expected_tools}, certs = 3, since 2024")

text = all_text(at)
assert at.title[0].value == NAME
check(at, "name is the page title (h1)")
assert [h.value for h in at.sidebar.header] == ["Quick Access"]
assert [h.value for h in at.sidebar.subheader] == ["Profiles", "Downloads"]
assert not at.sidebar.markdown
profiles = {b.label: b.proto.url for b in at.sidebar.get("link_button")}
assert profiles == {
    "LinkedIn": content.LINKEDIN,
    "GitHub": content.GITHUB,
    "Email": f"https://mail.google.com/mail/?view=cm&fs=1&to={quote(content.EMAIL)}",
}, profiles
assert not at.sidebar.get("popover")
check(at, "sidebar: Quick Access -> Profiles (LinkedIn, GitHub, Email) and Downloads only")
email_me = next(b for b in at.get("link_button") if b.proto.label == "Email me")
assert email_me.proto.url == profiles["Email"]
assert not [p for p in at.get("popover") if "Email" in p.proto.popover.label]
check(at, "'Email me' and 'Email' are plain buttons that open Gmail (no dropdown)")
assert "mailto:" not in all_text(at)
check(at, "no mailto: links left")
footer = at.caption[-1].value
assert footer == f"© {dt.date.today().year} {NAME} · Section {SECTION} · Built with Streamlit", footer
hero_line = f"{content.PROGRAM} · {content.YEAR_LEVEL} · Section {SECTION}"
assert f'<p class="hero-line">{hero_line}</p>' in text
check(at, f"hero line '{hero_line}'; name and Section {SECTION} also in the footer")
for cert in CERTIFICATIONS:
    assert f"- {cert['name']} ({cert['issuer']})" in text, cert
check(at, f"certifications as a bulleted list of {len(CERTIFICATIONS)}")
for label, items in content.MILESTONES:
    assert label in text and all(f"- {item}" in text for item in items), label
check(at, f"milestones: {len(content.MILESTONES)} year groups, every item listed")
for interest in content.INTERESTS:
    assert interest in text
check(at, "interests listed")
for paragraph in [*content.ABOUT, *content.BACKGROUND]:
    assert paragraph in text, paragraph[:40]
check(at, f"{len(content.ABOUT)} About paragraphs and {len(content.BACKGROUND)} Background paragraphs shown")
education = at.tabs[0].table
assert len(education) == 1, len(education)
assert list(education[0].value.columns) == ["School", "Level", "Years"]
assert [tuple(row) for row in education[0].value.itertuples(index=False)] == content.EDUCATION
check(at, f"education: st.table School | Level | Years, {len(content.EDUCATION)} rows, most recent first")
assert "TODO" not in text
check(at, "no TODO left anywhere on the page")
assert download_labels(at)[0] == "Résumé (PDF)"
check(at, f"downloads in the sidebar: {download_labels(at)}")

for removed in ("color_picker", "toggle", "date_input", "number_input", "feedback", "map",
                "deck_gl_json_chart", "balloons", "segmented_control", "pills"):
    assert not at.get(removed), removed
check(at, "removed widgets are gone (picker, toggle, playground, map, pills...)")

button(at, "View projects").click().run()
assert at.session_state.tab == "Projects"
check(at, "'View projects' switches to the Projects tab")

# Skills tab
levels = [v for skills in SKILLS.values() for v in skills.values()]
assert all(v is None or v in content.SKILL_SCALE for v in levels), levels
ok("skill levels are 1-5 or None")
assert len(at.get("vega_lite_chart")) == 1
assert "Skills by self-rated proficiency" in text
assert any(c.value == "Self-assessed on a 1–5 scale." for c in at.caption)
check(at, "one Altair chart, titled, with the 1–5 caption")
rated = skills_table().dropna(subset=["Level"])
assert len(rated) == sum(v is not None for v in levels)
ok(f"chart data: the {len(rated)} rated skills only")
assert "**Languages:**" in text
check(at, "skills also listed in text by category")

# Project images: the real files in assets/images
for p in PROJECTS:
    found = find_image(p["image"])
    assert found is not None, p["image"]
    assert found.stat().st_size < 1024 * 1024, f"{found.name} is over 1 MB"
assert find_image(content.PROFILE_IMAGE).stat().st_size < 1024 * 1024
ok("every project has an image file, and every image used is under 1 MB")
images = at.get("image")
assert len(images) == 1 + len(PROJECTS), len(images)
captions = [img.proto.imgs[0].caption for img in images[1:]]
assert captions == [p["caption"] for p in PROJECTS], captions
check(at, "portrait + one captioned image per project")
# projects.py stretches landscape pictures and shows the rest at NARROW_IMAGE_WIDTH.
wide = [load_image(p["image"], p["image_ratio"], crop=False) for p in PROJECTS]
assert [w.width > w.height for w in wide] == [True, False, True, True]
ok("VizuaLearn's square logo shown narrow, landscape screenshots full width")

# Projects tab: cards only, no table
assert not at.tabs[2].table and "Projects at a glance" not in text
assert len(at.table) == 1  # only Education until a contact submission
check(at, "Education is the only table on first load (no Projects table)")
assert card_titles(at) == EXPECTED_ORDER, card_titles(at)
check(at, f"projects in order: {card_titles(at)}")
assert not at.json and not at.get("popover")
check(at, "no 'View as JSON' popover on any project")
page = " ".join(m.value for m in at.markdown)
assert page.count("**My role:**") == page.count("**Outcome:**") == len(PROJECTS)
check(at, "every card shows role, tools, outcome")
for category in at.multiselect(key="project_categories").options:
    at.multiselect(key="project_categories").set_value([category]).run()
    check(at, f"filter = {category} -> {card_titles(at)}")
at.multiselect(key="project_categories").set_value(["Web App", "Mobile"]).run()
assert card_titles(at) == ["VizuaLearn", "AutoLease", "LuxWatch"]
check(at, "filter = Web App + Mobile")
at.multiselect(key="project_categories").set_value([]).run()

# Contact form: empty, no robot box, valid, then clear
at.form_submit_button[0].click().run()
assert at.error
check(at, "contact: empty -> error")


def fill(at: AppTest) -> None:
    at.text_input(key="contact_name").set_value("Ada")
    at.text_input(key="contact_email").set_value("ada@example.com")
    at.selectbox(key="contact_reason").set_value("Collaboration")
    at.radio(key="contact_found").set_value("GitHub")
    at.slider(key="contact_rating").set_value(9)
    at.text_area(key="contact_message").set_value("Hello!")


fill(at)
at.form_submit_button[0].click().run()
assert at.warning and at.text_input(key="contact_name").value == "Ada"
check(at, "contact: no robot checkbox -> warning, fields kept")
fill(at)
at.checkbox(key="contact_robot").check()
at.form_submit_button[0].click().run()
assert at.success and len(at.session_state.submissions) == 1
row = at.session_state.submissions[0]
assert (row["Reason"], row["Found via"], row["Rating"]) == ("Collaboration", "GitHub", 9)
assert at.text_input(key="contact_name").value == ""
check(at, "contact: valid -> success, stored in session_state, fields reset")
submitted = [t for t in at.table if "Message" in t.value.columns]
assert len(submitted) == 1 and len(submitted[0].value) == 1
check(at, "  -> submissions st.table appears right after the first successful send")
button(at, "Clear submissions").click().run()
assert at.session_state.submissions == [] and not [t for t in at.table if "Message" in t.value.columns]
check(at, "'Clear submissions' empties the list")

print(f"\nAll {checks} checks passed.")
