#-*-coding:utf-8-*-
import csv
import json
import sys
import codecs

#reload(sys)
#sys.setdefaultencoding( "utf-8" )

def trans(path):
	# csvfile = open(path+'.csv', 'w') # 此处这样写会导致写出来的文件会有空行
	# csvfile = open(path+'.csv', 'wb') # python2下
	csvfile = open(path+'.csv', 'w', newline='') # python3下
	#writer = csv.writer(csvfile, delimiter='，', quoting=csv.QUOTE_ALL)
	writer = csv.writer(csvfile, delimiter=',')
	flag = True
	l = 0
	line_item_nr = 0

	with open(path, 'r') as f:
		for line in f:
			l += 1

			line = line.strip(' \n,');
			if line == '[' or line == ']':
				continue

			dic = json.loads(line.encode('utf-8'), encoding='utf-8')

			if flag:
				kw_dict = {
					'code' : '代码',
					'period' : '报告期',
					'exchange' : '交易所',
					'reg_capital' : '注册资本(元)',
					'date' : '日期',
					'name' : '简称',
					'region' : '区域',
					'industry' : '所属证监会行业',
					'eps' : u'基本每股收益(元)',
					'neps' : u'扣非每股收益(元)',
					'deps' : u'稀释每股收益(元)',
					'bvps' : u'每股净资产(元)',
					'cfps' : u'每股公积金(元)',
					'uddps' : u'每股未分配利润(元)',
					'ocfps' : u'每股经营现金流(元)',
					'gr' : u'营业总收入(元)',
					'gp' : u'毛利润(元)',
					'anp' : u'归属净利润(元)',
					'nnp' : u'扣非净利润(元)',
					'yygtr' : u'营业总收入同比增长(%)',
					'anpg' : u'归属净利润同比增长(%)',
					'nnpg' : u'扣非净利润同比增长(%)',
					'grrrc' : u'营业总收入滚动环比增长(%)',
					'anprrc' : u'归属净利润滚动环比增长(%)',
					'nnprrc' : u'扣非净利润滚动环比增长(%)',
					'wnay' : u'加权净资产收益率(%)',
					'ridna' : u'摊薄净资产收益率(%)',
					'dacer' : u'摊薄总资产收益率(%)',
					'gpr' : u'毛利率(%)',
					'npr' : u'净利率(%)',
					'etr' : u'实际税率(%)',
					'rrpr' : u'预收款/营业收入',
					'scfrr' : u'销售现金流/营业收入',
					'oircf' : u'经营现金流/营业收入',
					'ttc' : u'总资产周转率(次)',
					'dso' : u'应收账款周转天数(天)',
					'dii' : u'存货周转天数(天)',
					'alr' : u'资产负债率(%)',
					'tlrcl' : u'流动负债/总负债(%)',
					'lr' : u'流动比率',
					'qr' : u'速动比率',
				}

				keys = list(dic.keys())
				for i in range(len(keys)):
					keys[i] = kw_dict[keys[i]]

				line_item_nr = len(keys)
				print('line item nr: ' + str(line_item_nr))
				print(keys)

				writer.writerow(keys)
				flag = False
			try:
				if (len(dic) != line_item_nr):
					print(l)
					print(dic)

				writer.writerow(list(dic.values()))
			except Exception as e:
				print(e)
	csvfile.close()

if __name__ == '__main__':
	path=str(sys.argv[1]) # 获取path参数
	print(path)
	trans(path)
