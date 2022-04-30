#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on 2021-07-19 22:00:09
# @Author: zzm
from sketch import Draw2Label

import argparse
import os

'''
处理绘制后的图像，整理之后，保存为标注工具使用的格式
'''

def get_parser(prog='select image'):
    parser=argparse.ArgumentParser(prog)
    
    parser.add_argument('--draw_post_path',
                        default='/home/zzm/datasets/sti-data/draw-end/field/results1',
                        help='the path of finishing draw sketch ')
    
    parser.add_argument('--label_pre_path',
                        default="/home/zzm/tmp/data",
                        help='the path of pre-label, deal draw sketch and save here')
    
    parser.add_argument('--filename',
                        default = "",
                        help = 'just deal single sketch file')
    
    return parser

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    d2l = Draw2Label(args.draw_post_path, args.label_pre_path, args.filename)
    d2l.generate() 