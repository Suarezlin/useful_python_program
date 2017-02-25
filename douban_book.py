import requests
from pyquery import PyQuery as pq
import time
import re
from lxml import etree


class Doubanbook():
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Referer': 'http://space.bilibili.com/24034283/'
        }

    def get_book_info(self, args, **kwargs):
        if kwargs['type'] == 'douban_num':
            url = 'https://book.douban.com/subject/{}/'.format(args)
            text = requests.get(url, headers=self.header).text
            p_title = re.compile('<span property="v:itemreviewed">(.*?)</span>')
            p_rate=re.compile('property="v:average"> (.*?) </strong>',re.S)
            p_comment=re.compile('全部 (.*?) 条',re.S)
            info = {}
            info['rate']=re.findall(p_rate,text)[0]
            info['title'] = re.findall(p_title, text)[0]
            info['short comment']=re.findall(p_comment,text)[0]
            info['comment']=re.findall(p_comment,text)[1]
            p = re.compile('<div id="info" class="">(.*?)</div>', re.S)
            text = re.findall(p, text)[0]
            doc = pq(text)
            info['author'] = doc('a').text()
            pattern = re.compile(':</span> (.*?)<br/>', re.S)
            result = re.findall(pattern, text)
            info['publisher'] = result[0]
            info['date'] = result[1]
            info['pages'] = result[2]
            info['price'] = result[3]
            info['isbn'] = result[5]
            info['douban_num'] = args
            return info
        elif kwargs['type'] == 'name':
            search_url = 'https://book.douban.com/subject_search?search_text={}&cat=1001'.format(args)
            url=[]
            for it in pq(requests.get(search_url).text)('.info').items():
                url.append(it('a').attr('href'))
            douban_num=url[0][32:-1]
            result= self.get_book_info(douban_num,type='douban_num')
            return result
        elif kwargs['type'] == 'isbn':
            search_url = 'https://book.douban.com/subject_search?search_text={}&cat=1001'.format(args)
            text=requests.get(search_url).text
            url=[]
            for it in pq(requests.get(search_url).text)('.info').items():
                url.append(it('a').attr('href'))
            douban_num=url[0][32:-1]
            result = self.get_book_info(douban_num, type='douban_num')
            return result


douban = Doubanbook()
douban.get_book_info('9787540477776', type='isbn')
