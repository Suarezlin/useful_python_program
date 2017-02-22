import requests, requests.utils
import qrcode
from PIL import Image
import time
import json
from pyquery import PyQuery as pq


class Bilibili():
    def __init__(self):
        self.login_page = 'https://passport.bilibili.com/login'
        self.getloginurl = 'https://passport.bilibili.com/qrcode/getLoginUrl'
        self.session = requests.session()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Referer': 'http://space.bilibili.com/24034283/'
        }

    def get_QR(self):
        qr_page = self.session.get(self.getloginurl).json()['data']
        self.oauthKey = qr_page['oauthKey']
        qr_url = qr_page['url']
        qr_code = qrcode.make(qr_url)
        qr_code.save('./qrcode.png')

    def login(self):
        try:
            with open('cookie.txt', 'r') as f:
                cookie = requests.utils.cookiejar_from_dict(json.load(f))
            self.session.cookies = cookie
            url = 'http://space.bilibili.com/ajax/member/MyInfo?_=' + str(int(time.time()) * 1000)
            result = self.session.get(url).json()['status']
            if not result:
                raise AttributeError("unavaliable cookie")
        except:
            self.get_QR()
            login_info_url = 'https://passport.bilibili.com/qrcode/getLoginInfo'
            qrcode = Image.open('./qrcode.png')
            qrcode.show()
            data = {
                'oauthKey': self.oauthKey,
                'gourl': ''
            }
            while (True):
                login_info = self.session.post(login_info_url, data=data).json()['data']
                if login_info == -5:
                    print('请在手机 app 上确认登录')
                elif login_info == -4:
                    pass
                else:
                    print('登录成功')
                    self.session.get(login_info['url'])
                    with open('cookie.txt', 'w') as f:
                        json.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)
                    break
                print(login_info)
                time.sleep(4)

    def get_info(self, mid):
        url = 'http://space.bilibili.com/ajax/member/GetInfo'
        data = {
            'mid': str(mid),
            '_': int(time.time() * 1000)
        }
        result = self.session.post(url, data=data, headers=self.header).json()['data']
        return result

    def my_info(self):
        url = 'http://space.bilibili.com/ajax/member/MyInfo?_=' + str(int(time.time()) * 1000)
        return self.session.get(url).json()['data']

    def get_submit_video(self, mid, page):
        url = 'http://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&ts={}&page={}&pagesize=25'.format(mid, str(
            int(time.time()) * 1000), page)
        result = self.session.get(url).json()['data']['vlist']
        return result

    def get_favorite_list(self, mid):
        url = 'http://space.bilibili.com/ajax/fav/getBoxList?mid={}&_={}'.format(mid, str(
            int(time.time()) * 1000))
        result = self.session.get(url).json()['data']['list']
        return result

    def get_fan_list(self, mid, page):
        url = 'http://space.bilibili.com/ajax/friend/GetFansList?mid={}&page={}&_={}'.format(mid, page, str(
            int(time.time()) * 1000))
        result = self.session.get(url).json()['data']['list']
        return result

    def get_attention_list(self, mid, page):
        url = 'http://space.bilibili.com/ajax/friend/GetAttentionList?mid={}&page={}&_={}'.format(mid, page, str(
            int(time.time()) * 1000))
        return self.session.get(url).json()['data']['list']

    def get_hot_video(self, fromdata, todata):
        url = 'http://www.bilibili.com/list/hot-17-1-{}~{}.html'.format(todata, fromdata)
        # url='http://www.bilibili.com/list/hot-17-1-2017-02-15~2017-02-22.html'
        text = self.session.get(url).text
        doc = pq(text)
        video = doc('.l-item')
        info = []
        for it in video.items():
            info.append(self.get_video_info(it('.title').attr('href')[7:-1]))
        return info

    def get_video_info(self, av_num):
        url = 'http://www.bilibili.com/video/' + av_num + '/'
        play_url = 'http://api.bilibili.com/archive_stat/stat?aid=' + av_num[2:]
        data = self.session.get(play_url).json()['data']
        doc = pq(self.session.get(url).text)
        info = {}
        info['title'] = doc('.v-title h1').text()
        info['up'] = doc('.name').text()
        info['up-mid'] = doc('.name').attr('mid')
        info['about_video'] = doc('#v_desc').text()
        info['time'] = doc('[itemprop=startDate]').text()
        info['play'] = data['view']
        info['danmu'] = data['danmaku']
        info['comment'] = data['reply']
        info['favorite'] = data['favorite']
        info['coin'] = data['coin']
        info['share'] = data['share']
        return info


if __name__ == '__main__':
    bilibili = Bilibili()
    bilibili.login()
    bilibili.get_favorite_list('433351')
    bilibili.get_favorite_list('433351')
