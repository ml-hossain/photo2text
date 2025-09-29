#!/usr/bin/env python3
"""
Photo2Text Web Application
A simple web application for extracting text from images using OCR.
"""

from app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)