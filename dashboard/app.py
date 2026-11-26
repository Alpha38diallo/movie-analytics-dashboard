import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# Page Config
# =====================================

st.set_page_config(
    page_title="Movie Analytics Dashboard",
    page_icon="🎬",
    layout="wide"
)

# =====================================
# Load Data
# =====================================

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/movies_clean.csv")

df = load_data()

# =====================================
# Sidebar Filters
# =====================================

st.sidebar.header("Filters")

genres = ["All"] + sorted(df["main_genre"].dropna().unique().tolist())

selected_genre = st.sidebar.selectbox(
    "Genre",
    genres
)

min_year = int(df["year"].min())
max_year = int(df["year"].max())

selected_year = st.sidebar.slider(
    "Year Range",
    min_year,
    max_year,
    (min_year, max_year)
)

# =====================================
# Apply Filters
# =====================================

filtered_df = df.copy()

if selected_genre != "All":
    filtered_df = filtered_df[
        filtered_df["main_genre"] == selected_genre
    ]

filtered_df = filtered_df[
    (filtered_df["year"] >= selected_year[0]) &
    (filtered_df["year"] <= selected_year[1])
]

# =====================================
# Dashboard Title
# =====================================

st.title("🎬 Movie Analytics Dashboard")
st.markdown(
    "Interactive analysis of movies using the TMDB 5000 Movies Dataset."
)

# =====================================
# KPI Calculations
# =====================================

total_movies = len(filtered_df)

total_revenue = filtered_df["revenue"].sum() / 1e9

average_rating = filtered_df["vote_average"].mean()

total_profit = (
    filtered_df["revenue"].sum()
    - filtered_df["budget"].sum()
) / 1e9

# =====================================
# KPI Cards
# =====================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "🎬 Total Movies",
        f"{total_movies:,}"
    )

with kpi2:
    st.metric(
        "💰 Revenue",
        f"{total_revenue:.1f} B$"
    )

with kpi3:
    st.metric(
        "⭐ Average Rating",
        f"{average_rating:.2f}"
    )

with kpi4:
    st.metric(
        "📈 Profit",
        f"{total_profit:.1f} B$"
    )

st.divider()
# =====================================
# Charts Layout
# =====================================

col1, col2 = st.columns(2)

# =====================================
# Movies Released per Year
# =====================================

with col1:

    st.subheader("📈 Movies Released per Year")

    movies_year = (
        filtered_df.groupby("year")
        .size()
        .reset_index(name="movies_count")
    )

    movies_year = movies_year[
        movies_year["year"] >= 1980
    ]

    fig = px.line(
        movies_year,
        x="year",
        y="movies_count",
        markers=True,
        template="plotly_dark"
    )

    fig.update_traces(
        line=dict(width=4)
    )

    fig.update_layout(
        title=None,
        xaxis_title="Année",
        yaxis_title="Nombre de films"
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================
# Revenue by Genre
# =====================================

with col2:

    st.subheader("💰 Top 15 Revenue-Generating Genres")

    genre_revenue = (
        filtered_df[
        filtered_df["main_genre"] != "Unknown"
    ]
        .groupby("main_genre")["revenue"]
        .sum()
        .reset_index()
        .sort_values("revenue", ascending=False)
        .head(15)
    )

    fig = px.bar(
        genre_revenue.sort_values("revenue"),
        x="revenue",
        y="main_genre",
        orientation="h",
        color="revenue",
        template="plotly_dark"
    )

    fig.update_layout(
        title=None,
        xaxis_title="Revenus (B$)",
        yaxis_title="Genre"
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================
# Second Row
# =====================================

col3, col4 = st.columns(2)

# =====================================
# Top Revenue Movies
# =====================================

with col3:

    st.subheader("🏆 Top 10 Highest-Grossing Movies")

    top_revenue = (
        filtered_df.sort_values(
            "revenue",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top_revenue,
        x="revenue",
        y="title",
        orientation="h",
        color="revenue",
        template="plotly_dark"
    )

    fig.update_layout(
        title=None,
        yaxis=dict(
            autorange="reversed"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================
# Top Profitable Movies
# =====================================

with col4:

    st.subheader("💎 Top 10 Most Profitable Movies")

    profit_df = filtered_df.copy()

    profit_df["profit"] = (
        profit_df["revenue"]
        - profit_df["budget"]
    )

    top_profit = (
        profit_df.sort_values(
            "profit",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top_profit,
        x="profit",
        y="title",
        orientation="h",
        color="profit",
        template="plotly_dark"
    )

    fig.update_layout(
        title=None,
        yaxis=dict(
            autorange="reversed"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

st.caption(
    "Source: TMDB 5000 Movies Dataset | Data cleaning included the removal of records with missing " \
    "release dates, missing ratings, zero budgets, and zero revenues. Only the primary genre was retained "
    "for genre analysis, and profit was calculated as Revenue minus Budget. Final dataset: 3,229 movies."
)