import json
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Saad Khan | Plant Genetics & Bioinformatics",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).parent
POSTS_JSON = BASE_DIR / "data" / "posts.json"
PROFILE_IMG = BASE_DIR / "assets" / "profile.jpg"


def load_posts() -> pd.DataFrame:
    if not POSTS_JSON.exists():
        return pd.DataFrame(
            columns=["title", "file", "category", "date", "summary", "featured"]
        )

    with open(POSTS_JSON, "r", encoding="utf-8") as f:
        posts = json.load(f)

    df = pd.DataFrame(posts)
    if df.empty:
        return pd.DataFrame(
            columns=["title", "file", "category", "date", "summary", "featured"]
        )

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["featured"] = df["featured"].fillna(False)
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


def get_category_color(category: str) -> str:
    # Brighter palette
    color_map = {
        "Plant Genetics": "#00b894",
        "Bioinformatics": "#0984e3",
        "PhD Positions": "#f39c12",
        "Research": "#6c5ce7",
        "Current Affairs": "#e17055",
        "Opportunities": "#00cec9",
        "General": "#2d3436",
    }
    return color_map.get(category, "#2d3436")


def safe_date_str(dt) -> str:
    if pd.notna(dt):
        return dt.strftime("%d %B %Y")
    return "No date"


def render_post_card(post: pd.Series) -> None:
    pill_color = get_category_color(post["category"])
    date_text = safe_date_str(post["date"])

    st.markdown(
        f"""
        <div class="post-card">
          <div class="post-top">
            <span class="post-pill" style="background:{pill_color};">
              {post["category"]}
            </span>
            <span class="post-date">{date_text}</span>
          </div>

          <div class="post-title">{post["title"]}</div>
          <div class="post-summary">{post["summary"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Read full post"):
        st.markdown(read_post_md(post["file"]))


# ---------- Bright custom styling ----------
st.markdown(
    """
    <style>
      :root{
        --ink:#0b1220;
        --muted:#516070;
        --card:#ffffff;
        --border:#e7eef5;

        --a:#00b894;    /* teal */
        --b:#0984e3;    /* bright blue */
        --c:#6c5ce7;    /* violet */
        --d:#f39c12;    /* orange */
        --e:#00cec9;    /* aqua */
        --f:#e17055;    /* coral */
      }

      .stApp{
        background: radial-gradient(900px 600px at 10% 10%, rgba(9,132,227,.14), transparent 60%),
                    radial-gradient(900px 600px at 85% 10%, rgba(108,92,231,.14), transparent 60%),
                    radial-gradient(900px 600px at 20% 85%, rgba(0,184,148,.16), transparent 60%),
                    linear-gradient(180deg, #f8fbff 0%, #f7fffb 100%);
      }

      .block-container{
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1220px;
      }

      /* Top ribbon */
      .top-ribbon{
        border-radius: 22px;
        padding: 1rem 1.1rem;
        border: 1px solid rgba(231,238,245,.9);
        background: linear-gradient(120deg, rgba(9,132,227,.10), rgba(0,184,148,.10), rgba(108,92,231,.10));
        box-shadow: 0 18px 40px rgba(17, 24, 39, 0.06);
        margin-bottom: 1rem;
      }

      .main-title{
        font-size: 3rem;
        font-weight: 900;
        color: var(--ink);
        line-height: 1.05;
        margin: 0;
      }

      .subtitle{
        font-size: 1.05rem;
        color: var(--muted);
        margin-top: 0.35rem;
        margin-bottom: 0.1rem;
      }

      .chips{
        margin-top: 0.65rem;
        display:flex;
        gap:0.45rem;
        flex-wrap:wrap;
      }

      .chip{
        display:inline-flex;
        align-items:center;
        gap:0.35rem;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 700;
        border: 1px solid rgba(231,238,245,.9);
        background: rgba(255,255,255,.75);
        color: var(--ink);
        backdrop-filter: blur(8px);
      }

      .chip-dot{
        width:10px;
        height:10px;
        border-radius:999px;
        display:inline-block;
      }

      /* Cards */
      .stat-card{
        background: rgba(255,255,255,.85);
        border: 1px solid rgba(231,238,245,.95);
        border-radius: 18px;
        padding: 1rem 1rem;
        box-shadow: 0 12px 30px rgba(17, 24, 39, 0.06);
        text-align: left;
        backdrop-filter: blur(10px);
      }

      .stat-number{
        font-size: 1.9rem;
        font-weight: 900;
        color: var(--ink);
        line-height: 1;
      }

      .stat-label{
        font-size: 0.92rem;
        color: var(--muted);
        margin-top: 0.35rem;
      }

      .section-title{
        font-size: 1.55rem;
        font-weight: 900;
        color: var(--ink);
        margin-top: 0.65rem;
        margin-bottom: 0.35rem;
      }

      .mini-note{
        color: var(--muted);
        font-size: 0.97rem;
        margin-bottom: 0.9rem;
      }

      .post-card{
        background: rgba(255,255,255,.88);
        border: 1px solid rgba(231,238,245,.95);
        border-radius: 20px;
        padding: 1rem 1rem;
        box-shadow: 0 14px 35px rgba(17, 24, 39, 0.06);
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        transition: transform .12s ease, box-shadow .12s ease;
      }

      .post-card:hover{
        transform: translateY(-2px);
        box-shadow: 0 18px 45px rgba(17, 24, 39, 0.09);
      }

      .post-top{
        display:flex;
        justify-content: space-between;
        align-items:center;
        gap: 0.75rem;
        margin-bottom: 0.6rem;
      }

      .post-pill{
        display: inline-block;
        padding: 0.30rem 0.75rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 800;
        color: white;
        letter-spacing: 0.2px;
      }

      .post-title{
        font-size: 1.18rem;
        font-weight: 900;
        color: var(--ink);
        margin-bottom: 0.35rem;
        line-height: 1.25;
      }

      .post-date{
        font-size: 0.86rem;
        color: var(--muted);
        white-space: nowrap;
      }

      .post-summary{
        font-size: 0.98rem;
        color: #263445;
        margin-bottom: 0.15rem;
      }

      .footer-box{
        text-align: center;
        color: var(--muted);
        font-size: 0.92rem;
        padding: 1rem 0 0.5rem 0;
      }

      .sidebar-title{
        color: var(--ink);
        font-weight: 900;
        font-size: 1.02rem;
        margin-bottom: 0.35rem;
      }

      /* Make Streamlit buttons a bit brighter */
      div.stButton > button{
        border-radius: 12px;
        border: 1px solid rgba(231,238,245,.95);
        box-shadow: 0 10px 25px rgba(17, 24, 39, 0.06);
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Load data ----------
posts_df = load_posts()

if not posts_df.empty:
    featured_df = posts_df[posts_df["featured"] == True]
    all_categories = ["All"] + sorted(posts_df["category"].dropna().unique().tolist())
else:
    featured_df = pd.DataFrame()
    all_categories = ["All"]

total_posts = len(posts_df)
total_categories = posts_df["category"].nunique() if not posts_df.empty else 0
featured_count = len(featured_df)

# ---------- Sidebar ----------
st.sidebar.markdown('<div class="sidebar-title">Site Controls</div>', unsafe_allow_html=True)
selected_category = st.sidebar.selectbox("Browse by category", all_categories)
show_featured_only = st.sidebar.checkbox("Show featured only", value=False)

search_query = st.sidebar.text_input("Search posts", value="", placeholder="Title or keywords")

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-title">Quick Links</div>', unsafe_allow_html=True)

# Only include the GitHub link you already shared previously.
st.sidebar.markdown("• GitHub: https://github.com/Saddeekhan")

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-title">Recent Posts</div>', unsafe_allow_html=True)
if posts_df.empty:
    st.sidebar.write("No posts yet.")
else:
    for _, row in posts_df.head(6).iterrows():
        st.sidebar.write(f"• {row['title']}")

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-title">Focus Areas</div>', unsafe_allow_html=True)
st.sidebar.write("• Plant Genetics")
st.sidebar.write("• Bioinformatics")
st.sidebar.write("• Research Insights")
st.sidebar.write("• PhD Opportunities")
st.sidebar.write("• Scientific Commentary")

# ---------- Top ribbon / Hero ----------
top_left, top_right = st.columns([1.2, 2.4], gap="large")

with top_left:
    try:
        if PROFILE_IMG.exists():
            st.image(str(PROFILE_IMG), use_container_width=True)
        else:
            st.info("Add your profile image to assets/profile.jpg")
    except Exception:
        st.warning("Profile image could not be loaded. Please use a valid JPG or PNG.")

with top_right:
    st.markdown('<div class="top-ribbon">', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Saad Khan</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Plant Genetics | Bioinformatics | Transcriptomics | Academic Opportunities</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="chips">
          <span class="chip"><span class="chip-dot" style="background:var(--a)"></span>Plant Genomics</span>
          <span class="chip"><span class="chip-dot" style="background:var(--b)"></span>RNA-seq</span>
          <span class="chip"><span class="chip-dot" style="background:var(--c)"></span>Computational Biology</span>
          <span class="chip"><span class="chip-dot" style="background:var(--d)"></span>PhD Opportunities</span>
          <span class="chip"><span class="chip-dot" style="background:var(--e)"></span>Reproducible Pipelines</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        """
        Welcome to my academic website. I share research insights, practical bioinformatics content,
        and curated academic opportunities. The goal is clear, actionable science communication with
        strong technical depth.
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Stats ----------
stat1, stat2, stat3 = st.columns(3)

with stat1:
    st.markdown(
        f"""
        <div class="stat-card">
          <div class="stat-number">{total_posts}</div>
          <div class="stat-label">Published posts</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with stat2:
    st.markdown(
        f"""
        <div class="stat-card">
          <div class="stat-number">{total_categories}</div>
          <div class="stat-label">Categories</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with stat3:
    st.markdown(
        f"""
        <div class="stat-card">
          <div class="stat-number">{featured_count}</div>
          <div class="stat-label">Featured</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- Featured posts ----------
st.markdown('<div class="section-title">Featured</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="mini-note">Quick picks for high-impact reading.</div>',
    unsafe_allow_html=True,
)

if featured_df.empty:
    st.info("No featured posts yet.")
else:
    cols = st.columns(2)
    for i, (_, row) in enumerate(featured_df.iterrows()):
        with cols[i % 2]:
            render_post_card(row)

# ---------- Latest posts ----------
st.markdown('<div class="section-title">Latest</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="mini-note">Recent updates, opportunities, and scientific commentary.</div>',
    unsafe_allow_html=True,
)

filtered_df = posts_df.copy()

if not filtered_df.empty and selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]

if not filtered_df.empty and show_featured_only:
    filtered_df = filtered_df[filtered_df["featured"] == True]

if not filtered_df.empty and search_query.strip():
    q = search_query.strip().lower()
    filtered_df = filtered_df[
        filtered_df["title"].str.lower().str.contains(q)
        | filtered_df["summary"].str.lower().str.contains(q)
        | filtered_df["category"].str.lower().str.contains(q)
    ]

if filtered_df.empty:
    st.warning("No posts found for this filter.")
else:
    # Show latest in a brighter 2-column grid when possible
    cols = st.columns(2)
    for i, (_, row) in enumerate(filtered_df.iterrows()):
        with cols[i % 2]:
            render_post_card(row)

# ---------- Footer ----------
st.markdown("---")
st.markdown(
    """
    <div class="footer-box">
      © 2026 Saad Khan | Plant Genetics & Bioinformatics
    </div>
    """,
    unsafe_allow_html=True,
)
