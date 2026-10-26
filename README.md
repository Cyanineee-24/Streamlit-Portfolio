# Charles Daragosa — Portfolio

A personal autobiography and portfolio built with [Streamlit](https://streamlit.io).

**Live app:** https://charles-daragosa.streamlit.app/?classId=023f15cd-f802-4f13-a2a4-00dcaf3358d8&assignmentId=b8772722-2beb-48fd-9c5c-a7d5de9264dc&submissionId=460dd74e-52fd-1c7e-f7fa-63a427bb6917

Charles Benedict B. Daragosa · BS Computer Science, 3rd Year · Section F2
Cebu Institute of Technology – University · Applied AI

---

## What's inside

- **About** — background, my story from BS Biology to Computer Science, education, interests, milestones, and certifications
- **Skills** — skills grouped by category, with a chart of self-rated proficiency (1–5)
- **Projects** — ResiboReportAI, VizuaLearn, AutoLease, and LuxWatch, each with role, tools, status, and outcome; filterable by category
- **Contact** — a contact and feedback form that validates input and responds on submit
- **Quick Access sidebar** — links to my profiles and a résumé download

## Built with

- Python
- Streamlit
- pandas and NumPy
- Altair (charts)
- Pillow (image handling)
- fpdf2 (résumé PDF fallback)

## Run it locally

Requires Python 3.12 or newer.

```bash
git clone https://github.com/Cyanineee-24/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

The app opens at http://localhost:8501.

## Project structure

```
├── app.py                 # Entry point: page setup, sidebar, hero, tabs, footer
├── content.py             # All personal content: bio, education, skills, projects
├── portfolio.py           # Data helpers for skills and projects
├── media.py               # Image loading and fallbacks
├── resume.py              # Résumé PDF fallback
├── sections/              # One module per tab (skills, projects, contact)
├── assets/                # Stylesheet, images, and optional résumé PDF
├── .streamlit/config.toml # Theme
├── tests/smoke_test.py    # Headless test of the whole app
└── requirements.txt
```

To update the content, edit `content.py`. No other file needs to change.

## Testing

```bash
python tests/smoke_test.py
```

## Contact

- Email: charlesbenedictdaragosa@gmail.com
- LinkedIn: https://www.linkedin.com/in/charles-daragosa-124856445/
- GitHub: https://github.com/Cyanineee-24
