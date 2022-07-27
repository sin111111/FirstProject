# %%
# 라이브러리 import
from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib3
urllib3.disable_warnings()

# 지정된 변수
init_url = 'https://www.kovo.co.kr/stats/42001_team-totalrecord.asp'
cols = ['순위', '팀', '경기수', '세트수', '공격', '블로킹', '서브', '득점']

# 파라미터 데이터 추출
html = requests.get(init_url, verify=False)

if(html.status_code == 200):
    soup = BeautifulSoup(html.content, 'html.parser')
    html.close()
else:
    print("Request ERROR ::: status code ::: " + str(html.status_code)) # 항상 에러 발생을 염두에 두자..


param_names = ['s_season', 's_pr', 'e_season', 'e_pr', 'part'] # 파라미터 이름

for name in param_names:
    temp_dict = {}
    for option in soup.find('select', {'name' : name}).find_all('option'):
        key = option.attrs['value'] # '018'
        value = option.getText() # '도드람 2021-2022 V-리그'
        temp_dict[key] = value

    locals()[str(name)+ '_dict'] = temp_dict


'''
locals() :
Update and return a dictionary representing the current local symbol table.
Free variables are returned by locals() when it is called in function blocks, but not in class blocks

동적으로 변수 생성 시 사용하는 파이썬 내장함수.
현재 지역 변수들을 dictionary 형태로 return함. (전역 변수들을 dictonary 형태로 return하는 함수는 globals())
'''

# %%
# 특정 값을 요청하는 경우
# 팀 누적 기록 중 '도드람 2021-2022 V-리그' 시즌 부터의 기록 요청

param = 's_season'
key = '018'

def param_call(param, key):
    html_spec = requests.get(init_url, verify=False, params={param: key, 'part':'point'})
    
    if(html_spec.status_code == 200):
        soup_spec = BeautifulSoup(html_spec.content, 'html.parser')
        html_spec.close()
    else:
        print("param_call Request ERROR ::: status code ::: " + str(html_spec.status_code))
        return

    return soup_spec.find('tbody')

tbody_spec = param_call(param, key)

# temp_data = []
# for i in range(1, 8):
#     row = tbody_spec.select_one('tr:nth-child(' + str(i) + ')')
#     temp_array = []
#     for j in range(1,len(cols)+1):
#         data = row.select_one('td:nth-child(' + str(j) + ')').get_text()
#         temp_array.append(data)
#     temp_data.append(temp_array) # loc를 지양하기 위해 부득이하게 수정

# df = pd.DataFrame(data=temp_data, columns=cols)
# df

# %%
# 모든 값을 요청하는 경우
# 위에서 추출한 파라미터 정보 이용

for name in param_names:
    for dict_key in locals()[str(name) + '_dict'].keys(): # dict_key = 's_season'
        print("param_name :::: " + name + " && key :::: " + dict_key)
        tbody_all = param_call(name, dict_key)

        # temp_data = []
        # for i in range(1, 8):
        #     row = tbody_all.select_one('tr:nth-child(' + str(i) + ')')
        #     temp_array = []
        #     for j in range(1,len(cols)+1):
        #         data = row.select_one('td:nth-child(' + str(j) + ')').get_text()
        #         temp_array.append(data)
        #     temp_data.append(temp_array) # loc를 지양하기 위해 부득이하게 수정

        # df = pd.DataFrame(data=temp_data, columns=cols)
        # print(df)
