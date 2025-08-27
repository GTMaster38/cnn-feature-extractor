#!/usr/bin/env python3
"""
Local test script for CNN Feature Extractor
Run this to verify your app works before deploying to EC2
"""

import requests
import base64
import io
from PIL import Image
import numpy as np

def create_test_image():
    """Create a simple test image for testing"""
    # Create a 100x100 test image with some patterns
    img_array = np.zeros((100, 100), dtype=np.uint8)
    
    # Add some test patterns
    img_array[20:30, 20:80] = 255  # Horizontal line
    img_array[40:80, 40:50] = 255  # Vertical line
    img_array[60:70, 60:90] = 128  # Gray rectangle
    
    # Convert to PIL Image
    img = Image.fromarray(img_array)
    
    # Save to bytes buffer
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return buffer

def test_app():
    """Test the Flask application"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing CNN Feature Extractor...")
    
    try:
        # Test 1: Check if app is running
        print("1. Testing if app is running...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("   ✅ App is running!")
        else:
            print(f"   ❌ App returned status code: {response.status_code}")
            return False
            
        # Test 2: Test health endpoint
        print("2. Testing health endpoint...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("   ✅ Health endpoint working!")
            print(f"   📊 Response: {response.json()}")
        else:
            print(f"   ❌ Health endpoint failed: {response.status_code}")
            
        # Test 3: Test image upload and processing
        print("3. Testing image processing pipeline...")
        
        # Create test image
        test_img = create_test_image()
        
        # Test convolution
        files = {'image_upload': ('test.png', test_img, 'image/png')}
        data = {
            'action': 'convolve',
            'filter_select': 'Edge Detect'
        }
        
        response = requests.post(f"{base_url}/", files=files, data=data)
        if response.status_code == 200:
            print("   ✅ Convolution step working!")
        else:
            print(f"   ❌ Convolution failed: {response.status_code}")
            return False
            
        print("\n🎉 All tests passed! Your app is ready for deployment.")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the app. Make sure it's running on localhost:5000")
        print("   Run: python app.py")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    print("CNN Feature Extractor - Local Test")
    print("=" * 40)
    
    success = test_app()
    
    if success:
        print("\n🚀 Ready for EC2 deployment!")
        print("📚 Check README.md for deployment instructions")
    else:
        print("\n🔧 Fix the issues above before deploying")
        print("💡 Make sure to run: python app.py")
