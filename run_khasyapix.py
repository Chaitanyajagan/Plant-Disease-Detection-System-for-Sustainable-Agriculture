#!/usr/bin/env python3
"""
KHASYAPIX - AI Plant Disease Detection System
Advanced Neural Network Technology for Sustainable Agriculture
"""

import subprocess
import sys
import os
import webbrowser
import time
import threading
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'tensorflow',
        'numpy',
        'Pillow',
        'pandas',
        'matplotlib',
        'seaborn',
        'scikit-learn',
        'opencv-python-headless'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("🔬 KHASYAPIX: Installing required neural network dependencies...")
        for package in missing_packages:
            print(f"   📦 Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
        print("✅ KHASYAPIX dependencies installed successfully!")
    
    return True

def check_model_file():
    """Check if the trained model file exists"""
    model_path = Path("trained_plant_disease_model.keras")
    if not model_path.exists():
        print("⚠️  KHASYAPIX Warning: Neural network model not found!")
        print("   Please ensure 'trained_plant_disease_model.keras' is in the project directory.")
        return False
    return True

def open_browser():
    """Open browser after a short delay"""
    time.sleep(3)
    webbrowser.open("http://localhost:8501")

def main():
    """Main function to run KHASYAPIX"""
    print("🔬" + "="*60)
    print("    KHASYAPIX - AI Plant Disease Detection System")
    print("    Advanced Neural Network Technology")
    print("="*60)
    print()
    
    # Check requirements
    print("🔍 Initializing KHASYAPIX neural network...")
    check_requirements()
    
    # Check model file
    print("🔍 Verifying neural network model...")
    check_model_file()
    
    # Create .streamlit directory if it doesn't exist
    streamlit_dir = Path(".streamlit")
    streamlit_dir.mkdir(exist_ok=True)
    
    # Start browser opening thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    print("\n🚀 Launching KHASYAPIX Neural Network Interface...")
    print("📱 The application will open in your browser automatically")
    print("🌐 Local Access: http://localhost:8501")
    print("🔗 Network Access: http://0.0.0.0:8501")
    print("\n💡 KHASYAPIX Features:")
    print("   🔬 Advanced AI-powered disease detection")
    print("   🌙 Vibrant dark theme with neon accents")
    print("   ⚡ Real-time neural network analysis")
    print("   📊 38 different plant disease classifications")
    print("   🎨 Modern UI with smooth animations")
    print("\n" + "="*60)
    
    try:
        # Run Streamlit with external access
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "main.py",
            "--server.address", "0.0.0.0",
            "--server.port", "8501",
            "--server.headless", "true",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down KHASYAPIX Neural Network System...")
        print("Thank you for using KHASYAPIX!")
    except Exception as e:
        print(f"\n❌ KHASYAPIX Error: {e}")
        print("Please check your installation and try again.")

if __name__ == "__main__":
    main()
