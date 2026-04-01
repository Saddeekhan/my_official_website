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
    color_map = {
        "Plant Genetics": "#2e8b57",
        "Bioinformatics": "#1f6feb",
        "PhD Positions": "#d97706",
        "Research": "#7c3aed",
        "Current Affairs": "#c2410c",
        "Opportunities": "#0f766e",
    }
    return color_map.get(category, "#3b5b52")


def render_post_card(post: pd.Series) -> None:
    pill_color = get_category_color(post["category"])
    date_text = "No date"
    if pd.notna(post["date"]):
        date_text = post["date"].strftime("%d %B %Y")

    st.markdown(
        f"""
        <div class="post-card">
          <span class="post-pill" style="background:{pill_color};">
            {post["category"]}
          </span>
          <div class="post-title">{post["title"]}</div>
          <div class="post-date">{date_text}</div>
          <div class="post-summary">{post["summary"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Read full post"):
        st.markdown(read_post_md(post["file"]))


# ---------- Custom styling ----------
st.markdown(
    """
    <style>
      .block-container {
        padding-top: 1.6rem;
        padding-bottom: 2rem;
        max-width: 1200px;
      }
      .main-title {
        font-size: 3rem;
        font-weight: 800;
        color: #0f3d2e;
        margin-bottom: 0.2rem;
        line-height: 1.1;
      }
      .subtitle {
        font-size: 1.15rem;
        color: #456b5d;
        margin-bottom: 1rem;
      }
      .hero-box {
        background: linear-gradient(135deg, #f4fbf7 0%, #edf6ff 100%);
        border: 1px solid #dceee4;
        border-radius: 22px;
        padding: 1.4rem;
        box-shadow: 0 10px 30px rgba(15, 61, 46, 0.06);
        margin-bottom: 1.2rem;
      }
      .section-title {
        font-size: 1.55rem;
        font-weight: 700;
        color: #143b2f;
        margin-top: 0.6rem;
        margin-bottom: 0.7rem;
      }
      .mini-note {
        color: #5b6e67;
        font-size: 0.96rem;
        margin-bottom: 1rem;
      }
      .stat-card {
        background: white;
        border: 1px solid #e4efe8;
        border-radius: 18px;
        padding: 1rem;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.03);
        text-align: center;
      }
      .stat-number {
        font-size: 1.7rem;
        font-weight: 800;
        color: #0f3d2e;
        line-height: 1;
        margin-bottom: 0.3rem;
      }
      .stat-label {
        font-size: 0.92rem;
        color: #5d6d66;
      }
      .post-card {
        background: white;
        border: 1px solid #e7efe9;
        border-radius: 20px;
        padding: 1rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.04);
        margin-bottom: 1rem;
      }
      .post-pill {
        display: inline-block;
        padding: 0.28rem 0.72rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.6rem;
        letter-spacing: 0.2px;
      }
      .post-title {
        font-size: 1.22rem;
        font-weight: 700;
        color: #143b2f;
        margin-bottom: 0.25rem;
        line-height: 1.25;
      }
      .post-date {
        font-size: 0.86rem;
        color: #76857f;
        margin-bottom: 0.7rem;
      }
      .post-summary {
        font-size: 0.98rem;
        color: #394641;
        margin-bottom: 0.2rem;
      }
      .footer-box {
        text-align: center;
        color: #63736d;
        font-size: 0.92rem;
        padding: 1rem 0 0.5rem 0;
      }
      .sidebar-title {
        color: #143b2f;
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 0.4rem;
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
st.sidebar.markdown(
    '<div class="sidebar-title">Site Controls</div>', unsafe_allow_html=True
)
selected_category = st.sidebar.selectbox("Browse by category", all_categories)
show_featured_only = st.sidebar.checkbox("Show featured only", value=False)

st.sidebar.markdown("---")
st.sidebar.markdown(
    '<div class="sidebar-title">About this website</div>', unsafe_allow_html=True
)
st.sidebar.write(
    """
    A personal academic platform for plant genetics, bioinformatics, research commentary,
    and PhD opportunities.
    """
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    '<div class="sidebar-title">Recent Posts</div>', unsafe_allow_html=True
)

if posts_df.empty:
    st.sidebar.write("No posts yet.")
else:
    for _, row in posts_df.head(5).iterrows():
        st.sidebar.write(f"• {row['title']}")

st.sidebar.markdown("---")
st.sidebar.markdown(
    '<div class="sidebar-title">Focus Areas</div>', unsafe_allow_html=True
)
st.sidebar.write("• Plant Genetics")
st.sidebar.write("• Bioinformatics")
st.sidebar.write("• Research Insights")
st.sidebar.write("• PhD Opportunities")
st.sidebar.write("• Scientific Commentary")

# ---------- Hero section ----------
left_col, right_col = st.columns([1.1, 2.2], gap="large")

with left_col:
    try:
        if PROFILE_IMG.exists():
            st.image(str(PROFILE_IMG), use_container_width=True)
        else:
            st.info("Add your profile image to assets/profile.jpg")
    except Exception:
        st.warning("Profile image could not be loaded. Please use a valid JPG or PNG.")

with right_col:
    st.markdown('<div class="hero-box">', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Saad Khan</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Plant Genetics | Bioinformatics | Research Communication | Academic Opportunities</div>',
        unsafe_allow_html=True,
    )
    st.write(
        """
        Welcome to my official academic website. This platform is dedicated to sharing research insights,
        scientific commentary, current affairs in plant science, bioinformatics topics, and academic opportunities
        including PhD positions, scholarships, and research updates.
        """
    )
    st.write(
        """
        My goal is to make scientific information more accessible, useful, and connected to real academic
        and community needs.
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
          <div class="stat-label">Published Posts</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with stat2:
    st.markdown(
        f"""
        <div class="stat-card">
          <div class="stat-number">{total_categories}</div>
          <div class="stat-label">Content Categories</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with stat3:
    st.markdown(
        f"""
        <div class="stat-card">
          <div class="stat-number">{featured_count}</div>
          <div class="stat-label">Featured Articles</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- Featured posts ----------
st.markdown('<div class="section-title">Featured Posts</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="mini-note">Highlighted articles and research notes selected for quick access.</div>',
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
st.markdown('<div class="section-title">Latest Posts</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="mini-note">Recent updates, opportunities, and scientific commentary.</div>',
    unsafe_allow_html=True,
)

filtered_df = posts_df.copy()

if not filtered_df.empty and selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]

if not filtered_df.empty and show_featured_only:
    filtered_df = filtered_df[filtered_df["featured"] == True]

if filtered_df.empty:
    st.warning("No posts found for this filter.")
else:
    for _, row in filtered_df.iterrows():
        render_post_card(row)

# ---------- Footer ----------
st.markdown("---")
st.markdown(
    """
    <div class="footer-box">
      © 2026 Saad Khan | Plant Genetics & Bioinformatics Academic Website
    </div>
    """,
    unsafe_allow_html=True,
)
