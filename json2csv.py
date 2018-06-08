#-*-coding:utf-8-*-
import csv
import json
import sys
import codecs

reload(sys)
sys.setdefaultencoding( "utf-8" )

def trans(path):
    # csvfile = open(path+'.csv', 'w') # 此处这样写会导致写出来的文件会有空行
    csvfile = open(path+'.csv', 'wb') # python2下
    # csvfile = open(path+'.csv', 'w', newline='') # python3下
    #writer = csv.writer(csvfile, delimiter='，', quoting=csv.QUOTE_ALL)
    writer = csv.writer(csvfile, delimiter=',')
    flag = True
    with open(path, 'r') as f:
        for line in f:
            line = line.strip(' \n,');
            if line == '[' or line == ']':
                continue

            dic = json.loads(line.encode('utf-8'), encoding='utf-8')
            if flag:
                kw_dict = {
                    'code' : 'code',
                    'period' : 'period',
                    'exchange' : 'exchange',
                    'reg_capital' : 'reg_capital',
                    'date' : 'date',
                    'name' : 'name',
                    'region' : 'region',
                    'industry' : 'industry',
                    'eps' : u'??????(?)',
                    'neps' : u'??????(?)',
                    'deps' : u'??????(?)',
                    'bvps' : u'?????(?)',
                    'cfps' : u'?????(?)',
                    'uddps' : u'???????(?)',
                    'ocfps' : u'???????(?)',
                    'gr' : u'?????(?)',
                    'gp' : u'???(?)',
                    'anp' : u'?????(?)',
                    'nnp' : u'?????(?)',
                    'yygtr' : u'?????????(%)',
                    'anpg' : u'?????????(%)',
                    'nnpg' : u'?????????(%)',
                    'grrrc' : u'???????????(%)',
                    'anprrc' : u'???????????(%)',
                    'nnprrc' : u'???????????(%)',
                    'wnay' : u'????????(%)',
                    'ridna' : u'????????(%)',
                    'dacer' : u'????????(%)',
                    'gpr' : u'???(%)',
                    'npr' : u'???(%)',
                    'etr' : u'????(%)',
                    'rrpr' : u'???/????',
                    'scfrr' : u'?????/????',
                    'oircf' : u'?????/????',
                    'ttc' : u'??????(?)',
                    'dso' : u'????????(?)',
                    'dii' : u'??????(?)',
                    'alr' : u'?????(%)',
                    'tlrcl' : u'????/???(%)',
                    'lr' : u'????',
                    'qr' : u'????',
                }

                keys = list(dic.keys())
                for i in range(len(keys)):
                    keys[i] = kw_dict[keys[i]]

                print(keys)
                writer.writerow(keys)
                flag = False
            try:
               writer.writerow(list(dic.values()))
            except Exception as e:
                print(e)
    csvfile.close()

if __name__ == '__main__':
    path=str(sys.argv[1]) # 获取path参数
    print (path)
    trans(path)
