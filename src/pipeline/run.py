import configparser
import json
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

from engine import Engine
from extract_data import (
    get_exchange_rates,
    get_fake_stock_data,
    get_newsdataio_news,
    get_stock_data_alpha_vantage,
    get_stock_data_market_stack,
    get_weather_data,
)
from load_data import (
    ExchangeRateData,
    NewsData,
    StockData,
    WeatherData,
    buildEngine,
    create_tables,
    insert_exchange_rates,
    insert_news_articles,
    insert_stock_data,
    insert_weather_data,
)
from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

time.sleep(10)

engine: Engine = buildEngine()
create_tables(engine)


with open('configs/my_stocks.json', 'r') as file:
    # Load the JSON data
    my_stocks = json.load(file)

for country, stocks in my_stocks["stocks"].items():
    for stock in stocks:
        insert_stock_data(engine, get_stock_data_market_stack(stock["symbol"]))


insert_news_articles(engine, get_newsdataio_news("de"))
insert_news_articles(engine, get_newsdataio_news("gb"))
insert_news_articles(engine, get_newsdataio_news("us"))
insert_news_articles(engine, get_newsdataio_news("in"))
insert_exchange_rates(engine, get_exchange_rates(["USD", "EUR", "GBP", "INR"]))
insert_weather_data(engine, get_weather_data("Munich"))

Session = sessionmaker(bind=engine.db_engine)

with Session.begin() as session:
    rows = session.query(StockData).all()
    for row in rows:
        print(row)
        print("\n")

    rows = session.query(NewsData).all()
    for row in rows:
        print(row)
        print("\n")

    rows = session.query(ExchangeRateData).all()
    for row in rows:
        print(row)
        print("\n")

    rows = session.query(WeatherData).all()
    for row in rows:
        print(row)
        print("\n")
