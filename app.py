import os
from flask import Flask, render_template, request, send_file
import pdfplumber
from PIL import Image
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = None
    if request.method == 'POST':
        action = request.form.get('action')
        file = request.files.get('file')

        if file and file.filename != '':
            if action == 'pdf_to_text':
                with pdfplumber.open(file) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += (page.extract_text() or "") + "\n"
                extracted_text = text
                return render_template('index.html', text=extracted_text)
            
            elif action == 'img_to_pdf':
                image = Image.open(file)
                pdf_bytes = io.BytesIO()
                image.convert('RGB').save(pdf_bytes, format='PDF')
                pdf_bytes.seek(0)
                return send_file(pdf_bytes, as_attachment=True, download_name="converted.pdf")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


