__author__ = 'Suarezlin'
import requests
import re
import xlrd
import xlwt

data = xlrd.open_workbook(r'E:\GitHub\ipsearch\visit.xlsx')
table = data.sheets()[0]
a=table.col_values(0)
b=table.col_values(1)
url='http://www.ip138.com/ips138.asp?ip={}&action=2'
result=[]
pattern=re.compile('<li>本站数据：(.*?)</li>',re.S)
for i in range(0,len(a)):
    urll=url.format(a[i])
    text=requests.get(urll).text
    aa=re.findall(pattern,text)
    result.append(aa)
    print(i)
print(result)