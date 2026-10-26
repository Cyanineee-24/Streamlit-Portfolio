"""
All personal content for the portfolio lives here.
Edit this file to update the site. There is no Streamlit code in this file.
"""

NAME = "Charles Benedict B. Daragosa"
SHORT_NAME = "Charles Daragosa"
PROGRAM = "BS Computer Science"
YEAR_LEVEL = "3rd Year"
SECTION = "F2"
SCHOOL = "Cebu Institute of Technology – University"
LOCATION = "Cebu, Philippines"
START_YEAR = 2024  # the year I started BS Computer Science
TAGLINE = "Back-end Development · AI Agents & Automation · CS Student"
EMAIL = "charlesbenedictdaragosa@gmail.com"
GITHUB = "https://github.com/Cyanineee-24"
LINKEDIN = "https://www.linkedin.com/in/charles-daragosa-124856445/"

# Images: drop files into assets/images/ with these names.
#   .jpg, .jpeg, .png or .webp all work for the same name. Any size works.
#   The profile photo is center-cropped to 4:5; project screenshots are fitted
#   whole inside their slot (see image_ratio on each project), never cropped.
#   Keep each file under 1 MB for deployment; full-size originals go in
#   assets/images/originals/ (not used by the app).
#   Missing profile photo: a labelled stand-in is shown in the same frame.
#   Missing project screenshot: that project is shown text-only.
PROFILE_IMAGE = "assets/images/img_displayPicture.jpg"  # hero portrait, 4:5

# Downloads (sidebar)
#   Résumé: if the PDF is missing, a one-page PDF résumé built from this file is offered instead.
#   Certificates: every .pdf in the folder gets its own button, labelled from its
#   file name ("C-Programming-Certificate.pdf" -> "C Programming Certificate").
RESUME_PDF = "assets/resume.pdf"
RESUME_DOWNLOAD_NAME = "Charles-Daragosa-Resume.pdf"
CERTIFICATES_DIR = "assets/certificates"

HERO_SENTENCE = (
    "Computer Science student at CIT-U, focused on backend work: APIs, databases, "
    "and the business logic that makes applications run."
)
CONTACT_SENTENCE = "Write to me about backend internships or a project you're building."

ABOUT = [
    "I'm a Computer Science student at Cebu Institute of Technology – University, but I didn't "
    "start out in CS. I first studied BS Biology, learning about plants and animals well beyond their "
    "taxonomy. The memorization was relentless: I'd cram for each exam, then forget almost all of it "
    "once it was over. Around the same time, I found software development through online content, and "
    "it stuck in a way biology never did. So I made the leap to Computer Science. It's still the "
    "decision I'm proudest of.",
    "The transition was hard at first: going from pure memorization to real understanding, "
    "especially in OOP, Data Structures and Algorithms, and Design and Analysis of Algorithms. "
    "But the struggle paid off. It gave me a solid grasp of the fundamentals, and I've grown a lot "
    "as a developer since.",
    "My strongest languages are Java and Python. I've worked with Django, NumPy, and Pandas, and "
    "I'm comfortable with object-oriented design and design patterns from applying them in projects.",
    "Lately I've been building applications with AI features, including retrieval-augmented "
    "generation (RAG), AI agents, and workflow automation. I want to understand not just how to call a "
    "model, but how to design the systems around it so they're reliable and useful. I'm looking for "
    "internship opportunities where I can grow as a backend developer.",
]

BACKGROUND = [  # paragraphs
    "I'm from Poblacion, Argao, Cebu. My first dream was to become a humble community doctor, "
    "bringing health services to people who need them most. That's why I first took up Biology. But "
    "the longer I studied, the clearer I saw how long and demanding the path to becoming a doctor "
    "really is. So I took a leap of faith into software development.",
    "The goal didn't change, only the tools. I still want to build things that help people, "
    "especially in communities like the one I grew up in. Software lets me do that at scale: tools "
    "that save small businesses time, make services easier to reach, and help students learn better.",
    "Now I'm a third-year Computer Science student at CIT-U and a two-time Parangal awardee. "
    "I'm focused on backend development and AI, and I'm currently in the GCI World Data Science and "
    "Machine Learning Camp. The kid from Argao who wanted to heal people is now learning to build "
    "systems that serve them.",
]
EDUCATION = [  # (school, program, years), most recent first
    (SCHOOL, PROGRAM, "2024 – present"),
    ("Cebu Normal University", "BS Biology", "2023 – 2024"),
    ("Argao National High School", "Junior & Senior High School", "Graduated 2023"),
    ("Argao Central Elementary School", "Elementary", "Graduated 2017"),
]
INTERESTS = [
    "Competitive Gaming (Deadlock, Valorant, CS2)",
    "Watching Anime/TV Series",
    "Reading Light Novels, Web Novels, Manga, Manhwa, Manhua",
]

MILESTONES = [  # (label, [items]) — one row per year group, in order
    ("2023 · Senior High School", [
        "Division Festival of Talents: First Place, Sineliksik",
        "Regional Festival of Talents: First Place, Sineliksik",
        "DOST-SEI MERIT Scholarship",
    ]),
    ("A.Y. 2024–2025", [
        "CIT-U Parangal Awardee",
        "Certified C Programmer (CodeChum)",
    ]),
    ("A.Y. 2025–2026", [
        "CIT-U Parangal Awardee",
        "CIT-U Intramurals Champion: Honor of Kings",
        "Java OOP Certification (CodeChum)",
    ]),
    ("A.Y. 2026–2027", [
        "GCI World Data Science and Machine Learning Camp (ongoing)",
    ]),
]

CERTIFICATIONS = [  # shown as a bulleted list: "name (issuer)"
    {"name": "C Programming Certification", "issuer": "CodeChum / CIT-U"}, 
    {"name": "Java OOP Certification", "issuer": "CodeChum / CIT-U"}, 
    {"name": "Claude Code 101", "issuer": "Claude Academy"},
]

# Skills: grouped by category, in display order.
#   skill: my own rating on a 1-5 scale, or None if not rated yet (left out of the chart).
#     1 Beginner · 2 Basic · 3 Comfortable · 4 Proficient · 5 Advanced
#   Any tech used in PROJECTS but missing here is still shown, under
#   "Uncategorized", so the two lists can't silently drift apart.
SKILL_SCALE = {1: "Beginner", 2: "Basic", 3: "Comfortable", 4: "Proficient", 5: "Advanced"}

SKILLS = {
    "Languages": {
        "Python": 5,  
        "Java": 4,  
        "Kotlin": 5,
        "C#": 3,
        "JavaScript": 4,
        "C": 5,
    },
    "Frameworks & Libraries": {
        "Django": 4,  
        "Streamlit": 3,
        "Blazor": 3,
        "Tailwind CSS": 4,
        "NumPy": 4,
        "Pandas": 4,
    },
    "Tools & Databases": {
        "SQLite": 4,
        "PostgreSQL": 3,
    },
    "Areas & Practices": {
        "Web Development": 4,  
        "Backend Development": 3,
        "Object-Oriented Design": 5,
        "Design Patterns": 5,
        "RAG": 3,
        "AI Agents": 3,
        "Workflow Automation": 2,
    },
}

# Projects: shown in this order.
#   category:    one of PROJECT_CATEGORIES
#   status:      one of PROJECT_STATUSES, or None if not set
#   role:        what I did on the project
#   outcome:     what came of it (shipped, grade, users, what I learned...)
#   link:        URL, or "" if there isn't one
#   image:       screenshot path (see Images above)
#   image_ratio: (width, height) of the slot the screenshot is fitted into
#   caption:     short line shown under the screenshot
PROJECT_CATEGORIES = ["Web App", "AI / ML", "Mobile"]
PROJECT_STATUSES = ["In progress", "Completed", "Prototype"]

PROJECTS = [  # completed first, then in progress
    {
        "title": "ResiboReportAI",
        "category": "AI / ML",
        "desc": "A personal project of mine intended for businesses to digitalize their "
                "incoming and outgoing GCash transactions, securely.",
        "tech": ["Python", "Streamlit"],
        "status": "Completed",
        "role": "Solo developer: AI integration, data processing, Streamlit app",
        "outcome": "A working app that reads GCash receipt screenshots and turns them into a "
                   "transaction record.",
        "link": "",
        "image": "assets/images/img_resiboreport.jpg",
        "image_ratio": (3, 2),
        "caption": "ResiboReportAI: receipt upload screen",
    },
    {
        "title": "VizuaLearn",
        "category": "Mobile",
        "desc": "AI-based flash cards and mind-map maker. A personal project of mine with "
                "the aim of revolutionizing how students learn with AI & Technology.",
        "tech": ["Kotlin", "SQLite"],
        "status": "Completed",
        "role": "Solo developer: Android app (Kotlin), local database (SQLite), AI features",
        "outcome": "A working Android app that generates flash cards and mind maps from study "
                   "material.",
        "link": "",
        "image": "assets/images/img_vizuaLearn.png",
        "image_ratio": (1, 1),
        "caption": "VizuaLearn: app logo",
    },
    {
        "title": "AutoLease",
        "category": "Web App",
        "desc": "A platform for people looking for rent and companies/people wanting "
                "to rent out their cars, all in one place.",
        "tech": ["Python", "Django", "PostgreSQL"],
        "status": "In progress",
        "role": "Solo developer: full stack (Django, PostgreSQL), database design",
        "outcome": "Landing, login, register, home, profile, and settings screens working on Django "
                   "with Supabase PostgreSQL; ERD designed. Next: fleet and booking features.",
        "link": "",
        "image": "assets/images/img_autoLease.jpg",
        "image_ratio": (3, 2),
        "caption": "AutoLease: landing page",
    },
    {
        "title": "LuxWatch",
        "category": "Web App",
        "desc": "A platform for watch collectors to buy, sell, trade luxury watches "
                "with complete security and user protection",
        "tech": ["C#", "Blazor", "Tailwind CSS"],
        "status": "In progress",
        "role": "Solo developer: UI/UX, front end (Blazor + Tailwind), data modeling",
        "outcome": "Landing page, Discover flow, watch detail page, and seller rating/comment page "
                   "built; UML class diagram and initial C# models done. Next: the marketplace "
                   "dashboard with filters and pagination.",
        "link": "",
        "image": "assets/images/img_luxwatch.jpg",
        "image_ratio": (3, 2),
        "caption": "LuxWatch: landing page",
    },
]
