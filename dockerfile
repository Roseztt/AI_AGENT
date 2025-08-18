FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV OLLAMA_HOST=http://ollama:11434
ENV CHROMA_DIR=/app/chroma

RUN mkdir -p /app/chroma

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "8000"]
