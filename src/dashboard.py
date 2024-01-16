from dash import Dash, dcc, html, Input, Output

import dash_bootstrap_components as dbc 
import plotly.express as px

import plotly.graph_objects as go 
import pandas as pd
import numpy as np 
import requests

app = Dash(external_stylesheets=[dbc.themes.CYBORG])

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
            html.H3("Real Time Stock Tracker")
        ])
    
    elif tab == "news":
        return html.Div([
            html.H3("News")
        ])

    elif tab == "weather":
        return html.Div([
            html.H3("Weather")
        ])

    elif tab == "exchange-rates":
        return html.Div([
            html.H3("Exchange Rates")
        ])
        

if __name__ == "__main__":
    app.run_server(debug=True)