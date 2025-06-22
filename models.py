"""
models.py
---------
Funções de recomendação e busca para o sistema de livros.
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def best_seller_recommendations(books_df: pd.DataFrame, top_n: int = 10):
    min_ratings = 100
    filtered = books_df[books_df["ratings_count"] >= min_ratings].copy()
    if filtered.empty:
        filtered = books_df.copy()
    best_sellers = filtered.sort_values(
        by=["average_rating", "ratings_count"], ascending=[False, False]
    )
    cols = [
        "bookID",
        "title",
        "authors",
        "average_rating",
        "ratings_count",
        "publication_date",
        "publisher",
    ]
    available = [c for c in cols if c in best_sellers.columns]
    return best_sellers[available].head(top_n).to_dict(orient="records")

def most_popular_recommendations(books_df: pd.DataFrame, top_n: int = 10):
    popular = books_df.sort_values("ratings_count", ascending=False)
    cols = [
        "bookID",
        "title",
        "authors",
        "average_rating",
        "ratings_count",
        "publication_date",
        "publisher",
    ]
    available = [c for c in cols if c in popular.columns]
    return popular[available].head(top_n).to_dict(orient="records")

def content_based_recommendations(books_df: pd.DataFrame, book_id: int, top_n: int = 10):
    target = books_df[books_df["bookID"] == book_id]
    if target.empty:
        return []
    books_df = books_df.copy()
    books_df["combined_features"] = (
        books_df["title"].fillna("") + " " + books_df["authors"].fillna("")
    )
    tfidf = TfidfVectorizer(stop_words="english", max_features=5000)
    tfidf_matrix = tfidf.fit_transform(books_df["combined_features"])
    idx = target.index[0]
    cosine_sim = cosine_similarity(tfidf_matrix[idx : idx + 1], tfidf_matrix).flatten()
    sim_scores = list(enumerate(cosine_sim))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1 : top_n + 1]
    indices = [i[0] for i in sim_scores]
    cols = ["bookID", "title", "authors", "average_rating", "ratings_count"]
    available = [c for c in cols if c in books_df.columns]
    similar = books_df.iloc[indices][available].copy()
    similar["similarity_score"] = [i[1] for i in sim_scores]
    return similar.to_dict(orient="records")

def hybrid_recommendations(books_df: pd.DataFrame, book_id: int | None = None, top_n: int = 10):
    if book_id is not None:
        content_recs = content_based_recommendations(books_df, book_id, top_n // 2)
        content_ids = {b["bookID"] for b in content_recs}
        remaining = books_df[~books_df["bookID"].isin(content_ids)]
        popular_recs = most_popular_recommendations(remaining, top_n - len(content_recs))
        return (content_recs + popular_recs)[:top_n]
    return most_popular_recommendations(books_df, top_n)

def search_books(books_df: pd.DataFrame, query: str, top_n: int = 10):
    query = query.lower().strip()
    mask = (
        books_df["title"].str.lower().str.contains(query, na=False)
        | books_df["authors"].str.lower().str.contains(query, na=False)
    )
    results = books_df[mask].sort_values("ratings_count", ascending=False)
    cols = [
        "bookID",
        "title",
        "authors",
        "average_rating",
        "ratings_count",
        "publication_date",
    ]
    available = [c for c in cols if c in results.columns]
    return results[available].head(top_n).to_dict(orient="records")
