from nis import cat
import os
import argparse

from scipy.io import loadmat
from tqdm import tqdm
import numpy as np

'''
statistic SketchyCOCO dataset: the number of category of sketch, the number of sketches of category, the number of object of sketch  
'''

def sta_sketch_category_num(sketches):
    print("statistic mean/max/min category of {} sketches:".format(len(sketches)))
    cats_num = []
    for sketch in tqdm(sketches):
        sketch_list = list(set(sketch.flatten().tolist()))
        sketch_list.remove(0)
        cats_num.append(len(sketch_list))
    print('max cat_num is {}, min cat_num is {}, mean cat_num is {}'.format(max(cats_num), min(cats_num), np.mean(cats_num)))

def sta_category_sketch_num(sketches):
    print("statistic mean/max/min {} sketch number of category:".format(len(sketches)))
    cats = list()
    for sketch in tqdm(sketches):
        sketch_list = list(set(sketch.flatten().tolist()))
        sketch_list.remove(0)
        cats.extend(sketch_list)
    cats_set = set(cats)
    sketch_nums = list()
    for cat in cats_set:
        sketch_nums.append(cats.count(cat))
    print("categroy number is {}".format(len(cats_set)))
    print('max sketch_num is {}, min sketch_num is {}, mean sketch_num is {}'.format(max(sketch_nums), min(sketch_nums), np.mean(sketch_nums)))

def sta_sketch_object_num(sketches):
    print("statistic mean/max/min object number of {} sketch:".format(len(sketches)))
    object_nums = list()
    for sketch in tqdm(sketches):
        sketch_list = list(set(sketch.flatten().tolist()))
        sketch_list.remove(0)
        object_nums.append(len(sketch_list))
    print('max object_nums is {}, min object_nums is {}, mean object_nums is {}'.format(max(object_nums), min(object_nums), np.mean(object_nums)))

def get_all_sketches(path, type):
    sketches_mat = []
    for split in ["trainInTrain", "val", "valInTrain"]:
        split_path = os.path.join(path, split, type)
        sketches_mat += [os.path.join(path, split, type, file) for file in os.listdir(split_path) if os.path.isfile(os.path.join(split_path, file))]
    sketches = []
    print("load dataset:")
    for sm in tqdm(sketches_mat):
        sketches.append(loadmat(sm)[type])
    return sketches

def get_parser(prog='statistics SketchyCOCO'):
    parser=argparse.ArgumentParser(prog)

    parser.add_argument('--root_path',
                        default='~/datasets/SketchyCOCO/Scene/Annotation/paper_version',
                        help='the path of sketch')
    parser.add_argument('--sketch_cat_num',
                    type=bool,
                    default=False,
                    help='statistic the number of object category in every sketch')
    parser.add_argument('--cat_sketch_num',
                    type=bool,
                    default=False,
                    help='statistic the number of sketch in every category')
    parser.add_argument('--sketch_object_num',
                        type=bool,
                        default=False,
                        help='statistic the number of objects in every sketch')
    return parser.parse_args()

if __name__ == '__main__':
    args=get_parser()

    if args.sketch_object_num:
        sketches=get_all_sketches(args.root_path, "INSTANCE_GT")
        sta_sketch_object_num(sketches)
    if args.sketch_cat_num:
        sketches=get_all_sketches(args.root_path, "CLASS_GT")
        sta_sketch_category_num(sketches)
    if args.cat_sketch_num:
        sketches=get_all_sketches(args.root_path, "CLASS_GT")
        sta_category_sketch_num(sketches)