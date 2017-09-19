import requests
import time
import os


class Ykt():
    def __init__(self):
        self.session = requests.session()
        self.cookie = 'sessionid=7d6cr6icrxcf3ycdem0i5u4skhvhft4r; _ga=GA1.2.1039719887.1505826649; _gid=GA1.2.1240686482.1505826649; csrftoken=ai6GdFXYBjppTNgZ8VsQa43SxKOuD5tW'
        self.cookies = {}
        for i in self.cookie.split(';'):
            name, value = i.strip().split('=', 1)
            self.cookies[name] = value  # 为字典 cookies 添加内容
        self.pptInfo = []
        self.ppt = []

    def getLessonInfo(self):
        lessonInfoUrl = 'http://ykt.io/v/course_meta/manage_classroom_teachinglogs/59815/77062?_date='
        request = self.session.get(lessonInfoUrl + str(int(time.time())),
                                   cookies=self.cookies).json()
        self.lessonInfo = request["data"]["activities"]
        return request

    def getPptInfo(self):
        pptInfoUrl = 'http://ykt.io/v/lesson/learning_lesson_detail_v2/{}/?_date={}'
        for item in self.lessonInfo:
            id = item["courseware_id"]
            now = int(time.time())
            urlPptInfo = pptInfoUrl.format(id, now)
            try:
                self.pptInfo.append(self.session.get(
                    urlPptInfo,
                    cookies=self.cookies).json()["data"]["presentations"][0])
            except:
                ii = self.session.get(
                    urlPptInfo,
                    cookies=self.cookies).json()
        return self.pptInfo

    def getPptDownloadUrl(self):
        pptUrl = 'http://ykt.io/v/lesson/show_studentsPPT/{}/?_date={}'
        for item in self.pptInfo:
            id = item["id"]
            now = int(time.time())
            urlPpt = pptUrl.format(id, now)
            self.ppt.append(self.session.get(
                urlPpt,
                cookies=self.cookies).json()["data"])
        return self.ppt

    def downloadPpt(self):
        for item in self.ppt:
            pptName = item["lessonPresentation"]["title"]
            pptUrl = item["presentationSlides"]["Slides"]
            if os.path.exists(pptName):
                pass
            else:
                os.mkdir(pptName);
            i = 1
            for url in pptUrl:
                u = url["Cover"]
                try:
                    ppt = self.session.get(u, cookies=self.cookies, stream=True)
                    if ppt.status_code == 200:
                        with open('./{}/{}.png'.format(pptName, i), 'wb') as f:
                            for chunk in ppt:
                                f.write(chunk)
                except:
                    pass
                i += 1
                # print("下载 {}.png 成功".format(i))
            print("下载 {} 成功".format(pptName))
        print("下载完成")


if __name__ == '__main__':
    ykt = Ykt()
    ykt.getLessonInfo()
    ykt.getPptInfo()
    ykt.getPptDownloadUrl()
    ykt.downloadPpt()
