# %%
# 라이브러리 import
from bs4 import BeautifulSoup
from numpy import nan as NA
import requests
import pandas as pd
import urllib3
import numpy as np
from log import mylogger

urllib3.disable_warnings()


mylogger.info('================ crawling start ================')

init_url = 'https://www.kovo.co.kr/stats/42001_team-totalrecord.asp'

html = requests.get(init_url, verify=False)

if(html.status_code == 200):
    soup = BeautifulSoup(html.content, 'html.parser')
    html.close()
else:
    mylogger.error('===== request 중 오류 발생 =====')
    mylogger.error(traceback.format_exc())

# %%
# 파라미터 데이터 추출
param_names = ['s_season', 's_pr', 'e_season', 'e_pr', 'part'] # 파라미터 이름

for name in param_names:
    temp_dict = {}
    for option in soup.find('select', {'name' : name}).find_all('option'):
        key = option.attrs['value'] # '018'
        value = option.getText() # '도드람 2021-2022 V-리그'
        temp_dict[key] = value

    mylogger.info('===== locals()를 이용하여 파라미터 데이터 정리 ======')
    locals()[str(name)+ '_dict'] = temp_dict

# %%
# 파라미터 요청 전 예외처리
# ( s_season, s_pr , e_season, e_pr )
# 1. s_pr == null 이면 s_pr = '201|1'로 지정. e_pr == null 이면 e_pr = '203|1'
# 2. s_season == null 이면 s_season = '001'로 지정. e_season == null 이면 e_season = '018'    
# 3. s_season <= e_season
# 4. s_season == e_season이면 s_pr <= e_pr

def param_validate(paramdict):
    try:
        mylogger.info('===== def param_validate start ======')
        ssk = paramdict['s_season'] if paramdict.get('s_season') != None else '001'
        spk = paramdict['s_pr'] if paramdict.get('s_pr') != None else '201|1'
        esk = paramdict['e_season'] if paramdict.get('e_season') != None else '018'
        epk = paramdict['e_pr'] if paramdict.get('e_pr') != None else '203|1'
        partk = paramdict['part'] if paramdict.get('part') != None else 'point' # 카테고리

        if(int(ssk) >  int(esk)):
            mylogger.info('===== def param_validate INFO : ====== 사용자 FROM TO 시즌 변수 설정 오류')
            result = '= 사용자 FROM TO 시즌 변수 설정 오류' + '\n\n' + '올바른 기간을 입력하세요.'
            return result
        if(int(ssk) ==  int(esk) & 
            ( int(spk.split("|")[0]) > int(epk.split("|")[0]) | 
            ( int(spk.split("|")[0]) == int(epk.split("|")[0]) & int(spk.split("|")[1]) > int(epk.split("|")[1])))):
            mylogger.info('===== def param_validate INFO : ====== 사용자 FROM TO 라운드 변수 설정 오류')
            result = '= 사용자 FROM TO 시즌 라운드 설정 오류' + '\n\n' + '올바른 기간을 입력하세요.'
            return result

        mylogger.info('===== def param_validate end ======')
        return {'s_seaon': ssk, 's_pr' : spk, 'e_season': esk, 'e_pr': epk, 'part': partk}
    except:
        mylogger.error('===== def param_validate ERROR : ====== 변수 예외처리 중 오류 발생')
        mylogger.error(traceback.format_exc())
        result = '= 변수 예외처리 중 오류 발생' + '\n\n' + traceback.format_exc()
        return result
# %%
# 특정 값을 요청하는 경우
# 팀 누적 기록 중 '도드람 2021-2022 V-리그' 시즌 부터의 기록 요청

def param_call(paramdict):
    try:
        mylogger.info('===== def param_call start ======')
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

            mylogger.info('===== def param_call end ======')
            return {'data': temp_data, 'cols' : cols}

 
        elif(html_spec.status_code == 500):
            mylogger.info('===== def param_call INFO : ====== 서버 500 에러 발생')
            result = '= 서버 500 에러' + '\n\n' + '관리자에게 문의하세요.'
            return result                  
    except:
        mylogger.error('===== def param_call ERROR : ====== 변수 request 중 오류 발생')
        mylogger.error(traceback.format_exc())
        result = '= request 중 오류 발생' + '\n\n' + traceback.format_exc()
        return result




mylogger.debug('log test start')
table = param_call({})
mylogger.debug('log test end')


mylogger.info('================ crawling end ================')