# %%
# 파라미터 Dict 객체 생성
# url = https://www.kovo.co.kr/stats/42001_team-totalrecord.asp

from bs4 import BeautifulSoup
import requests
import pandas as pd

# %%
init_url = 'https://www.kovo.co.kr/stats/42001_team-totalrecord.asp'

html = requests.get(init_url, verify=False)

if(html.status_code == 200):
    soup = BeautifulSoup(html.content, 'html.parser')
    html.close()

# %%
# 모든 파라미터의 변수명을 알기 위해서 기록보기 버튼을 클릭하면
# url = 'https://www.kovo.co.kr/stats/42001_team-totalrecord.asp?s_part=1&spart=&s_season=016&s_pr=201%7C3&e_season=017&e_pr=201%7C1&part=point' 를 얻게 된다.
# 해당 페이지의 변수는 s_part, spart, s_season, s_pr, e_season, e_pr, part 총 7개이다.
# 이 중 남자부,여자부를 구분하는 s_part와 null값을 보내는 spart를 제외하면
# select 태그를 이용해서 사용자가 선택하는 파라미터는 5개이다.

param_names = ['s_season', 's_pr', 'e_season', 'e_pr', 'part']

# %%
dict = {}
for name in param_names:
    selects = soup.find('select', {'name': name})
    temp_dict = {}
    for i, option in enumerate(selects):
        if i % 2 != 0: # 이해 조금 어려움...
            option_value = str(option).split('value="')[1].split('">')[0]
            temp_dict.setdefault(option_value,option.get_text())

    dict.setdefault(name, temp_dict)


for name in param_names:
    print(name + " ::: " + str(dict[name]))

# %%



