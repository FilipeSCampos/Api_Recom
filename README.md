# Documentação da API de Recomendação de Livros

Filipe Sampaio
Rafael Meirelles
Thiago Leal

## Visão Geral
API para recomendações de livros usando técnicas de:
- **Best Sellers**: Livros mais bem avaliados
- **Mais Populares**: Livros com mais avaliações
- **Baseado em Conteúdo**: Similaridade entre títulos e autores
- **Híbrido**: Combinação de conteúdo + popularidade

---

## Endpoints

### 1. Recomendações
| Endpoint | Método | Descrição | Parâmetros |
|----------|--------|-----------|------------|
| `/books/best-sellers/` | GET | Livros mais bem avaliados | `top_n` (opcional, padrão=10) |
| `/books/most-popular/` | GET | Livros mais populares | `top_n` (opcional, padrão=10) |
| `/books/recommendations/content/{book_id}` | GET | Recomendações baseadas em conteúdo | `book_id` (obrigatório), `top_n` (opcional) |
| `/books/recommendations/hybrid/` | GET | Recomendações híbridas | `book_id` (opcional), `top_n` (opcional) |

### 2. Busca e Informações
| Endpoint | Método | Descrição | Parâmetros |
|----------|--------|-----------|------------|
| `/books/search/` | GET | Busca por título/autor | `query` (obrigatório), `top_n` (opcional) |
| `/books/{book_id}` | GET | Detalhes de um livro | `book_id` (obrigatório) |
| `/books/stats/` | GET | Estatísticas do acervo | - |
| `/health/` | GET | Status do serviço | - |

---

## Exemplos de Uso

### Best Sellers
```bash
curl "http://localhost:8000/books/best-sellers/?top_n=5"
```

Resposta:

```json
{
  "books": [
    {
      "bookID": 1,
      "title": "The Hunger Games",
      "authors": "Suzanne Collins",
      "average_rating": 4.34,
      "ratings_count": 4780653,
      "publication_date": "2008-09-14",
      "publisher": "Scholastic Press"
    }
  ]
}
```
Busca por Livros

```bash
curl "http://localhost:8000/books/search/?query=harry+potter&top_n=3"
```

Resposta:

```json
{
  "results": [
    {
      "bookID": 2,
      "title": "Harry Potter and the Sorcerer's Stone",
      "authors": "J.K. Rowling",
      "average_rating": 4.44,
      "ratings_count": 4602479,
      "publication_date": "1997-06-26"
    }
  ]
}
```
