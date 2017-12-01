# /usr/bin/ python3
import requests
import re
from bs4 import BeautifulSoup
import random
import time


class B(object):
    isNotEmpty = True;


class Webix(object):
    rules = B()


class PingJiao():
    def __init__(self):
        self.login = 'https://cas.xjtu.edu.cn/login'
        self.postUrl = 'http://ssfw.xjtu.edu.cn/index.portal'
        self.pingjiaoInfoUrl = 'http://zhpj.xjtu.edu.cn/app/sshd4Stu/list.do?key=value'
        self.pingjiaoTableUrl = 'http://zhpj.xjtu.edu.cn/app/student/genForm.do?assessment={}&cj_able={}&data_jxb_id={}&data_jxb_js_id={}&hbqk={}&jsbh={}&jsxm={}&jxbid={}&kcdm={}&kcmc={}&msgbutton={}&pjlbmc={}&skls_duty=&xnxqdm={}&id={}'
        self.saveformUrl = 'http://zhpj.xjtu.edu.cn/app/student/saveForm.do'
        self.session = requests.session()

    def getLt(self):
        request = self.session.get(self.postUrl)
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
        r = self.session.get(self.postUrl)
        soup = BeautifulSoup(r.text, 'html.parser').find('meta').get('content')[
               6:]
        # self.session.get(soup)
        # 登录完成
        print("登录成功")

    def getPingjiaoInfo(self):
        self.logIn()
        res = self.session.get(self.pingjiaoInfoUrl).json()
        return res

    def getPingjiaoTable(self, info):
        res = self.session.get(
            self.pingjiaoTableUrl.format(info['assessment'], info['cj_able'],
                                         info['data_jxb_id'],
                                         info['data_jxb_js_id'], info['hbqk'],
                                         info['jsbh'], info['jsxm'],
                                         info['jxbid'], info['kcdm'],
                                         info['kcmc'], info['msgbutton'],
                                         info['pjlbmc'], info['xnxqdm'],
                                         int(time.time())))
        text = res.text
        pattern = re.compile('.*?pjzbApp.form = (.*?);.*?', re.S)
        webix = Webix()
        webix.rules.isNotEmpty = True;
        result = eval(re.findall(pattern, text)[0])
        return result

    def processPingjiao(self):
        infos = self.getPingjiaoInfo()
        for info in infos:
            if info['assessment'] == 'allow':
                form = self.getPingjiaoTable(info)
                params = {
                    "standard_id": form['elements'][0]['value'],
                    "standard_name": form['elements'][1]['value'],
                    "jxbid": form['elements'][2]['value'],
                    "jsbh": form['elements'][3]['value'],
                    "kcdm": form['elements'][4]['value'],
                    form['elements'][5]['rows'][1]['id']:
                        form['elements'][5]['rows'][1]['options'][1]['id'],
                    form['elements'][5]['rows'][3]['cols'][1]['rows'][-1][
                        'id']: '好好好',
                }
                temp = []
                for item in form['elements'][5]['rows'][3]['cols'][1]['rows']:
                    if ('cols' in item.keys()):
                        for item2 in item['cols']:
                            if ('rows' in item2.keys()):
                                for item3 in item2['rows']:
                                    temp.append(item3)
                for item in form['elements'][5]['rows'][4]['cols'][1]['rows']:
                    temp.append(item)
                for item in temp:
                    params[item['id']] = item['options'][random.randint(1, 2)][
                        'id'];
                res = self.session.post(self.saveformUrl, data=params)
                if (res.status_code == 200):
                    print(info['kcmc'] + " " + info['jsxm'] + " 评教成功")
                else:
                    print(info['kcmc'] + " " + info[
                        'jsxm'] + " 评教失败 错误代码: " + str(res.status_code))


if __name__ == '__main__':
    pingjiao = PingJiao()
    pingjiao.processPingjiao()
