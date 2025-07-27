@echo off
title AI Candy Store RAG Demo
color 0A

echo.
echo  🍭 AI Candy Store RAG Demo 🍭
echo  ==============================
echo  Starting interactive RAG demonstration...
echo.
echo  Backend:  http://localhost:8000
echo  Frontend: http://localhost:3000
echo  
echo  Press Ctrl+C to stop both servers
echo  ==============================
echo.

:: Start backend in background
echo 🔧 Starting backend server...
start /b cmd /c "cd backend && venv\Scripts\activate && python openai_main.py"

:: Wait a moment for backend to initialize
echo ⏳ Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

:: Start frontend
echo 🎨 Starting frontend server...
cd frontend
start cmd /c "npm start"

echo.
echo ✅ Both servers are starting up!
echo 🌐 Frontend will be available at: http://localhost:3000
echo 🔧 Backend API available at: http://localhost:8000
echo 📖 API docs available at: http://localhost:8000/docs
echo.
echo ⏰ Please wait a moment for both servers to fully initialize...
echo 🛑 Close this window to stop the demo
echo.

:: Keep this window open
pause