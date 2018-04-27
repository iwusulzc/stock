#-*-coding:utf-8-*-
import csv
import json
import sys
import codecs

def trans(path):
    jsonData = codecs.open(path, 'r', 'utf-8')
    # csvfile = open(path+'.csv', 'w') # 此处这样写会导致写出来的文件会有空行
    # csvfile = open(path+'.csv', 'wb') # python2下
    csvfile = open(path+'.csv', 'w', newline='') # python3下
    #writer = csv.writer(csvfile, delimiter='，', quoting=csv.QUOTE_ALL)
    writer = csv.writer(csvfile, delimiter=',')
    flag = True
    for line in jsonData:
        dic = json.loads(line[0:-1])
        if flag:
            # 获取属性列表
            keys = list(dic.keys())
            print(keys)
            writer.writerow(keys) # 将属性列表写入csv中
            flag = False
        # 读取json数据的每一行，将values数据一次一行的写入csv中
        try:
            writer.writerow(list(dic.values()))
        except Exception as e:
            print(e)
    jsonData.close()
    csvfile.close()

if __name__ == '__main__':
    path=str(sys.argv[1]) # 获取path参数
    print (path)
    trans(path)
