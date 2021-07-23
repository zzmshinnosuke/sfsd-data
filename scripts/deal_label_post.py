#!/usr/bin/env python333
# -*- coding: utf-8 -*-
# Created on 2021-07-19 09:36:42
# @Author: zzm

from sketch import LabelPost

import argparse
import os

def get_parser(prog='deal post-label sketch'):
    parser=argparse.ArgumentParser(prog)

    parser.add_argument('--label_pre_path',
                        default="/home/zzm/tmp/test-sti-data/field-label-pre",
                        required=True,
                        help='the path of pre-label sketch')
    
    parser.add_argument('--label_post_path',
                        default="/home/zzm/tmp/test-sti-data/field-label-post",
                        required=True,
                        help='the path of post-label sketch')
    
    parser.add_argument('--save_path',
                        default="/home/zzm/tmp/test-sti-data/sketch",
                        required=True,
                        help='the path of deal post-label sketch')

    parser.add_argument('--root_coco_path',
                        default='/home/zzm/datasets/coco2017/',
                        required=True,
                        help='the path of root coco')
    
    parser.add_argument('--coco_split',
                        default='train2017',
                        required=True,
                        help='the split of coco')

    parser.add_argument('--scene',
                        default='field',
                        required=True,
                        help='field,sport,vehicle')

    return parser

if __name__ == '__main__':
    parser=get_parser()
    args=parser.parse_args()
    lp=LabelPost(args.label_pre_path,args.label_post_path,args.save_path,args.root_coco_path,args.coco_split,args.scene)
    lp.generate()

