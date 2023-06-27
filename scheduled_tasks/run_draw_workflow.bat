@echo off
call F:\_workflow\venv310-ci-i2i\Scripts\activate.bat
cd /d F:\_workflow\ci-i2i-202305
python watch-ci-i2i-202305.py

pause
