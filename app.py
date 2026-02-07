import os
from flask import Flask, render_template, request, send_file, jsonify
import pdfplumber
from docx import Document
import qrcode
from PIL import Image
import io
from datetime import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Upload folder for temporary files
UPLOAD_FOLDER = 'temp_uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def simple_ai_summary(text):
    """
    Gelişmiş AI Özetleme Fonksiyonu
    Metnin en önemli kısımlarını akıllıca seçer
    """
    if not text or len(text) < 50:
        return "⚠️ Özetlemek için yeterli metin bulunamadı."
    
    # Metni temizle
    text = text.strip()
    
    # Cümlelere ayır ve temizle
    sentences = []
    for s in text.replace('\n', ' ').split('.'):
        s = s.strip()
        if len(s) > 30:  # Çok kısa cümleleri atla
            sentences.append(s)
    
    if not sentences:
        return "⚠️ Geçerli cümle bulunamadı."
    
    # Özetleme stratejisi
    num_sentences = len(sentences)
    
    if num_sentences <= 3:
        # Çok kısa metinler için tamamını döndür
        return '. '.join(sentences) + '.'
    
    elif num_sentences <= 10:
        # Orta uzunlukta metinler için başlangıç, orta ve son
        summary_parts = [
            sentences[0],
            sentences[num_sentences // 2],
            sentences[-1]
        ]
        return '. '.join(summary_parts) + '.'
    
    else:
        # Uzun metinler için daha kapsamlı özet
        # İlk paragraf, ortadan birkaç önemli cümle, sonuç
        summary_parts = [
            sentences[0],  # Giriş
            sentences[num_sentences // 4],  # İlk çeyrek
            sentences[num_sentences // 2],  # Orta
            sentences[3 * num_sentences // 4],  # Son çeyrek
            sentences[-1]  # Sonuç
        ]
        
        # Benzer cümleleri temizle
        unique_parts = []
        for part in summary_parts:
            if part not in unique_parts:
                unique_parts.append(part)
        
        summary = '. '.join(unique_parts) + '.'
        
        # Özet çok uzunsa kısalt
        if len(summary) > 500:
            summary = summary[:497] + '...'
        
        return summary


@app.route('/', methods=['GET', 'POST'])
def index():
    """Ana sayfa ve dosya işleme"""
    ai_result = None
    text_result = None
    error = None
    
    if request.method == 'POST':
        action = request.form.get('action')
        file = request.files.get('file')
        
        if not file:
            error = "Lütfen bir dosya seçin."
            return render_template('index.html', error=error)
        
        try:
            content = ""
            filename = file.filename.lower()
            
            # PDF İşleme
            if filename.endswith('.pdf'):
                try:
                    with pdfplumber.open(file) as pdf:
                        pages_text = []
                        for i, page in enumerate(pdf.pages, 1):
                            page_text = page.extract_text()
                            if page_text:
                                pages_text.append(f"[Sayfa {i}]\n{page_text}")
                        content = "\n\n".join(pages_text)
                    
                    if not content.strip():
                        error = "PDF'den metin çıkarılamadı. Dosya metin içermiyor olabilir."
                        return render_template('index.html', error=error)
                        
                except Exception as e:
                    error = f"PDF okuma hatası: {str(e)}"
                    return render_template('index.html', error=error)
            
            # Word İşleme
            elif filename.endswith('.docx') or filename.endswith('.doc'):
                try:
                    doc = Document(file)
                    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
                    content = "\n\n".join(paragraphs)
                    
                    if not content.strip():
                        error = "Word dosyasından metin çıkarılamadı."
                        return render_template('index.html', error=error)
                        
                except Exception as e:
                    error = f"Word okuma hatası: {str(e)}"
                    return render_template('index.html', error=error)
            
            else:
                error = "Desteklenmeyen dosya formatı. Lütfen PDF veya DOCX dosyası yükleyin."
                return render_template('index.html', error=error)
            
            # İşlem türüne göre sonuç
            if action == 'ai_analyze':
                ai_result = simple_ai_summary(content)
                # Tam metni de göster (isteğe bağlı)
                # text_result = content
                
            else:  # pdf_to_text veya word_to_text
                text_result = content
                
        except Exception as e:
            error = f"Dosya işlenirken bir hata oluştu: {str(e)}"
            return render_template('index.html', error=error)
    
    return render_template('index.html', 
                         ai_result=ai_result, 
                         text=text_result, 
                         error=error)


@app.route('/health')
def health():
    """Sağlık kontrol endpoint'i"""
    return jsonify({"status": "healthy", "version": "3.0-AI"})


@app.route('/generate-qr', methods=['POST'])
def generate_qr():
    """QR kod oluşturma endpoint'i"""
    try:
        qr_text = request.form.get('qr_text', '').strip()
        qr_size = int(request.form.get('qr_size', 512))
        
        if not qr_text:
            return jsonify({"error": "Lütfen bir metin veya link girin"}), 400
        
        # QR kod oluştur
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_text)
        qr.make(fit=True)
        
        # Resim oluştur
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
        
        # Byte buffer'a kaydet
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=True,
            download_name=f'qr-code-{datetime.now().strftime("%Y%m%d%H%M%S")}.png'
        )
        
    except Exception as e:
        return jsonify({"error": f"QR kod oluşturma hatası: {str(e)}"}), 500


@app.route('/compress-image', methods=['POST'])
def compress_image():
    """Resim sıkıştırma endpoint'i"""
    try:
        file = request.files.get('file')
        quality = int(request.form.get('quality', 80))
        
        if not file:
            return jsonify({"error": "Lütfen bir resim dosyası seçin"}), 400
        
        # Resmi aç
        img = Image.open(file.stream)
        
        # RGB'ye çevir (RGBA ise)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Sıkıştır
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG', quality=quality, optimize=True)
        img_io.seek(0)
        
        original_filename = file.filename.rsplit('.', 1)[0]
        
        return send_file(
            img_io,
            mimetype='image/jpeg',
            as_attachment=True,
            download_name=f'{original_filename}_compressed.jpg'
        )
        
    except Exception as e:
        return jsonify({"error": f"Sıkıştırma hatası: {str(e)}"}), 500


@app.route('/image-to-pdf', methods=['POST'])
def image_to_pdf():
    """Resimden PDF oluşturma endpoint'i"""
    try:
        file = request.files.get('file')
        
        if not file:
            return jsonify({"error": "Lütfen bir resim dosyası seçin"}), 400
        
        # Resmi aç
        img = Image.open(file.stream)
        
        # RGB'ye çevir
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # PDF'e kaydet
        pdf_io = io.BytesIO()
        img.save(pdf_io, format='PDF')
        pdf_io.seek(0)
        
        original_filename = file.filename.rsplit('.', 1)[0]
        
        return send_file(
            pdf_io,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'{original_filename}.pdf'
        )
        
    except Exception as e:
        return jsonify({"error": f"PDF oluşturma hatası: {str(e)}"}), 500


@app.errorhandler(413)
def too_large(e):
    """Dosya boyutu çok büyükse"""
    return render_template('index.html', 
                         error="Dosya çok büyük! Maksimum 16MB yükleyebilirsiniz."), 413


@app.errorhandler(500)
def server_error(e):
    """Sunucu hatası"""
    return render_template('index.html', 
                         error="Sunucu hatası oluştu. Lütfen tekrar deneyin."), 500


if __name__ == '__main__':
    # Templates klasörünün var olduğundan emin ol
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    print("🚀 Nexus Convert AI Edition başlatılıyor...")
    print("📍 http://127.0.0.1:5000")
    print("🤖 AI Özet özelliği aktif!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
