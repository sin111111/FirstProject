# %%
# 1. BeautifulSoup 라이브러리로 다양한 HTML 태그 이용해서 데이터 가져오기
## 예제 url: https://www.kovo.co.kr/game/v-league/11302_player-ranking_view.asp
## 전제조건 정리
## 1) 현 예제의 테이블 컬럼 개수를 동일하게 필요한 데이터는 득점 부문만 가져온다. (공격/오픈공격/시간차공격/이동공격/후위공격/속공/퀵오픈)
## 2) 1)에 의해서 컬럼 리스트는 다음과 같다. ['순위', '선수', '팀', '경기수', '세트수', '시도', '성공', '공격차단', '범실', '성공률']
## 3) 1)과 동일하게 row 최대 개수도 동일하게 하기 위해 최대 TOP 5 선수의 기록만 가져온다.

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
import selenium
import pandas

# %%
# url = 'https://www.kovo.co.kr/game/v-league/11302_player-ranking_view.asp'
url = 'https://www.kovo.co.kr/game/v-league/11302_player-ranking_view.asp?season=018&g_part=201&r_round=0&s_part=1&r_part=at&'

cols = ['순위', '선수', '팀', '경기수', '세트수', '시도', '성공', '공격차단', '범실', '성공률']


# %%
## 1.1.selector
## 해당 tbody 내에 있는 <tr>태그 중 하나를 골라 selector 복사를 해보자
## #tab1_1 > div > table > tbody > tr:nth-child(1) :1위 선수
## 위에서 선택한 <tr>태그 안의 <td> 태그 중 하나를 골라 동일하게 selector 복사를 해보면
## #tab1_2 > div > table > tbody > tr:nth-child(1) > td:nth-child(1)

html = requests.get(url, verify=False)

if(html.status_code == 200):
    soup = BeautifulSoup(html.content, 'html.parser')
html.close()

tbody = soup.find('tbody')

temp_data1 = []
for i in range(1,6): # Top 5명
    row = tbody.select_one('tr:nth-child(' + str(i) + ')') # tr 태그
    temp_row = []
    for j in range(1,11): # column 개수 10개
        data = row.select_one('td:nth-child(' + str(j) + ')').get_text() # td 태그
        temp_row.append(data)
    temp_data1.append(temp_row)


df = pd.DataFrame(temp_data1, columns=cols) # column Index만 있는 빈 DataFrame
df

# %%
## 1.2.XPath
## 해당 tbody 내에 있는 <tr>태그 중 하나를 골라 XPath 복사를 해보자
## //*[@id="tab1_1"]/div/table/tbody/tr[1] : 1위 선수

driver = webdriver.Chrome('./chromedriver.exe')
driver.get(url)
driver.implicitly_wait(time_to_wait=5)

temp_data2 = []

xpath = '//*[@id="tab1_2"]/div/table/tbody/tr[1]'

for i in range(1,6): # Top 5명
    rowxpath = '//*[@id="tab1_2"]/div/table/tbody/tr[' + str(i) + ']'
    row = driver.find_elements("xpath", rowxpath)[0].text
    temp_row = row.split() # row에서 split만 해주면 된다.
    temp_data2.append(temp_row)


driver.quit()

df = pd.DataFrame(temp_data2, columns=cols) # column Index만 있는 빈 DataFrame
df


