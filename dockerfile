# Use a imagem base do Python 3.11
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos necessários
COPY requirements.txt .
COPY fastapi.py .
COPY models.py .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta da aplicação
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "fastapi:app", "--host", "0.0.0.0", "--port", "8000"]