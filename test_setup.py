#!/usr/bin/env python3
"""
Test script to verify the Photo2Text application setup
"""

import sys
import os
import tempfile
from PIL import Image, ImageDraw, ImageFont

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_test_image():
    """Create a simple test image with text"""
    # Create a white image
    img = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add some text
    text = "Hello World!\nThis is a test image\nfor OCR extraction."
    
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        font = None
    
    # Draw text on image
    draw.text((50, 50), text, fill='black', font=font)
    
    # Save to temporary file
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    img.save(temp_file.name)
    return temp_file.name

def test_ocr():
    """Test OCR functionality"""
    print("Testing OCR functionality...")
    
    try:
        from app import extract_text_from_image
        
        # Create test image
        test_image_path = create_test_image()
        print(f"Created test image: {test_image_path}")
        
        # Extract text
        result = extract_text_from_image(test_image_path)
        
        print(f"Extracted text: '{result['text']}'")
        print(f"Confidence score: {result['confidence']:.1f}%")
        print(f"Image dimensions: {result['width']}x{result['height']}")
        
        # Clean up
        os.unlink(test_image_path)
        
        if result['text'].strip():
            print("✅ OCR test PASSED - Text was extracted successfully!")
            return True
        else:
            print("❌ OCR test FAILED - No text was extracted")
            return False
            
    except Exception as e:
        print(f"❌ OCR test FAILED - Error: {e}")
        return False

def test_database():
    """Test database functionality"""
    print("\nTesting database functionality...")
    
    try:
        from app import init_database, save_extraction_to_db
        
        # Initialize database
        init_database()
        print("✅ Database initialized successfully")
        
        # Test saving extraction
        extraction_id = save_extraction_to_db(
            "test.png", 
            "test_original.png", 
            "Test extracted text", 
            85.5, 
            1024, 
            400, 
            200
        )
        
        print(f"✅ Test extraction saved with ID: {extraction_id}")
        return True
        
    except Exception as e:
        print(f"❌ Database test FAILED - Error: {e}")
        return False

def test_dependencies():
    """Test all required dependencies"""
    print("Testing dependencies...")
    
    dependencies = [
        'flask',
        'PIL', 
        'pytesseract',
        'cv2',
        'sqlite3'
    ]
    
    failed_deps = []
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} imported successfully")
        except ImportError as e:
            print(f"❌ {dep} import FAILED: {e}")
            failed_deps.append(dep)
    
    return len(failed_deps) == 0

def main():
    """Run all tests"""
    print("=== Photo2Text Application Test ===\n")
    
    tests_passed = 0
    total_tests = 3
    
    # Test dependencies
    if test_dependencies():
        tests_passed += 1
    
    # Test database
    if test_database():
        tests_passed += 1
    
    # Test OCR
    if test_ocr():
        tests_passed += 1
    
    print(f"\n=== Test Results ===")
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 All tests PASSED! Your Photo2Text application is ready to use.")
        print("\nTo start the application, run:")
        print("  python app.py")
        print("\nThen open your browser to: http://localhost:5000")
    else:
        print("❌ Some tests FAILED. Please check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())