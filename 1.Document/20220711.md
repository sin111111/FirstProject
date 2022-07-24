# 1. Selector와 Xpath를 이용하여 데이터 추출하기

## 전제조건 정리
1. 현 예제의 테이블 컬럼 개수를 동일하게 필요한 데이터는 득점 부문만 가져온다.
2. 1에 의해서 컬럼 리스트는 다음과 같다. ['순위', '선수', '팀', '경기수', '세트수', '시도', '성공', '공격차단', '범실', '성공률']
3. 1과 동일하게 row 최대 개수도 동일하게 하기 위해 최대 TOP 5 선수의 기록만 가져온다.
4. Selector는 BeautifulSoup, Xpath는 Selenium 라이브러리를 이용한다.

```
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
import selenium
import pandas

url = 'https://www.kovo.co.kr/game/v-league/11302_player-ranking_view.asp?season=018&g_part=201&r_round=0&s_part=1&r_part=at&'
cols = ['순위', '선수', '팀', '경기수', '세트수', '시도', '성공', '공격차단', '범실', '성공률']
row_index = 5
```
    
## 1.1. Selector
해당 tbody 내에 있는 <tr>태그 중 하나를 골라 selector 복사한다.
    
`tab1_1 > div > table > tbody > tr:nth-child(1) :1위 선수`
    
위에서 선택한 <tr>태그 안의 <td> 태그 중 하나를 골라 동일하게 selector 복사를 아래와 같은 결과가 나온다.
    
`tab1_2 > div > table > tbody > tr:nth-child(1) > td:nth-child(1)`
    
정리한 코드와 그 Output은 아래와 같다.
```
html = requests.get(url, verify=False)

if(html.status_code == 200):
    soup = BeautifulSoup(html.content, 'html.parser')
    html.close()

tbody = soup.find('tbody') # 해당 tbody

temp_data1 = []
for i in range(1,row_index +1): # Top 5명
    row = tbody.select_one('tr:nth-child(' + str(i) + ')') # tr 태그
    temp_row = []
    for j in range(1,len(cols)+1): # column 개수 10개
        data = row.select_one('td:nth-child(' + str(j) + ')').get_text() # td 태그
        temp_row.append(data)
    temp_data1.append(temp_row)


df = pd.DataFrame(temp_data1, columns=cols) # column Index만 있는 빈 DataFrame
df
```
    
![image](https://user-images.githubusercontent.com/106735612/180634482-5023b1a6-555a-4313-9496-39e73280b147.png)


## 1.2. Xpath
    
해당 tbody 내에 있는 <tr>태그 중 하나를 골라 XPath 복사를 한다.
`//*[@id="tab1_1"]/div/table/tbody/tr[1] : 1위 선수`

Selenium 라이브러리를 사용하기 위해서는, 자신이 사용하는 브라우저의 driver 설치가 필요하다.
* 참고 : https://dhznsdl.tistory.com/21
```
driver = webdriver.Chrome('./chromedriver.exe')
driver.get(url)
driver.implicitly_wait(time_to_wait=5)
```    

정리한 코드와 그 Output은 아래와 같다.
```
temp_data2 = []

xpath = '//*[@id="tab1_2"]/div/table/tbody/tr[1]'

for i in range(1,row_index +1): # Top 5명
    rowxpath = '//*[@id="tab1_2"]/div/table/tbody/tr[' + str(i) + ']'
    row = driver.find_elements("xpath", rowxpath)[0].text
    temp_row = row.split() # row에서 split만 해주면 된다.
    temp_data2.append(temp_row)


driver.quit()

df = pd.DataFrame(temp_data2, columns=cols) # column Index만 있는 빈 DataFrame
df
```
    
![image](https://user-images.githubusercontent.com/106735612/180634601-45c97474-11b9-488e-bc56-290131003a51.png)
    
__1.1 예제와 1.2 예제의 Output이 동일함을 알 수 있다.__


# 2. 코드 리팩토링 후 함수화해야할 코드를 알아보고, 그 근거 작성하기

```
for i in range(1, 8):
    row = tbody.select_one('tr:nth-child(' + str(i) + ')')
    temp_array = []
    for j in range(1,9):
        data = row.select_one('td:nth-child(' + str(j) + ')').get_text()
        temp_array.append(data)
    temp_data.append(temp_array) # loc를 지양하기 위해 부득이하게 수정
```

1. 프로젝트 방향성  
   해당 프로젝트는 상용화 목표/데이터 분석 두 가지의 방향 중 하나로 가게된다. 
   두 목표 모두 어떤 데이터를 가지고 진행하냐가 중요한데, 이에 공통점은 해당 Url 파라미터를 어떻게 던지느냐에 따라 다르다.
   해당 사이트는 비슷한 테이블 구조를 가지고 있으나, 두 가지의 차이점을 지니고 있다.
      * len(columns)의 차이: 성공률이 중요한 공격 부문, 기타 서브, 블로킹, 리시브 부문, 그리고 이 전체를 아우르는 득점 부문 별로 컬럼 개수에 차이가 있다. 
      * rowIndex의 차이: 남자부는 2013년 러시앤캐시(현 OK금융그룹) 창단 이후로 7개구단, 여자부는 2021년 페퍼저축은행 창단 이후로 7개구단으로 운영중이다.
2. 해당 사이트의 HTML 테이블 태그 공통점  
   해당 프로젝트는 __KOVO 한국배구연맹__ 에서 제공하는 데이터를 수집하고 있다. 그 HTML을 살펴보면 팀 누적 기록, 선수 누적 기록, 톱랭킹 등의 테이블 모두 비슷한 selector 구조를 지니고 있음을 알수 있다.
      * #tab1 > div.wrp_lst > table > tbody > tr:nth-child(1) > td:nth-child(5)


  따라서 데이터 수집에 있어 중요 변수인 기록 카테고리, 시즌 년도 별로 각 __column,row 개수__ 만 변수로 지정해 준다면, 이 코드를 함수화하여 지속적으로 사용할 수 있다.
  


# 3. 파라미터를 dictionary 자료형 응용하여 정리하기
* 해당 예제 url: 'https://www.kovo.co.kr/stats/42001_team-totalrecord.asp'

    ## 3.1. 파라미터의 정보를 얻고, 그 변수명을 List로 정리하기
    우선 이 예제에서 request 요청 시 보내는 모든 파라미터의 정보를 얻으려면, 해당 페이지의 `기록보기` 버튼을 클릭한다.  
    그럼 아래와 같은 새로운 url을 얻을 수 있다.
    
    ![image](https://user-images.githubusercontent.com/106735612/180022347-f54cb985-bfe6-4e86-9660-0ff3a1a82109.png)
    
    해당 페이지 request 요청 시, 파라미터는 s_part, spart, s_season, s_pr, e_season, e_pr, part 총 7개이다.  
    우리는 이 중 남자부,여자부를 구분하는 `s_part`와 null값을 보내는 `spart`를 제외할 것이다.  
    그러면 5개가 남는데, 이는 select 태그를 이용해서 사용자가 값을 선택할 수 있는 파라미터이다.  
    ```
    param_names = ['s_season', 's_pr', 'e_season', 'e_pr', 'part']
    ```
    
    
    ## 3.2. 변수명에 따라 해당 변수 데이터 추출하기
    지금까지 해온 예제들은 모두 tbody 안의 태그들을 이용해 추출해왔지만, 이 예제는 다르다.  
    아래의 캡처를 보면, 모두 combobox 형태를 지니고 있다.  
    ![image](https://user-images.githubusercontent.com/106735612/180023985-93361c27-abb7-4e40-8fa0-b34b9363fb03.png)
    
    이들의 HTML 태그를 살펴보면, 모두 select 태그로 표현되며, 각 name의 속성이 3.1.에서 정리한 name과 동일함을 알 수 있다.
    ![image](https://user-images.githubusercontent.com/106735612/180025449-611fe6c9-1502-46e9-bab5-e2658f38f78d.png)  
    
    
    이를 통해, 아래의 코드와 같이 데이터를 추출할 수 있다.
    ```
    for name in param_names:
        selects = soup.find('select', {'name': name})
    ```
    
    
    ## 3.3. 각 파라미터 별 option들을 key, value로 dictionary 객체에 넣기
    우선, 각 파라미터 별로 option의 개수가 몇 개인지 알 수 없기 때문에, enumerate 내장함수를 사용한다.
    ```
    for name in param_names:
        selects = soup.find('select', {'name': name})
        for i, option in enumerate(selects):
            print(str(i)+ " ::: " + str(option))
    ```  
    ![image](https://user-images.githubusercontent.com/106735612/180027838-4ff0c4f7-87f0-4c95-91bf-6ca9924ae950.png)
    
    우리가 필요한 option 데이터는 홀수 index 일때만이므로, if문을 사용한다.
    ```
    if i % 2 != 0:
    ```
    
    
    또한, 다음과 같은 key, value로 정리한다.
          
        
    * `key`: option태그의 value 속성. split()을 이용해서 값을 가져온다. __str(option).split('value="')[1].split('">')[0]__
    * `value`: option태그의 innerHTML. __option.get_text()__

    ***
    지금까지의 코드 결과값은 아래와 같다.      
    ![image](https://user-images.githubusercontent.com/106735612/180029890-2e90dfa2-2011-4332-8d8b-701904f027d4.png)
    
    
    따라서 각 변수명별(name) key, value 정보를 dictionary 객체에 넣기 위해, 지금까지의 예제와 동일하게 temp성 객체를 생성하고, 이에 하나씩 update해준다.

    
    ## 3.4. 전체 코드    
    ```
    dict = {}
    for name in param_names:
        selects = soup.find('select', {'name': name})
        temp_dict = {}
        for i, option in enumerate(selects):
            if i % 2 != 0: # 이해 조금 어려움...
                option_value = str(option).split('value="')[1].split('">')[0]
                temp_dict.setdefault(option_value,option.get_text())

        dict.setdefault(name, temp_dict)
    ```
    * setdefault(key[, value]):
        * key가 딕셔너리에 존재하면, 해당 값을 돌려준다.
        * 그렇지 않으면, value 값을 갖는 key를 삽입한 후, value를 반환한다.
        * value의 default는 None이다.
        
     
    


    
