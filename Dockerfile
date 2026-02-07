FROM python:3.10-slim

WORKDIR /app

# Bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tüm dosyaları kopyala
COPY . .

# Render için portu sabitle ve uygulamayı doğrudan başlat
# gunicorn_config.py yerine doğrudan komut satırı kullanalım ki hata payı sıfırlansın
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]


