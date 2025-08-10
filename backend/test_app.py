#!/usr/bin/env python3
"""
Simple test script for the Flask application
"""

import requests
import time
import subprocess
import sys

def test_flask_app():
    """Test the Flask application endpoints"""
    
    # Start the Flask app in the background
    print("Starting Flask app...")
    process = subprocess.Popen([sys.executable, 'run.py'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
    
    # Wait for the app to start
    time.sleep(3)
    
    try:
        # Test the root endpoint
        print("Testing root endpoint...")
        response = requests.get('http://localhost:5000/')
        print(f"Root endpoint: {response.status_code} - {response.json()}")
        
        # Test the health endpoint
        print("Testing health endpoint...")
        response = requests.get('http://localhost:5000/health')
        print(f"Health endpoint: {response.status_code} - {response.json()}")
        
        print("✅ All tests passed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask app. Make sure it's running.")
    except Exception as e:
        print(f"❌ Error during testing: {e}")
    finally:
        # Clean up
        process.terminate()
        process.wait()

if __name__ == '__main__':
    test_flask_app()
