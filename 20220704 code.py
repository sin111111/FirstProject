# %%
# %%
from bs4 import BeautifulSoup
import requests
import pandas as pd

# 파라미터 지정
def request_param(paramtype):
    key = 'part'
    param_dict = {
        '득점' : 'point',
        '공격' : 'at',
        '오픈공격' : 'oa',
        '시간차공격' : 'ta',
        '이동공격' : 'mad',
        '후위공격' : 'ba',
        '속공' : 'sa',
        '퀵오픈' : 'csa',
        '서브' : 's',
        '블로킹' : 'b',
        '디그' : 'd',
        '세트' : 'set',
        '리시브' : 'r',
        '벌칙' : 'w',
        '범실' : 'e',
        '팀범실' : 'te'
    }

    return { key : param_dict[paramtype] }


# 컬럼 정보 추출
def set_columns(soup):
    col_list = [] # 테이블 columns
    col_data = soup.findAll('th', scope='col')

    for item in col_data:
        col_list.append(item.text) # 컬럼명 # ['순위', '팀', '경기수', '세트수', '공격', '블로킹', '서브', '득점']

    return col_list



# 빈 데이터프레임 생성
def create_dataframe(col_list):
    null_data = {}
    data_frame = pd.DataFrame(null_data, columns=col_list)

    return data_frame


# tbody
def get_tbody(soup):
    tbody = soup.find('tbody')
    return tbody


# row num
def get_rownum(tbody):
    row_num = len(tbody.select('tr'))
    
    return row_num


# column count
def get_colmuns_count(col_list):
    columns_count = len(col_list)

    return columns_count


# 빈 데이터프레임에 데이터 넣기
def insert_data(df, tbody, row_num, columns_count):
    for i in range(1, row_num+1):
        row = tbody.select_one('tr:nth-child('+str(i)+')')
        temp_array = []
        for j in range(1, columns_count+1):
            temp_array.append(row.select_one('td:nth-child('+str(j)+')').get_text())
        df.loc[i-1] = temp_array

    return df


def preprocess_data():
    col_list = set_columns(soup)
    data_frame = create_dataframe(col_list)
    tbody = get_tbody(soup)
    row_num  = get_rownum(tbody)
    columns_count = get_colmuns_count(col_list)

    df = insert_data(data_frame, tbody, row_num, columns_count)
    return df



# %%
url = 'https://www.kovo.co.kr/stats/42001_team-totalrecord.asp'

dataparam = request_param('팀범실')
html = requests.get(url, verify=False, data=dataparam)

# %%
if(html.status_code == 200):
    soup = BeautifulSoup(html.content, 'html.parser')
    html.close()


# %%
df = preprocess_data()
df


