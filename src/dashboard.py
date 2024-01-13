from dash import Dash, dcc, html, Input, Output

import dash_bootstrap_components as dbc 
import plotly.express as px

import plotly.graph_objects as go 
import pandas as pd
import numpy as np 
import requests

app = Dash(external_stylesheets=[dbc.themes.CYBORG])

def create_dropdown(options, id):
    return html.Div([
        html.H2(id.replace("-select", "").replace("-", " ").capitalize(), style={"padding" : "0px 30px 0px 30px"}), 
        dcc.Dropdown(options, id=id, value=options[0])
    ], style={"padding" : "0px 20px 0px 20px"})

app.layout = html.Div([

    html.Div([
        # Shows us all the options we can select from and we have a default "value" setup
        create_dropdown(["btcusd", "ethusd", "xrpusd"], id="coin-select"),
        create_dropdown(["60", "3600", "86400"], id="timeframe-select"),
        create_dropdown(["20", "50", "100"], id="num-bars-select"),
    ], style={"display" : "flex", "margin" : "auto", "width" : "1200px", "justify-content" : "space-around"}),

    
    html.Div([
        dcc.RangeSlider(0, 20, 1, value= [0, 20], id="range-slider")
    ], id="range-slider-container", style={"width":"1200px", "margin":"auto", "padding-top":"30px"}),
    dcc.Graph(id="candles"), 
    dcc.Interval(id="interval", interval=2000)
])



@app.callback(Output("range-slider-container", "children"), Input("num-bars-select", "value"))
def update_range_slider(num_bars):
    return dcc.RangeSlider(min=0, max=int(num_bars), step=int(int(num_bars)/20), value=[0, int(num_bars)], id="range-slider")

# interval is the id of the interval we had above, and n_interval indicates the number of intervals which have passed which we can see in the Interval documentation
# callback decorators allows our function to be called when something happens to the input id object

# Basically first parameter is the id and the second parameter is the particular attribute we want from that object with the particular id
@app.callback(Output("candles", "figure"), Input("interval", "n_intervals"), Input("coin-select", "value"), Input("timeframe-select", "value"), Input("num-bars-select", "value"), Input("range-slider", "value"))
def update_figure(n_intervals, coin_pair, timeframe, num_bars, range_values):

    url = f"https://www.bitstamp.net/api/v2/ohlc/{coin_pair}"

    params = {
        "step" : timeframe, 
        "limit" : num_bars
    }

    data = requests.get(url, params=params).json()["data"]["ohlc"]

    data = pd.DataFrame(data)

    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')

    data = data.iloc[range_values[0]:range_values[1]]

    candles = go.Figure(
        data = [
            go.Candlestick(
                x =  data.timestamp,
                open = data.open, 
                high = data.high,
                low = data.low,
                close = data.close
            )
        ]
    )

    candles.update_layout(xaxis_rangeslider_visible=False, template="plotly_dark")


    return candles


if __name__ == "__main__":
    app.run_server(debug=True)