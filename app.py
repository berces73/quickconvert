import os
from flask import Flask, render_template, request, send_file
import pdfplumber
from docx import Document
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
import io

# NLTK verilerini indir (Özetleme için gerekli)
nltk.download('punkt')

app = Flask(__name__)

def summarize_text(text):
    if len(text) < 100: return "Özetlemek için çok kısa bir metin."
    parser = PlaintextParser.from_string(text, Tokenizer("turkish"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 3) # En önemli 3 cümleyi seçer
    return " ".join([str(sentence) for sentence in summary])

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = None
    summary = None
    if request.method == 'POST':
        action = request.form.get('action')
        file = request.files.get('file')

        if file:
            try:
                text = ""
                if action == 'pdf_to_ai' or action == 'pdf_to_text':
                    with pdfplumber.open(file) as pdf:
                        text = "\n".join([page.extract_text() or "" for page in pdf.pages])
                
                elif action == 'word_to_ai':
                    doc = Document(file)
                    text = "\n".join([para.text for para in doc.paragraphs])

                if 'to_ai' in action:
                    summary = summarize_text(text)
                    return render_template('index.html', ai_result=summary)
                else:
                    return render_template('index.html', text=text)
            except:
                return render_template('index.html', error="AI analizi başarısız.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)





