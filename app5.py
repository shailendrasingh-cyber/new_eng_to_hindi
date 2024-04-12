from flask import Flask, render_template, request, flash, redirect, url_for
import fitz  # PyMuPDF
from googletrans import Translator
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for flash messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    if 'pdf_file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))

    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))

    upload_folder = 'uploads'
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, pdf_file.filename)
    pdf_file.save(file_path)

    pdf_content = extract_text_from_pdf(file_path)

    if pdf_content is None:
        flash('Error extracting text from PDF')
        return redirect(url_for('index'))

    translated_content = translate_text(pdf_content)

    os.remove(file_path)

    if translated_content is None:
        flash('Error translating text')
        return redirect(url_for('index'))

    return render_template('result.html', translated_content=translated_content)

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def translate_text(text):
    try:
        translator = Translator()
        translated_result = translator.translate(text, dest='hi')
        if translated_result.text:
            translated_text = translated_result.text
        else:
            translated_text = "Translation not available"
        return translated_text
    except Exception as e:
        print(f"Error translating text: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
