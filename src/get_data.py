import datetime
import logging
import sys
from typing import Any, Dict, List, Optional

import requests

from datetime import datetime


import json

from newsapi import NewsApiClient

import configparser

def get_stock_data_market_stack(symbol : str = "AAPL") -> List[Dict[str, Any]]:

    """
    :param symbol: The company or index you would like to get information from AlphaAvantage API e.g. TSLA
    :return: List of dictionaries where each dictionary contains stock data information for the symbol at a particular time point

    For more info about MarketData API: https://marketstack.com/documentation
    Max of 1000 monthly API calls per month on free version. 
    """

    config = configparser.ConfigParser()
    config.read("configs/api_keys.ini")

    api_key = config.get("api_keys", "Marketstack_api_key")

    # TODO: change "eod" to "eod/latest" so we can inserting duplicate data later
    url=f"http://api.marketstack.com/v1/eod?access_key={api_key}&symbols={symbol}"

    try:
        response = requests.get(url)
    except requests.ConnectionError as ce:
        logging.error(f"There was an error with the request: {ce}")
        sys.exit(1)

    if response.status_code == 200:
        content = json.loads(response.content)

        try:
            stock_data = content["data"]

            # Transformation

            formatted_stock_data = []

            relevant_columns = {"symbol", "datetime", "open", "high", "low", "close", "volume"}

            for stock_data_point in stock_data:

                stock_data_point['datetime'] = datetime.strptime(stock_data_point['date'], "%Y-%m-%dT%H:%M:%S%z")

                if stock_data_point["volume"]:
                    stock_data_point["volume"] = int(stock_data_point["volume"])
                else:
                    stock_data_point["volume"] = None

                formatted_stock_data_point = {key : value for key, value in stock_data_point.items() if key in relevant_columns}

                formatted_stock_data.append(formatted_stock_data_point)         

            return formatted_stock_data

        except KeyError:
            logging.error("'data' field is not present in content")
            sys.exit(1)

    else:
        logging.error(f"Response had the following status code: {response.status_code}")
        sys.exit(1)


def get_stock_data_alpha_vantage(symbol : str) -> List[Dict[str, Any]]:
    """
    :param symbol: The company or index you would like to get information from AlphaAvantage API e.g. TSLA
    :return: List of dictionaries where each dictionary contains stock data information for the symbol at a particular time point

    For more info about AlphaVantage API: https://www.alphavantage.co/documentation/
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
            
            # Transformations
            # TODO: Move the transform functionality into a separate function

            price_data = {datetime.strptime(date, "%Y-%m-%d %H:%M:%S") : attributes for date, attributes in price_data.items()}

            column_renamings={
                    '1. open':'open',
                    '2. high':'high',
                    '3. low':'low',
                    '4. close':'close',
                    '5. volume':'volume'}
            
            formatted_price_data = []

            for date, attributes in price_data.items():
                attributes = {column_renamings[key] : float(value) for key, value in attributes.items()}
                attributes["volume"] = int(attributes["volume"])

                attributes.update({"datetime" : date, "symbol" : symbol})
                formatted_price_data.append(attributes)          

            return formatted_price_data

        except KeyError:
            logging.error("Time Series (60min) field is not present in content")
            sys.exit(1)

    else:
        logging.error(f"Response had the following status code: {response.status_code}")
        sys.exit(1)


def get_fake_stock_data():

    """
    For testing purposes to prevent unnecessary API requests since there is a limit of 25 API requests per day
    """

    # TODO: Make this method better by using mocking or storing the data in a file

    res = [{'open': 185.675, 'high': 185.7, 'low': 185.56, 'close': 185.63, 'volume': 25944, 'date': datetime(2024, 1, 12, 19, 0), 'symbol': 'AAPL'}, {'open': 185.8, 'high': 185.81, 'low': 185.65, 'close': 185.67, 'volume': 9115, 'date': datetime(2024, 1, 12, 18, 0), 'symbol': 'AAPL'}, {'open': 185.83, 'high': 185.92, 'low': 175.279, 'close': 185.8, 'volume': 216241, 'date': datetime(2024, 1, 12, 17, 0), 'symbol': 'AAPL'}, {'open': 185.91, 'high': 185.99, 'low': 185.45, 'close': 185.835, 'volume': 16247450, 'date': datetime(2024, 1, 12, 16, 0), 'symbol': 'AAPL'}, {'open': 185.31, 'high': 185.98, 'low': 185.22, 'close': 185.92, 'volume': 6578518, 'date': datetime(2024, 1, 12, 15, 0), 'symbol': 'AAPL'}, 
           ]

    return res

def get_newsapi_news(country: str ="us", category: str = "general") -> List[Dict[str, Any]]:

    """
    :param country: The country you would like to receive news information about. Default is US. India and US seem to get good data, but hardly any data for Germany and not so good data for uk. 
    :param category: The category of news that you would be interested in

    :return: List of dictionaries containing the relevant news articles from NewsAPI

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

        articles = response['articles']

        formatted_articles = []

        # Transformations

        column_renamings={"publishedAt":"published_date"}

        for article in articles:
            
            article = {column_renamings.get(key, key) : value for key, value in article.items()}

            formatted_article = {key : value for key, value in article.items() if key != 'source' and key != 'content' and key != 'urlToImage'}

            formatted_article.update({"source_name" : article["source"]["name"]})

            formatted_articles.append(formatted_article)

        return formatted_articles
        
    else:
        logging.error("Could not retrieve news information successfully")
        sys.exit(1)

def get_newsdataio_news(country: str ="de", category: str = "top") -> List[Dict[str, Any]]:

    """
    :param country: The country you would like to receive news information about. Default is Germany. This API returns good results for UK (gb), Germany (de), United States (us), India (in) 
    :param category: The category of news that you would be interested in e.g. business, domestic, sports, technology

    :return: List of dictionaries containing the relevant news articles from NewsDataIO
    
    For more documentation: https://newsdata.io/documentation/#latest-news
    """

    config = configparser.ConfigParser()
    config.read("configs/api_keys.ini")

    api_key = config.get("api_keys", "NewsDataIO_api_key")

    url= f"https://newsdata.io/api/1/news?apikey={api_key}&country={country}&prioritydomain=top&timeframe=24&category={category}"

    try:
        response = requests.get(url)
    except requests.ConnectionError as ce:
        logging.error(f"There was an error with the request: {ce}")
        sys.exit(1)
    
    if response.status_code == 200:
        data = json.loads(response.content)

        try:
            articles = data['results']
            
            # Transformations

            column_renamings={"pubDate":"published_date", 
                              "source_id" : "source_name", 
                              "creator" : "author", 
                              "link":"url"}

            relevant_columns = {"title", "description", "source_name", "author", "url", "published_date"}

            formatted_articles = []

            for article in articles:
                article = {column_renamings.get(key, key) : value for key, value in article.items()}

                article['published_date'] = datetime.strptime(article['published_date'], "%Y-%m-%d %H:%M:%S")

                formatted_article = {key : value for key, value in article.items() if key in relevant_columns}
                formatted_article['country'] = country
                formatted_articles.append(formatted_article)
            
            return formatted_articles

        except KeyError:
            logging.error("No 'results' field")
            sys.exit(1)

    else:
        logging.error(f"Response had the following status code: {response.status_code}")
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

def get_exchange_rates(currencies : List[str] = ["USD", "EUR", "GBP", "INR"]) -> List[Dict[str, Any]]:

    """
    :param currencies: List of currencies which you want currency exchange info e.g. ["USD", "EUR", "GBP", "INR"]
    :return: List of dictionaries containing currency exchange info
    """

    config = configparser.ConfigParser()
    config.read("configs/api_keys.ini")

    api_key = config.get("api_keys", "ExchangeRateAPI_api_key")

    exchange_rates = []

    currencies = set(currencies)

    for first_currency in currencies:
        url= f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{first_currency}"

        try:
            response = requests.get(url)
        except requests.ConnectionError as ce:
            logging.error(f"There was an error with the request: {ce}")
            sys.exit(1)
        
        if response.status_code == 200:
            data = json.loads(response.content)

            try:
                conversion_rates = data['conversion_rates']

                for second_currency, value in conversion_rates.items():
                    if first_currency != second_currency and second_currency in currencies:
                        exchange_rates.append({"first_currency":first_currency, "second_currency":second_currency, "exchange_rate":float(value), "datetime": datetime.strptime(data['time_last_update_utc'], "%a, %d %b %Y %H:%M:%S %z")})
            
            except KeyError:
                logging.error("No 'conversion_rates' field")
                sys.exit(1)

        else:
            logging.error(f"Response had the following status code: {response.status_code}")
            sys.exit(1)

    return exchange_rates

def get_weather_data(city : str = "Munich") -> Dict[str, Any]:
    """
    :param city: The city you would like to receive weather data for
    :return: Dictionary containing weather info for the particular city
    """

    config = configparser.ConfigParser()
    config.read("configs/api_keys.ini")

    api_key = config.get("api_keys", "WeatherAPI_api_key")
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    try:
        response = requests.get(url)
    except requests.ConnectionError as ce:
        logging.error(f"There was an error with the request: {ce}")
        sys.exit(1)
    
    if response.status_code == 200:
        data = json.loads(response.content)

        try:

            # Extract the information from the nested json
            weather_data = {"city": data["location"]["name"],
                            "country": data["location"]["country"],
                            "condition": data["current"]["condition"]["text"],
                            "temp_celsius": data["current"]["temp_c"],
                            "temp_feels_like_celsius": data["current"]["feelslike_c"],
                            "wind_kph": data["current"]["wind_kph"],
                            "humidity": data["current"]["humidity"],
                            "datetime": datetime.strptime(data["location"]["localtime"], "%Y-%m-%d %H:%M")
                            }                           
            
            return weather_data

        except KeyError as ke:
            logging.error("Missing mandatory field: {ke}")
            sys.exit(1)

    else:
        logging.error(f"Response had the following status code: {response.status_code}")
        sys.exit(1)

if __name__=="__main__":
    # print(get_stock__data("AAPL"))
    # print(get_newsapi_news("in"))
    # print("\n\n")
    # print(get_newsdataio_news())
    # print(get_crypto_exchange_data())
    # print(get_exchange_rates())
    # print(get_weather_data("Chennai"))

    print(get_stock_data_market_stack())

    # TODO: Maybe use finnhub API for getting stock info instead of AlphaVantage since it offers real time and has a high limit of 30 API calls per second instead of 25 API calls per day with Alpha Vantage