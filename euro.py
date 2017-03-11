import requests
import re
import json


class Euro:
    def __init__(self, team):
        self.team = team
        self.num = 1
        self.match_list = {'1': 'Group_Match_1', '2': 'Group_Match_2', '3': 'Group_Match_3', '4': 'Group_Match_4',
                           '5': 'Group_Match_5', '6': 'Group_Match_6', '7': 'Group_Match_Result', '8': '1_8_final',
                           '9': 'Quarter_Finals',
                           '10': 'Semi_Finals', '11': 'Final'}
        self.match_list_1 = {'1': 'First_Round', '2': 'Second_Round', '3': 'Quarter_Finals_1', '4': 'Quarter_Finals_2',
                             '5': 'Quarter_Finals_3', '6': 'Quarter_Finals_4', '7': 'Quarter_Finals_5',
                             '8': 'Quarter_Finals_6', '9': 'Quarter_Final_Result', '10': 'Final'}
        self.match_list_2 = {'1': 'First_Round', '2': 'Second_Round', '3': 'Quarter_Finals', '4': 'Semi_Finals',
                             '5': 'Final'}
        self.match_list_3 = {'1': 'First_Round', '2': 'Quarter_Finals', '3': 'Semi_Finals', '4': 'Final'}
        self.match_list_4 = {'1': 'Preliminary_Round', '2': 'First_Round', '3': 'Quarter_Finals', '4': 'Semi_Finals',
                             '5': 'Final'}

    def get_Url(self):
        url = 'http://www.rsssf.com/ec/ecomp.html'
        text = requests.get(url).text
        p1 = re.compile('<A NAME="results">The Results</A></H3>(.*?)<H3><A NAME="finals">The Finals</A></H3>', re.S)
        text = re.findall(p1, text)[0]
        p2 = re.compile('<A HREF="(.*?)"', re.S)
        url = re.findall(p2, text)
        url = list(map((lambda x: 'http://www.rsssf.com/ec/' + x), url))
        return url

    def strip_tags(self, html):
        # """
        # Python中过滤HTML标签的函数
        # >>> str_text=strip_tags("<font color=red>hello</font>")
        # >>> print str_text
        # hello
        # """
        from html.parser import HTMLParser
        html = html.strip()
        html = html.strip("\n")
        result = []
        parser = HTMLParser()
        parser.handle_data = result.append
        parser.feed(html)
        parser.close()
        return ''.join(result)

    def isNone(self, s):
        return s and s.strip

    def get_Data(self, url):
        text = requests.get(url).text
        try:
            p1 = re.compile('<A NAME="ccg">Group Phase</A>(.*?)<P><A HREF="ecomp\.html">Index</A>', re.S)
            text = re.findall(p1, text)[0]
        except:
            try:
                p1 = re.compile('<a name="ccg1">Group Phase 1</a>(.*?)<P><A href="ecomp\.html">Index</A>', re.S)
                text = re.findall(p1, text)[0]
            except:
                try:
                    p1 = re.compile('Additional Match Details</a>(.*?)<a href=', re.S)
                    text = re.findall(p1, text)[0]
                except:
                    try:
                        p1 = re.compile('<pre>(.*?)</pre>', re.S)
                        text = re.findall(p1, text)[0]
                    except:
                        p1 = re.compile('<PRE>(.*?)</PRE>', re.S)
                        text = re.findall(p1, text)[0]
        item = text.split('\n')
        item = list(map(self.strip_tags, item))
        item = list(filter(self.isNone, item))
        return item

    def have_team(self, data):
        if self.team in data or self.team.upper() in data :
            return True
        else:
            if self.team=='Bayern München':
                if 'Bayern Munich' in data or 'Bayern Munich'.upper() in data:
                    return True
            return False

    def hasNumbers(self, inputString):
        return any(char.isdigit() for char in inputString)

    def get_replace(self, s, season):
        if int(season) >=200910:
            s = re.split(r'[\:]+', s)
            l = {}
            if len(s) > 1:
                if not self.hasNumbers(s[1]):
                    return {}
                ss = s[1]
                l = {'date': s[0], 'team_1': s[1][1:25], 'team_1_goal': s[1][30:31], 'team_2': s[1][33:57],
                     'team_2_goal': s[1][61:62]}
                self.num += 1
            else:
                try:
                    a = re.match(
                        r'([a-zA-zøöüñ\-\']+\s*[a-zA-Zøöüñ\-\']+\s*[a-zA-Zøöüñ\-\']*)\s*([0-9]+)\s*([0-9]+)\s*([0-9]+)\s*([0-9]+)\s*([0-9]+)\s*([0-9]+)\s*([0-9]+)',
                        s[0])
                    l = {'team': a.group(1), 'matches': a.group(2), 'win': a.group(3), 'draw': a.group(4),
                         'lose': a.group(5), 'goals': a.group(6), 'lose_goals': a.group(7), 'score': a.group(8)}
                except:
                    l = {'team_1': s[0][:25], 'team_2': s[0][30:55], 'first_turn': s[0][61:64],
                         'second_turn': s[0][66:69],
                         'sum': s[0][71:74]}
            return l
        elif int(season) >= 199596:
            s = re.split(r'[\:]+', s)
            l = {}
            if len(s) > 1:
                if not self.hasNumbers(s[1]):
                    return {}
                ss = s[1]
                l = {'date': s[0], 'team_1': s[1][1:25], 'team_1_goal': s[1][30:31], 'team_2': s[1][33:58],
                     'team_2_goal': s[1][62:63]}
                self.num += 1
            else:
                try:
                    a = re.match(
                        r'([a-zA-zøöüñ\-\']+\s*[a-zA-Zøöüñ\-\']+\s*[a-zA-Zøöüñ\-\']*)\s*([0-9]+)\s*([0-9]+)\s*([0-9]+)\s*([0-9]+)\s*([0-9]+)\s*([0-9]+)\s*([0-9]+)',
                        s[0])
                    l = {'team': a.group(1), 'matches': a.group(2), 'win': a.group(3), 'draw': a.group(4),
                         'lose': a.group(5), 'goals': a.group(6), 'lose_goals': a.group(7), 'score': a.group(8)}
                except:
                    l = {'team_1': s[0][:25], 'team_2': s[0][30:55], 'first_turn': s[0][61:64],
                         'second_turn': s[0][66:69],
                         'sum': s[0][71:74]}
            return l
        elif int(season) >= 199192:
            if len(s) > 70:
                l = {'team_1': s[:25], 'team_2': s[30:55], 'first_turn': s[61:64], 'second_turn': s[66:69],
                     'sum': s[71:74]}
            elif len(s) > 50:
                l = {'team_1': s[:25], 'team_1_goals': s[29:30], 'team_2': s[32:57], 'team_2_goals': s[61:62]}
            else:
                l = {'team': s[:27], 'matches': s[27:28], 'win': s[30:31], 'drew': s[33:34], 'lose': s[36:37],
                     'goals': s[38:40], 'lose_goals': s[41:43], 'score': s[44:46]}
            return l
        elif int(season) >= 198485:
            if len(s) > 70:
                l = {'team_1': s[:25], 'team_2': s[30:55], 'first_turn': s[61:64], 'second_turn': s[66:69],
                     'sum': s[71:74]}
                return l
            else:
                l = {'team_1': s[:25], 'team_1_goals': s[29:30], 'team_2': s[32:57], 'team_2_goals': s[61:62]}
                return l
        elif int(season) >= 196970:
            if len(s) > 70:
                l = {'team_1': s[:25], 'team_2': s[30:55], 'first_turn': s[60:63], 'second_turn': s[65:68],
                     'sum': s[70:73]}
                return l
            else:
                l = {'team_1': s[:25], 'team_1_goals': s[29:30], 'team_2': s[32:57], 'team_2_goals': s[61:62]}
                return l

        elif int(season) >= 196263:
            if len(s) > 70:
                l = {'team_1': s[:25], 'team_2': s[30:55], 'first_turn': s[61:64], 'second_turn': s[66:69],
                     'sum': s[71:74]}
                return l
            else:
                l = {'team_1': s[:25], 'team_1_goals': s[29:30], 'team_2': s[32:57], 'team_2_goals': s[61:62]}
                return l
        else:
            if len(s) > 70:
                l = {'team_1': s[:25], 'team_2': s[30:55], 'first_turn': s[61:64], 'second_turn': s[66:69],
                     'sum': s[71:74]}
            else:
                l = {'team_1': s[:25], 'team_1_goals': s[29:30], 'team_2': s[32:57], 'team_2_goals': s[61:62]}
            return l

    def get_teamgrade(self, item, season):
        if int(season) >= 199495:
            i = 1
            result = {}
            for it in item:
                if self.hasNumbers(it):
                    try:
                        result[self.match_list[str(i)]] = self.get_replace(it, season)
                    except:
                        result['ps'] = self.get_replace(it, season)
                    i += 1
            return result
        elif int(season) >= 199192:
            i = 1
            result = {}
            for it in item:
                if self.hasNumbers(it):
                    try:
                        result[self.match_list_1[str(i)]] = self.get_replace(it, season)
                    except:
                        result['ps'] = self.get_replace(it, season)
                    i += 1
            return result
        elif int(season) >= 196263:
            i = 1
            result = {}
            for it in item:
                if self.hasNumbers(it):
                    try:
                        result[self.match_list_2[str(i)]] = self.get_replace(it, season)
                    except:
                        result['ps'] = self.get_replace(it, season)
                    i += 1
            return result
        else:
            i = 1
            result = {}
            item = list(filter(self.hasNumbers, item))
            for it in item:
                if len(item) == 4:
                    result[self.match_list_3[str(i)]] = self.get_replace(it, season)
                    i += 1
                else:
                    result[self.match_list_4[str(i)]] = self.get_replace(it, season)
                    i += 1
            return result

    def get_TeamData(self):
        url = self.get_Url()
        result = {}
        for it in url:
            print(it)
            data = self.get_Data(it)
            l = list(filter(self.have_team, data))
            if len(list(filter(self.hasNumbers, l))) < 4:
                l = []
            result[it[26:32]] = self.get_teamgrade(l, it[26:32])

        return result
        # def make_Json(self):


if __name__ == '__main__':
    euro = Euro('Manchester United')
    data = euro.get_TeamData()
    json_data = json.dumps(data)
    fileObject = open('MTU.json', 'w')
    fileObject.write(json_data)
    fileObject.close()
