FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . . 
# Üstteki satır tüm dosyaları (templates dahil) içeri aktarır.
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]


