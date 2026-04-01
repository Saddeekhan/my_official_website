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

# Optional: set your links (keep empty if you do not want to show them)
LINK_GITHUB = "https://github.com/Saddeekhan"
LINK_LINKEDIN = ""  # add if you want
LINK_RESEARCHGATE = ""  # add if you want
LINK_EMAIL = ""  # e.g. "mailto:your@email.com"


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
    # Extra-bright palette
    color_map = {
        "Plant Genetics": "#00D2A3",
        "Bioinformatics": "#00A3FF",
        "PhD Positions": "#FFB703",
        "Research": "#7C4DFF",
        "Current Affairs": "#FF5C8A",
        "Opportunities": "#00E5FF",
        "General": "#111827",
    }
    return color_map.get(category, "#111827")


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


# ---------- Ultra-bright custom styling ----------
st.markdown(
    """
    <style>
      :root{
        --ink:#0B1020;
        --muted:#54657A;

        --a:#00D2A3;   /* teal */
        --b:#00A3FF;   /* bright blue */
        --c:#7C4DFF;   /* violet */
        --d:#FFB703;   /* orange */
        --e:#00E5FF;   /* aqua */
        --f:#FF5C8A;   /* pink */
      }

      .stApp{
        background:
          radial-gradient(900px 600px at 12% 10%, rgba(0,163,255,.28), transparent 60%),
          radial-gradient(900px 600px at 90% 10%, rgba(124,77,255,.26), transparent 60%),
          radial-gradient(900px 600px at 15% 90%, rgba(0,210,163,.28), transparent 60%),
          radial-gradient(700px 500px at 92% 85%, rgba(255,92,138,.20), transparent 62%),
          linear-gradient(180deg, #F6FBFF 0%, #F7FFF9 100%);
      }

      .block-container{
        padding-top: 1.1rem;
        padding-bottom: 2rem;
        max-width: 1240px;
      }

      /* Hero */
      .hero{
        border-radius: 24px;
        padding: 1.15rem 1.2rem;
        border: 1px solid rgba(231,238,245,.95);
        background:
          linear-gradient(120deg, rgba(0,163,255,.18), rgba(0,210,163,.18), rgba(124,77,255,.16), rgba(255,183,3,.14));
        box-shadow: 0 18px 50px rgba(16, 24, 40, 0.10);
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
      }

      .hero::before{
        content:"";
        position:absolute;
        inset:-2px;
        background:
          radial-gradient(500px 200px at 20% 30%, rgba(255,255,255,.45), transparent 60%),
          radial-gradient(420px 220px at 80% 20%, rgba(255,255,255,.35), transparent 60%),
          radial-gradient(520px 240px at 70% 80%, rgba(255,255,255,.25), transparent 62%);
        pointer-events:none;
      }

      .main-title{
        font-size: 3.05rem;
        font-weight: 950;
        color: var(--ink);
        line-height: 1.03;
        margin: 0;
        letter-spacing: -0.5px;
        position: relative;
        z-index: 1;
      }

      .subtitle{
        font-size: 1.06rem;
        color: rgba(11,16,32,.78);
        margin-top: 0.40rem;
        margin-bottom: 0.1rem;
        position: relative;
        z-index: 1;
      }

      .chips{
        margin-top: 0.70rem;
        display:flex;
        gap:0.5rem;
        flex-wrap:wrap;
        position: relative;
        z-index: 1;
      }

      .chip{
        display:inline-flex;
        align-items:center;
        gap:0.38rem;
        padding: 0.36rem 0.75rem;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 800;
        border: 1px solid rgba(255,255,255,.70);
        background: rgba(255,255,255,.70);
        color: rgba(11,16,32,.95);
        backdrop-filter: blur(10px);
      }

      .chip-dot{
        width:10px;
        height:10px;
        border-radius:999px;
        display:inline-block;
        box-shadow: 0 0 0 3px rgba(255,255,255,.55);
      }

      .cta-row{
        display:flex;
        gap: 0.6rem;
        flex-wrap:wrap;
        margin-top: 0.85rem;
        position: relative;
        z-index: 1;
      }

      a.cta-btn{
        text-decoration:none !important;
        display:inline-flex;
        align-items:center;
        gap:0.4rem;
        padding: 0.55rem 0.9rem;
        border-radius: 14px;
        font-weight: 900;
        font-size: 0.92rem;
        border: 1px solid rgba(255,255,255,.70);
        background: rgba(255,255,255,.80);
        color: rgba(11,16,32,.95);
        box-shadow: 0 12px 28px rgba(16, 24, 40, 0.10);
        transition: transform .12s ease, box-shadow .12s ease;
      }
      a.cta-btn:hover{
        transform: translateY(-1px);
        box-shadow: 0 16px 36px rgba(16, 24, 40, 0.14);
      }

      /* Stats */
      .stat-card{
        background: rgba(255,255,255,.85);
        border: 1px solid rgba(231,238,245,.95);
        border-radius: 18px;
        padding: 1rem 1rem;
        box-shadow: 0 14px 35px rgba(16, 24, 40, 0.08);
        backdrop-filter: blur(10px);
        position: relative;
        overflow:hidden;
      }

      .stat-card::after{
        content:"";
        position:absolute;
        right:-40px;
        top:-40px;
        width:160px;
        height:160px;
        background: radial-gradient(circle, rgba(0,163,255,.22), transparent 60%);
        transform: rotate(20deg);
      }

      .stat-number{
        font-size: 2.0rem;
        font-weight: 950;
        color: var(--ink);
        line-height: 1;
        position: relative;
        z-index: 1;
      }

      .stat-label{
        font-size: 0.92rem;
        color: var(--muted);
        margin-top: 0.35rem;
        position: relative;
        z-index: 1;
      }

      /* Sections */
      .section-title{
        font-size: 1.62rem;
        font-weight: 950;
        color: var(--ink);
        margin-top: 0.75rem;
        margin-bottom: 0.35rem;
      }

      .mini-note{
        color: var(--muted);
        font-size: 0.98rem;
        margin-bottom: 0.95rem;
      }

      /* Post cards */
      .post-card{
        background: rgba(255,255,255,.88);
        border-radius: 20px;
        padding: 1rem 1rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        position: relative;
        overflow:hidden;
        box-shadow: 0 16px 40px rgba(16, 24, 40, 0.09);
        border: 1px solid rgba(231,238,245,.95);
      }

      .post-card::before{
        content:"";
        position:absolute;
        inset:0;
        padding:1px;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(0,163,255,.55), rgba(0,210,163,.55), rgba(124,77,255,.45), rgba(255,183,3,.45));
        -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events:none;
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
        font-weight: 900;
        color: white;
        letter-spacing: 0.2px;
        box-shadow: 0 12px 24px rgba(16,24,40,.10);
      }

      .post-title{
        font-size: 1.2rem;
        font-weight: 950;
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
        font-size: 0.99rem;
        color: rgba(11,16,32,.90);
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
        font-weight: 950;
        font-size: 1.02rem;
        margin-bottom: 0.35rem;
      }

      div.stButton > button{
        border-radius: 14px !important;
        font-weight: 900 !important;
        border: 1px solid rgba(231,238,245,.95) !important;
        box-shadow: 0 12px 28px rgba(16, 24, 40, 0.08) !important;
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
st.sidebar.markdown('<div class="sidebar-title">Links</div>', unsafe_allow_html=True)
if LINK_GITHUB:
    st.sidebar.write(f"• GitHub: {LINK_GITHUB}")
if LINK_LINKEDIN:
    st.sidebar.write(f"• LinkedIn: {LINK_LINKEDIN}")
if LINK_RESEARCHGATE:
    st.sidebar.write(f"• ResearchGate: {LINK_RESEARCHGATE}")

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-title">Recent Posts</div>', unsafe_allow_html=True)
if posts_df.empty:
    st.sidebar.write("No posts yet.")
else:
    for _, row in posts_df.head(6).iterrows():
        st.sidebar.write(f"• {row['title']}")

# ---------- Hero ----------
col_img, col_hero = st.columns([1.15, 2.55], gap="large")

with col_img:
    try:
        if PROFILE_IMG.exists():
            st.image(str(PROFILE_IMG), use_container_width=True)
        else:
            st.info("Add your profile image to assets/profile.jpg")
    except Exception:
        st.warning("Profile image could not be loaded. Please use a valid JPG or PNG.")

with col_hero:
    st.markdown('<div class="hero">', unsafe_allow_html=True)
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
          <span class="chip"><span class="chip-dot" style="background:var(--f)"></span>Science Communication</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        """
        Welcome to my academic website. I share research insights, practical bioinformatics content,
        and curated academic opportunities. The goal is bright, clear, and useful science communication
        with strong technical depth.
        """
    )

    # CTA buttons (only show if link exists)
    btns = []
    if LINK_EMAIL:
        btns.append(f'<a class="cta-btn" href="{LINK_EMAIL}">✉️ Email</a>')
    if LINK_GITHUB:
        btns.append(f'<a class="cta-btn" href="{LINK_GITHUB}" target="_blank">💻 GitHub</a>')
    if LINK_LINKEDIN:
        btns.append(f'<a class="cta-btn" href="{LINK_LINKEDIN}" target="_blank">🔗 LinkedIn</a>')
    if LINK_RESEARCHGATE:
        btns.append(f'<a class="cta-btn" href="{LINK_RESEARCHGATE}" target="_blank">📚 ResearchGate</a>')

    if btns:
        st.markdown(f'<div class="cta-row">{"".join(btns)}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Stats ----------
s1, s2, s3 = st.columns(3)

with s1:
    st.markdown(
        f"""
        <div class="stat-card">
          <div class="stat-number">{total_posts}</div>
          <div class="stat-label">Published posts</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with s2:
    st.markdown(
        f"""
        <div class="stat-card">
          <div class="stat-number">{total_categories}</div>
          <div class="stat-label">Categories</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with s3:
    st.markdown(
        f"""
        <div class="stat-card">
          <div class="stat-number">{featured_count}</div>
          <div class="stat-label">Featured</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- Featured ----------
st.markdown('<div class="section-title">Featured</div>', unsafe_allow_html=True)
st.markdown('<div class="mini-note">High-impact reading selected for quick access.</div>', unsafe_allow_html=True)

if featured_df.empty:
    st.info("No featured posts yet.")
else:
    cols = st.columns(2)
    for i, (_, row) in enumerate(featured_df.iterrows()):
        with cols[i % 2]:
            render_post_card(row)

# ---------- Latest ----------
st.markdown('<div class="section-title">Latest</div>', unsafe_allow_html=True)
st.markdown('<div class="mini-note">Recent updates, opportunities, and scientific commentary.</div>', unsafe_allow_html=True)

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
