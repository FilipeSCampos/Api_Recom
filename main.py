"""
fastapi.py
----------
Rotas e inicialização do FastAPI para o sistema de recomendação de livros.
"""
from pathlib import Path
import os
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import (
    best_seller_recommendations,
    most_popular_recommendations,
    content_based_recommendations,
    hybrid_recommendations,
    search_books,
)

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CSV_PATH = BASE_DIR / "books.csv"
CSV_PATH = Path(os.getenv("BOOKS_CSV", DEFAULT_CSV_PATH))

if not CSV_PATH.exists():
    raise FileNotFoundError(
        f"Arquivo de dados '{CSV_PATH}' não encontrado. "
        "Defina a variável de ambiente BOOKS_CSV com o caminho correto para o csv."
    )

books = pd.read_csv(CSV_PATH, on_bad_lines="skip", engine="python")

app = FastAPI(title="Book Recommendation API", version="1.0.0")

templates_dir = BASE_DIR / "templates"
if not templates_dir.exists():
    templates_dir.mkdir(parents=True, exist_ok=True)
    (templates_dir / "index.html").write_text(
        """<!DOCTYPE html><html><head><title>Book Rec API</title></head><body>\n        <h1>Book Recommendation API is running! ✅</h1></body></html>""",
        encoding="utf-8",
    )

templates = Jinja2Templates(directory=str(templates_dir))

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/books/best-sellers/")
async def api_best_sellers(top_n: int = 10):
    return {"books": best_seller_recommendations(books, top_n)}

@app.get("/books/most-popular/")
async def api_most_popular(top_n: int = 10):
    return {"books": most_popular_recommendations(books, top_n)}

@app.get("/books/recommendations/content/{book_id}")
async def api_content_recs(book_id: int, top_n: int = 10):
    recs = content_based_recommendations(books, book_id, top_n)
    if not recs:
        raise HTTPException(404, "Book not found or no recommendations available")
    return {"recommendations": recs}

@app.get("/books/recommendations/hybrid/")
async def api_hybrid_recs(book_id: int | None = None, top_n: int = 10):
    return {"books": hybrid_recommendations(books, book_id, top_n)}

@app.get("/books/search/")
async def api_search(query: str, top_n: int = 10):
    if len(query.strip()) < 2:
        raise HTTPException(400, "Query must be at least 2 characters long")
    return {"results": search_books(books, query, top_n)}

@app.get("/books/{book_id}")
async def api_book_details(book_id: int):
    book = books[books["bookID"] == book_id]
    if book.empty:
        raise HTTPException(404, "Book not found")
    return book.to_dict(orient="records")[0]

@app.get("/books/stats/")
async def api_book_stats():
    total_books = len(books)
    avg_rating = books["average_rating"].mean()
    total_ratings = books["ratings_count"].sum()
    most_rated = books.loc[books["ratings_count"].idxmax()]
    highest_rated = books.loc[books["average_rating"].idxmax()]
    return {
        "total_books": int(total_books),
        "average_rating": round(float(avg_rating), 2),
        "total_ratings": int(total_ratings),
        "most_rated_book": {
            "title": most_rated["title"],
            "authors": most_rated["authors"],
            "ratings_count": int(most_rated["ratings_count"]),
        },
        "highest_rated_book": {
            "title": highest_rated["title"],
            "authors": highest_rated["authors"],
            "average_rating": float(highest_rated["average_rating"]),
        },
    }

@app.get("/health/")
async def health():
    return {"status": "healthy", "total_books": len(books)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi:app", host="0.0.0.0", port=8000, reload=True)
