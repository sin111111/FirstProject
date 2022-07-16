# %%
import pandas as pd
import numpy as np

# %%
# Pandas DataFrame 살펴보기
# 참고 문서: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html

# 1. 기본 개념 잡기
## pandas.DataFrame(data, index, columns, dtype, copy)
## 2차원 행렬. Series 객체를 위한 dict 컨테이너라고 볼 수 있음.
## 매개변수 설명
## * data: ndarray, Itertable(list, tuple 등), dict, DataFrame
## * index: RangeIndex가 default
## * columns: column 명 리스트
## * dtype: 지정하고 싶은 데이터 타입
## * copy: true일 경우 Pandas 객체 복사. deep copy(원본과 사본과 별개)와 shallow copy(원본 수정시 사본의 데이터도 수정) 기능 지원

# %%
# 2. 생성 예제
## dictonary
d = {'col1': [1,2], 'col2': [3,4]} # dtype: int64
df = pd.DataFrame(data=d)
df

# %%
## Series
d1 = {'col1': [0,1,2,3], 'col2': pd.Series([2,3], index=[2,3])}
df1 = pd.DataFrame(data=d1, index=[0,1,2,3])
df1

# %%
## array1
df2 = pd.DataFrame(np.array([[1,2,3], [4,5,6], [7,8,9]]), columns=['a','b','c'])
df2

# %%
## array2
d3 = np.array([(1,2,3), (4,5,6), (7,8,9)], dtype=[("a", "i4"), ("b", "i4"), ("c", "i4")]) # *i4 = int32
df3 = pd.DataFrame(data=d3, columns=['c','a'])
df3

# %%
# 3. 실무적으로 사용하기
dataframe = pd.DataFrame(data={'A': [1,4,7], 'B': [2,5,8], 'C': [3,6,9]}, index=['가','나','다'])
print(dataframe)
print('######################')
## row 조회
print(dataframe.iloc[0])  # df.iloc[행 인덱스, 열 인덱스]
print(dataframe.loc['가'])   # df.loc[행 인덱싱 값, 열 인덱싱 값]
print('######################')
## column 조회
print(dataframe.loc[:, 'A'])
print(dataframe['A'])
print('######################')
## 특정 row, column 선택
print(dataframe.iloc[0][0])
print(dataframe.loc['가']['A'])


