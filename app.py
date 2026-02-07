import os
from flask import Flask, render_template, request, send_file
import pdfplumber
from docx import Document
from PIL import Image
import qrcode
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = None
    stats = None
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'generate_qr':
            qr_data = request.form.get('qr_text')
            img = qrcode.make(qr_data)
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            return send_file(buf, as_attachment=True, download_name="qrcode_mega.png")

        file = request.files.get('file')
        if file:
            try:
                if action == 'pdf_to_text':
                    with pdfplumber.open(file) as pdf:
                        text = "\n".join([page.extract_text() or "" for page in pdf.pages])
                    extracted_text = text
                    stats = {"words": len(text.split()), "chars": len(text)}
                
                elif action == 'word_to_text':
                    doc = Document(file)
                    text = "\n".join([para.text for para in doc.paragraphs])
                    extracted_text = text
                    stats = {"words": len(text.split()), "chars": len(text)}

                elif action == 'compress_img':
                    img = Image.open(file)
                    buf = io.BytesIO()
                    img.save(buf, format=img.format, quality=25, optimize=True)
                    buf.seek(0)
                    return send_file(buf, as_attachment=True, download_name=f"ultra_compressed_{file.filename}")

                return render_template('index.html', text=extracted_text, stats=stats)
            except Exception as e:
                return render_template('index.html', error="İşlem başarısız oldu.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)




