from PIL import Image
from pprint import pprint
import re
import io
import os
import json
import time
import numpy
import base64
import random
import requests
import subprocess
import _log_ci_i2i_202305 as _log


_ip = "127.0.0.1"
_port = "12345"
url = f"http://{_ip}:{_port}"


def sys_cmd(_str):
    st = time.time()
    _log.logger.info(f">>> {_str}")
    _out = subprocess.getoutput(_str)
    _log.logger.info(f">>> {_out}")
    time.sleep(1)
    et = time.time()
    dt = et - st
    dt_fmt = time.strftime("%H:%M:%S", time.gmtime(dt))
    _log.logger.info(f"<<< {dt_fmt}\n\n")


def run_cmd(_str):
    _out = subprocess.getoutput(_str)
    time.sleep(1)


def api_upscale(img_in, img_out):
    _url = f"{url}/sdapi/v1/extra-single-image"
    _up_X = 4
    _payload = {
        "image": b64_img(img_in),
        # "resize_mode": 0,
        # "show_extras_results": True,
        # "gfpgan_visibility": 0,
        # "codeformer_visibility": 0,
        # "codeformer_weight": 0,
        "upscaling_resize": _up_X,
        # "upscaling_resize_w": 512,
        # "upscaling_resize_h": 512,
        # "upscaling_crop": True,
        "upscaler_1": "R-ESRGAN 4x+",
        "upscaler_2": "None",
        # "extras_upscaler_2_visibility": 0,
        # "upscale_first": False,
    }
    req = requests.post(url=_url, json=_payload)
    # print(req)
    left, right = os.path.splitext(img_out)
    out_png = f"{left}_{_up_X}x.png"
    r_image = ""
    if req.status_code == 200:
        r = req.json()
        r_image = r["image"]
    if r_image:
        # prYellow(out_png)
        print(out_png)
        i_img2img = Image.open(io.BytesIO(base64.b64decode(r_image)))
        i_img2img.save(out_png)
    return out_png


def api_interrogate(img_fn):
    _url = f"{url}/sdapi/v1/interrogate"
    _payload = {"image": b64_img(img_fn), "model": "clip"}
    req = requests.post(url=_url, json=_payload)
    _content = ""
    _style = ""
    if req.status_code == 200:
        req_json = req.json()
        _caption = req_json["caption"]
        # print(_caption)
        if _caption:
            _s = _caption.split(", ")
            if _s[0][-1] == ",":
                _content = _s[0][:-1]
            else:
                _content = _s[0]
            _style = ", ".join(_s[1:])
    # print(f'content: {_content}\nstyle: {_style}')
    return _content, _style


def api_reload_model(_model):
    _url = f"{url}/sdapi/v1/options"
    req = requests.get(url=_url)
    if req.status_code == 200:
        req_json = req.json()
        _old = req_json["sd_model_checkpoint"]
        # print(f'current model: {_old}')
    _payload = {
        "sd_model_checkpoint": _model,
    }
    req = requests.post(url=_url, json=_payload)
    _new = ""
    _hash = ""
    if req.status_code == 200:
        req_check = requests.get(url=_url)
        if req_check.status_code == 200:
            req_json = req_check.json()
            _new = req_json["sd_model_checkpoint"]
            # print(f'replaced model: {_new}')
            _hash = req_json["sd_checkpoint_hash"]
    return _new, _hash


def api_t2i(_payload, _out, model_name):
    _url = f"{url}/sdapi/v1/txt2img"
    req = requests.post(url=_url, json=_payload)
    # print(req)
    r_images = ""
    r_info = ""
    if req.status_code == 200:
        r = req.json()
        r_images = r["images"]
        r_info = r["info"]
    if r_images and r_info:
        r_info_json = json.loads(r_info)
        # pprint(r_info_json)
        infotexts = info_report(r_info_json, model_name)
        out_txt = f"{_out}.txt"
        # prYellow(out_txt)
        print(out_txt)
        with open(out_txt, "w", encoding="utf8") as _txt:
            _txt.write(infotexts)
        _n = len(r_images)
        if _n >= 1:
            out_png = f"{_out}_ignore.png"
            print(out_png)
            i_img2img = Image.open(io.BytesIO(base64.b64decode(r_images[0])))
            i_img2img.save(out_png)
        # for i in range(_n):
        #     if _n == 1:
        #         out_png = f"{_out}.png"
        #     else:
        #         out_png = f"{_out}_{i}.png"
        #     # prYellow(out_png)
        #     print(out_png)
        #     i_img2img = Image.open(io.BytesIO(base64.b64decode(r_images[i])))
        #     i_img2img.save(out_png)


def api_i2i(_payload, _out, model_name):
    _url = f"{url}/sdapi/v1/img2img"
    req = requests.post(url=_url, json=_payload)
    print(req)
    r_images = ""
    r_info = ""
    if req.status_code == 200:
        r = req.json()
        r_images = r["images"]
        r_info = r["info"]
    if r_images and r_info:
        r_info_json = json.loads(r_info)
        # pprint(r_info_json)
        infotexts = info_report(r_info_json, model_name)
        out_txt = f"{_out}.txt"
        # prYellow(out_txt)
        print(out_txt)
        with open(out_txt, "w", encoding="utf8") as _txt:
            _txt.write(infotexts)
        _n = len(r_images)
        if _n >= 1:
            out_png = f"{_out}_ignore.png"
            print(out_png)
            i_img2img = Image.open(io.BytesIO(base64.b64decode(r_images[0])))
            i_img2img.save(out_png)
        # for i in range(_n):
        #     if _n == 1:
        #         out_png = f"{_out}.png"
        #     else:
        #         out_png = f"{_out}_{i}.png"
        #     # prYellow(out_png)
        #     print(out_png)
        #     i_img2img = Image.open(io.BytesIO(base64.b64decode(r_images[i])))
        #     i_img2img.save(out_png)


def parse_creative(creative, sys_payload):
    _re = sys_payload
    if creative == "高":
        if _re["denoising_strength"] < 0.95:
            _re["denoising_strength"] = 0.95
    elif creative == "中":
        if _re["denoising_strength"] < 0.75:
            _re["denoising_strength"] = 0.75
    elif creative == "低":
        if _re["denoising_strength"] < 0.2:
            _re["denoising_strength"] = 0.2
    else:
        print(f"ERROR: creative（{creative}） must be 高/中/低!")
    return _re


def parse_sd1x_lora(lora):
    _lora = {
        "多彩": "_happyyu:0.7",
        "线稿": "_Lineart",
        "大头3D": "cbzbb",
        "大头2D": "chibi",
        "玻璃": "glasssculpture:0.6",
        "温暖": "khyle:0.75",
        "矢量艺术": "kurzgesagt",
        "线条阴影": "kyabakurabakufu",
        "土豆泥": "made_of_mashed_potatoes_and_gravy",
        "猫眼圆手": "neco-arc",
        "定格3D": "zukki_style",
    }
    _style = []
    for i in lora:
        if lora[i] != 0:
            i_lora = _lora[i]
            i_lora_ = i_lora.split(":")
            if len(i_lora_) == 2:
                i_str = f"<lora:{i_lora}>"
            else:
                i_str = f"<lora:{i_lora}:{lora[i]}>"
            if i[0] != "_":
                i_str = f"{i_str}, {i_lora.replace('_', ' ')}"
            _style.append(i_str)
    _str = ", ".join(_style)
    return _str


def parse_ctrl_net(_str):
    _module = ""
    _model = ""
    _net = {
        # "style": ["clip_vision", "t2iadapter_style_sd14v1 [202e85cc]"],
        # # "style": ["clip_vision", "coadapter_style_sd15v1 [c7dc5801]"],
        # "color": ["color", "t2iadapter_color_sd14v1 [8522029d]"],
        # # "color": ["color", "coadapter_color_sd15v1 [91c6f0e5]"],
        # "depth": ["depth", "control_depth-fp16 [400750f6]"],
        # # "depth": ["depth", "coadapter_depth_sd15v1 [93aff3ab]"],
        # "canny": ["canny", "control_canny-fp16 [e3fe7712]"],
        # # "canny": ["canny", "coadapter_canny_sd15v1 [0f01fb68]"],
        # "hed": ["hed", "control_hed-fp16 [13fee50b]"],
        # "normal_map": ["normal_map", "control_normal-fp16 [63f96f7c]"],
        # "scribble": ["scribble", "control_scribble-fp16 [c508311e]"],
        # "fake_scribble": ["fake_scribble", "control_scribble-fp16 [c508311e]"],
        # "segmentation": ["segmentation", "control_seg-fp16 [b9c1cc12]"],
        # # "segmentation": ["segmentation", "t2iadapter_seg-fp16 [0e677718]"],
        # "openpose": ["openpose", "control_openpose-fp16 [9ca67cc5]"],
        # "skeleton": ["none", "control_openpose-fp16 [9ca67cc5]"],
        # # "openpose": ["openpose", "t2iadapter_openpose-fp16 [4286314e]"],

        "depth": ["depth_midas", "control_v11f1p_sd15_depth [cfd03158]"],
        "canny": ["canny", "control_v11p_sd15_canny [d14c016b]"],
        "softedge": ["softedge_pidinet", "control_v11p_sd15_softedge [a8575a2a]"],
        "scribble": ["scribble_xdog", "control_v11p_sd15_scribble [d4ba51ff]"],
        "openpose": ["openpose_full", "control_v11p_sd15_openpose [cab727d4]"],
        "skeleton": ["none", "control_v11p_sd15_openpose [cab727d4]"],
        "shuffle": ["shuffle", "control_v11e_sd15_shuffle [526bfdae]"],
        "style": ["t2ia_style_clipvision", "t2iadapter_style_sd14v1 [202e85cc]"],
        "none": ["reference_only", "None"],
    }
    if _str in _net.keys():
        _module = _net[_str][0]
        _model = _net[_str][1]
    elif _str == "none":
        _module = "none"
        _model = "none"
    return _module, _model


def parse_ctrl11_units(_ctrls, user_sys_conf):
    _re = []
    for i in _ctrls.keys():
        i_module, i_model = parse_ctrl_net(i)
        print(f"parse_ctrl_units: {i_module}, {i_model}")
        _i = {
            "input_image": b64_img(_ctrls[i]),
            "module": i_module,
            "model": i_model,
            "weight": 1.0,
            "lowvram": True,
            "control_mode": 0,
            "resize_mode": "Envelope (Outer Fit)",
            # "guidance": 1,
            "guidance_start": 0.0,
            "guidance_end": 1.0,
            "processor_res": 512,
            # "mask": "",
            # "threshold_a": 64,
            # "threshold_b": 64,
        }
        if i_module == "softedge" and user_sys_conf == "线稿":
            _i["processor_res"] = 2048
        if i_module == "scribble" and user_sys_conf == "猜想":
            _i["control_mode"] = 1 # Balanced, MY prompt is more important, ControlNet is more important
        if i_module == "depth" and user_sys_conf == "布局":
            _i["control_mode"] = 2 # Balanced, MY prompt is more important, ControlNet is more important
        if i_module == "softedge" and user_sys_conf == "轮廓":
            _i["control_mode"] = 2 # Balanced, MY prompt is more important, ControlNet is more important
        if i_module == "canny" and user_sys_conf == "细节":
            _i["control_mode"] = 2 # Balanced, MY prompt is more important, ControlNet is more important
        _re.append(_i)
    return _re


# def b64_img_cv2(path):
#     import cv2
#     from base64 import b64encode
#     img = cv2.imread(path)
#     retval, buffer = cv2.imencode('.jpg', img)
#     b64img = b64encode(buffer).decode("utf-8")
#     return b64img


def b64_img(img_fn):
    img = Image.open(img_fn)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = "data:image/png;base64," + str(
        base64.b64encode(buffered.getvalue()), "utf-8"
    )
    return img_base64


def create_blank_png(_w, _h, _fn):
    _array = numpy.full((_h, _w, 3), 255, dtype=numpy.uint8)
    img = Image.fromarray(_array, "RGB")
    img.save(_fn, "PNG")


def info_report(info, model_name):
    _report = {
        "prompt": "Prompt",
        "negative_prompt": "Negative Prompt",
        "sampler_name": "Sampler",
        "steps": "Steps",
        "size": "Size",
        "cfg_scale": "CFG Scale",
        "denoising_strength": "Denoising Strength",
        "seed": "Seed",
        "styles": "Styles",
        "model_name": "Model Name",
        "sd_model_hash": "Model Hash",
    }
    # pprint(info['infotexts'])
    info["size"] = f"{info['width']}*{info['height']}"
    info["model_name"] = model_name
    _add = {
        # "face_restoration_model": "Face Restoration"
        # 'clip_skip': 'Clip Skip',
        # 'is_using_inpainting_conditioning': 'is_using_inpainting_conditioning',
    }
    _report.update(_add)
    _txt = []
    for i in _report.keys():
        if i in info.keys():
            _txt.append(f"{_report[i]}: {info[i]}")
    _infotexts = "\n".join(info["infotexts"][0].split("\\n"))
    _txt.append(f"\ninfotexts: \n{_infotexts}\n")
    return "\n".join(_txt)


def is_human(prompt, human):
    if_human = False
    prompt_words = re.sub(r"[^\w\s]", "", prompt)
    for p in human:
        if f" {p} " in prompt_words:
            # print(p)
            if_human = True
    return if_human


def random_human(prompt, human, race):
    _prompt = prompt
    prompt_words = re.sub(r"[^\w\s]", "", prompt)
    for p in human:
        if f" {p} " in prompt_words:
            # print(p)
            _race = random.choice(race)
            _prompt = _prompt.replace(f" {p} ", f" ({_race} {p}:1.2) ")
    return _prompt


def merge_dict(d1, d2):
    d1.update(d2)
    return d1


def create_caption_txt(_img_content, caption_txt):
    _content, _style = api_interrogate(_img_content)
    _caption = f"{_content}, {_style}"
    with open(caption_txt, "w", encoding="utf8") as _txt:
        _txt.write(_caption)
    print(f"{caption_txt}:")
    # prCyan(_content)
    # prPurple(_style)
    print(_content)
    print(_style)
    return _caption


def read_txt(fn):
    _re = ""
    with open(fn, "r", encoding="utf8") as rf:
        _lis = rf.readlines()
        _re = "\n".join(_lis)
    # print(_re)
    return _re


def merge_prompt(_p1, _p2):
    if _p1 and _p2:
        _re = f"{_p1}, {_p2}"
    elif _p1:
        _re = _p1
    elif _p2:
        _re = _p2
    else:
        _re = ""
    return _re


def prRed(skk):
    print("\033[91m{}\033[00m".format(skk))


def prGreen(skk):
    print("\033[92m{}\033[00m".format(skk))


def prYellow(skk):
    print("\033[93m{}\033[00m".format(skk))


def prLightPurple(skk):
    print("\033[94m{}\033[00m".format(skk))


def prPurple(skk):
    print("\033[95m{}\033[00m".format(skk))


def prCyan(skk):
    print("\033[96m{}\033[00m".format(skk))


def prLightGray(skk):
    print("\033[97m{}\033[00m".format(skk))


def prBlack(skk):
    print("\033[98m{}\033[00m".format(skk))



# def api_t2i_ctrl(_payload, _out, model_name):
#     # del _payload['denoising_strength']
#     # print(_payload.keys())
#     _url = f"{url}/controlnet/txt2img"
#     req = requests.post(url=_url, json=_payload)
#     # print(req)
#     r_images = ""
#     r_info = ""
#     if req.status_code == 200:
#         r = req.json()
#         r_images = r["images"]
#         r_info = r["info"]
#     if r_images and r_info:
#         r_info_json = json.loads(r_info)
#         # pprint(r_info_json)
#         infotexts = info_report(r_info_json, model_name)
#         out_txt = f"{_out}.txt"
#         # prYellow(out_txt)
#         print(out_txt)
#         with open(out_txt, "w", encoding="utf8") as _txt:
#             _txt.write(infotexts)
#         _n = len(r_images)
#         if _n >= 1:
#             out_png = f"{_out}_ignore.png"
#             print(out_png)
#             i_img2img = Image.open(io.BytesIO(base64.b64decode(r_images[0])))
#             i_img2img.save(out_png)
#         # for i in range(_n):
#         #     if _n == 1:
#         #         out_png = f"{_out}.png"
#         #     else:
#         #         out_png = f"{_out}_{i}.png"
#         #     # prYellow(out_png)
#         #     if i == 0:
#         #         print(out_png)
#         #         i_img2img = Image.open(io.BytesIO(base64.b64decode(r_images[i])))
#         #         i_img2img.save(out_png)


# def api_i2i_ctrl(_payload, _out, model_name):
#     _url = f"{url}/controlnet/img2img"
#     req = requests.post(url=_url, json=_payload)
#     # print(req)
#     r_images = ""
#     r_info = ""
#     if req.status_code == 200:
#         r = req.json()
#         r_images = r["images"]
#         r_info = r["info"]
#     if r_images and r_info:
#         r_info_json = json.loads(r_info)
#         # pprint(r_info_json)
#         infotexts = info_report(r_info_json, model_name)
#         out_txt = f"{_out}.txt"
#         # prYellow(out_txt)
#         print(out_txt)
#         with open(out_txt, "w", encoding="utf8") as _txt:
#             _txt.write(infotexts)
#         _n = len(r_images)
#         if _n >= 1:
#             out_png = f"{_out}_ignore.png"
#             print(out_png)
#             i_img2img = Image.open(io.BytesIO(base64.b64decode(r_images[0])))
#             i_img2img.save(out_png)
#         # for i in range(_n):
#         #     if _n == 1:
#         #         out_png = f"{_out}.png"
#         #     else:
#         #         out_png = f"{_out}_{i}.png"
#         #     # prYellow(out_png)
#         #     if i == 0:
#         #         print(out_png)
#         #         i_img2img = Image.open(io.BytesIO(base64.b64decode(r_images[i])))
#         #         i_img2img.save(out_png)


# def parse_ctrl_units(_ctrls, user_sys_conf):
#     _re = []
#     for i in _ctrls.keys():
#         i_module, i_model = parse_ctrl_net(i)
#         print(f"parse_ctrl_units: {i_module}, {i_model}")
#         _i = {
#             "input_image": b64_img(_ctrls[i]),
#             "module": i_module,
#             "model": i_model,
#             "weight": 1,
#             "lowvram": True,
#             "guessmode": False,
#             "resize_mode": "Envelope (Outer Fit)",
#             "guidance": 1,
#             "guidance_start": 0,
#             "guidance_end": 1,
#             "processor_res": 512,
#             # "mask": "",
#             # "threshold_a": 64,
#             # "threshold_b": 64,
#         }
#         if i_module == "softedge" and user_sys_conf == "线稿":
#             _i["processor_res"] = 2048
#         if i_module == "scribble" and user_sys_conf == "猜想":
#             _i["guessmode"] = True
#         _re.append(_i)
#     return _re
