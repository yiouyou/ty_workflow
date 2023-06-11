from _util_202303 import sys_cmd, prCyan, api_upscale
from _util_openai import zh_txt_2_en_txt, zh_txt_2_en_prompt

_txt_out_dir = "F:\\_workflow\\tmp\\test"
_img_out_dir = "F:\\_workflow\\tmp\\test"

_user_conf_json = [
    # 'ci-i2i-user-i2i-ctrl-bj.json',
    'ci-i2i-user-i2i-ctrl-xg.json',
    # 'ci-i2i-user-i2i-ctrl-fg.json',
    # 'ci-i2i-user-i2i.json',
    # 'ci-i2i-user-t2i-ctrl-kl.json',
    # 'ci-i2i-user-t2i.json',
]

# for i in _user_conf_json:
#     cmd_ci_i2i = f"python ci-i2i-202303.py -txtoutdir {_txt_out_dir} -imgoutdir {_img_out_dir} -userconf {i}"
#     prCyan(cmd_ci_i2i)
#     sys_cmd(cmd_ci_i2i)

# api_upscale("F:\\_workflow\\tmp\\test\\xg_sd1_00_1678872845_0.png")

# print(isChinese('测试'))

_txt = "<lora:ty3Dbear:1>, ty3Dbear, 考拉在公园里放风筝"

# _txt = """Ignore previous instructions. As a stable-diffusion prompt engineer, you need to write stable-diffusion prompts. The basic rule is that the most important keywords are at the beginning and then every additional keywords are separated by a comma. If you add an art style by an artist or multiple artists, this information should always be at the end.
#     For example, if you need to write a prompt of an image of cartoon character for kids, you probable write is as 
#     "very cute kid's film character, disney pixar zootopia character concept artwork, 3d concept, high detail iconic character for upcoming film, trending on artstation, character design, 3d artistic render, highly detailed, cartoon"
#     By using a similar syntax, please write me a clean and precise prompt an image of content for kids."""


# {{Prompt}}, anthro, very cute kid's film character, disney pixar zootopia character concept artwork, 3d concept, detailed fur, high detail iconic character for upcoming film, trending on artstation, character design, 3d artistic render, highly detailed, octane, blender, cartoon, shadows, lighting



print(zh_txt_2_en_prompt(_txt))
print(zh_txt_2_en_txt(_txt))

