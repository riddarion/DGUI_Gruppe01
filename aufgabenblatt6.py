import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

owidDataPath = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
owidData = pd.read_csv(owidDataPath)
situation = pd.DataFrame(owidData)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Test Title")
])
