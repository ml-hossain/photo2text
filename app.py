from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import cv2
import pytesseract
from PIL import Image
import sqlite3
from datetime import datetime
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect('photo2text.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS extractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            extracted_text TEXT NOT NULL,
            confidence_score REAL,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            file_size INTEGER,
            image_width INTEGER,
            image_height INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()

def extract_text_from_image(image_path):
    """Extract text from image using Tesseract OCR"""
    try:
        # Read image using PIL
        image = Image.open(image_path)
        
        # Get image dimensions
        width, height = image.size
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Use Tesseract to extract text with confidence scores
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        
        # Extract text and calculate average confidence
        text_parts = []
        confidences = []
        
        for i in range(len(data['text'])):
            if int(data['conf'][i]) > 0:  # Only include text with confidence > 0
                text_parts.append(data['text'][i])
                confidences.append(int(data['conf'][i]))
        
        extracted_text = ' '.join(text_parts).strip()
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        return {
            'text': extracted_text,
            'confidence': avg_confidence,
            'width': width,
            'height': height
        }
    
    except Exception as e:
        print(f"Error extracting text: {e}")
        return {
            'text': '',
            'confidence': 0,
            'width': 0,
            'height': 0
        }

def save_extraction_to_db(filename, original_filename, extracted_text, confidence, file_size, width, height):
    """Save extraction results to database"""
    conn = sqlite3.connect('photo2text.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO extractions 
        (filename, original_filename, extracted_text, confidence_score, file_size, image_width, image_height)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (filename, original_filename, extracted_text, confidence, file_size, width, height))
    
    extraction_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return extraction_id

@app.route('/')
def index():
    """Main page with upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and text extraction"""
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{original_filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save uploaded file
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        # Extract text from image
        extraction_result = extract_text_from_image(file_path)
        
        # Save to database
        extraction_id = save_extraction_to_db(
            unique_filename,
            original_filename,
            extraction_result['text'],
            extraction_result['confidence'],
            file_size,
            extraction_result['width'],
            extraction_result['height']
        )
        
        flash('Text extracted successfully!')
        return redirect(url_for('view_extraction', extraction_id=extraction_id))
    
    else:
        flash('Invalid file type. Please upload an image file.')
        return redirect(url_for('index'))

@app.route('/extraction/<int:extraction_id>')
def view_extraction(extraction_id):
    """View extraction results"""
    conn = sqlite3.connect('photo2text.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM extractions WHERE id = ?
    ''', (extraction_id,))
    
    extraction = cursor.fetchone()
    conn.close()
    
    if extraction:
        extraction_data = {
            'id': extraction[0],
            'filename': extraction[1],
            'original_filename': extraction[2],
            'extracted_text': extraction[3],
            'confidence_score': extraction[4],
            'upload_time': extraction[5],
            'file_size': extraction[6],
            'image_width': extraction[7],
            'image_height': extraction[8]
        }
        return render_template('extraction.html', extraction=extraction_data)
    else:
        flash('Extraction not found')
        return redirect(url_for('index'))

@app.route('/history')
def history():
    """View all extractions"""
    conn = sqlite3.connect('photo2text.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, original_filename, upload_time, confidence_score, 
               SUBSTR(extracted_text, 1, 100) as preview
        FROM extractions 
        ORDER BY upload_time DESC
    ''')
    
    extractions = cursor.fetchall()
    conn.close()
    
    extractions_data = []
    for extraction in extractions:
        extractions_data.append({
            'id': extraction[0],
            'original_filename': extraction[1],
            'upload_time': extraction[2],
            'confidence_score': extraction[3],
            'preview': extraction[4] + ('...' if len(extraction[4]) == 100 else '')
        })
    
    return render_template('history.html', extractions=extractions_data)

@app.route('/api/extract', methods=['POST'])
def api_extract():
    """API endpoint for text extraction"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400
    
    # Generate unique filename
    original_filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{original_filename}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    
    # Save uploaded file
    file.save(file_path)
    file_size = os.path.getsize(file_path)
    
    # Extract text from image
    extraction_result = extract_text_from_image(file_path)
    
    # Save to database
    extraction_id = save_extraction_to_db(
        unique_filename,
        original_filename,
        extraction_result['text'],
        extraction_result['confidence'],
        file_size,
        extraction_result['width'],
        extraction_result['height']
    )
    
    return jsonify({
        'extraction_id': extraction_id,
        'extracted_text': extraction_result['text'],
        'confidence_score': extraction_result['confidence'],
        'image_dimensions': {
            'width': extraction_result['width'],
            'height': extraction_result['height']
        }
    })

@app.route('/api/extractions')
def api_extractions():
    """API endpoint to get all extractions"""
    conn = sqlite3.connect('photo2text.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM extractions ORDER BY upload_time DESC
    ''')
    
    extractions = cursor.fetchall()
    conn.close()
    
    extractions_data = []
    for extraction in extractions:
        extractions_data.append({
            'id': extraction[0],
            'filename': extraction[1],
            'original_filename': extraction[2],
            'extracted_text': extraction[3],
            'confidence_score': extraction[4],
            'upload_time': extraction[5],
            'file_size': extraction[6],
            'image_width': extraction[7],
            'image_height': extraction[8]
        })
    
    return jsonify(extractions_data)

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)