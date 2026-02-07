# app.py
from flask import Flask, render_template, request, send_file
import pdfplumber
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['pdf_file']
    if file:
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        
        # Metni bir dosya gibi hazırla
        output = io.BytesIO()
        output.write(text.encode('utf-8'))
        output.seek(0)
        
        return send_file(output, mimetype='text/plain', as_attachment=True, download_name='donusturuldu.txt')

if __name__ == '__main__':
    app.run(debug=True)