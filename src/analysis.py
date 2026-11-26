import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ============================
# Configuration
# ============================

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# ============================
# Create visuals folder
# ============================

Path("visuals").mkdir(exist_ok=True)

# ============================
# Load data
# ============================

print("Loading data...")

df = pd.read_csv("data/processed/movies_clean.csv")

# ============================
# Profit calculation
# ============================

df["profit"] = df["revenue"] - df["budget"]

# ============================
# 1. Movies Released Per Year
# ============================

movies_per_year = (
    df.groupby("year")
    .size()
)

plt.figure(figsize=(12, 6))

movies_per_year.plot(
    kind="line",
    marker="o",
    color="royalblue",
    linewidth=2
)

plt.title("Movies Released Per Year", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Number of Movies")
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("visuals/movies_per_year.png")
plt.close()

# ============================
# 2. Revenue by Genre
# ============================

genre_revenue = (
    df.groupby("main_genre")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))

sns.barplot(
    x=genre_revenue.values,
    y=genre_revenue.index,
    palette="viridis"
)

plt.title("Top 10 Genres by Revenue", fontsize=14)
plt.xlabel("Total Revenue ($)")
plt.ylabel("Genre")

plt.tight_layout()
plt.savefig("visuals/revenue_by_genre.png")
plt.close()

# ============================
# 3. Average Rating by Genre
# ============================

genre_rating = (
    df.groupby("main_genre")["vote_average"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))

sns.barplot(
    x=genre_rating.values,
    y=genre_rating.index,
    palette="magma"
)

plt.title("Top 10 Genres by Average Rating", fontsize=14)
plt.xlabel("Average Rating")
plt.ylabel("Genre")

plt.tight_layout()
plt.savefig("visuals/average_rating_by_genre.png")
plt.close()

# ============================
# 4. Top 10 Movies by Revenue
# ============================

top_revenue = (
    df.sort_values("revenue", ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))

sns.barplot(
    data=top_revenue,
    x="revenue",
    y="title",
    palette="Blues_r"
)

plt.title("Top 10 Movies by Revenue", fontsize=14)
plt.xlabel("Revenue ($)")
plt.ylabel("Movie")

plt.tight_layout()
plt.savefig("visuals/top_movies_revenue.png")
plt.close()

# ============================
# 5. Top 10 Most Profitable Movies
# ============================

top_profit = (
    df.sort_values("profit", ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))

sns.barplot(
    data=top_profit,
    x="profit",
    y="title",
    palette="Greens_r"
)

plt.title("Top 10 Most Profitable Movies", fontsize=14)
plt.xlabel("Profit ($)")
plt.ylabel("Movie")

plt.tight_layout()
plt.savefig("visuals/top_profitable_movies.png")
plt.close()

print("✅ movies_per_year.png")
print("✅ revenue_by_genre.png")
print("✅ average_rating_by_genre.png")
print("✅ top_movies_revenue.png")
print("✅ top_profitable_movies.png")
print("✅ All visualizations generated successfully.")