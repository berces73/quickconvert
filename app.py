# -*- coding: utf-8 -*-
"""
Nexus Convert | AI Edition - Flask backend
"""
import io
import os
import re
from pathlib import Path

from flask import Flask, render_template, request, send_file, jsonify

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB
UPLOAD_FOLDER = Path(app.root_path) / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)


def extract_text_from_pdf(file_bytes):
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        parts = []
        for page in reader.pages:
            parts.append(page.extract_text() or "")
        return "\n\n".join(parts).strip()
    except Exception as e:
        raise ValueError(f"PDF okunamadı: {e}")


def extract_text_from_docx(file_bytes):
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        return "\n\n".join(p.text for p in doc.paragraphs).strip()
    except Exception as e:
        raise ValueError(f"Word dosyası okunamadı: {e}")


def simple_summarize(text, max_sentences=8):
    """Basit metin özeti: ilk paragraflar ve anahtar cümleler."""
    if not text or len(text) < 200:
        return text[:1500] if text else "Özet çıkarılamadı."
    # İlk birkaç paragraf
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    taken = []
    total_len = 0
    for p in paragraphs:
        if total_len > 1200:
            break
        taken.append(p)
        total_len += len(p) + 2
    result = "\n\n".join(taken)
    if len(result) < 400 and len(paragraphs) > len(taken):
        for p in paragraphs[len(taken) : len(taken) + 3]:
            if total_len > 1500:
                break
            taken.append(p)
            total_len += len(p) + 2
        result = "\n\n".join(taken)
    return result[:2000] + ("..." if len(result) > 2000 else "")


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    ai_result = None
    text = None

    if request.method == "POST":
        action = request.form.get("action")
        file = request.files.get("file")

        if not file or file.filename == "":
            error = "Lütfen bir dosya seçin."
            return render_template("index.html", error=error, ai_result=ai_result, text=text)

        try:
            raw = file.read()
        except Exception as e:
            error = f"Dosya okunamadı: {e}"
            return render_template("index.html", error=error, ai_result=ai_result, text=text)

        if action == "ai_analyze":
            ext = (Path(file.filename).suffix or "").lower()
            if ext == ".pdf":
                full_text = extract_text_from_pdf(raw)
            elif ext in (".doc", ".docx"):
                full_text = extract_text_from_docx(raw)
            else:
                error = "Sadece PDF veya Word (.docx) destekleniyor."
                return render_template("index.html", error=error, ai_result=ai_result, text=text)
            ai_result = simple_summarize(full_text)
            return render_template("index.html", error=error, ai_result=ai_result, text=text)

        if action == "pdf_to_text":
            try:
                text = extract_text_from_pdf(raw)
            except ValueError as e:
                error = str(e)
            else:
                return render_template("index.html", error=error, ai_result=ai_result, text=text or "(Metin bulunamadı)")

        if action == "word_to_text":
            try:
                text = extract_text_from_docx(raw)
            except ValueError as e:
                error = str(e)
            else:
                return render_template("index.html", error=error, ai_result=ai_result, text=text or "(Boş)")

    return render_template("index.html", error=error, ai_result=ai_result, text=text)


@app.route("/generate-qr", methods=["POST"])
def generate_qr():
    try:
        qr_text = request.form.get("qr_text", "").strip()
        size = int(request.form.get("qr_size", 512))
        if not qr_text:
            return jsonify({"error": "Metin veya link girin"}), 400
        size = max(128, min(2048, size))
    except (ValueError, TypeError):
        return jsonify({"error": "Geçersiz boyut"}), 400

    try:
        import qrcode
        buf = io.BytesIO()
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(qr_text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((size, size))
        img.save(buf, format="PNG")
        buf.seek(0)
        return send_file(buf, mimetype="image/png", as_attachment=False, download_name="qr-code.png")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/compress-image", methods=["POST"])
def compress_image():
    file = request.files.get("file")
    if not file or file.filename == "":
        return jsonify({"error": "Dosya seçin"}), 400
    try:
        quality = int(request.form.get("quality", 80))
        quality = max(10, min(100, quality))
    except (ValueError, TypeError):
        quality = 80

    try:
        from PIL import Image
        img = Image.open(io.BytesIO(file.read()))
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        buf.seek(0)
        return send_file(buf, mimetype="image/jpeg", as_attachment=True, download_name="image_compressed.jpg")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/image-to-pdf", methods=["POST"])
def image_to_pdf():
    file = request.files.get("file")
    if not file or file.filename == "":
        return jsonify({"error": "Dosya seçin"}), 400

    try:
        from PIL import Image
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.utils import ImageReader
        from reportlab.pdfgen import canvas

        raw = file.read()
        img = Image.open(io.BytesIO(raw))
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="JPEG", quality=95)
        img_bytes.seek(0)

        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        w, h = A4
        iw, ih = img.size
        scale = min(w / iw, h / ih)
        c.drawImage(ImageReader(img_bytes), 0, 0, width=iw * scale, height=ih * scale)
        c.save()
        buf.seek(0)
        return send_file(buf, mimetype="application/pdf", as_attachment=True, download_name="image.pdf")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
