每次机器重启后，需要运行下面几个服务（已在win10的“任务计划程序”中设置）：

# “从封面图片生成益智题目集”（F:\dd-llm）
## 运行
···
cd dd-llm
venv/Script/activate
python ui_cn.py
···

# “从文本描述生成音乐旋律”（F:\dd-melody）
## 运行
···
cd dd-melody
venv/Script/activate
python ui_cn.py
···

# Ai画画服务（F:\dd-ci-i2i-v2）
## 运行
···
cd dd-ci-i2i-v2
dd-runui.bat
···

# DayDream工作流（F:\_workflow）
## 运行
···
cd _workflow
venv310-ci-i2i/Script/activate
cd ci-i2i-202305
python watch-ci-i2i-202305.py
···

# WLS 运行DayDream数据连接（/mnt/e/tanyue_script）
## 运行
···
cd /mnt/e/tanyue_script/
start.sh
ps -ef|grep watch
···

