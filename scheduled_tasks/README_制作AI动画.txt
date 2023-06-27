# 准备素材
0）参考 F:\dd-animation\ty\ip\lx-template 里的 mask.png 和 texture.png 生成ip素材

# 修正素材
1）进入 F:\dd-animation\ty\ip，运行 _imageMagic_fix_libpng_convert.bat

# 生成模型
2a）运行 python .\image_to_animation.py .\ip\lx-**.png .\ip\lx-**
2b）将 F:\dd-animation\ty\ip\lx-template 里的 char_cfg.yaml 拷贝到 lx-**

# 修正模型
3a）打开 win10 docker containers，运行 docker_torchserve
3b）测试运行 curl http://localhost:8080/ping
3c）运行 python .\fix_annotations.py .\ip\lx-**
3d）测试运行 python .\annotations_to_animation.py .\ip\lx-** .\config\motion\dab.yaml .\config\retarget\fair1_ppf.yaml test_video

# 生成mvc
4）运行 python .\_make_mvc_for_ip.py -motion bvh\cmusgx_motion -mvc mvc -gif gif -ip lx-smile3 -retarget retarget_cmu_max.yaml

# 生成gif
5）运行 python .\_make_mvc_gif.py -mvc .\ip\lx-**\mvc

