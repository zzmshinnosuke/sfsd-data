from sketch import OpenSFSD

import os
import json

def readJson(path):
    with open(path, "r") as f:
        try:
            load_dict = json.load(f)
            return  load_dict
        except json.decoder.JSONDecodeError:
            print(path)
    return None

def train_test(origin_SFSD_path, open_SFSD_path):
    # 加载原sketch的train和test划分文件
    filename_txt = 'test_names.txt'
    filename_path = os.path.join(origin_SFSD_path,  filename_txt)
    assert os.path.exists(filename_path), 'not find {}'.format(filename_path)
    with open(filename_path, 'r') as f:
        test_files = [line.strip() for line in f.readlines()]
    test_ids = []
    for tf in test_files:
        sketch = readJson(os.path.join(origin_SFSD_path, 'sketch', tf))
        test_ids.append(sketch["reference"].split('.')[0])
    # print(test_image_ids)
    # print(len(set(test_image_ids)))

    # 加载开源sketch的全部文件
    open_sketch_path = os.path.join(open_SFSD_path, "sketches/")
    print(open_sketch_path)
    traintest_ids = [file.split('.')[0] for file in os.listdir(open_sketch_path) if os.path.isfile(os.path.join(open_sketch_path, file))]

    # 原来的测试集3000尽量保留，跑了一下发现有一个多的，就把训练集的最后一个拿过来了
    test_ids = list(set(traintest_ids).intersection(test_ids))
    train_ids = list(set(traintest_ids) - set(test_ids))
    test_ids.append(train_ids[-1])
    train_ids = train_ids[:-1]

    # print(len(set(traintest_ids)), len(set(test_ids)), len(set(train_ids)), len(set(train_ids).intersection(test_ids)))
    # 写入开源SFSD中
    with open(os.path.join(open_SFSD_path, 'test_names.txt'), 'w') as fe:
            for te in test_ids:
                fe.write(te + '\n')
    with open(os.path.join(open_SFSD_path, 'train_names.txt'), 'w') as fr:
        for tr in train_ids:
            fr.write(tr + '\n')

if __name__ == '__main__':
    # oSFSD = OpenSFSD("/home/zzm/datasets/SFSD", "/home/zzm/datasets/SFSD-open", '/home/zzm/datasets/coco2017/', 'train2017')
    # print(len(oSFSD.files))
    # oSFSD.set_num()
    # oSFSD.save_sketches()
    # oSFSD.save_images()
    # oSFSD.save_sketchimgs()

    train_test("/home/zzm/datasets/SFSD", "/home/zzm/datasets/SFSD-open")
    