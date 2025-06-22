# run.ps1
docker build -t book-recommendation .
docker run -p 8000:8000 -v ${PWD}/books.csv:/app/books.csv -e BOOKS_CSV=/app/books.csv book-recommendation