import os
import time
from _util_202305 import (
    sys_cmd,
    prRed,
    prGreen,
    prYellow,
    prLightPurple,
    prPurple,
    prCyan,
    prLightGray,
    prBlack,
)
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler

watch_path = "../tmp/input/ci-i2i"
fs = []
txt_out_path = "../tmp/output/ci-i2i/ci"
img_out_path = "../tmp/output/ci-i2i/i2i"


def cmd_ci_i2i(_src):
    left_src, right_src = os.path.splitext(_src)
    left, right = os.path.splitext(os.path.basename(_src))
    # print(_src, right)
    if right.lower() in [".json"]:
        st = time.time()
        prGreen(f"get: {_src}")
        _src_ = _src.split("\\")
        _txt_out_dir = os.path.join(txt_out_path, _src_[-2])
        _img_out_dir = os.path.join(img_out_path, _src_[-2])
        print(f"{_txt_out_dir}, {_img_out_dir}")

        _user_conf_json = "ci-i2i-user.json"
        _if_user_conf_json = f"{left_src}.json"
        # print(_if_user_conf_json)
        if os.path.exists(_if_user_conf_json):
            _user_conf_json = _if_user_conf_json
        prRed(f"{_user_conf_json}")

        cmd_ci_i2i = f"python ci-i2i-202305.py -txtoutdir {_txt_out_dir} -imgoutdir {_img_out_dir} -userconf {_user_conf_json}"
        prCyan(cmd_ci_i2i)
        sys_cmd(cmd_ci_i2i)

        et = time.time()
        dt = et - st
        dt_fmt = time.strftime("%H:%M:%S", time.gmtime(dt))
        print(f"<<< {dt_fmt}\n")


def cmd_if_new(_new):
    global fs
    if _new not in fs:
        cmd_ci_i2i(_new)
        fs.append(_new)
        left_new, right_new = os.path.splitext(os.path.basename(_new))
        if right_new.lower() in [".json"]:
            print(f"<<< {len(fs)}\n")


class input_EH(FileSystemEventHandler):
    def on_created(self, event):
        _src = event.src_path
        if event.is_directory:
            print(f"{_src}\n")
        else:
            cmd_if_new(_src)


if __name__ == "__main__":
    ob = Observer()
    ob.schedule(input_EH(), watch_path, recursive=True)
    # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    # ob.schedule(LoggingEventHandler(), watch_path, recursive=True)

    ob.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        ob.stop()
    ob.join()
