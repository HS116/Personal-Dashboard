from typing import List

import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from dash import Dash, Input, Output, dcc, html
from engine import Engine
from insert_data import NewsData, buildEngine
from sqlalchemy.orm import sessionmaker

app = Dash(external_stylesheets=[dbc.themes.SLATE], suppress_callback_exceptions=True)

app.layout = html.Div(
    [
        html.Div([html.H1("Country Comparison Dashboard", style={'text-align': 'center'})]),
        dcc.Tabs(
            id="tabs",
            value="real-time-stocks",
            children=[
                dcc.Tab(label="Stocks", value="stocks"),
                dcc.Tab(label="News", value="news"),
                dcc.Tab(label="Weather", value="weather"),
                dcc.Tab(label="Exchange Rates", value="exchange-rates"),
            ],
        ),
        html.Div(id="current-tab"),
    ]
)


def create_country_dropdowns(info_type: str) -> html.Div:
    """
    return: html.Div which contains the relevant heading and country dropdowns with the particular ids.
    """

    return html.Div(
        [
            html.H3(info_type, style={'text-align': 'center'}),
            html.Div(
                [
                    dcc.Dropdown(
                        ["Germany", "Great Britain", "United States", "India"],
                        id=f"select-country1-{info_type.lower()}",
                        value="Germany",
                        style={"width": "200px"},
                    ),
                    dcc.Dropdown(
                        ["Germany", "Great Britain", "United States", "India"],
                        id=f"select-country2-{info_type.lower()}",
                        value="United States",
                        style={"width": "200px"},
                    ),
                ],
                style={"display": "flex", "margin": "auto", "width": "1800px", "justify-content": "space-around"},
            ),
            html.Div(
                [
                    dbc.Card(
                        "Something",
                        id=f"country1-{info_type.lower()}",
                        color="secondary",
                        inverse=True,
                        style={
                            'height': '100vh',
                            'padding': '20px',
                            'flex': '1',
                            'margin-right': '10px',
                            'overflow': 'auto',
                        },
                    ),
                    dbc.Card(
                        "Something",
                        id=f"country2-{info_type.lower()}",
                        color="secondary",
                        inverse=True,
                        style={
                            'height': '100vh',
                            'padding': '20px',
                            'flex': '1',
                            'margin-left': '10px',
                            'overflow': 'auto',
                        },
                    ),
                ],
                style={"display": "flex", "justify-content": "space-around", "width": "100%", "padding": "20px"},
            ),
        ],
        style={'padding': '20px'},
    )


@app.callback(Output("current-tab", "children"), Input("tabs", "value"))
def render_content(tab):
    if tab == "stocks":
        return create_country_dropdowns("Stocks")

    elif tab == "news":
        return create_country_dropdowns("News")

    elif tab == "weather":
        return html.Div(
            [
                html.H3("Weather", style={'text-align': 'center'}),
                dbc.Card("Something", color="secondary", inverse=True, style={'height': '100vh', 'padding': '20px'}),
            ],
            style={'padding': '20px'},
        )

    elif tab == "exchange-rates":
        return html.Div(
            [
                html.H3("Exchange Rates", style={'text-align': 'center'}),
                dbc.Card("Something", color="secondary", inverse=True, style={'height': '100vh', 'padding': '20px'}),
            ],
            style={'padding': '20px'},
        )


def create_stocks_graph(symbols: List[str]):
    engine: Engine = buildEngine()

    # Convert table from database into datafram since plotly relies on dataframes
    df = pd.read_sql_table("StockData", engine.db_engine.connect())

    df = df[['symbol', 'datetime', 'close']]

    df = df.query(f"symbol in {symbols}")

    fig = px.line(df, x="datetime", y="close", color="symbol")

    fig.update_layout(template="plotly_dark")

    return dcc.Graph(figure=fig)


@app.callback(Output("country1-stocks", "children"), Input("select-country1-stocks", "value"))
def stocks1(selected_country):
    engine: Engine = buildEngine()

    Session = sessionmaker(bind=engine.db_engine)

    if selected_country == "Germany":
        return create_stocks_graph(["ALV.XFRA", "BMW.XFRA", "DAII.XFRA"])

    elif selected_country == "Great Britain":
        return create_stocks_graph(["TSCO.XLON", "SHEL.XLON", "HSBA.XLON"])

    elif selected_country == "United States":
        return create_stocks_graph(["AAPL", "TSLA", "KO"])

    elif selected_country == "India":
        return create_stocks_graph(["RELIANCE.XNSE", "INFY.XNSE", "TCS.XNSE"])


@app.callback(Output("country2-stocks", "children"), Input("select-country2-stocks", "value"))
def stocks2(selected_country):
    engine: Engine = buildEngine()

    Session = sessionmaker(bind=engine.db_engine)

    if selected_country == "Germany":
        return create_stocks_graph(["ALV.XFRA", "BMW.XFRA", "DAII.XFRA"])

    elif selected_country == "Great Britain":
        return create_stocks_graph(["TSCO.XLON", "SHEL.XLON", "HSBA.XLON"])

    elif selected_country == "United States":
        return create_stocks_graph(["AAPL", "TSLA", "KO"])

    elif selected_country == "India":
        return create_stocks_graph(["RELIANCE.XNSE", "INFY.XNSE", "TCS.XNSE"])


@app.callback(Output("country1-news", "children"), Input("select-country1-news", "value"))
def render_news_country1(selected_country):
    engine: Engine = buildEngine()

    Session = sessionmaker(bind=engine.db_engine)

    with Session.begin() as session:
        content = []

        articles = session.query(NewsData).filter(NewsData.country == selected_country)
        for article in articles:
            content.append(
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3([article.title], style={"font-size": "20px"}),
                                html.P([article.description]),
                                html.P([article.url]),
                            ]
                        )
                    ]
                )
            )

        return content


@app.callback(Output("country2-news", "children"), Input("select-country2-news", "value"))
def render_news_country2(selected_country):
    engine: Engine = buildEngine()

    Session = sessionmaker(bind=engine.db_engine)

    with Session.begin() as session:
        content = []

        articles = session.query(NewsData).filter(NewsData.country == selected_country)
        for article in articles:
            content.append(
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3([article.title], style={"font-size": "20px"}),
                                html.P([article.description]),
                                html.P([article.url]),
                            ]
                        )
                    ]
                )
            )

        return content


if __name__ == "__main__":
    app.run_server(debug=True)
