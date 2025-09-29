#!/usr/bin/env python3
"""
Example usage of the Photo2Text API
This script demonstrates how to interact with the Photo2Text application programmatically.
"""

import requests
import json

# Example 1: Get all extracted texts via API
def get_all_texts():
    """Retrieve all stored text extractions"""
    try:
        response = requests.get('http://localhost:5000/api/texts')
        if response.status_code == 200:
            texts = response.json()
            print(f"Found {len(texts)} extracted texts:")
            for text in texts:
                print(f"ID: {text['id']}, File: {text['filename']}")
                print(f"Text preview: {text['extracted_text'][:100]}...")
                print(f"Date: {text['created_at']}\n")
        else:
            print(f"Error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Error: Make sure the Flask application is running on localhost:5000")

# Example 2: Upload an image programmatically
def upload_image(image_path):
    """Upload an image and extract text"""
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post('http://localhost:5000/upload', files=files)
            
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print(f"Successfully extracted text from {result['filename']}:")
                print(result['extracted_text'])
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")
        else:
            print(f"Error: {response.status_code}")
    except FileNotFoundError:
        print(f"Error: Image file '{image_path}' not found")
    except requests.exceptions.ConnectionError:
        print("Error: Make sure the Flask application is running on localhost:5000")

if __name__ == '__main__':
    print("Photo2Text API Examples")
    print("=" * 30)
    
    # Example usage:
    # get_all_texts()
    # upload_image('path/to/your/image.jpg')
    
    print("Uncomment the function calls above to test the API")
    print("Make sure to start the Flask app first: python app.py")