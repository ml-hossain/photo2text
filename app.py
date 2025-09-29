import os
import sqlite3
from datetime import datetime
from flask import Flask, request, render_template, jsonify, redirect, url_for
from PIL import Image
import pytesseract
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database setup
def init_db():
    conn = sqlite3.connect('photo2text.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS extracted_texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            extracted_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_image(image_path):
    """Extract text from image using OCR"""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"Error extracting text: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from image
        extracted_text = extract_text_from_image(filepath)
        
        # Save to database
        conn = sqlite3.connect('photo2text.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO extracted_texts (filename, extracted_text) VALUES (?, ?)',
            (filename, extracted_text)
        )
        conn.commit()
        conn.close()
        
        # Clean up uploaded file (optional)
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'extracted_text': extracted_text
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/history')
def history():
    conn = sqlite3.connect('photo2text.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM extracted_texts ORDER BY created_at DESC')
    texts = cursor.fetchall()
    conn.close()
    return render_template('history.html', texts=texts)

@app.route('/api/texts')
def api_texts():
    conn = sqlite3.connect('photo2text.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM extracted_texts ORDER BY created_at DESC')
    texts = cursor.fetchall()
    conn.close()
    
    # Convert to list of dictionaries
    result = []
    for text in texts:
        result.append({
            'id': text[0],
            'filename': text[1],
            'extracted_text': text[2],
            'created_at': text[3]
        })
    
    return jsonify(result)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)