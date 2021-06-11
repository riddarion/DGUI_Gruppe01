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


#df.to_csv(r'C:\Users\leare\OneDrive\DGUI\dashboard\dashboardv2\covid-data-2.csv')

app.layout = html.Div(children =[
    
    #container für Titel
    html.Div(id='begruessung', children = [
    html.H1('COVID-19 DATENSET'),
    html.H3 ('Unser eigenes dynamisches User Interface')
    ]),
    
    
    #Container für content
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
                style = {'width': '30%'}
                ),

        
        ]), #dropdown div
    
    html.Div(id='output_container1', className='graphenboxen', children=[
    html.Br(),   
    
            html.Div(id='graph1', children=[
                dcc.Graph(className='graphen', id='covidplot', figure = {}, style = {'display': 'inline-block'}),
                html.Div(className='beschreibungen', id='beschreibung1', children=[
                    html.P(['Das gestaplete Histogramm zeigt die Anzahl voll geimpfter Personen.', html.Br(), 'Die Zeit ist hier auf Jahresbeginn 2021 beschränkt, da es vorher keine Impfung gab.']),
                ]),
            ]),
            
        html.Div(id='graph2', children=[
            dcc.Graph(className='graphen', id='covidplot2', figure = {}, style = {'display': 'inline-block'}),
            html.Div(className='beschreibungen', id='beschreibung2', children=[
                    html.P(['Die Treemap zeigt das Gesamttotal aller Ansteckungsfälle jedes Landes', html.Br(), 'zum neusten erfassten Zeitpunkt.'])
                ]),
        ]),
    ]),
    
    html.Div(children = [
    
        #Graph 1 mit Dropdown input
        html.Div(id='eingabe', children = [
            dcc.DatePickerRange(
                id='datepicker',
                min_date_allowed=date(2020, 1, 22),
                start_date=date(2020, 1, 22),
                max_date_allowed=newestDate,
                end_date=newestDate,
            ),
         ]),
    ]),
        
    html.Div(id='output_container2', className='graphenboxen', children=[
    html.Br(),   
    
        html.Div(id='graph3', children=[
           dcc.Graph(className='graphen', id='covidplot3', figure = {}, style = {'display': 'inline-block'}),
              html.Div(className='beschreibungen', id='beschreibung3', children=[
                    html.P(['Dieser Scatterplot zeigt die Anzahl neuer Ansteckung (x-Achse) in Relation zu', html.Br(), 'den gemeldeten Todesfälle (y-Achse) in Zusammenhang mit Covid-19.'])
                ]),
        ]),
        
        html.Div(id='graph4', children=[
            dcc.Graph(className='graphen', id='covidplot4', figure = {}, style = {'display': 'inline-block'}),
            html.Div(className='beschreibungen', id='beschreibung4', children=[
                    html.P(['Das Liniendiagramm zeigt die neuen Ansteckungsfälle auf der y-Achse über den', html.Br(), 'eingestellten Zeitraum auf der x-Achse.'])
                ]),
        ]),

    
        ]) #output container
    ]) #container content
 #app Layout
    

@app.callback(
    [#Output(component_id='output_container1', component_property='children'),
     Output(component_id='covidplot', component_property='figure'),
     Output(component_id='covidplot2', component_property='figure'),
     #Output(component_id='output_container2', component_property='children'), 
     Output(component_id='covidplot3', component_property='figure'),
     Output(component_id='covidplot4', component_property='figure')],
    [Input(component_id='continent', component_property='value'),
     #Input(component_id='datepicker', component_property='value'),
     Input(component_id='datepicker', component_property='start_date'),
     Input(component_id='datepicker', component_property='end_date')]
)



def update_graph(option_slctd, option_slctd3, option_slctd4):
    #option_slctd2, 
    #print(option_slctd, option_slctd2)
    #print(type(option_slctd, option_slctd2))
   
    dff = df.copy()

    dff = dff[dff["continent"] == option_slctd]
    #dff = dff[dff["datepicker"] == option_slctd2]
    
    dff = dff[dff["date"] >= option_slctd3]
    dff = dff[dff["date"] <= option_slctd4]
    
    
    dfff = df.copy()
    
    dfff = dfff[dfff["continent"] == option_slctd]
    
    dfff1 = dfff[dfff["date"] > "2021-01-01"]
    
    mostRecentDate = dfff["date"].max()
    dfff2 = dfff[dfff["date"] == mostRecentDate]
    


    
# Plotly Express
    
    fig = px.bar(dfff1, x = "date", y = "people_fully_vaccinated", color = "location",
                  title = "Impfverlauf seit Beginn des Jahres 2021")
    fig.update_yaxes(title=None)
    fig.update_xaxes(title=None)
    
    fig2 = px.treemap(dfff2, path = ['location', 'total_cases'],
                      values = 'total_cases',
                      title = "Summe aller Fälle nach Land zum aktuellen Zeitpunkt")
    fig2.update_yaxes(title=None)
    fig2.update_xaxes(title=None)


    fig3 = px.scatter(dff, x="new_cases", y="new_deaths", 
                     color = "location", #size = "gdp_per_capita",
                     marginal_x = "box", marginal_y = "box", #trendline = "lowess",
                     title = "Gemeldete Ansteckungen in Relation mit neuen Todesfällen")
    fig3.update_yaxes(title=None)
    fig3.update_xaxes(title=None)
    
    fig4 = px.line(dff, x = "date", y = "new_cases", color = 'location',
                   title = "Zeitverlauf der neuen Ansteckungsfälle")
    fig4.update_yaxes(title=None)
    fig4.update_xaxes(title=None)
    
    

    


    


    return fig, fig2, fig3, fig4
    


if __name__ == '__main__':
    app.run_server(debug=False)