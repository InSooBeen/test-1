#!/usr/bin/env python
# coding: utf-8

# In[153]:


import numpy as np
import pandas as pd

file_path="ratings.dat"
data=pd.read_csv(file_path, sep="::", engine='python', names=['UserID', 'MovieID', 'Rating', 'Timestamp'])
data


# In[154]:


data_matrix=pd.pivot_table(data, index='UserID', columns='MovieID', values='Rating')
movie=np.arange(1, 3953)
data_matrix=data_matrix.reindex(columns=movie)
data_matrix.fillna(0, inplace=True)
data_matrix


# In[155]:


from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

#데이터 정규화 하기
scaler=StandardScaler()
scaled_data_matrix=scaler.fit_transform(data_matrix)
#군집 3개, 초기화시도 횟수 10, random_state를 42로 설정해서 항상 동일한 결과 얻기
kMeans=KMeans(n_clusters=3, n_init=10, random_state=42)  
#학습
kMeans.fit(scaled_data_matrix)
#kmean 결과를 data_matrix 끝에 추가
data_matrix['user_group']= kMeans.labels_ 
data_matrix


# In[156]:


group1 = data_matrix[data_matrix['user_group']==0]
group2 = data_matrix[data_matrix['user_group']==1]
group3 = data_matrix[data_matrix['user_group']==2]

group1
group2
group3


# In[157]:


#각 그룹별로 movieId에 대한 모든 유저의 평점 더하기(추가했던 user_group 열은 빼고 계산)
group1_sum = group1.drop(columns='user_group').sum()
group2_sum = group2.drop(columns='user_group').sum()
group3_sum = group3.drop(columns='user_group').sum()

group1_sum


# In[158]:


group1_AU =pd.DataFrame(group1_sum, columns=["AU"]).transpose()
group2_AU =pd.DataFrame(group2_sum, columns=["AU"]).transpose()
group3_AU =pd.DataFrame(group3_sum, columns=["AU"]).transpose()

group1_AU


# In[159]:


#각 그룹별 평균
group1_mean = group1.drop(columns='user_group').mean()
group2_mean = group2.drop(columns='user_group').mean()
group3_mean = group3.drop(columns='user_group').mean()

group1_mean


# In[160]:


group1_Avg =pd.DataFrame(group1_mean, columns=["Avg"]).transpose()
group2_Avg =pd.DataFrame(group2_mean, columns=["Avg"]).transpose()
group3_Avg =pd.DataFrame(group3_mean, columns=["Avg"]).transpose()

group1_Avg


# In[161]:


group1_total = pd.concat([group1_AU, group1_Avg])
group2_total = pd.concat([group2_AU, group2_Avg])
group3_total = pd.concat([group3_AU, group3_Avg])


# In[162]:


group1_total
group2_total
group3_total


# In[163]:


group1_cnt = group1.drop(columns='user_group').apply(lambda x: x[x != 0].count())
group2_cnt = group2.drop(columns='user_group').apply(lambda x: x[x != 0].count())
group3_cnt = group3.drop(columns="user_group").apply(lambda x: x[x!=0].count())

group1_cnt
group2_cnt
group3_cnt


# In[164]:


group1_SC =pd.DataFrame(group1_cnt, columns=["SC"]).transpose()
group2_SC =pd.DataFrame(group2_cnt, columns=["SC"]).transpose()
group3_SC =pd.DataFrame(group3_cnt, columns=["SC"]).transpose()

group1_SC
group2_SC
group3_SC


# In[165]:



group1_total = pd.concat([group1_total, group1_SC])
group2_total = pd.concat([group2_total, group2_SC])
group3_total = pd.concat([group3_total, group3_SC])


# In[166]:


group1_total
group2_total
group3_total


# In[167]:


#그룹별로 SC구하기
group1_av = group1.drop(columns='user_group').apply(lambda x: x[x > 4].sum())
group2_av = group2.drop(columns='user_group').apply(lambda x: x[x > 4].sum())
group3_av = group3.drop(columns="user_group").apply(lambda x: x[x > 4].sum())

group1_av


# In[168]:


group1_AV =pd.DataFrame(group1_av, columns=["AV"]).transpose()
group2_AV =pd.DataFrame(group2_av, columns=["AV"]).transpose()
group3_AV =pd.DataFrame(group3_av, columns=["AV"]).transpose()


# In[169]:


group1_AV
group2_AV
group3_AV


# In[170]:


group1_total = pd.concat([group1_total, group1_AV])
group2_total = pd.concat([group2_total, group2_AV])
group3_total = pd.concat([group3_total, group3_AV])


# In[171]:


group1_total
group2_total
group3_total


# In[172]:


#그룹별 사용자마다 rank계산 (처음에 0을 NaN으로 채워서 rank에 영향을 줄 수 있으므로 
#다시 NaN으로 바꾼 뒤에 rank를 계산하고 NaN에 0을 채운다)
group1_nan = group1.drop(columns="user_group").replace(0, np.nan)
group2_nan = group2.drop(columns="user_group").replace(0, np.nan)
group3_nan = group3.drop(columns="user_group").replace(0, np.nan) 

group1_rank = group1_nan.rank(axis=1, method='average')-1
group2_rank = group2_nan.rank(axis=1, method='average')-1
group3_rank = group3_nan.rank(axis=1, method='average')-1

group1_rank = group1_rank.fillna(0)
group2_rank = group2_rank.fillna(0)
group3_rank = group3_rank.fillna(0)

group1_rank
group2_rank
group3_rank


# In[173]:


#BC 구하기
group1_bc =group1_rank.sum()
group2_bc =group2_rank.sum()
group3_bc =group3_rank.sum()

group1_BC =pd.DataFrame(group1_bc, columns=["BC"]).transpose()
group2_BC =pd.DataFrame(group2_bc, columns=["BC"]).transpose()
group3_BC =pd.DataFrame(group3_bc, columns=["BC"]).transpose()

group1_BC


# In[174]:


group1_total = pd.concat([group1_total, group1_BC])
group2_total = pd.concat([group2_total, group2_BC])
group3_total = pd.concat([group3_total, group3_BC])


# In[177]:


group1_total
group2_total
group3_total


# In[179]:


group1


# In[271]:


# user_group을 제외한 데이터만 추출
group1_set = group1.drop(columns= 'user_group')
group1_set = group1_set.to_numpy()
group1_cr = np.zeros((3952,3952))

group2_set = group2.drop(columns='user_group')
group2_set=group2_set.to_numpy()
group2_cr = np.zeros((3952, 3952))

group3_set = group3.drop(columns='user_group')
group3_set=group3_set.to_numpy()
group3_cr = np.zeros((3952, 3952))

for i in range(3952):
    g1 = (group1_set[:,i].reshape(-1,1) - group1_set).transpose()
    group1_cr[:,i] = np.where(np.sum(np.sign(g1)) >0,1,-1)
    group1_cr[i,i]=0
    
    g2 = (group2_set[:,i].reshape(-1,1) - group2_set).transpose()
    group2_cr[:,i] = np.where(np.sum(np.sign(g2))>0,1,-1)
    group2_cr[i,i]=0
   
    g3 = (group3_set[:,i].reshape(-1,1) - group3_set).transpose()
    group3_cr[:,i] = np.where(np.sum(np.sign(g3))>0,1,-1)
    group3_cr[i,i]=0


# In[327]:


group1_CR = group1_cr.sum(axis=1)
group2_CR = group2_cr.sum(axis=1)
group3_CR = group3_cr.sum(axis=1)


# In[331]:


group1_CR_ =pd.DataFrame(group1_CR, columns=["CR"]).transpose()
group2_CR_ =pd.DataFrame(group2_CR, columns=["CR"]).transpose()
group3_CR_ =pd.DataFrame(group3_CR, columns=["CR"]).transpose()

group1_CR_.columns = group1_total.columns
group2_CR_.columns = group2_total.columns
group3_CR_.columns = group3_total.columns


# In[332]:


group1_total_ = pd.concat([group1_total, group1_CR_])
group2_total_ = pd.concat([group2_total, group2_CR_])
group3_total_ = pd.concat([group3_total, group3_CR_])


# In[336]:


group1_total_
group2_total_
group3_total_

