# Photo2Text

A web application that converts images to text using OCR (Optical Character Recognition) and stores the extracted data for future reference.

## Features

- **Image Upload**: Upload images in various formats (PNG, JPG, JPEG, GIF, BMP, TIFF)
- **Text Extraction**: Uses Tesseract OCR to extract text from images
- **Data Storage**: Stores extracted text in a SQLite database
- **History View**: Browse all previous extractions with search functionality
- **Web Interface**: Clean, responsive web interface
- **REST API**: JSON API endpoints for programmatic access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ml-hossain/photo2text.git
cd photo2text
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Tesseract OCR:
   - **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
   - **macOS**: `brew install tesseract`
   - **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your browser and go to `http://localhost:5000`

3. Upload an image and extract text!

## API Endpoints

- `GET /` - Main upload page
- `POST /upload` - Upload image and extract text
- `GET /history` - View extraction history
- `GET /api/texts` - Get all extractions as JSON

## Technology Stack

- **Backend**: Python Flask
- **OCR**: Tesseract via pytesseract
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Image Processing**: Pillow (PIL)

## File Structure

```
photo2text/
├── app.py              # Main Flask application
├── run.py              # Application runner
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html      # Base template
│   ├── index.html     # Upload page
│   └── history.html   # History page
└── uploads/           # Temporary upload directory
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.