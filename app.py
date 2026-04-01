import json
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Your Name | Plant Genetics & Bioinformatics",
    page_icon="🧬",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
POSTS_JSON = BASE_DIR / "data" / "posts.json"
PROFILE_IMG = BASE_DIR / "assets" / "profile.jpg"


def load_posts():
    with open(POSTS_JSON, "r", encoding="utf-8") as f:
        posts = json.load(f)
    df = pd.DataFrame(posts)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date", ascending=False).reset_index(drop=True)
    return df


def read_post_md(file_path: str) -> str:
    path = BASE_DIR / file_path
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Post content not found."


def render_post_card(post):
    with st.container(border=True):
        st.caption(f"{post['category']} | {post['date'].date()}")
        st.subheader(post["title"])
        st.write(post["summary"])
        with st.expander("Read post"):
            st.markdown(read_post_md(post["file"]))


posts_df = load_posts()
featured_df = posts_df[posts_df["featured"] == True]
all_categories = ["All"] + sorted(posts_df["category"].unique().tolist())

st.title("Your Name")
st.subheader("Plant Genetics | Bioinformatics | Research | Opportunities")

col1, col2 = st.columns([1, 2])

with col1:
    if PROFILE_IMG.exists():
        st.image(str(PROFILE_IMG), use_container_width=True)
    else:
        st.info("Add your profile image to assets/profile.jpg")

with col2:
    st.write(
        """
        Welcome to my official academic website.

        This platform is designed to share:
        - research insights in plant genetics and bioinformatics
        - scientific commentary and current affairs
        - PhD opportunities and academic announcements
        - publications, projects, and resources
        """
    )

st.markdown("---")

st.sidebar.title("Navigation")
st.sidebar.info("Use the built-in page menu for About, Research, Opportunities, and Contact.")
selected_category = st.sidebar.selectbox("Filter posts by category", all_categories)
show_featured_only = st.sidebar.checkbox("Show featured posts only", value=False)

st.sidebar.markdown("---")
st.sidebar.subheader("Recent posts")
for _, row in posts_df.head(5).iterrows():
    st.sidebar.write(f"• {row['title']}")

st.header("Featured Posts")
if featured_df.empty:
    st.info("No featured posts yet.")
else:
    cols = st.columns(2)
    for i, (_, row) in enumerate(featured_df.iterrows()):
        with cols[i % 2]:
            render_post_card(row)

st.markdown("---")

st.header("Latest Posts")
filtered_df = posts_df.copy()

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]

if show_featured_only:
    filtered_df = filtered_df[filtered_df["featured"] == True]

if filtered_df.empty:
    st.warning("No posts found for this filter.")
else:
    for _, row in filtered_df.iterrows():
        render_post_card(row)

st.markdown("---")
st.caption("© 2026 Your Name | Academic website built with Streamlit")