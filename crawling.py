# %%
# 라이브러리 import
from bs4 import BeautifulSoup
from numpy import nan as NA
import requests
import pandas as pd
import urllib3
import numpy as np
from log import logger

urllib3.disable_warnings()

init_url = 'https://www.kovo.co.kr/stats/42001_team-totalrecord.asp'

html = requests.get(init_url, verify=False)

if(html.status_code == 200):
    soup = BeautifulSoup(html.content, 'html.parser')
    html.close()
else:
    # logger.info('STATUS CODE is ' + + str(html.status_code))
    logger.error()

# %%
# 파라미터 데이터 추출
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
# 파라미터 요청 전 예외처리
# ( s_season, s_pr , e_season, e_pr )
# 1. s_pr == null 이면 s_pr = '201|1'로 지정. e_pr == null 이면 e_pr = '203|1'
# 2. s_season == null 이면 s_season = '001'로 지정. e_season == null 이면 e_season = '018'    
# 3. s_season <= e_season
# 4. s_season == e_season이면 s_pr <= e_pr

def param_validate(paramdict):
    ssk = paramdict['s_season'] if paramdict.get('s_season') != None else '001'
    spk = paramdict['s_pr'] if paramdict.get('s_pr') != None else '201|1'
    esk = paramdict['e_season'] if paramdict.get('e_season') != None else '018'
    epk = paramdict['e_pr'] if paramdict.get('e_pr') != None else '203|1'
    partk = paramdict['part'] if paramdict.get('part') != None else 'point' # 카테고리

    if(int(ssk) >  int(esk)):
        print("올바른 기간을 입력하세요.")
        return
    if(int(ssk) ==  int(esk) & 
        ( int(spk.split("|")[0]) > int(epk.split("|")[0]) | 
        ( int(spk.split("|")[0]) == int(epk.split("|")[0]) & int(spk.split("|")[1]) > int(epk.split("|")[1])))):
        print("올바른 기간을 입력하세요.")
        return

    return {'s_seaon': ssk, 's_pr' : spk, 'e_season': esk, 'e_pr': epk, 'part': partk}

# %%
# 특정 값을 요청하는 경우
# 팀 누적 기록 중 '도드람 2021-2022 V-리그' 시즌 부터의 기록 요청

def param_call(paramdict):
    params = param_validate(paramdict) # 파라미터 요청 전 예외처리
    html_spec = requests.get(init_url, verify=False, params=params)
    
    if(html_spec.status_code == 200):
        soup_spec = BeautifulSoup(html_spec.content, 'html.parser')
        html_spec.close()

        tbody_spec = soup_spec.find('tbody') # tbody
        rowIndex = len(tbody_spec.find_all('td', attrs={'class':'name'})) # row 개수

        cols = []
        for col in soup_spec.select('thead > tr > th'): # col 개수
            cols.append(col.get_text())

        temp_data = []
        for i in range(1, rowIndex + 1):
            row = tbody_spec.select_one('tr:nth-child(' + str(i) + ')')
            temp_array = []
            for j in range(1,len(cols)+1):
                data = row.select_one('td:nth-child(' + str(j) + ')').get_text()
                temp_array.append(data)
            temp_data.append(temp_array) # loc를 지양하기 위해 부득이하게 수정            

    else:
        # logger.info('params is ' + str(params))
        # logger.info('STATUS CODE is ' + + str(html_spec.status_code))
        logger.error('', stack_info=True)        
        return

    return {'data': temp_data, 'cols' : cols}


# %%
param_dict = {'s_season':'018', 'part':'at'}

table_data_dict = param_call(param_dict)

df = pd.DataFrame(data=table_data_dict['data'], columns=table_data_dict['cols'])
df

# %%
# 모든 값을 요청하는 경우
# 위에서 추출한 파라미터 정보 이용
# 위의 특정값 요청하는 경우에서 사용한 함수 동일사용

for name in param_names:
    for dict_key in locals()[str(name) + '_dict'].keys(): # dict_key = 's_season'
        print("param_name :::: " + name + " && key :::: " + dict_key)
        
        table_data_dict = param_call({name:dict_key})

        df = pd.DataFrame(data=table_data_dict['data'], columns=table_data_dict['cols'])
        df


# %%
# 현재 코드 문제점
# 1. 예외 발생 시 로깅 필요
# 2. 시즌마다 round에서 없는 값이 있음 -> 에러 발생
#    사이트에선 goRound() 함수를 사용해 시즌 선택 시 라운드 콤보의 값을 받아오도록 되어있음
# 3. round 준플레이오프 < 플레이오프 < 챔피언결정전 순이어야함. param_validate 예외처리에서 수정 필요


