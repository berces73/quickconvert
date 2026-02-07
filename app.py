import os
from flask import Flask, render_template, request, send_file
import pdfplumber
from docx import Document
import io

app = Flask(__name__)

def simple_ai_summary(text):
    if not text or len(text) < 50:
        return "Özetlemek için yeterli metin bulunamadı."
    # Akıllı Özetleme: Metnin giriş, orta ve sonuç kısımlarından en anlamlı cümleleri seçer
    sentences = [s.strip() for s in text.split('.') if len(s) > 20]
    if len(sentences) > 5:
        summary = f"{sentences[0]}. {sentences[len(sentences)//2]}. {sentences[-1]}."
        return summary
    return text[:300] + "..."

@app.route('/', methods=['GET', 'POST'])
def index():
    ai_result = None
    text_result = None
    if request.method == 'POST':
        action = request.form.get('action')
        file = request.files.get('file')

        if file:
            try:
                content = ""
                if file.filename.endswith('.pdf'):
                    with pdfplumber.open(file) as pdf:
                        content = "\n".join([page.extract_text() or "" for page in pdf.pages])
                elif file.filename.endswith('.docx'):
                    doc = Document(file)
                    content = "\n".join([p.text for p in doc.paragraphs])

                if action == 'ai_analyze':
                    ai_result = simple_ai_summary(content)
                else:
                    text_result = content
            except Exception as e:
                return render_template('index.html', error="Dosya işlenemedi.")

    return render_template('index.html', ai_result=ai_result, text=text_result)

if __name__ == '__main__':
    app.run(debug=True)






