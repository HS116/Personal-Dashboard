from dash import Dash, dcc, html, Input, Output

import dash_bootstrap_components as dbc 
import plotly.express as px

import plotly.graph_objects as go 
import pandas as pd
import numpy as np 
import requests

app = Dash(external_stylesheets=[dbc.themes.SLATE])

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
            dcc.Dropdown(["Germany", "United Kingdom", "United States", "India"], id="select-country1-news", value="Germany", style={"width":"200px"}), 
            dcc.Dropdown(["Germany", "United Kingdom", "United States", "India"], id="select-country2-news", value="United Kingdom", style={"width":"200px"})
            ], style={"display" : "flex", "margin" : "auto", "width" : "1800px", "justify-content" : "space-around"}),

            html.Div([
            dbc.Card("Something", id="country1-news", color="secondary", inverse=True, style={'height': '100vh', 'padding':'20px', 'flex': '1', 'margin-right': '10px'}), 
            dbc.Card("Something", id="country2-news", color="secondary", inverse=True, style={'height': '100vh', 'padding':'20px', 'flex': '1', 'margin-left': '10px'})
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
        

if __name__ == "__main__":
    app.run_server(debug=True)