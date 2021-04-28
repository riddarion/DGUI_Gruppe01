#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import plotly.express as px


df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
df.replace('', "nicht zugeordnet", inplace=True)
df.replace(np.NaN, "nicht zugeordnet", inplace=True) 

fig = px.scatter_matrix(df,
    dimensions=["total_cases", "hosp_patients", "new_cases", "new_vaccinations"],
    color='continent')

fig.show()

