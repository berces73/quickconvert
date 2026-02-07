# 1. Aşama: Hafif bir Python temel imajı kullan
FROM python:3.10-slim

# 2. Aşama: Çalışma dizinini oluştur
WORKDIR /app

# 3. Aşama: Sistem araçlarını güncelle ve temiz tut
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Aşama: Bağımlılıkları kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Aşama: Tüm proje dosyalarını (templates, app.py vb.) kopyala
COPY . .

# 6. Aşama: Uygulamanın çalışacağı portu belirt (Render için)
EXPOSE 5000

# 7. Aşama: Gunicorn ile uygulamayı başlat
CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]