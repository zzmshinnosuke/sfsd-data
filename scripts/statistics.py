#!/usr/bin/env python333
# -*- coding: utf-8 -*-
# Created on 2021-07-20 21:51:06
# @Author: zzm


def statistics_image_cat_save(generateScene,ids,path):
    '''
    统计图片id列表中，包含的所有物体类别
    :param generateScene:
    :param ids:
    :return:
    '''
    cats={};
    for id in ids:
        OImage=generateScene.coco.loadImgs(ids=id)[0]
        annIds = generateScene.coco.getAnnIds(imgIds=id, iscrowd=None)
        anns = generateScene.coco.loadAnns(annIds)
        for seg in anns:
            # print(generateScene.getCatNameFCatId(seg['category_id']))
            cat_name=generateScene.getCatNameFCatId(seg['category_id'])
            if cat_name in cats.keys():
                cats[cat_name]+=1
            else:
                cats[cat_name]=1
        #break
    #print(cats.items())
    cats = sorted(cats.items(), key=lambda x: x[1], reverse=True)
    print(cats)
    with open(path,'w',encoding='utf-8') as f:
        for cat in cats:
            f.write("'"+cat[0]+"' ,");f.write('\n')
    print(len(cats),dict(cats))