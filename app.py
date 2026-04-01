cd my_official_website && \
mkdir -p .streamlit && \

cat > .streamlit/config.toml <<'TOML'
[theme]
primaryColor = "#00C2FF"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F6FBFF"
textColor = "#0B1B2B"
font = "sans serif"
TOML

cat > content.py <<'PY'
import json
from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).parent
POSTS_JSON = BASE_DIR / "data" / "posts.json"

@st.cache_data(show_spinner=False)
def load_posts() -> pd.DataFrame:
    cols = ["title", "file", "category", "date", "summary", "featured"]
    if not POSTS_JSON.exists():
        return pd.DataFrame(columns=cols)

    with open(POSTS_JSON, "r", encoding="utf-8") as f:
        posts = json.load(f)

    df = pd.DataFrame(posts)
    if df.empty:
        return pd.DataFrame(columns=cols)

    for c in cols:
        if c not in df.columns:
            df[c] = None

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["featured"] = df["featured"].fillna(False).astype(bool)
    df["title"] = df["title"].fillna("")
    df["file"] = df["file"].fillna("")
    df["category"] = df["category"].fillna("General")
    df["summary"] = df["summary"].fillna("")
    df = df.sort_values("date", ascending=False).reset_index(drop=True)
    return df

def read_post_md(file_path: str) -> str:
    path = BASE_DIR / file_path
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Post content not found."
PY

cat > site_style.py <<'PY'
import streamlit as st

def inject_global_css() -> None:
    st.markdown(
        """
<style>
/* Layout */
.block-container {max-width: 1200px; padding-top: 1.2rem; padding-bottom: 2.2rem;}
[data-testid="stSidebar"] {border-right: 1px solid #E8F1FF;}

/* Typography */
.h-title {font-size: 2.8rem; font-weight: 900; line-height: 1.05; margin: 0;}
.h-sub {font-size: 1.05rem; color: #315066; margin-top: 0.45rem; margin-bottom: 0;}
.kicker {font-size: 0.9rem; font-weight: 800; letter-spacing: 0.08em; color: #0077B6; text-transform: uppercase;}

/* Header / hero */
.hero {
  background: radial-gradient(1200px 500px at 15% 0%, rgba(0,194,255,0.18), transparent 60%),
              radial-gradient(900px 420px at 85% 15%, rgba(124,58,237,0.16), transparent 60%),
              linear-gradient(135deg, #F6FBFF 0%, #FFFFFF 70%);
  border: 1px solid #E8F1FF;
  border-radius: 22px;
  padding: 1.25rem 1.25rem;
  box-shadow: 0 14px 40px rgba(10, 30, 70, 0.08);
}

/* Cards */
.card {
  background: #FFFFFF;
  border: 1px solid #EAF2FF;
  border-radius: 18px;
  padding: 1rem 1rem;
  box-shadow: 0 10px 26px rgba(10, 30, 70, 0.06);
}
.card h3 {margin: 0 0 0.35rem 0; font-size: 1.05rem;}
.card p {margin: 0; color: #36576E; font-size: 0.95rem;}

/* Small chips */
.chip {
  display: inline-block;
  padding: 0.22rem 0.6rem;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 800;
  color: #0B1B2B;
  background: #E9F7FF;
  border: 1px solid #CFEFFF;
}

/* Post card */
.post {
  background: #FFFFFF;
  border: 1px solid #EAF2FF;
  border-radius: 18px;
  padding: 1rem;
  box-shadow: 0 10px 26px rgba(10, 30, 70, 0.06);
}
.post-title {font-size: 1.15rem; font-weight: 850; margin: 0.15rem 0 0.35rem 0; color: #0B1B2B;}
.post-meta {font-size: 0.85rem; color: #5A7386; margin-bottom: 0.6rem;}
.post-summary {font-size: 0.97rem; color: #2E4A5F; margin-bottom: 0.2rem;}

/* Buttons row */
.btnrow a {
  display: inline-block;
  text-decoration: none;
  font-weight: 850;
  border-radius: 14px;
  padding: 0.55rem 0.8rem;
  margin-right: 0.5rem;
  border: 1px solid #D9ECFF;
  background: #FFFFFF;
  color: #0B1B2B;
}
.btnrow a.primary {
  background: linear-gradient(135deg, #00C2FF 0%, #2F80ED 100%);
  color: white;
  border: 0;
}

/* Section header */
.sec {margin-top: 1.2rem;}
.sec h2 {font-size: 1.4rem; font-weight: 900; margin: 0 0 0.25rem 0;}
.sec p {margin: 0 0 0.8rem 0; color: #476274;}
</style>
        """,
        unsafe_allow_html=True,
    )

def sidebar() -> None:
    st.sidebar.markdown("### Site Controls")
    st.sidebar.caption("Use filters on the Home page to browse posts.")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Quick links")
    st.sidebar.markdown("- Home\n- About\n- Research\n- Opportunities\n- Contact")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Focus areas")
    st.sidebar.markdown("• Plant Genetics\n\n• Bioinformatics\n\n• Omics + Pipelines\n\n• Academic Opportunities")
PY

cat > app.py <<'PY'
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import streamlit as st

from content import load_posts, read_post_md
from site_style import inject_global_css, sidebar

st.set_page_config(
    page_title="Saad Khan | Plant Genetics & Bioinformatics",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).parent
PROFILE_IMG = BASE_DIR / "assets" / "profile.jpg"
CV_PDF = BASE_DIR / "assets" / "Saad_Khan_CV.pdf"  # optional if you add it

inject_global_css()
sidebar()

posts_df = load_posts()
featured_df = posts_df[posts_df["featured"] == True] if not posts_df.empty else pd.DataFrame()

def fmt_date(x) -> str:
    if pd.notna(x):
        return x.strftime("%d %b %Y")
    return "No date"

def pill_color(category: str) -> str:
    cmap = {
        "Plant Genetics": "#E9FFF2",
        "Bioinformatics": "#E9F7FF",
        "PhD Positions": "#FFF4E6",
        "Opportunities": "#EAF7FF",
        "Research": "#F3ECFF",
        "Current Affairs": "#FFECEC",
    }
    return cmap.get(category, "#E9F7FF")

def render_post(post: pd.Series) -> None:
    bg = pill_color(post["category"])
    st.markdown(
        f"""
<div class="post">
  <span class="chip" style="background:{bg};">{post["category"]}</span>
  <div class="post-title">{post["title"]}</div>
  <div class="post-meta">{fmt_date(post["date"])}</div>
  <div class="post-summary">{post["summary"]}</div>
</div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("Read full post"):
        st.markdown(read_post_md(post["file"]))

# HERO
left, right = st.columns([1.0, 2.2], gap="large")
with left:
    if PROFILE_IMG.exists():
        st.image(str(PROFILE_IMG), use_container_width=True)
    else:
        st.info("Add your profile image to assets/profile.jpg")

with right:
    cv_link = ""
    if CV_PDF.exists():
        cv_link = f'<a class="primary" href="{CV_PDF.name}" target="_blank">Download CV</a>'
    mailto = "mailto:saadkhanuom@gmail.com?subject=" + quote("Hello Saad")
    st.markdown(
        f"""
<div class="hero">
  <div class="kicker">Plant genetics • bioinformatics • research communication</div>
  <h1 class="h-title">Saad Khan</h1>
  <p class="h-sub">
    I build reproducible genomics pipelines and translate sequencing data into clear biological insight.
    This site shares my research notes, opportunities, and practical bioinformatics writing.
  </p>
  <div style="height:0.85rem"></div>
  <div class="btnrow">
    {cv_link}
    <a class="primary" href="{mailto}">Email</a>
    <a href="https://github.com/Saddeekhan" target="_blank">GitHub</a>
    <a href="https://www.researchgate.net/profile/Saad-Khan-111" target="_blank">ResearchGate</a>
    <a href="https://www.linkedin.com/in/saad-khan-bioinformatician-434586157" target="_blank">LinkedIn</a>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )

# HIGHLIGHTS
st.markdown('<div class="sec"><h2>Highlights</h2><p>Quick overview of what you will find here.</p></div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="card"><h3>Research focus</h3><p>Plant genomics, transcriptomics, comparative analysis, and computational biology.</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="card"><h3>Toolbox</h3><p>Python, R, Linux, Git, Conda, reproducible pipelines, omics interpretation.</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="card"><h3>Opportunities</h3><p>Curated PhD calls, scholarships, and research roles that match your interests.</p></div>', unsafe_allow_html=True)

# POSTS
st.markdown('<div class="sec"><h2>Browse posts</h2><p>Search, filter, and open any post.</p></div>', unsafe_allow_html=True)

top = st.columns([1.6, 1.0, 1.0])
with top[0]:
    q = st.text_input("Search", placeholder="Search title, summary, or category...")
with top[1]:
    categories = ["All"] + (sorted(posts_df["category"].dropna().unique().tolist()) if not posts_df.empty else [])
    cat = st.selectbox("Category", categories)
with top[2]:
    featured_only = st.toggle("Featured only", value=False)

filtered = posts_df.copy()
if not filtered.empty:
    if q.strip():
        qq = q.strip().lower()
        filtered = filtered[
            filtered["title"].str.lower().str.contains(qq)
            | filtered["summary"].str.lower().str.contains(qq)
            | filtered["category"].str.lower().str.contains(qq)
        ]
    if cat != "All":
        filtered = filtered[filtered["category"] == cat]
    if featured_only:
        filtered = filtered[filtered["featured"] == True]

if filtered.empty:
    st.warning("No posts found for this filter.")
else:
    if not featured_df.empty and not featured_only and cat in ["All"] and not q.strip():
        st.markdown('<div class="sec"><h2>Featured</h2><p>Highlighted articles selected for quick access.</p></div>', unsafe_allow_html=True)
        for _, row in featured_df.iterrows():
            render_post(row)

    st.markdown('<div class="sec"><h2>Latest</h2><p>Recent updates and posts.</p></div>', unsafe_allow_html=True)
    for _, row in filtered.iterrows():
        render_post(row)

st.markdown("---")
st.caption("© 2026 Saad Khan | Plant Genetics & Bioinformatics")
PY

cat > pages/1_About.py <<'PY'
import streamlit as st
from site_style import inject_global_css, sidebar

st.set_page_config(page_title="About | Saad Khan", page_icon="🧬", layout="wide")
inject_global_css()
sidebar()

st.markdown('<div class="sec"><h2>About</h2><p>Short, clear, and professional overview.</p></div>', unsafe_allow_html=True)

c1, c2 = st.columns([1.5, 1.2], gap="large")
with c1:
    st.markdown(
        """
<div class="card">
  <h3>Who I am</h3>
  <p>
    I work at the intersection of genetics and computation, building reproducible workflows that turn sequencing data into
    biological insight. My interests include gene regulation, comparative genomics, and computational approaches that
    support crop improvement and stress biology.
  </p>
</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
<div class="card" style="margin-top:0.9rem">
  <h3>What I care about</h3>
  <p>
    I enjoy projects where careful data work leads to real biological answers: clear hypotheses, robust pipelines, and
    results that can be reused and built on.
  </p>
</div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
<div class="card">
  <h3>Core strengths</h3>
  <p>• RNA-seq and transcriptomics workflows</p>
  <p>• Comparative genomics and ortholog analysis</p>
  <p>• Python, R, Linux, Git, Conda</p>
  <p>• Clear scientific writing and communication</p>
</div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.caption("Tip: If you want, I can convert this page into a timeline style (Education, Research, Publications).")
PY

cat > pages/2_Research.py <<'PY'
import streamlit as st
from site_style import inject_global_css, sidebar

st.set_page_config(page_title="Research | Saad Khan", page_icon="🧬", layout="wide")
inject_global_css()
sidebar()

st.markdown('<div class="sec"><h2>Research</h2><p>Selected themes and the kind of work I enjoy doing.</p></div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="card"><h3>Transcriptomics</h3><p>RNA-seq pipelines, differential expression, functional interpretation, network thinking.</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="card"><h3>Comparative genomics</h3><p>Ortholog prediction, cross-species comparison, pathway level analysis.</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="card"><h3>Reproducible pipelines</h3><p>Clean workflows with clear inputs/outputs, version control, and documentation.</p></div>', unsafe_allow_html=True)

st.markdown('<div class="sec"><h2>Selected outputs</h2><p>Add 3 to 6 items here (papers, preprints, datasets, tools).</p></div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="card">
  <h3>Example template</h3>
  <p><b>Project:</b> Comparative transcriptomics in Arabidopsis (floral transition)</p>
  <p><b>Methods:</b> QC, alignment, quantification, DE, functional analysis, reproducible scripts</p>
  <p><b>Outcome:</b> Candidate gene sets and interpretable biological story ready for publication</p>
</div>
    """,
    unsafe_allow_html=True,
)
PY

cat > pages/3_Opportunities.py <<'PY'
import streamlit as st
from content import load_posts, read_post_md
from site_style import inject_global_css, sidebar

st.set_page_config(page_title="Opportunities | Saad Khan", page_icon="🧬", layout="wide")
inject_global_css()
sidebar()

st.markdown('<div class="sec"><h2>Opportunities</h2><p>PhD calls, internships, and funding options I share or track.</p></div>', unsafe_allow_html=True)

df = load_posts()
if df.empty:
    st.info("No posts found. Add opportunities in data/posts.json (category: Opportunities or PhD Positions).")
else:
    opp = df[df["category"].isin(["Opportunities", "PhD Positions"])].copy()
    if opp.empty:
        st.info("No opportunities posts yet. Add category = Opportunities or PhD Positions in posts.json.")
    else:
        for _, row in opp.iterrows():
            st.markdown(
                f"""
<div class="post">
  <span class="chip">{row["category"]}</span>
  <div class="post-title">{row["title"]}</div>
  <div class="post-meta">{row["date"].strftime("%d %b %Y") if row["date"] is not None else ""}</div>
  <div class="post-summary">{row["summary"]}</div>
</div>
                """,
                unsafe_allow_html=True,
            )
            with st.expander("Read full post"):
                st.markdown(read_post_md(row["file"]))
PY

cat > pages/4_Contact.py <<'PY'
from urllib.parse import quote
import streamlit as st
from site_style import inject_global_css, sidebar

st.set_page_config(page_title="Contact | Saad Khan", page_icon="🧬", layout="wide")
inject_global_css()
sidebar()

st.markdown('<div class="sec"><h2>Contact</h2><p>Quick ways to reach me.</p></div>', unsafe_allow_html=True)

c1, c2 = st.columns([1.2, 1.6], gap="large")

with c1:
    st.markdown(
        """
<div class="card">
  <h3>Direct</h3>
  <p><b>Email:</b> saadkhanuom@gmail.com</p>
  <p><b>LinkedIn:</b> linkedin.com/in/saad-khan-bioinformatician-434586157</p>
  <p><b>ResearchGate:</b> researchgate.net/profile/Saad-Khan-111</p>
  <p><b>GitHub:</b> github.com/Saddeekhan</p>
</div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown('<div class="card"><h3>Send a message</h3><p>This opens your email app with a pre-filled message.</p></div>', unsafe_allow_html=True)
    with st.form("contact_form"):
        name = st.text_input("Your name")
        email = st.text_input("Your email (optional)")
        msg = st.text_area("Message", height=140)
        submitted = st.form_submit_button("Generate email link")

    if submitted:
        subject = quote(f"Website message from {name}".strip() or "Website message")
        body_lines = []
        if name.strip():
            body_lines.append(f"Name: {name.strip()}")
        if email.strip():
            body_lines.append(f"Email: {email.strip()}")
        body_lines.append("")
        body_lines.append(msg.strip())
        body = quote("\n".join(body_lines).strip())
        mailto = f"mailto:saadkhanuom@gmail.com?subject={subject}&body={body}"
        st.markdown(f'<div class="btnrow"><a class="primary" href="{mailto}">Open email draft</a></div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("If you want a real contact form (without email client), we can add a lightweight backend later.")
PY

git add . && \
git commit -m "Professional UI polish across pages" && \
git push
