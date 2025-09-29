@echo off
echo ============================================================
echo SETUP GIT REPOSITORY - SOBS ZALO TOKEN
echo ============================================================

REM Initialize Git repository
git init

REM Add remote repository
git remote add origin https://github.com/huyphan5677/sobs_zalo_token.git

REM Configure user (replace with your info)
git config user.name "Your Name"
git config user.email "your.email@example.com"

REM Create .gitignore
echo zalo_access_token.txt > .gitignore
echo __pycache__/ >> .gitignore
echo *.pyc >> .gitignore
echo *.log >> .gitignore

REM Add all files except ignored ones
git add .

REM Commit with message
git commit -m "Initial commit: Zalo OA Token Generator

Features:
- OAuth flow automation
- Access token generation 
- API client wrapper
- Interactive menu system
- Configuration management"

REM Push to GitHub (may require authentication)
git branch -M main
git push -u origin main

echo ============================================================
echo DONE! Repository pushed to GitHub
echo https://github.com/huyphan5677/sobs_zalo_token.git
echo ============================================================
pause