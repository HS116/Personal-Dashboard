import datetime
import logging
import sys
from typing import Any, Dict, List, Optional

import requests

import json

from newsapi import NewsApiClient

import configparser


def get_stock__data(symbol : str) -> Dict[str, Any]:
    """
    :param symbol: The company or index you would like to get information from AlphaAvantage API e.g. TSLA
    :return: dictionary containing the stock info for that particular symbol e.g. IBM

    For more info about AlphaVantage API documentation: https://www.alphavantage.co/documentation/
    """

    config = configparser.ConfigParser()
    config.read("configs/api_keys.ini")

    api_key = config.get("api_keys", "AlphaAvantage_api_key")

    url= f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=60min&apikey={api_key}"

    try:
        response = requests.get(url)
    except requests.ConnectionError as ce:
        logging.error(f"There was an error with the request: {ce}")
        sys.exit(1)

    if response.status_code == 200:
        data = json.loads(response.content)

        try:
            price_data = data['Time Series (60min)']
            return price_data

        except KeyError:
            logging.error("Time Series (60min) field is not present in content")
            sys.exit(1)

    else:
        logging.error(f"Response had the following status code: {response.status_code}")


def get_news(country: str ="us", category: str = "general") -> List[str]:

    """
    :param country: The country you would like to receive news information about. Default is US. India and US seem to get good data, but hardly any data for Germany and not so good data for uk. 
    :param category: The category of news that you would be interested in

    :return: List of strings containing the relevant news headlines. 

    For more info about NewsAPI documentation: https://newsapi.org/docs and https://newsapi.org/docs/endpoints/top-headlines 
    """

    config = configparser.ConfigParser()
    config.read("configs/api_keys.ini")

    api_key = config.get("api_keys", "NewsAPI_api_key")

    newsapi = NewsApiClient(api_key=api_key)
    
    try:
        response = newsapi.get_top_headlines(country=country,category=category)
    except ValueError as ve:
        logging.error(f"Request failed due to {ve}")
        sys.exit(1)
    

    if response["status"] == "ok":
        titles = [article['title'] for article in response['articles']]
        return titles
    else:
        logging.error("Could not retrieve news information successfully")
        sys.exit(1)

def get_crypto_exchange_data() -> List[Dict[str, Any]]:

    """
    :return: List of dictionaries containing crypto exchange data
    """

    url = 'https://api.coincap.io/v2/exchanges'
    try:
        response = requests.get(url)
    except requests.ConnectionError as ce:
        logging.error(f"There was an error with the request, {ce}")
        sys.exit(1)
    return response.json().get('data', [])


if __name__=="__main__":
    print(get_stock__data("AAPL"))
    print(get_news("in"))
    #print(get_crypto_exchange_data())