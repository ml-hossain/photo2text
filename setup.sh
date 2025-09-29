#!/bin/bash

# Install system dependencies for Tesseract OCR
echo "Installing system dependencies..."
apt-get update
apt-get install -y tesseract-ocr tesseract-ocr-eng

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setup complete!"
echo "You can now run the application with: python app.py"