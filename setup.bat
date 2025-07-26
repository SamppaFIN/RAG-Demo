@echo off
title AI Candy Store RAG Demo - Setup
color 0A

echo.
echo  🍭 AI Candy Store RAG Demo Setup 🍭
echo  ====================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python first:
    echo 1. Visit https://python.org/downloads
    echo 2. Download Python 3.11 or newer
    echo 3. During installation, check "Add Python to PATH"
    echo 4. Run this script again after installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python found!
python --version

:: Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed
    echo.
    echo Please install Node.js first:
    echo 1. Visit https://nodejs.org
    echo 2. Download the LTS version
    echo 3. Run this script again after installation
    echo.
    pause
    exit /b 1
)

echo ✅ Node.js found!
node --version

echo.
echo 🔧 Setting up backend...
echo.

:: Setup backend
cd backend

:: Create virtual environment
echo Creating Python virtual environment...
python -m venv venv

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

echo ✅ Backend setup complete!

:: Return to root directory
cd ..

echo.
echo 🎨 Setting up frontend...
echo.

:: Setup frontend
cd frontend

:: Install Node.js dependencies
echo Installing Node.js dependencies...
npm install

if %errorlevel% neq 0 (
    echo ❌ Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo ✅ Frontend setup complete!

:: Return to root directory
cd ..

echo.
echo 🎉 Setup completed successfully!
echo.
echo To start the demo, you can either:
echo 1. Run "start_demo.bat" for automatic startup
echo 2. Or manually start both servers:
echo    - Backend: cd backend ^&^& venv\Scripts\activate ^&^& python main.py
echo    - Frontend: cd frontend ^&^& npm start
echo.
echo The demo will be available at:
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend:  http://localhost:8000
echo.
pause 