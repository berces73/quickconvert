import os
from flask import Flask, render_template, request, send_file
import pdfplumber
from docx import Document
from PIL import Image
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = None
    if request.method == 'POST':
        action = request.form.get('action')
        file = request.files.get('file')

        if not file or file.filename == '':
            return render_template('index.html', error="Lütfen bir dosya seçin.")

        try:
            # 1. PDF -> METİN
            if action == 'pdf_to_text':
                with pdfplumber.open(file) as pdf:
                    text = "\n".join([page.extract_text() or "" for page in pdf.pages])
                return render_template('index.html', text=text)

            # 2. WORD -> METİN
            elif action == 'word_to_text':
                doc = Document(file)
                text = "\n".join([para.text for para in doc.paragraphs])
                return render_template('index.html', text=text)

            # 3. GÖRSEL -> PDF
            elif action == 'img_to_pdf':
                img = Image.open(file).convert('RGB')
                buf = io.BytesIO()
                img.save(buf, format='PDF')
                buf.seek(0)
                return send_file(buf, as_attachment=True, download_name="convert.pdf")

            # 4. GÖRSEL FORMAT DEĞİŞTİR (Örn: PNG Yap)
            elif action == 'to_png':
                img = Image.open(file)
                buf = io.BytesIO()
                img.save(buf, format='PNG')
                buf.seek(0)
                return send_file(buf, as_attachment=True, download_name="convert.png")

        except Exception as e:
            return render_template('index.html', error=f"Hata oluştu: {str(e)}")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)



