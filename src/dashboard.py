from dash import Dash, dcc, html, Input, Output

import dash_bootstrap_components as dbc 
import plotly.express as px

import plotly.graph_objects as go 
import pandas as pd
import numpy as np 
import requests

from insert_data import buildEngine, NewsData
from sqlalchemy.orm import sessionmaker
from engine import Engine

app = Dash(external_stylesheets=[dbc.themes.SLATE], suppress_callback_exceptions=True)

app.layout = html.Div([

    html.Div([
        html.H1("Personal Dashboard", style={'text-align': 'center'})
    ]),

    dcc.Tabs(id="tabs", value="real-time-stocks", children=[
        dcc.Tab(label="Real Time Stocks Tracker", value="real-time-stocks"), 
        dcc.Tab(label="News", value="news"), 
        dcc.Tab(label="Weather", value="weather"), 
        dcc.Tab(label="Exchange Rates", value="exchange-rates")
    ]),

    html.Div(id="current-tab"),
])

@app.callback(Output("current-tab", "children"),
              Input("tabs", "value"))
def render_content(tab):
    if tab == "real-time-stocks":
        return html.Div([
            html.H3("Real Time Stock Tracker", style={'text-align': 'center'}), 
            dbc.Card("Something", color="secondary", inverse=True, style={'height': '100vh', 'padding':'20px'})
        ], style={'padding':'20px'})
    
    elif tab == "news":
        return html.Div([
            html.H3("News", style={'text-align': 'center'}), 

            html.Div([
            dcc.Dropdown(["Germany", "Great Britain", "United States", "India"], id="select-country1-news", value="Germany", style={"width":"200px"}), 
            dcc.Dropdown(["Germany", "Great Britain", "United States", "India"], id="select-country2-news", value="Great Britain", style={"width":"200px"})
            ], style={"display" : "flex", "margin" : "auto", "width" : "1800px", "justify-content" : "space-around"}),

            html.Div([
            dbc.Card("Something", id="country1-news", color="secondary", inverse=True, style={'height': '100vh', 'padding':'20px', 'flex': '1', 'margin-right': '10px', 'overflow':'auto'}), 
            dbc.Card("Something", id="country2-news", color="secondary", inverse=True, style={'height': '100vh', 'padding':'20px', 'flex': '1', 'margin-left': '10px', 'overflow':'auto'})
            ], style={"display": "flex", "justify-content": "space-around", "width": "100%", "padding":"20px"})

        ], style={'padding':'20px'})

    elif tab == "weather":
        return html.Div([
            html.H3("Weather", style={'text-align': 'center'}), 
            dbc.Card("Something", color="secondary", inverse=True, style={'height': '100vh', 'padding':'20px'})
        ], style={'padding':'20px'})

    elif tab == "exchange-rates":
        return html.Div([
            html.H3("Exchange Rates", style={'text-align': 'center'}), 
            dbc.Card("Something", color="secondary", inverse=True, style={'height': '100vh', 'padding':'20px'})
        ], style={'padding':'20px'})
    

@app.callback(Output("country1-news", "children"),
              Input("select-country1-news", "value"))
def render_news_country1(selected_country):

    engine: Engine = buildEngine()

    Session = sessionmaker(bind=engine.db_engine)

    with Session.begin() as session:

        content = []
        
        articles = session.query(NewsData).filter(NewsData.country == selected_country)
        for article in articles:
            content.append(html.Div([
                html.Div([
                    html.H3([article.title], style={"font-size":"20px"}), 
                    html.P([article.description]), 
                    html.P([article.url]), 
                ])
            ]))

        return content
            
@app.callback(Output("country2-news", "children"),
              Input("select-country2-news", "value"))
def render_news_country1(selected_country):

    engine: Engine = buildEngine()

    Session = sessionmaker(bind=engine.db_engine)

    with Session.begin() as session:

        content = []
        
        articles = session.query(NewsData).filter(NewsData.country == selected_country)
        for article in articles:
            content.append(html.Div([
                html.Div([
                    html.H3([article.title], style={"font-size":"20px"}), 
                    html.P([article.description]), 
                    html.P([article.url]), 
                ])
            ]))

        return content
        

if __name__ == "__main__":
    app.run_server(debug=True)