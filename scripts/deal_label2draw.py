#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on 2022-03-29 16:51:16
# @Author: zzm

from sketch import Label2Draw

import argparse
import os

'''
处理标注完的草图，可以转换为绘制格式，可以再次绘制
'''

def get_parser(prog = 'select image'):
    parser = argparse.ArgumentParser(prog)
    
    parser.add_argument('--label_end_path',
                        default = '/home/zzm/datasets/sfsd-data/label-end/results1',
                        help = 'the path of finishing label sketch ')
    
    parser.add_argument('--draw_end_path',
                        default = "/home/zzm/tmp/test",
                        help = 'the path of draw sketch and save here')
    
    parser.add_argument('--filename',
                        default = "",
                        help = 'just deal single sketch file')
    
    parser.add_argument('--useless',
                        type = bool,
                        default = True,
                        help = 'the path of draw sketch and save here')
    
    return parser

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    l2d = Label2Draw(args.label_end_path, args.draw_end_path, args.useless, args.filename)
    l2d.generate() 