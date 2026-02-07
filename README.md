# 🚀 Nexus Convert - AI Edition

Modern, AI destekli dosya dönüştürme ve özetleme platformu.

## ✨ Özellikler

### 🤖 AI Özellikleri
- **Akıllı Özetleme**: PDF ve Word dosyalarını otomatik özetler
- **Gelişmiş Analiz**: En önemli bilgileri çıkarır
- **Hızlı İşlem**: Saniyeler içinde sonuç

### 📄 Dönüştürme Araçları
- **PDF → Metin**: PDF dosyalarından metin çıkarma
- **Word → Metin**: DOCX dosyalarını düz metne çevirme
- **QR Kod Oluşturma**: Link ve metinler için QR kod
- **Resim Sıkıştırma**: Kaliteyi koruyarak boyut azaltma
- **Resim → PDF**: Resimleri PDF'e dönüştürme
- **Sayfa Desteği**: Çok sayfalı belgeleri işleyebilir

### 🎨 Modern Arayüz
- **Glassmorphism** tasarım
- **Animasyonlu** arka plan
- **Responsive** tasarım (mobil uyumlu)
- **Smooth** geçişler ve efektler

## 🛠️ Kurulum

### Geliştirme Modu (Development)

#### 1. Gereksinimleri Yükleyin

```bash
pip install -r requirements.txt
```

#### 2. Uygulamayı Başlatın

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```cmd
start.bat
```

**Manuel:**
```bash
python app.py
```

#### 3. Tarayıcıda Açın

```
http://127.0.0.1:5000
```

### Production Modu

#### Gunicorn ile (Linux/Mac)

```bash
chmod +x start-production.sh
./start-production.sh
```

Veya manuel:
```bash
gunicorn --config gunicorn_config.py app:app
```

#### Docker ile

```bash
# Build
docker build -t nexus-convert .

# Run
docker run -p 8000:8000 nexus-convert
```

#### Docker Compose ile

```bash
docker-compose up -d
```

Tarayıcıda: `http://localhost:8000`

## 📦 Gereksinimler

- Python 3.8+
- Flask 3.0.0
- pdfplumber 0.10.3
- python-docx 1.1.0

## 🎯 Kullanım

### AI Özetleme
1. "AI Akıllı Özet" kartını bulun
2. PDF veya Word dosyanızı seçin
3. "AI ile Özetle" butonuna tıklayın
4. Otomatik özet oluşturulur

### Metin Dönüştürme
1. PDF veya Word kartından birini seçin
2. Dosyanızı yükleyin
3. "Dönüştür" butonuna tıklayın
4. Tam metin görüntülenir

## 🔧 Yapılandırma

### Maksimum Dosya Boyutu
`app.py` dosyasında varsayılan 16MB:

```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
```

### AI Özet Uzunluğu
`simple_ai_summary()` fonksiyonunda:

```python
if len(summary) > 500:
    summary = summary[:497] + '...'
```

## 📁 Proje Yapısı

```
nexus-convert/
│
├── app.py                 # Flask backend
├── requirements.txt       # Python bağımlılıkları
├── README.md             # Dokümantasyon
│
└── templates/
    └── index.html        # Ana sayfa template
```

## 🚀 Özellik Detayları

### AI Özetleme Algoritması

1. **Metin Temizleme**: Gereksiz karakterleri temizler
2. **Cümle Ayrıştırma**: Metni cümlelere böler
3. **Akıllı Seçim**: 
   - Kısa metinler: Tamamını döndürür
   - Orta metinler: Başlangıç, orta ve son
   - Uzun metinler: Stratejik noktalardan seçim
4. **Optimizasyon**: Benzer cümleleri temizler

### PDF İşleme

- Çok sayfalı PDF desteği
- Her sayfa ayrı işaretlenir
- OCR gerektirmez (native metin)
- Hata yönetimi

### Word İşleme

- DOCX format desteği
- Paragraf koruması
- Stil temizleme
- Hızlı işlem

## 🎨 Tasarım Özellikleri

### Renk Paleti
- **Primary**: #8b5cf6 (Mor)
- **Secondary**: #ec4899 (Pembe)
- **Accent**: #f97316 (Turuncu)
- **Success**: #10b981 (Yeşil)

### Animasyonlar
- Floating background
- Hover effects
- Smooth transitions
- Loading states

## 🐛 Hata Ayıklama

### Yaygın Hatalar

**1. "Dosya işlenemedi"**
- Dosya formatını kontrol edin
- Dosya boyutunu kontrol edin (max 16MB)

**2. "PDF'den metin çıkarılamadı"**
- PDF görsel tabanlı olabilir
- OCR gerektirebilir

**3. "Port kullanımda"**
- Başka bir Flask uygulaması çalışıyor olabilir
- Port değiştirin: `app.run(port=5001)`

## 📊 Performans

- **Ortalama İşlem Süresi**: 1-3 saniye
- **Maksimum Dosya Boyutu**: 16MB
- **Desteklenen Formatlar**: PDF, DOC, DOCX
- **Eş Zamanlı Kullanıcı**: 50+ (production'da daha fazla)

## 🔒 Güvenlik

- Dosya boyutu limiti
- Format doğrulama
- Hata yakalama
- Güvenli dosya işleme

## 🌟 Gelecek Özellikler

- [ ] Excel → JSON dönüştürme
- [ ] Çoklu dosya yükleme
- [ ] Toplu işleme (batch processing)
- [ ] API endpoint'leri
- [ ] Kullanıcı kimlik doğrulama
- [ ] Gelişmiş AI modelleri (GPT entegrasyonu)
- [ ] OCR desteği (görsel PDF'ler için)
- [ ] Video → GIF dönüştürme
- [ ] Cloud storage entegrasyonu

## 📄 Lisans

MIT License - Özgürce kullanabilirsiniz!

## 🤝 Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır!

## 💬 İletişim

Sorularınız için issue açabilirsiniz.

---

**Made with ❤️ and AI**

🚀 Nexus Convert v3.0 - AI Edition
