from sketch import OpenSFSD

if __name__ == '__main__':
    oSFSD = OpenSFSD("/home/zzm/datasets/SFSD", "/home/zzm/datasets/SFSD-open", '/home/zzm/datasets/coco2017/', 'train2017')
    print(len(oSFSD.files))
    oSFSD.set_num()
    oSFSD.save_sketches()
    oSFSD.save_images()
    oSFSD.save_sketchimgs()
    