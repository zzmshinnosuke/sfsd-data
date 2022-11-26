# 有79张单物体草图，第一、二次分别有一张，第三次有77张，重新绘制之后再复制处理目录，

if __name__ == '__main__':
    files=[]
    path='/home/zzm/single.txt'
    with open(path,'r') as f:
        line = f.readline()            
        while line:               
            image,scene_type,sketch_id=line.strip().split(" ")
            if(scene_type=="vehicle"):
                files.append('{}.json'.format(sketch_id))
            print(image,scene_type,sketch_id)
            line = f.readline()
    print(len(files))

    from shutil import copyfile,copy
    from sys import exit
    import os

    for file in files:
        source=os.path.join("/opt/lampp/htdocs/skeimg3/results1",file)
        target="/home/zzm/datasets/sti-data-new/draw-end/vehicle/results"
    #     print(source,target)
        try:
            copy(source, target)
        except IOError as e:
            print("Unable to copy file. %s" % e)
            exit(1)
        except:
            print("Unexpected error:", sys.exc_info())
            exit(1)

