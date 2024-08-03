from flask import Flask, request, render_template, send_file, redirect, url_for
from PyPDF2 import PdfReader
from googletrans import Translator
import os

app = Flask(__name__)

# Ensure output directory exists
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the file from the form submission
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        # Read PDF content
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        
        # Translate text
        translator = Translator()
        translated = translator.translate(text, dest='fr')  # Translate to French
        translated_text = translated.text
        
        # Save the translated text to a file
        output_file_path = os.path.join(OUTPUT_DIR, 'translated_output.pdf')
        with open(output_file_path, 'w') as output_file:
            output_file.write(translated_text)

        return send_file(output_file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
