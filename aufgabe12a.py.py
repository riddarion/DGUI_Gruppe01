#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go


df = pd.read_csv("C:\\Users\\Sarah\Documents\\Studium\\DGUI\\owid-covid-data.csv")
df.replace('', "nicht zugeordnet", inplace=True)
df.replace(np.NaN, "nicht zugeordnet", inplace=True) 

fig = px.scatter_matrix(df,
    dimensions=["total_cases", "hosp_patients", "new_cases", "new_vaccinations"],
    color='continent')

fig.show()

