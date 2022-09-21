# %%
# 라이브러리 import
from sysconfig import get_scheme_names
from bs4 import BeautifulSoup
from numpy import nan as NA
import requests
import pandas as pd
import urllib3
import numpy as np
import traceback
from log import mylogger

urllib3.disable_warnings()

mylogger.info('================ crawling start ================')

init_url = 'https://www.kovo.co.kr/stats/42001_team-totalrecord.asp'

html = requests.get(init_url, verify=False)

if(html.status_code == 200):
    soup = BeautifulSoup(html.content, 'html.parser')
    html.close()
else:
    mylogger.error('====== request 중 오류 발생 =====')
    mylogger.error(traceback.format_exc())

# %%
# 파라미터 데이터 추출
param_names = ['s_season', 'e_season', 'part'] # 파라미터 이름

mylogger.info('====== locals()를 이용하여 파라미터 데이터 정리 ======')
for name in param_names:
    temp_dict = {}
    for option in soup.find('select', {'name' : name}).find_all('option'):
        key = option.attrs['value'] # '018'
        value = option.getText() # '도드람 2021-2022 V-리그'
        temp_dict[key] = value

    
    locals()[str(name)+ '_dict'] = temp_dict
    
# %%
# 라운드 파라미터 데이터 추출
# 시즌 콤보박스 valuechanged 시 시즌마다 변동되는 라운드 파라미터 추출 필요

def round_param_get(params):

    mylogger.info('====== def round_param_get INFO : ====== 라운드(s_pr/e_pr) 변수 데이터 추출 start')
    part_url = 'https://www.kovo.co.kr/stats/stats_r_round.asp'
    # params = {'spart':'s', 's_season':ssk, 'e_season':esk } 또는 {'spart':'e', 's_season':ssk, 'e_season':esk}

    html_part = requests.get(part_url, verify=False, params=params)

    if(html_part.status_code == 200):
        soup_part = BeautifulSoup(html_part.content, 'html.parser')
        html_part.close()

        temp_dict = {}
        for option in soup_part.find('select', {'name' : params['spart'] + '_pr'}).find_all('option'):
            key = option.attrs['value'] # '201|1'
            value = option.getText() # '1_Round'
            temp_dict[key] = value

        locals()[params['spart'] + '_pr'+ '_dict'] = temp_dict    
        mylogger.info('====== def round_param_get INFO : ====== 라운드(' + params['spart'] + '_pr)' +' 변수 데이터 추출 end')
        return locals()[params['spart'] + '_pr'+ '_dict']

    else:
        mylogger.info('====== def round_param_get INFO : ====== 라운드 변수 추출 중 서버 에러 발생')
        result = '=라운드 변수 추출 중 서버 ' + str(html_part.status_code) +' 에러' + '\n\n' + '관리자에게 문의하세요.'
        return result



# %%
# 파라미터 요청 전 예외처리

def param_validate(paramdict):
    try:
        mylogger.info('====== def param_validate start ======')
        mylogger.info('====== def param_validate INFO : ====== paramdict 누락 가능성 확인 start')

        if(paramdict.get('s_part') is None):
            mylogger.info('====== def param_validate INFO : ====== 사용자 남자부/여자부 필수 변수 없음')
            mylogger.info(paramdict)
            result = '= 사용자 남자부/여자부 필수 변수 없음' + '\n\n' + '부를 설정해주세요.'
            return result          


        elif(paramdict.get('s_season') is None or paramdict.get('e_season') is None):
            mylogger.info('====== def param_validate INFO : ====== 사용자 FROM TO 시즌 필수 변수 없음')
            mylogger.info(paramdict)
            result = '= 사용자 FROM TO 시즌 필수 변수 없음' + '\n\n' + '시즌을 모두 설정해주세요.'
            return result  


        elif(paramdict.get('s_pr') is None or paramdict.get('e_pr') is None):
            mylogger.info('====== def param_validate INFO : ====== 사용자 FROM TO 라운드 필수 변수 없음')
            mylogger.info(paramdict)
            result = '= 사용자 FROM TO 라운드 필수 변수 없음' + '\n\n' + '라운드를 모두 설정해주세요.'
            return result


        elif(paramdict.get('part') is None):
            mylogger.info('====== def param_validate INFO : ====== 사용자 카테고리 필수 변수 없음')
            mylogger.info(paramdict)
            result = '= 사용자 카테고리 필수 변수 없음' + '\n\n' + '기록을 확인할 카테고리를 설정해주세요.'
            return result              


        else:
            mylogger.info('====== def param_validate INFO : ====== paramdict 누락 가능성 확인 end')

            spartk = paramdict['s_part']
            ssk = paramdict['s_season']
            esk = paramdict['e_season']
            spk = paramdict['s_pr']
            epk = paramdict['e_pr']
            partk = paramdict['part']
            mylogger.info('====== def param_validate INFO : ====== paramdict => ' + ssk + ", " + spk + ", " + esk + ", " + epk + ", " + partk)            

            if(int(ssk) >  int(esk)):
                mylogger.info('====== def param_validate INFO : ====== 사용자 FROM TO 시즌 변수 설정 오류')
                mylogger.info(str(paramdict))
                result = '= 사용자 FROM TO 시즌 변수 설정 오류' + '\n\n' + '올바른 기간을 입력하세요.'
                return result


            mylogger.info('====== def param_validate INFO : ====== 라운드(s_pr/e_pr) 변수 데이터 추출 start')
            part_url = 'https://www.kovo.co.kr/stats/stats_r_round.asp'
            params_parts = [{'spart':'s', 's_season':ssk, 'e_season':esk },{'spart':'e', 's_season':ssk, 'e_season':esk}]

            for params in params_parts:
                html_part = requests.get(part_url, verify=False, params=params)

                if(html_part.status_code == 200):
                    soup_part = BeautifulSoup(html_part.content, 'html.parser')
                    html_part.close()

                    temp_dict = {}
                    for option in soup_part.find('select', {'name' : params['spart'] + '_pr'}).find_all('option'):
                        key = option.attrs['value'] # '201|1'
                        value = option.getText() # '1_Round'
                        temp_dict[key] = value

                    locals()[params['spart'] + '_pr'+ '_dict'] = temp_dict    
                    mylogger.info('====== def param_validate INFO : ====== 라운드(' + params['spart'] + '_pr)' +' 변수 데이터 추출 end')

                else:
                    mylogger.info('====== def param_validate INFO : ====== 라운드 변수 추출 중 서버 에러 발생')
                    result = '=라운드 변수 추출 중 서버 ' + str(html_part.status_code) +' 에러' + '\n\n' + '관리자에게 문의하세요.'
                    return result


            if (spk not in locals()['s_pr_dict']):
                mylogger.info('====== def param_validate INFO : ====== 사용자 FROM 라운드 변수 오류 발생')
                result = '= 사용자 FROM 라운드 변수 오류 발생' + '\n\n' + '해당 시즌에 ' + spk + '가 없습니다.'
                return result


            elif (epk not in locals()['e_pr_dict']):
                mylogger.info('====== def param_validate INFO : ====== 사용자 TO 라운드 변수 오류 발생')
                result = '= 사용자 TO 라운드 변수 오류 발생' + '\n\n' + '해당 시즌에 ' + epk + '가 없습니다.'
                return result


            else:
                if( int(spk.split("|")[0]) > int(epk.split("|")[0]) or 
                    ( int(spk.split("|")[0]) == int(epk.split("|")[0]) and int(spk.split("|")[1]) > int(epk.split("|")[1]))):
                    mylogger.info('====== def param_validate INFO : ====== 사용자 FROM TO 라운드 변수 설정 오류')
                    result = '= 사용자 FROM TO 라운드 변수 설정 오류' + '\n\n' + '올바른 기간을 입력하세요.'
                    return result


        return_paramdict = {'s_part': spartk, 's_season': ssk, 's_pr' : spk, 'e_season': esk, 'e_pr': epk, 'part': partk}
        mylogger.info('====== def param_validate INFO : ====== return_paramdict => ' + str(return_paramdict))
        mylogger.info('====== def param_validate end ======')
        return return_paramdict
    except:
        mylogger.error('====== def param_validate ERROR : ====== 변수 예외처리 중 오류 발생')
        mylogger.error(traceback.format_exc())
        result = '= 변수 예외처리 중 오류 발생' + '\n\n' + traceback.format_exc()
        return result


returndict = param_validate({'s_part': '1', 's_season':'018', 's_pr':'201|1', 'e_season':'018', 'e_pr':'201|1', 'part':'point'})

# %%
# 특정 값을 요청하는 경우
# 팀 누적 기록 중 '도드람 2021-2022 V-리그' 시즌 부터의 기록 요청

def param_call(params):
    try:
        mylogger.info('====== def param_call start ======')

        for key in ['s_part', 's_season', 's_pr', 'e_season', 'e_pr', 'part']:
            try:
                params[key]
            except:
                return params

        mylogger.info('====== def param_call INFO : ====== params => ' + str(params))
        html_spec = requests.get(init_url, verify=False, params=params)
        mylogger.info('====== def param_call INFO : ====== html_spec.status_code => ' + str(html_spec.status_code))
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

            mylogger.info('====== def param_call end ======')
            return {'data': temp_data, 'cols' : cols}


        elif(html_spec.status_code == 500):
            mylogger.info('====== def param_call INFO : ====== 서버 500 에러 발생')
            result = '= 서버 500 에러' + '\n\n' + '관리자에게 문의하세요.'
            return result                  
    except:
        mylogger.error('====== def param_call ERROR : ====== 변수 request 중 오류 발생')
        mylogger.error(traceback.format_exc())
        result = '= request 중 오류 발생' + '\n\n' + traceback.format_exc()
        return result



table = param_call(returndict)
print(table)