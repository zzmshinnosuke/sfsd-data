# coding=utf-8
'''
将图片放在html中显示
'''
import os

str=""

with open('/home/zzm/Desktop/tmp0521.txt', 'r') as f:
    line = f.readline()  # 调用文件的 readline()方法
    tmp="""<tr>
    <td><image src="DRAWING_GT/%s" width=256 /></td>
    <td><image src="reference_image/%s" width=256 /></td>
    <td><image src="reference_image/%s" width=256 /></td>
    <td><image src="reference_image/%s" width=256 /></td>
    <td><image src="reference_image/%s" width=256 /></td>
    <td><image src="reference_image/%s" width=256 /></td>
    </tr>"""
    while line:
        name=line.split()
        new_name=[]
        new_name.append('0'*(12-len(name[0]))+name[0]+'.png')
        new_name.append('0' * (12 - len(name[1])) + name[1] + '.jpg')
        new_name.append('0' * (12 - len(name[2])) + name[2] + '.jpg')
        new_name.append('0' * (12 - len(name[3])) + name[3] + '.jpg')
        new_name.append('0' * (12 - len(name[4])) + name[4] + '.jpg')
        new_name.append('0' * (12 - len(name[5])) + name[5] + '.jpg')
        str=str+(tmp%(new_name[0],new_name[1],new_name[2],new_name[3],new_name[4],new_name[5]))
        line = f.readline()

    print(str)
# for line in open("tmp0521.txt"):
#     print(line)

# 命名生成的html
GEN_HTML = "/home/zzm/Desktop/train/test.html"
# 打开文件，准备写入
with open(GEN_HTML, 'w') as f:
    message = """
    <html>
    <head></head>
    <body>
    <table>%s</table>
    </body>
    </html>""" % (str)
    f.write(message)


