FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps for Pillow (JPEG/PNG)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py gunicorn_config.py ./
COPY templates/ templates/

EXPOSE 5000

CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]





