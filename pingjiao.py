__author__ = 'Suarezlin'
import requests
import re
from bs4 import BeautifulSoup
import random
class Pingjiao:
    def __init__(self):
        self.login = 'https://cas.xjtu.edu.cn/login'
        self.posturl = 'http://ssfw.xjtu.edu.cn/index.portal'
        self.pingjiaourl = 'http://ssfw.xjtu.edu.cn/index.portal?.pn=p1142_p1182_p1183'
        self.session=requests.session()
    def getLt(self):
        request = self.session.get(self.posturl)
        request = request.text
        str = 'name="lt" value="(.*?)"'
        pattern = re.compile(str, re.S)
        lt = re.findall(pattern, request)
        return lt[0]

    def logIn(self):
        print('请输入NetID：')
        self.username = input()
        print('请输入密码：')
        self.password = input()
        print('登录中请稍候')
        str = '登录'
        str = str.encode('utf-8')
        postdata = {
            'username': self.username,
            'password': self.password,
            'code': '',
            'lt': self.getLt(),
            'execution': 'e1s1',
            '_eventId': 'submit',
            'submit': str
        }
        self.session.post(self.login, postdata)
        r = self.session.get(self.posturl)
        soup = BeautifulSoup(r.text, 'html.parser').find('meta').get('content')[6:]
        self.session.get(soup)
        # 登录完成
    def pinjiao(self):
        self.logIn()
        print('评教中请稍后...')
        r = self.session.get(self.pingjiaourl)
        text=r.text
        pattern=re.compile('未评教.*?<a href="(.*?)">评教</a>',re.S)
        content=re.findall(pattern,text)
        url=[]
        for it in content:
            if it[0]=='?':
                url.append(it)
        basicurl='http://ssfw.xjtu.edu.cn/index.portal'
        tureurl=[]
        for it in url:
            ping_url=basicurl+it
            pat=re.compile('method="post" action="(.*?)" class',re.S)
            r=self.session.get(ping_url)
            text=r.text
            ture_url=re.findall(pat,text)
            tureurl.append(ture_url[0])
        ii=0
        for it in url:
            ping_url=basicurl+it
            r=self.session.get(ping_url)
            text=r.text
            p=re.compile('<b>课程名称：</b><b>(.*?)</b>',re.S)
            name=re.findall(p,text)
            pattern=re.compile('id="wid_pgjxb" value="(.*?)" />.*?id="wid_pjzts" value="(.*?)"/>',re.S)
            pa=re.compile('<input name="(.*?)" type=".*?value="(.*?)"/>.*? name="(.*?)".*?<input name="(.*?)" type="hidden" value="(.*?)"/>.*?type="checkbox" name="(.*?)".*?value="(.*?)".*?type="checkbox" name="(.*?)".*?value="(.*?)"',re.S)
            co=re.findall(pa,text)
            content=re.findall(pattern,text)
            value=content[0]
            data=(
                ['wid_pgjxb',value[0]],
                ['wid_pgyj',''],
                ['type','2'],
                ['sfytj','true'],
                ['pjType','4'],
                ['wid_pjzts',value[1]],
                ['pgyj','老师非常认真，教的十分细致'],
                ['actionType','2'],
                ['ztpj','老师认真负责'],
                ['status','0'],
                ['sfmxpj','false']
            )
            data=list(data)
            for i in co:
                data.append([i[0],i[1]])
                data.append([i[2],''])
                data.append([i[3],i[4]])
                if random.random()>0.5:
                    data.append([i[5],i[6]])
                else:
                    data.append([i[5],i[8]])
            data=tuple(data)
            a=self.session.post(basicurl+tureurl[ii],data=data)
            print(name[0]+'评教完成')
            ii=ii+1

print('--西安交通大学教务处一键评教系统--')
pingjiao=Pingjiao()
pingjiao.pinjiao()
