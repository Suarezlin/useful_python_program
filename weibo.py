import requests
import re
from pyquery import PyQuery as pq
import time
from PIL import Image
import json


class Weibo():
    def __init__(self):
        self.session = requests.session()

    def get_QR(self):
        req_url = 'http://login.sina.com.cn/sso/qrcode/image?entry=weibo&size=180&callback=STK_' + str(
            int(time.time() * 1000))
        result = self.session.get(req_url).text
        p = re.compile('\((.*?)\)', re.S)
        result = eval(re.findall(p, result)[0])['data']
        qr = self.session.get(result['image'].replace('\\', ''), stream=True)
        open('qrcode.png', 'wb').write(qr.content)
        qrcode = Image.open('qrcode.png')
        qrcode.show()
        return result['qrid']

    def login(self, **kwargs):
        if kwargs['hot_reload'] is True:
            try:
                with open('cookie.txt', 'r') as f:
                    cookie = requests.utils.cookiejar_from_dict(json.load(f))
                self.session.cookies = cookie
            except:
                qr = self.get_QR()
                while (True):
                    auth_url = 'http://login.sina.com.cn/sso/qrcode/check?entry=weibo&qrid={}&callback=STK_{}'.format(
                        qr['qrid'], int(time.time() * 1000))
                    result=self.session.get(auth_url)


if __name__ == '__main__':
    weibo = Weibo()
    weibo.get_QR()
