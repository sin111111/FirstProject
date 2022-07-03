# %%
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

url = 'https://www.kovo.co.kr/stats/42001_team-totalrecord.asp'

html = requests.get(url, verify=False)

# %%
soup = BeautifulSoup(html.content, 'html.parser')
html.close()

# %%
col_list = [] # 테이블 columns
col_data = soup.findAll("th", scope="col")

for item in col_data:
    col_list.append(item.text) # 컬럼명 # ['순위', '팀', '경기수', '세트수', '공격', '블로킹', '서브', '득점']

# %%
row_data = soup.select("table > tbody > tr > td") # table rows

dataset = []

for idx, item in enumerate(row_data):
    num = idx/8
    row_idx = idx//8
    if(num == row_idx):
        dataset.append([])
    
    dataset[row_idx].append(item.text)

print(dataset)

# %%
df = pd.DataFrame(dataset, columns=col_list)
df



# %%
