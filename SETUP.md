# 🛠️ Setup Guide - AI Candy Store RAG Demo

This guide will help you get the AI Candy Store RAG Demo running on your system.

## 📋 Prerequisites Check

Before starting, let's check what you have installed:

### 1. Check Node.js (✅ Required for Frontend)
```bash
node --version
npm --version
```
- **Required**: Node.js 16+ and npm
- **Your system**: ✅ Node.js v22.16.0, npm 10.9.2

### 2. Check Python (❌ Currently Missing)
```bash
python --version
# or
python3 --version
```
- **Required**: Python 3.8+
- **Your system**: ❌ Not installed

## 🐍 Install Python

### Windows (Recommended Method)

**Option 1: Microsoft Store (Easiest)**
1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.12"
3. Click "Install"
4. After installation, test: `python --version`

**Option 2: Official Python Installer**
1. Go to [python.org/downloads](https://python.org/downloads/)
2. Download Python 3.11 or 3.12 for Windows
3. Run the installer
4. ⚠️ **IMPORTANT**: Check "Add Python to PATH" during installation
5. Test: `python --version`

### macOS
```bash
# Using Homebrew (recommended)
brew install python@3.11

# Or download from python.org
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

## 🚀 Quick Start (After Python Installation)

### Method 1: Automatic Setup (Windows)
1. Double-click `setup.bat` (will be created below)
2. Wait for installation to complete
3. Access the demo at `http://localhost:3000`

### Method 2: Manual Setup

#### Step 1: Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
python main.py
```

#### Step 2: Frontend Setup (New Terminal)
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## 🔧 Troubleshooting

### Python Issues

**Problem**: "Python not found" error
**Solution**: 
1. Restart your terminal after Python installation
2. Try `python3` instead of `python`
3. Check if Python is in your PATH

**Problem**: "pip not found"
**Solution**:
```bash
python -m ensurepip --upgrade
```

### Node.js Issues

**Problem**: npm install fails
**Solution**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and try again
rm -rf node_modules
npm install
```

### Port Issues

**Problem**: Port 8000 or 3000 already in use
**Solution**:
```bash
# Find and kill processes using the ports
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

## 🌟 Optional Enhancements

### Add AI Integration
1. Get an OpenAI API key from [platform.openai.com](https://platform.openai.com)
2. Create `backend/.env` file:
```
OPENAI_API_KEY=your_api_key_here
```
3. Restart the backend server

### Docker Alternative
If you prefer Docker:
```bash
# Build and run (requires Docker Desktop)
docker-compose up --build
```

## 📞 Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Look at common issues in the troubleshooting section above
- Create an issue if you encounter problems

## ✅ Verification Steps

After setup, verify everything works:

1. ✅ Backend responds: Visit `http://localhost:8000/health`
2. ✅ Frontend loads: Visit `http://localhost:3000`
3. ✅ RAG demo works: Ask "What's the sweetest candy?"
4. ✅ Language toggle: Switch between English and Finnish
5. ✅ Theme toggle: Switch between light and dark mode

Happy candy exploring! 🍭✨ 