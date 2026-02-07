import os
from flask import Flask, render_template, request, send_file
import pdfplumber
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="Dosya seçilmedi.")
        
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="Dosya adı boş.")

        if file:
            try:
                with pdfplumber.open(file) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
                extracted_text = text
            except Exception as e:
                return render_template('index.html', error="PDF okunurken bir hata oluştu.")

    return render_template('index.html', text=extracted_text)

if __name__ == '__main__':
    app.run(debug=True)

