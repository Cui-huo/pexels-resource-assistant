@echo off
chcp 65001 >nul
set CI_MODE=1
python test_setup.py
pause
