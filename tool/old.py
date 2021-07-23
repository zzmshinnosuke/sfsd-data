#!/usr/bin/env python333
# -*- coding: utf-8 -*-
# Created on 2021-07-22 16:08:24
# @Author: zzm

def deleteSameImg(source_path,target_path,first_path,second_path,third_path) :
    '''
    第三次选择的数据和以前的有很多重复的，因此去掉和之前重复的数据
    :param source_path:
    :param target_path:
    :param first_path:
    :param second_path:
    :param third_path:
    :return:
    '''
    names = []
    with open(source_path, "r", encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            names.append(line)
    ids, coconames = myCoCo.getImgIdsFromNames(names[1:])
    names=names[1:]

    first_names=[]
    with open(first_path, "r", encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            first_names.append(line)

    second_names = []
    with open(second_path, "r", encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            second_names.append(line)

    third_names = []
    with open(third_path, "r", encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            third_names.append(line)

    new_names=[]
    for name in names:
        if not (name in first_names or name in second_names or name in third_names):
            new_names.append(name)
    print(len(names))
    print(len(new_names))

    with open(target_path,"w",encoding='utf-8') as f:
        f.write(str(len(new_names)))
        f.write('\n')
        for name in new_names:
            f.write(name)
            f.write('\n')

    return 0

def boundingbox2names(mycoco,source_path,target_path,target_id_path):
    names=[]
    with open(source_path,"r",encoding='utf-8') as f:
        for line in f.readlines():
            line=line.strip()
            temp=line.split(';')[0]
            names.append(temp)

    with open(target_path,"w",encoding='utf-8') as f:
        for name in names:
            f.write(name)
            f.write('\n')
    ids, filenames = mycoco.getImgIdsFromNames(names[1:])
    with open(target_id_path, mode='w', encoding='utf-8') as f:
        for id in ids:
            f.write(str(id))
            f.write('\n')

def gen_backgroundtxt(generateScene,image_path="/home/zzm/Deal/sti/background/vehicle/other",background_path="../../files/vehicle"):
    '''
    从选出的图片文件夹中加载所有的图片名称，并获取图片id，保存在txt中，做为绘制过程中参考图片的配置文件
    :param generateScene :coco衍射类的索引
    :param image_path: 图片文件夹的路径
    :param background_path: 生成配置文件所在文件夹
    :return:
    '''
    path = image_path
    ids_file = os.path.join(background_path,"background_id.txt")
    names_file=os.path.join(background_path,"background.txt")
    if not os.path.exists(path):
        print("sti path is not exist")
        return
    if not os.path.exists(ids_file):
        os.mknod(ids_file)
    if not os.path.exists(names_file):
        os.mknod(names_file)
    files = os.listdir(path)
    # print(files)
    ids, filenames = generateScene.getImgIdsFromNames(files)
    with open(ids_file, mode='w', encoding='utf-8') as f:
        for id in ids:
            f.write(str(id))
            f.write('\n')
    with open(names_file, mode='w', encoding='utf-8') as f:
        f.write(str(len(filenames)))
        f.write('\n')
        for filename in filenames:
            f.write(str(filename))
            f.write('\n')

def background_box(myCoCo,source_path,target_path):
    names = []
    with open(source_path, "r", encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            names.append(line)
    ids,coconames=myCoCo.getImgIdsFromNames(names[1:])
    name_boxs=[]

    for id in ids:
        OImage = myCoCo.coco.loadImgs(ids=id)[0]
        annIds = myCoCo.coco.getAnnIds(imgIds=id, iscrowd=None)
        anns = myCoCo.coco.loadAnns(annIds)
        # print(anns[0]["bbox"])
        name_box=OImage['file_name']+";"
        for ann in anns:
            name_box+=str(ann["bbox"][0])+','+str(ann["bbox"][1])+','+str(ann["bbox"][2])+','+str(ann["bbox"][3])+','+str(ann['id'])+"#"
        name_boxs.append(name_box)

    with open(target_path, mode='w', encoding='utf-8') as f:
        f.write(str(len(name_boxs)))
        f.write('\n')
        for name_box in name_boxs:
            f.write(str(name_box))
            f.write('\n')

def genImgNameText(mycoco,source_path,target_path):
    ids=[]
    name_texts={}
    with open(source_path,"r",encoding='utf-8') as f:
        for line in f.readlines():
            line=line.strip()
            temp=line.split(';')[0]
            ids.append(temp)

    for id in ids:
        OImage = mycoco.coco.loadImgs(ids=[int(id)])[0]
        name=OImage['file_name']
        capIds = mycoco.coco_caption.getAnnIds(imgIds=int(id), iscrowd=None)
        caps = mycoco.coco_caption.loadAnns(capIds)
        name_texts[name]=caps

    with open(target_path, "w") as f:
        json.dump(name_texts, f)
        print("写入文件完成...")

def gen_background_text(myCoCo,images_path,config_path):
    ids=[]
    name_texts={}
    with open(source_path,"r",encoding='utf-8') as f:
        for line in f.readlines():
            line=line.strip()
            temp=line.split(';')[0]
            ids.append(temp)

    for id in ids:
        OImage = mycoco.coco.loadImgs(ids=[int(id)])[0]
        name=OImage['file_name']
        capIds = mycoco.coco_caption.getAnnIds(imgIds=int(id), iscrowd=None)
        caps = mycoco.coco_caption.loadAnns(capIds)
        name_texts[name]=caps

    with open(target_path, "w") as f:
        json.dump(name_texts, f)
        print("写入文件完成...")