#!/usr/bin/env python
# coding: utf-8

# In[46]:


import pandas as pd
import numpy as np
import plotly.express as px

from statistics import mean


df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
df.replace('', 0, inplace=True)
df.replace(np.NaN, 0, inplace=True)

keep_col = ["continent", "location", "total_cases", "hosp_patients", "new_cases", "new_vaccinations"]
new_df = df[keep_col]

dfma = new_df.groupby(['location', 'continent'])   [['total_cases', 'new_cases', 'hosp_patients', 'new_vaccinations']].   mean()
print(dfma) 

dfma_f = dfma.reset_index() 


fig = px.scatter_matrix(dfma_f,
    dimensions=["total_cases", "hosp_patients", "new_cases", "new_vaccinations"],
                        color=dfma_f.location)

fig.show()


# In[ ]:




