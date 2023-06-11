import logging

logger = logging.getLogger("dd_ci_i2i_202305")

# 输出DEBUG及以上级别的信息，针对所有输出的第一层过滤
logger.setLevel(level=logging.DEBUG)

# 获取文件日志句柄并设置日志级别，第二层过滤
handler = logging.FileHandler("../logs/dd_ci_i2i_202305.log")
handler.setLevel(logging.INFO)

# 生成并设置文件日志格式，其中name为上面设置的mylog
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# 获取流句柄并设置日志级别，第二层过滤
console = logging.StreamHandler()
console.setLevel(logging.WARNING)

# 为logger对象添加句柄
logger.addHandler(handler)
logger.addHandler(console)

