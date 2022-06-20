from bs4 import BeautifulSoup
import requests

def crawlData():
    url = 'https://www.kovo.co.kr/stats/42001_team-totalrecord.asp'
    # KOVO 팀 누적 기록 남자부

    html = requests.get(url)

    return html

print(1)
# 크롤링이란?
    # 인터넷으로 접근 가능한 웹사이트를 접근.
    # html을 가져와서 데이터를 가공하는 것 

# def test():
    # a = 1 #int
    # a = "1" #string 
    # int(a) #정수형
    # float(a) #실수형

    # PEP8 표준개발양식?
    # data_crawl = 1 # TabIndexError 주의

    # return a