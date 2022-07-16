# %%
# 20220704 코드 리팩토링
# * 코드 리팩토링: 결과의 변경 없이 코드의 구조를 재조정. 주로 가독성을 높이고 유지보수를 편하게 한다.

## 사용했던 라이브러리는 동일하게

from bs4 import BeautifulSoup
import requests
import pandas as pd

# %%
## 지정된 변수
## * 컬럼
cols = ['순위', '팀', '경기수', '세트수', '공격', '블로킹', '서브', '득점']
## * url
url = 'https://www.kovo.co.kr/stats/42001_team-totalrecord.asp'
## * RangeIndex = 7 (현 남자부 팀의 개수)

# %%
html = requests.get(url=url, verify=False)
soup = BeautifulSoup(html.content, 'html.parser')

tbody = soup.find('tbody')

temp_data = []
for i in range(1, 8):
    row = tbody.select_one('tr:nth-child(' + str(i) + ')')
    temp_array = []
    for j in range(1,9):
        data = row.select_one('td:nth-child(' + str(j) + ')').get_text()
        temp_array.append(data)
    temp_data.append(temp_array) # loc를 지양하기 위해 부득이하게 수정

df = pd.DataFrame(data=temp_data, columns=cols)
df


