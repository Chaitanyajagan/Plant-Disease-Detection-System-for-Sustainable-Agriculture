@echo off
title KHASYAPIX - AI Plant Disease Detection System
color 0A

echo.
echo ================================================================
echo    🔬 KHASYAPIX - AI Plant Disease Detection System
echo    Advanced Neural Network Technology for Sustainable Agriculture
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found - Initializing KHASYAPIX
echo.

REM Check if main.py exists
if not exist "main.py" (
    echo ❌ main.py not found in current directory
    echo Please run this script from the KHASYAPIX project directory
    pause
    exit /b 1
)

echo ✅ KHASYAPIX neural network files found
echo.

REM Install/upgrade required packages
echo 🔬 KHASYAPIX: Installing neural network dependencies...
python -m pip install --upgrade pip
python -m pip install streamlit tensorflow numpy Pillow pandas matplotlib seaborn scikit-learn opencv-python-headless

echo.
echo 🚀 Launching KHASYAPIX Neural Network Interface...
echo 📱 The application will open in your browser automatically
echo 🌐 Local URL: http://localhost:8501
echo 🔗 Network URL: http://0.0.0.0:8501
echo.
echo 💡 KHASYAPIX Features:
echo    🔬 Advanced AI-powered disease detection
echo    🌙 Vibrant dark theme with neon accents
echo    ⚡ Real-time neural network analysis
echo    📊 38 different plant disease classifications
echo    🎨 Modern UI with smooth animations
echo.
echo ================================================================
echo.

REM Start the KHASYAPIX application
python run_khasyapix.py

echo.
echo 👋 KHASYAPIX Neural Network System closed
pause
