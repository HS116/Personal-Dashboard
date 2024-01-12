from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker, declarative_base
import configparser

from dataclasses import dataclass
from datetime import datetime

from engine import Engine

from typing import List, Dict, Any

from financial_data_retriever import get_stock__data, get_news

# Define the ORM model
Base = declarative_base()

@dataclass
class StockData(Base):
    __tablename__ = "StockData"
    id : int = Column(Integer, primary_key=True, autoincrement=True)
    symbol : str = Column(String)
    date : datetime = Column(DateTime)
    open : float = Column(Float)
    high : float = Column(Float)
    low : float = Column(Float)
    close : float = Column(Float)
    volume : float = Column(Integer)

@dataclass
class NewsData(Base):
    __tablename__ = "NewsData"
    id : int = Column(Integer, primary_key=True, autoincrement=True)
    title : str = Column(String)
    description : str = Column(String)
    source_name : str = Column(String)
    author : str = Column(String)
    url : str = Column(String)
    published_date : datetime = Column(DateTime)

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
def create_tables(engine : Engine):
    Base.metadata.create_all(engine.db_engine)


def insert_stock_data(engine: Engine, stock_data: List[Dict[str, Any]]):

    # Create a session
    # https://docs.sqlalchemy.org/en/20/orm/session_basics.html#using-a-sessionmaker

    Session = sessionmaker(bind=engine.db_engine)

    # Using a context manager to automatically take care of begin(), commit(), and rollback()
    with Session.begin() as session:
        for stock_data_point in stock_data:

            # TODO: Query the data to be avoid adding a duplicate

            session.add(StockData(symbol=stock_data_point["symbol"], 
                                       date=stock_data_point["date"], 
                                       open=stock_data_point["open"], 
                                       high=stock_data_point["high"], 
                                       low=stock_data_point["close"], 
                                       close=stock_data_point["low"],
                                       volume=stock_data_point["volume"]))
            
def insert_news_articles(engine: Engine, news_data: List[Dict[str, Any]]):

    # Create a session
    # https://docs.sqlalchemy.org/en/20/orm/session_basics.html#using-a-sessionmaker

    Session = sessionmaker(bind=engine.db_engine)

    # Using a context manager to automatically take care of begin(), commit(), and rollback()
    with Session.begin() as session:
        for news_article in news_data:

            # TODO: Query the data to be avoid adding a duplicate

            session.add(NewsData(title=news_article["title"], 
                                       description=news_article["description"], 
                                       source_name=news_article["source_name"], 
                                       author=news_article["author"], 
                                       url=news_article["url"], 
                                       published_date=news_article["published_date"]))


if __name__=="__main__":

    engine: Engine = buildEngine()
    create_tables(engine)

    insert_stock_data(engine, get_stock__data("AAPL"))
    insert_news_articles(engine, get_news("in"))

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
