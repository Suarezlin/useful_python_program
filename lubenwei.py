import requests
import re
from selenium import webdriver

url = "https://api.pubgtracker.com/v2/search/steam?steamId=76561198424811549"
key = "22eb5389-3a6c-46d4-a19e-f9782df9722d"

headers = {
    "TRN-Api-Key": key,
}

session = requests.session()
res = session.get(url, headers=headers)
# print(res.text)
pattern1 = re.compile('name="jschl_vc" value="(.*?)"', re.S)
pattern2 = re.compile('name="pass" value="(.*?)"', re.S)
pattern3 = re.compile('var s,t,o,p,b,r,e,a,k,i,n,g,f, (.*?);', re.S)
pattern4 = re.compile(
    "f = document.getElementById\('challenge-form'\);(.*?)a.value", re.S)
pattern5 = re.compile("var s,t,o,p,b,r,e,a,k,i,n,g,f, (.*?)={", re.S)
pattern6 = re.compile('{"(.*?)":', re.S)
jschl_vc = re.findall(pattern1, res.text)[0]
Pass = re.findall(pattern2, res.text)[0]
js = re.findall(pattern3, res.text)[0] + re.findall(pattern4, res.text)[0]
name = re.findall(pattern5, res.text)[0]
key = re.findall(pattern6, js)[0]
js = 'return (function () {' + js + 'return ' + name + ';})()'

print(js)
driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
# driver.get('https://www.baidu.com')

r = driver.execute_script(js)[key] + len('api.pubgtracker.com')
cookieUrl = 'https://api.pubgtracker.com/cdn-cgi/l/chk_jschl?jschl_vc={}&pass={}&jschl_answer={}'.format(
    jschl_vc, Pass, r)

cookieHeaders = {
    ':authority': 'api.pubgtracker.com',
    ':method': 'GET',
    ':path': '/cdn-cgi/l/chk_jschl?jschl_vc={}&pass={}&jschl_answer={}'.format(jschl_vc, Pass, r),
    ':scheme': 'https',
    "TRN-Api-Key": key,
    "referer": url,
}
res1 = session.get(cookieUrl, headers=cookieHeaders)
res = session.get(url, headers=headers)
print(r)

print(jschl_vc)
print(Pass)
