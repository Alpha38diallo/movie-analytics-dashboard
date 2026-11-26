import pandas as pd
import ast
from pathlib import Path

# ============================
# Create folders
# ============================

Path("data/processed").mkdir(parents=True, exist_ok=True)

# ============================
# Load dataset
# ============================

print("Loading TMDB dataset...")

movies = pd.read_csv("data/raw/tmdb_5000_movies.csv")

# ============================
# Extract main genre
# ============================

def extract_main_genre(genres_str):
    try:
        genres = ast.literal_eval(genres_str)

        if isinstance(genres, list) and len(genres) > 0:
            return genres[0]["name"]

        return "Unknown"

    except Exception:
        return "Unknown"

movies["main_genre"] = movies["genres"].apply(extract_main_genre)

# ============================
# Extract year
# ============================

movies["release_date"] = pd.to_datetime(
    movies["release_date"],
    errors="coerce"
)

movies["year"] = movies["release_date"].dt.year

# ============================
# Keep useful columns
# ============================

columns_to_keep = [
    "title",
    "main_genre",
    "budget",
    "revenue",
    "release_date",
    "popularity",
    "runtime",
    "vote_average",
    "vote_count",
    "production_companies",
    "original_language",
    "year"
]

df = movies[columns_to_keep].copy()

# ============================
# Remove missing values
# ============================

df = df.dropna(
    subset=[
        "title",
        "main_genre",
        "budget",
        "revenue",
        "vote_average",
        "year"
    ]
)

# ============================
# Remove invalid rows
# ============================

df = df[
    (df["budget"] > 0)
    & (df["revenue"] > 0)
]

# ============================
# Save clean dataset
# ============================

output_path = "data/processed/movies_clean.csv"

df.to_csv(
    output_path,
    index=False
)

print("\n✅ Clean dataset saved.")
print(f"Shape: {df.shape}")
print(f"Saved to: {output_path}")

print("\nColumns:")
print(df.columns.tolist())

print("\nPreview:")
print(df.head())