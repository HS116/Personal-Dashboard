import configparser
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
from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from load_data import buildEngine, create_tables, insert_stock_data, insert_news_articles, insert_weather_data, insert_exchange_rates
from load_data import StockData, NewsData, WeatherData, ExchangeRateData

import json

import time

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

"""
# Read
rows = session.query(Test).all()
print("Read:")
for row in rows:
    print(row.id, row.name)

# Update
update_entry = session.query(Test).filter_by(name="John Doe").first()
if update_entry:
    update_entry.name = "Jane Smith"
    session.commit()
    print("Update: Entry updated successfully.")

# Read after update
rows = session.query(Test).all()
print("Read after update:")
for row in rows:
    print(row.id, row.name)

# Delete
delete_entry = session.query(Test).filter_by(name="Jane Smith").first()
if delete_entry:
    session.delete(delete_entry)
    session.commit()
    print("Delete: Entry deleted successfully.")

# Read after delete
rows = session.query(Test).all()
print("Read after delete:")
for row in rows:
    print(row.id, row.name)

"""