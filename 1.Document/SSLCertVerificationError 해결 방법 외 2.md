## 1. SSLCertVerificationError 해결 방법
* 사이트 중 https로 시작하는 url로 requests 로 요청 시 SSLCertVerificationError 에러가 날 수 있다. __SSL 인증__ 이 필요한 페이지이기 때문이다.
  * HTTPS(Hypertext Transfer Protocol Secure): SSL을 사용하는 HTTP 프로토콜의 보안 버전
  * SSL(Secure Sockedts Layer): 클라이언트와 서버간의 통신을 제3자가 보증해주는 전자화된 문서
* 해결방법: requests 요청을 보낼 때, __verify=False__ 라는 옵션을 추가한다. 단, 모든 상황에서 해결되는 것은 아니다.


  ```
  import requests

  url = 'https://www.kovo.co.kr/stats/42001_team-totalrecord.asp'  # KOVO 한국배구연맹 사이트

  html = requests.get(url, verify=False)
  ```
  



## 2. vscode에서 jupyter notebook 구동 방법
1. Python extension 설치
   vscode에서 jupyter notebook를 사용하려면, 우선적으로 Python extension이 설치되어야 한다.  
   이는 Microsoft에서 배포하며, 이를 설치하면 자동적으로 Jupyter extension이 설치된다.
   
   
   `The Python extension will automatically install the Pylance and Jupyter extensions to give you the best experience when working with Python files and Jupyter notebooks.`
2. jupyter notebook 파일 생성
   `Ctrl+Shift+P` 단축기를 이용하여, Command Palette를 실행한 후, jupyter notebook 파일을 생성한다.  
   (파일 형식: *.ipynb)
   
   
   ![image](https://user-images.githubusercontent.com/106735612/177044051-5e1f0c1d-28e6-4cf5-a9ce-b6210cf38047.png)
3. Python file(\*.py)로 Export  
   Export 클릭 > Command Palette에서 Python Script를 선택한다.
   
   
   ![image](https://user-images.githubusercontent.com/106735612/177044965-24fa1e32-494b-41f4-9156-350d63e24c23.png)

***
* 자주 쓰는 단축키 정리
   * `Esc`: 셀 edit 모드 -> command 모드 변환
   * `Ctrl+Enter`: 선택한 셀 run
   * `A` / `B`: 선택한 셀 바로 위 셀/ 아래 셀 추가
   * `Del`: 선택한 셀 삭제
   * `Ctrl+A`: 전체 셀 선택

* 디버깅
   1. 아래와 같이 혹은 `Ctrl+Alt+Shift+Enter' 단축키를 이용하여 디버깅을 할 수 있다.  
      ![image](https://user-images.githubusercontent.com/106735612/177044468-348dc50a-b3ae-47c6-8c5b-478f097657ff.png)

   2. 아래와 같이 중단점도 걸 수 있다.  
      ![image](https://user-images.githubusercontent.com/106735612/177044649-3d63c484-e74a-4f3c-be08-7f9ed71c28d6.png)

   3. 디버깅 단축키는 웹 F12 개발자도구에서의 단축키와 비슷하다.
      * `F5`: 다음 중단점까지 실행
      * `F10`: 단위 실행
* Plot 생성
   ```
   import numpy as np
   import pandas as pd
   import matplotlib.pyplot as plt

   x = [21, 22, 23,4,5,6,77,8,9,10,31,32,33,34,35,36,37,18,49,50,100]
   num_bins = 5
   plt.hist(x, num_bins)
   plt.show()
   ```
   ![image](https://user-images.githubusercontent.com/106735612/177044804-48c60761-5a92-4b9a-9363-8f6e7a50c631.png)

 

* 참고 사이트: https://code.visualstudio.com/docs/datascience/jupyter-notebooks<br><br>
  



## 3. BeautifulSoup, Pandas 라이브러리 이용한 HTML 크롤링 실전예제
### 도드람 2021-2022 V-리그 남자부 전체 득점 기록 크롤링하기
1. 필요 라이브러리 import하기
    
    
    ```
    from bs4 import BeautifulSoup
    import requests
    import pandas as pd
    ```
  

2. requests 라이브러리로 HTML 데이터 요청하여 갖고 오기


    ```
    url = 'https://www.kovo.co.kr/stats/42001_team-totalrecord.asp'

    html = requests.get(url, verify=False) # Making a put request
    print(html.status_code) # 상태 코드 200: 성공 응답
    ```


3. BeautifulSoup 라이브러리로 파싱하기
    ```
    soup = BeautifulSoup(html.content, 'html.parser')
    html.close() # closing the connection
    
    print(soup)
    ```
    참고로 위 코드의 출력값에는 다음과 같은 문구가 표시된다. _Text Line Limit 1000 을 초과했기 때문이다._
    
    `Output exceeds the size limit. Open the full output data in a text editor`  
    
    
4. 필요한 데이터 추출하기
    1. column 정보: column 정보가 thead > tr > th 태그에 속해있다. 또한 scope 속성값이 __"col"__ 이라는 공통점을 가지고 있다.
        
        
        
        ![image](https://user-images.githubusercontent.com/106735612/177041103-7f41c506-0028-49e1-8750-23ad554774ab.png)
          
          
        col_list에 컬럼 정보를 넣어준다.
        ```
        col_list = [] # 테이블 columns
        col_data = soup.findAll("th", scope="col")

        for item in col_data:
        col_list.append(item.text) # 컬럼명 # ['순위', '팀', '경기수', '세트수', '공격', '블로킹', '서브', '득점']
        ```
    ***
    2. row 정보: row 정보가 table > tbody > tr > td 태그에 속해있다.
        
        
        
        ![image](https://user-images.githubusercontent.com/106735612/177041477-e00fd81d-a796-4b3c-9009-ab1206617038.png)
          
          
        필요한 row_data를 추출한다.
        ```
        row_data = soup.select("table > tbody > tr > td") # table rows
        
        print(row_data)
        ```
        `[<td>1</td>, <td class="name">KB손해보험</td>, <td>40</td>, <td>161</td>, <td>2132</td>, <td>305</td>, <td>253</td>, <td>3702</td>, <td>2</td>, <td class="name">대한항공</td>, <td>39</td>, <td>155</td>, <td>2004</td>, <td>331</td>, <td>231</td>, <td>3551</td>, <td>3</td>, <td class="name">한국전력</td>, <td>38</td>, <td>150</td>, <td>1774</td>, <td>388</td>, <td>164</td>, <td>3307</td>, <td>4</td>, <td class="name">우리카드</td>, <td>37</td>, <td>147</td>, <td>1793</td>, <td>359</td>, <td>179</td>, <td>3279</td>, <td>5</td>, <td class="name">OK금융그룹</td>, <td>36</td>, <td>142</td>, <td>1758</td>, <td>286</td>, <td>193</td>, <td>3133</td>, <td>6</td>, <td class="name">현대캐피탈</td>, <td>36</td>, <td>142</td>, <td>1810</td>, <td>324</td>, <td>111</td>, <td>3085</td>, <td>7</td>, <td class="name">삼성화재</td>, <td>36</td>, <td>141</td>, <td>1656</td>, <td>256</td>, <td>209</td>, <td>2982</td>]`
        
        
        column 정보와 마찬가지로, dataset에 row_data를 넣어준다.
        ```
        dataset = []

        for idx, item in enumerate(row_data):
        num = idx/8
        row_idx = idx//8
        if(num == row_idx):
            dataset.append([])

        dataset[row_idx].append(item.text)
        
        print(dataset)
        ```
        `[['1', 'KB손해보험', '40', '161', '2132', '305', '253', '3702'], ['2', '대한항공', '39', '155', '2004', '331', '231', '3551'], ['3', '한국전력', '38', '150', '1774', '388', '164', '3307'], ['4', '우리카드', '37', '147', '1793', '359', '179', '3279'], ['5', 'OK금융그룹', '36', '142', '1758', '286', '193', '3133'], ['6', '현대캐피탈', '36', '142', '1810', '324', '111', '3085'], ['7', '삼성화재', '36', '141', '1656', '256', '209', '2982']]`
        
  

5. pandas 라이브러리로 DataFrame 생성하기
    ```
    df = pd.DataFrame(dataset, columns=col_list)
    df
    ```
    
    ![image](https://user-images.githubusercontent.com/106735612/177042026-bc2d1a31-d8ae-45d1-b242-5c981eb0ed02.png)


6. 전체 코드
    ```
    # 1. 필요 라이브러리 import하기
    from bs4 import BeautifulSoup
    import requests
    import pandas as pd
    
    # 2. requests 라이브러리로 HTML 데이터 요청하여 갖고 오기
    url = 'https://www.kovo.co.kr/stats/42001_team-totalrecord.asp'

    html = requests.get(url, verify=False)

    # 3. BeautifulSoup 라이브러리로 파싱하기
    soup = BeautifulSoup(html.content, 'html.parser')
    html.close()

    # 4.1. 필요한 데이터 추출하기: column 정보
    col_list = [] # 테이블 columns
    col_data = soup.findAll("th", scope="col")

    for item in col_data:
        col_list.append(item.text) # 컬럼명 # ['순위', '팀', '경기수', '세트수', '공격', '블로킹', '서브', '득점']

    # 4.2. 필요한 데이터 추출하기: row 정보
    row_data = soup.select("table > tbody > tr > td") # table rows

    dataset = []

    for idx, item in enumerate(row_data):
        num = idx/8
        row_idx = idx//8
        if(num == row_idx):
            dataset.append([])

        dataset[row_idx].append(item.text)

    # 5. pandas 라이브러리로 DataFrame 생성하기
    df = pd.DataFrame(dataset, columns=col_list)
    df
    ```
