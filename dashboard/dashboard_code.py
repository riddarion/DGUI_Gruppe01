# -*- coding: utf-8 -*-
"""
Created on Wed May 26 09:10:42 2021

@author: leare
"""

import plotly.express as px
import pandas as pd
import numpy as np

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from datetime import date


app = dash.Dash(__name__)

df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
df.replace('', 0, inplace=True)
df.replace(np.NaN, 0, inplace=True)

newestDate = df["date"].max()

app.layout = html.Div(children =[
    
    #container für Titel
    html.Div(children = [
    html.H1('COVID-19 Datenset'),
    html.P ('unser eigenes dynamisches User Interface')
    ]),
    
    
    #Container für content
    html.Div(children = [
    
    #Graph 1 mit Dropdown input
    html.Div(children = [
        dcc.Dropdown(id='continent',
                options = [
                    {"label": "Nordamerika", "value": 'North America'},
                    {"label": "Südamerika", "value": 'South America'},
                    {"label": "Ozeanien", "value": 'Oceania'},
                    {"label": "Afrika", "value": 'Africa'},
                    {"label": "Europa", "value": 'Europe'},
                    {"label": "nicht zugeordnet", "value": 0},
                    {"label": "Asien", "value": 'Asia'}],
                multi = False,
                value = 'Europe',
                style = {"width": "40%"}
                ),
        
        dcc.DatePickerRange(
            id='datepicker',
            min_date_allowed=date(2020, 1, 22),
            start_date=date(2020, 1, 22),
            max_date_allowed=(2021, 6, 1),
            ),
        
        ]), #dropdown div
    
    html.Div(id='output_container', children=[
    html.Br(),   
    
    dcc.Graph(id='covidplot', figure = {}, style = {'display': 'inline-block'}),

    dcc.Graph(id='covidplot2', figure = {}, style = {'display': 'inline-block'}),
    html.Br(), 
    html.P ('Hier könnte eine Beschreibung zur Visualisierung stehen.'),
    html.Br(),
    
    dcc.Graph(id='covidplot3', figure = {}, style = {'display': 'inline-block'}),
    
    dcc.Graph(id='covidplot4', figure = {}, style = {'display': 'inline-block'}),
    
        ]) #output container
    ]) #container content
]) #app Layout
    

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='covidplot', component_property='figure'),
     Output(component_id='covidplot2', component_property='figure'),
     Output(component_id='covidplot3', component_property='figure'),
     Output(component_id='covidplot4', component_property='figure')],
    [Input(component_id='continent', component_property='value'),
     Input(component_id='date', component_property='value')]
)


def update_graph(option_slctd, option_slctd2, option_slctd3, option_slctd4):
    #print(option_slctd, option_slctd2)
    #print(type(option_slctd, option_slctd2))
   
    dff = df.copy()

    dff = dff[dff["continent"] == option_slctd]
    dff = dff[dff["date"] == option_slctd2]
    
    dff = dff[dff["date"] >= option_slctd3]
    dff = dff[dff["date"] <= option_slctd4]
    
    dff2 = dff[dff["date"] > "2021-01-01"]
    
    dff3 = dff[dff["date"] == newestDate]
    


    
# Plotly Express
    
    fig = px.scatter(dff, x="new_cases", y="new_deaths", 
                     color = "location", size = "gdp_per_capita",
                     marginal_x = "box", marginal_y = "box", trendline = "lowess",
                     width = 800,
                     title = "Neue Fälle in Relation mit neuen Todesfällen")
    fig.update_yaxes(title=None)
    fig.update_xaxes(title=None)
    
    
    fig2 = px.bar(dff2, x = "date", y = "total_vaccinations", color = "location",
                  width = 600,
                  title = "Impfverlauf seit Beginn des Jahres 2021")
    fig2.update_yaxes(title=None)
    fig2.update_xaxes(title=None)
    

    fig3 = px.treemap(dff3, path = ['location', 'total_cases'],
                      values = 'total_cases',
                      width = 700,
                      title = "Summe aller Fälle nach Land zum aktuellen Zeitpunkt")
    fig3.update_yaxes(title=None)
    fig3.update_xaxes(title=None)
    
    fig4 = px.line(dff, x = "date", y = "new_cases", color = 'location',
                   width = 700,
                   title = "Zeitverlauf der neuen Ansteckungsfälle")
    fig4.update_yaxes(title=None)
    fig4.update_xaxes(title=None)

    
    container = "Ausgabe"

    return container, fig, fig2, fig3, fig4
    


if __name__ == '__main__':
    app.run_server(debug=False)