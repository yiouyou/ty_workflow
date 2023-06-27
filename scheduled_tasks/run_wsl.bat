@echo off
wsl bash -c "cd /mnt/e/tanyue_script && bash ./start.sh && ls && ps -ef|grep watch"

pause
