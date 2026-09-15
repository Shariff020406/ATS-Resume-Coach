@echo off
title ATS Resume Chatbot - WhatsApp Server
color 0A
echo.
echo  ================================================
echo   ANTIGRAVITY ATS CHATBOT - WHATSAPP SERVER
echo  ================================================
echo.
cd /d "%~dp0"
python run_with_tunnel.py
echo.
echo [SERVER STOPPED] Press any key to restart...
pause
python run_with_tunnel.py
