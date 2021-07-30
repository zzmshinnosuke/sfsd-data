#!/usr/bin/env python333
# -*- coding: utf-8 -*-
# Created on 2021-07-23 09:01:27
# @Author: zzm

from sketch import Sketch

import argparse
import os

def get_all_sketches(path,sketches_json):
    print("load sketch json:")
    sketches=list()
    for sketch_json in tqdm(sketches_json):
        sketch=Sketch(sketch_path=os.path.join(path,sketch_json))
        sketches.append(sketch)
    return sketches
     
def get_parser(prog='deal sketch to model'):
    parser=argparse.ArgumentParser(prog)

    parser.add_argument('--sketch_path',
                        default='/home/zzm/tmp/sketch',
                        required=True,
                        help='the path of sketch')
    
    return parser


        
        


if __name__ == '__main__':
    parser=get_parser()
    args=parser.parse_args(args.sketch_path)
    sketch=Sketch()
    print(sketch)
    
