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

# Define the ORM model
Base = declarative_base()


@dataclass
class StockData(Base):
    __tablename__ = "StockData"
    symbol: str = Column(String, primary_key=True)
    datetime: datetime = Column(DateTime, primary_key=True)
    open: float = Column(Float)
    high: float = Column(Float)
    low: float = Column(Float)
    close: float = Column(Float)
    volume: float = Column(Integer)


@dataclass
class NewsData(Base):
    __tablename__ = "NewsData"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String)
    description: str = Column(String)
    source_name: str = Column(String)
    author: str = Column(String)
    url: str = Column(String)
    published_date: datetime = Column(DateTime)
    country: str = Column(String)


@dataclass
class ExchangeRateData(Base):
    __tablename__ = "ExchangeRateData"
    first_currency: str = Column(String, primary_key=True)
    second_currency: str = Column(String, primary_key=True)
    datetime: datetime = Column(DateTime, primary_key=True)
    exchange_rate: float = Column(Float)


@dataclass
class WeatherData(Base):
    __tablename__ = "WeatherData"
    city: str = Column(String, primary_key=True)
    country: str = Column(String, primary_key=True)
    datetime: datetime = Column(DateTime, primary_key=True)
    condition: str = Column(String)
    temp_celsius: float = Column(Float)
    temp_feels_like_celsius: float = Column(Float)
    wind_kph: float = Column(Float)
    humidity: float = Column(Float)


def buildEngine() -> Engine:
    config = configparser.ConfigParser()
    config.read("configs/database.ini")

    # Get the PostgreSQL connection details
    host = config.get("postgresql", "host")
    port = config.get("postgresql", "port")
    db_name = config.get("postgresql", "dbname")
    user = config.get("postgresql", "user")
    password = config.get("postgresql", "password")

    # Define the database connection
    return Engine(user=user, password=password, host=host, port=port, db_type="postgresql", db_name=db_name)


# Create the tables
def create_tables(engine: Engine):
    Base.metadata.create_all(engine.db_engine)


def insert_stock_data(engine: Engine, stock_data: List[Dict[str, Any]]):
    # Create a session
    # https://docs.sqlalchemy.org/en/20/orm/session_basics.html#using-a-sessionmaker

    Session = sessionmaker(bind=engine.db_engine)

    # Using a context manager to automatically take care of begin(), commit(), and rollback()
    with Session.begin() as session:
        for stock_data_point in stock_data:
            # Query the data to be avoid adding a duplicate
            existing_obj = (
                session.query(StockData)
                .filter_by(symbol=stock_data_point["symbol"], datetime=stock_data_point["datetime"])
                .first()
            )

            if not existing_obj:
                session.add(
                    StockData(
                        symbol=stock_data_point["symbol"],
                        datetime=stock_data_point["datetime"],
                        open=stock_data_point["open"],
                        high=stock_data_point["high"],
                        low=stock_data_point["close"],
                        close=stock_data_point["low"],
                        volume=stock_data_point["volume"],
                    )
                )


def insert_news_articles(engine: Engine, news_data: List[Dict[str, Any]]):
    Session = sessionmaker(bind=engine.db_engine)

    country_code_mappings = {"de": "Germany", "gb": "Great Britain", "us": "United States", "in": "India"}

    with Session.begin() as session:
        for news_article in news_data:
            session.add(
                NewsData(
                    title=news_article["title"],
                    description=news_article["description"],
                    source_name=news_article["source_name"],
                    author=news_article["author"],
                    url=news_article["url"],
                    published_date=news_article["published_date"],
                    country=country_code_mappings[news_article["country"]],
                )
            )


def insert_exchange_rates(engine: Engine, exchange_rates: List[Dict[str, Any]]):
    Session = sessionmaker(bind=engine.db_engine)

    with Session.begin() as session:
        for exchange_rate in exchange_rates:
            # Query the data to be avoid adding a duplicate
            existing_obj = (
                session.query(ExchangeRateData)
                .filter_by(
                    first_currency=exchange_rate["first_currency"],
                    second_currency=exchange_rate["second_currency"],
                    datetime=exchange_rate["datetime"],
                )
                .first()
            )

            if not existing_obj:
                session.add(
                    ExchangeRateData(
                        first_currency=exchange_rate["first_currency"],
                        second_currency=exchange_rate["second_currency"],
                        exchange_rate=exchange_rate["exchange_rate"],
                        datetime=exchange_rate["datetime"],
                    )
                )


def insert_weather_data(engine: Engine, weather_data: Dict[str, Any]):
    Session = sessionmaker(bind=engine.db_engine)

    with Session.begin() as session:
        # Query the data to be avoid adding a duplicate
        existing_obj = (
            session.query(WeatherData)
            .filter_by(city=weather_data["city"], country=weather_data["country"], datetime=weather_data["datetime"])
            .first()
        )

        if not existing_obj:
            session.add(
                WeatherData(
                    city=weather_data["city"],
                    country=weather_data["country"],
                    condition=weather_data["condition"],
                    temp_celsius=weather_data["temp_celsius"],
                    temp_feels_like_celsius=weather_data["temp_feels_like_celsius"],
                    wind_kph=weather_data["wind_kph"],
                    humidity=weather_data["humidity"],
                    datetime=weather_data["datetime"],
                )
            )


if __name__ == "__main__":
    engine: Engine = buildEngine()
    create_tables(engine)

    insert_stock_data(engine, get_stock_data_market_stack("TCS.XNSE"))

    # insert_stock_data(engine, get_fake_stock_data())
    # insert_news_articles(engine, get_newsdataio_news("de"))
    # insert_news_articles(engine, get_newsdataio_news("gb"))
    # insert_news_articles(engine, get_newsdataio_news("us"))
    # insert_news_articles(engine, get_newsdataio_news("in"))
    # insert_exchange_rates(engine, get_exchange_rates(["USD", "EUR", "GBP", "INR"]))
    # insert_weather_data(engine, get_weather_data("Munich"))

    Session = sessionmaker(bind=engine.db_engine)

    with Session.begin() as session:
        rows = session.query(StockData).all()
        for row in rows:
            print(row)
            print("\n")

        # rows = session.query(NewsData).all()
        # for row in rows:
        #     print(row)
        #     print("\n")

        # rows = session.query(ExchangeRateData).all()
        # for row in rows:
        #     print(row)
        #     print("\n")

        # rows = session.query(WeatherData).all()
        # for row in rows:
        #     print(row)
        #     print("\n")

