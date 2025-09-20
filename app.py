import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_page_config(page_title="CORD-19 Explorer", layout="wide")

# -------------------------
# Load data
# -------------------------
@st.cache_data
def load_data(path="cleaned_metadata_sample.csv"):
    df = pd.read_csv(path)
    # make sure publish_time is datetime and add publish_month
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors="coerce")
    df['publish_year'] = df['publish_time'].dt.year
    df['publish_month'] = df['publish_time'].dt.to_period("M")
    # simple word count for abstract
    df['abstract_words'] = df['abstract'].fillna("").str.split().str.len()
    return df

df = load_data()

# -------------------------
# Sidebar filters
# -------------------------
st.sidebar.header("Filters")

year_min, year_max = int(df['publish_year'].min()), int(df['publish_year'].max())
year_range = st.sidebar.slider("Publication Year Range",
                               min_value=year_min, max_value=year_max,
                               value=(year_min, year_max))

journal_choice = st.sidebar.selectbox(
    "Journal (optional)",
    options=["All"] + sorted(df['journal'].dropna().unique())
)

author_kw = st.sidebar.text_input("Author name contains (optional)")
min_words = st.sidebar.number_input("Minimum abstract word count", 0, 500, 0)

# Apply filters
mask = (
    (df['publish_year'].between(year_range[0], year_range[1])) &
    (df['abstract_words'] >= min_words)
)
if journal_choice != "All":
    mask &= df['journal'] == journal_choice
if author_kw:
    mask &= df['authors'].fillna("").str.contains(author_kw, case=False)

filtered_df = df[mask]

st.sidebar.write(f"**Papers after filtering:** {len(filtered_df):,}")

# Optional download of the filtered subset
st.sidebar.download_button(
    "Download CSV of current view",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="cord19_filtered.csv",
    mime="text/csv",
)

# -------------------------
# Main page
# -------------------------
st.title("CORD-19 Research Dataset Explorer")
st.markdown(
    "Interactively explore a sample of the **CORD-19** metadata. "
    "Filter by year, journal, author keyword, or abstract length."
)

# Show sample of data
st.subheader("Data Preview")
st.dataframe(filtered_df.head(30), use_container_width=True)

# -------------------------
# Publications by year
# -------------------------
st.subheader("Publications by Year")
fig1, ax1 = plt.subplots(figsize=(8,4))
(filtered_df['publish_year'].value_counts()
           .sort_index()
           .plot(kind="bar", ax=ax1, color="steelblue"))
ax1.set_xlabel("Year")
ax1.set_ylabel("Paper Count")
st.pyplot(fig1)

# Monthly trend for finer detail
st.subheader("Monthly Publication Trend")
fig1b, ax1b = plt.subplots(figsize=(10,4))
(filtered_df['publish_month'].value_counts()
           .sort_index()
           .plot(ax=ax1b, color="darkgreen"))
ax1b.set_xlabel("Month")
ax1b.set_ylabel("Paper Count")
st.pyplot(fig1b)

# -------------------------
# Top journals
# -------------------------
st.subheader("Top 10 Journals")
fig2, ax2 = plt.subplots(figsize=(6,4))
(filtered_df['journal'].value_counts()
           .head(10)
           .plot(kind="barh", ax=ax2, color="tomato"))
ax2.set_xlabel("Paper Count")
ax2.set_ylabel("Journal")
st.pyplot(fig2)

# -------------------------
# Top authors (split on ;)
# -------------------------
st.subheader("Most Frequent Authors (approx)")
author_series = (
    filtered_df['authors'].dropna()
    .str.split(';')
    .explode()
    .str.strip()
    .value_counts()
    .head(10)
)
fig3, ax3 = plt.subplots(figsize=(6,4))
author_series.plot(kind="barh", ax=ax3, color="purple")
ax3.set_xlabel("Paper Count")
ax3.set_ylabel("Author")
st.pyplot(fig3)

# -------------------------
# Word cloud of titles
# -------------------------
st.subheader("Word Cloud of Paper Titles")
title_text = " ".join(filtered_df['title'].dropna().tolist())
wc = WordCloud(width=800, height=400,
               background_color="white",
               stopwords={'the','and','of','in','for','to'}).generate(title_text)
fig4, ax4 = plt.subplots(figsize=(8,4))
ax4.imshow(wc, interpolation="bilinear")
ax4.axis("off")
st.pyplot(fig4)
