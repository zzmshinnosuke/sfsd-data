# STI DATASET 

## reference
- [coco 官方工具](https://github.com/dengdan/coco/blob/master/PythonAPI/pycocotools/coco.py)    
- [coco 数据格式说明1](https://www.jianshu.com/p/568a2f5195a9)  
- [coco 数据格式说明2](https://blog.csdn.net/zym19941119/article/details/80241663)

## tools
- [Draw sketch](https://github.com/zzmshinnosuke/sketch-draw.git)  
- [Annotation sketch](https://github.com/zzmshinnosuke/sketch-annotation.git)

## Create Dataset Flow
- 筛选参考图像  
从CoCo中挑选图像作为草图绘制的参考图像
    - 程序筛选
        ```
        python scripts/select_image.py \
            --root_coco_path /home/zzm/datasets/coco2017/ \
            --coco_split train2017 \
            --save_path /home/zzm/tmp/data
        ```
    - 人工筛选

- 绘制草图
    - 处理筛选后的图像，生成对应的配置文件   
        配置文件中第一行为总的图像数，后续每行为`image name;box_x1,box_y1,box_x2,box_y2,box_id#`
        ```
        python scripts/gen_backgroundtxt.py \
            --type background_box \
            --config_file /home/zzm/tmp/test-sti-data/background.txt \
            --draw_pre_path /home/zzm/tmp/test-sti-data/background/ \
            --root_coco_path /home/zzm/datasets/coco2017/ \
            --coco_split train2017 
        ```
    - 使用草图绘制系统Draw sketch，人工绘制
    
- 标注草图
    - 处理绘制完成的原始草图，用于标注系统（原始草图，把所有的信息都记录了下来）
        ```
        python scripts/deal_draw2label.py \
            --draw_post_path /home/zzm/tmp/test-sti-data/field-draw \
            --label_pre_path /home/zzm/tmp/test-sti-data/field-label-post/
        ```
    - 使用草图标注系统Annotation sketch,人工标注
    
- 后期处理
    - 处理标注完成的数据,便于模型读取
        ```
        python scripts/deal_label_post.py \
            --label_pre_path /home/zzm/tmp/test-sti-data/field-label-pre \
            --label_post_path /home/zzm/tmp/test-sti-data/field-label-post \
            --save_path /home/zzm/tmp/test-sti-data/sketch \
            --root_coco_path /home/zzm/datasets/coco2017/ \
            --coco_split train2017 \
            --scene field
        ```
- 统计草图
    - 统计草图中每个类别包含的物体个数
        ```
        
        ```
    - 统计每个草图中包含的笔画数
        ```
        
        ```
    - 统计每个草图中包含的点数
        ```
        
        ```
    - 统计每条笔画包含的点数
        ```
        
        ```
    - 