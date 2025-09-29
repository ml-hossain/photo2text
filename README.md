# Photo2Text - Image to Text Converter

A powerful web application built with Python Flask that extracts text from images using OCR (Optical Character Recognition) technology and stores the results in a database.

## Features

- **Advanced OCR**: Extract text from images using Tesseract OCR
- **Web Interface**: Clean, responsive web interface with drag-and-drop functionality
- **Data Storage**: Store extracted text with metadata in SQLite database
- **Confidence Scoring**: Get accuracy confidence scores for extracted text
- **History Tracking**: View all previous extractions with search and filter options
- **Multiple Formats**: Support for PNG, JPG, JPEG, GIF, BMP, and TIFF images
- **API Endpoints**: RESTful API for programmatic access
- **Text Export**: Download extracted text as TXT files
- **Copy to Clipboard**: Easy text copying functionality

## Quick Start

### Prerequisites

- Python 3.7+
- Tesseract OCR

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd photo2text
   ```

2. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   sudo ./setup.sh
   ```

3. **Start the application:**
   ```bash
   python app.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:5000`

## Manual Installation

If you prefer manual installation:

1. **Install system dependencies:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install tesseract-ocr tesseract-ocr-eng

   # macOS
   brew install tesseract

   # Windows
   # Download and install from: https://github.com/UB-Mannheim/tesseract/wiki
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

## Usage

### Web Interface

1. **Upload Image**: 
   - Drag and drop an image file onto the upload area
   - Or click "Choose File" to browse and select an image

2. **Extract Text**: 
   - Click "Extract Text" button
   - Wait for processing to complete

3. **View Results**:
   - See extracted text with confidence score
   - Copy text to clipboard
   - Download as TXT file
   - View extraction history

### API Usage

The application provides RESTful API endpoints:

#### Extract Text from Image
```bash
curl -X POST -F "file=@image.jpg" http://localhost:5000/api/extract
```

Response:
```json
{
  "extraction_id": 1,
  "extracted_text": "Sample extracted text...",
  "confidence_score": 85.5,
  "image_dimensions": {
    "width": 1920,
    "height": 1080
  }
}
```

#### Get All Extractions
```bash
curl http://localhost:5000/api/extractions
```

### Python Integration

You can also integrate the OCR functionality directly in your Python code:

```python
from app import extract_text_from_image

# Extract text from an image file
result = extract_text_from_image('path/to/image.jpg')
print(f"Extracted text: {result['text']}")
print(f"Confidence: {result['confidence']}%")
```

## Core Functions

### Main Functions

1. **`extract_text_from_image(image_path)`**
   - Extracts text from image using Tesseract OCR
   - Returns text, confidence score, and image dimensions
   - Handles various image formats and preprocessing

2. **`save_extraction_to_db(filename, original_filename, extracted_text, confidence, file_size, width, height)`**
   - Saves extraction results to SQLite database
   - Stores metadata including timestamps and file information
   - Returns unique extraction ID

3. **`init_database()`**
   - Initializes SQLite database with required tables
   - Creates extraction history schema
   - Handles database migrations

### API Endpoints

- **`POST /upload`** - Web form upload and extraction
- **`GET /extraction/<id>`** - View specific extraction result
- **`GET /history`** - View all extraction history  
- **`POST /api/extract`** - API endpoint for text extraction
- **`GET /api/extractions`** - API endpoint to get all extractions

## Database Schema

The application uses SQLite with the following schema:

```sql
CREATE TABLE extractions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    extracted_text TEXT NOT NULL,
    confidence_score REAL,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_size INTEGER,
    image_width INTEGER,
    image_height INTEGER
);
```

## Configuration

### Environment Variables

- `FLASK_ENV`: Set to 'development' for debug mode
- `SECRET_KEY`: Flask secret key (change from default)
- `UPLOAD_FOLDER`: Directory for uploaded files (default: 'uploads')
- `MAX_CONTENT_LENGTH`: Maximum file size in bytes (default: 16MB)

### Tesseract Configuration

The application uses default Tesseract settings. You can modify OCR parameters in the `extract_text_from_image()` function:

```python
# Custom Tesseract configuration
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(image, config=custom_config)
```

## File Structure

```
photo2text/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── setup.sh              # Setup script
├── README.md             # This file
├── templates/            # HTML templates
│   ├── index.html        # Main upload page
│   ├── extraction.html   # Results page
│   └── history.html      # History page
├── uploads/              # Uploaded files (created automatically)
└── photo2text.db         # SQLite database (created automatically)
```

## Supported Image Formats

- PNG
- JPG/JPEG
- GIF
- BMP
- TIFF

## Error Handling

The application includes comprehensive error handling for:

- Invalid file formats
- Corrupted images
- OCR processing errors
- Database connection issues
- File system permissions

## Performance Tips

1. **Image Quality**: Higher resolution images generally produce better OCR results
2. **File Size**: Images are automatically processed; very large files may take longer
3. **Text Clarity**: Clear, high-contrast text works best
4. **Language Support**: Install additional Tesseract language packs for non-English text

## Security Considerations

- File uploads are validated for allowed extensions
- Uploaded files are stored with unique names to prevent conflicts
- SQL injection protection through parameterized queries
- File size limits prevent DoS attacks

## Troubleshooting

### Common Issues

1. **"Tesseract not found"**
   - Ensure Tesseract OCR is installed and in PATH
   - On Windows, add Tesseract installation directory to PATH

2. **"Permission denied" errors**
   - Check file permissions for upload directory
   - Ensure database file is writable

3. **Poor OCR results**
   - Try higher resolution images
   - Ensure good contrast between text and background
   - Check if text orientation is correct

### Debug Mode

Run with debug mode for detailed error messages:

```bash
export FLASK_ENV=development
python app.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Tesseract OCR for text extraction engine
- Flask framework for web application
- Bootstrap for responsive UI components