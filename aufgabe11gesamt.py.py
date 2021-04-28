#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

from statistics import mean


df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")

print(df[['new_cases','location']])

list = df['new_cases']

list.replace('', np.NaN, inplace=True)
list.dropna(axis=0, inplace=True) 

print(sum(list)/len(list))
print(mean(list))
print(np.std(list))
print(np.var(list))
print(np.median(list))
print(np.max(list))


# In[26]:


import pandas as pd
import numpy as np

from statistics import mean


df = pd.read_csv("C:\\Users\\Sarah\Documents\\Studium\\DGUI\\owid-covid-data.csv")
df.replace('', 0, inplace=True)
df.replace(np.NaN, 0, inplace=True)

df.groupby(['location']).mean('new_cases').sort_values(by='new_cases', ascending=False)


# In[ ]:





# In[ ]:




