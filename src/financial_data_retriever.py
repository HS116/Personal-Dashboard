import datetime
import logging
import sys
from typing import Any, Dict, List, Optional

import requests
from util.config import config

import json

def get_stock__data(symbol : str) -> Dict[str, Any]:
    """
    :param symbol: The company or index you would like to get information from AlphaAvantage API e.g. TSLA
    :return: dictionary containing the stock info for that particular symbol e.g. IBM

    For more info about AlphaVantage API documentation: https://www.alphavantage.co/documentation/
    """

    url= f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=60min&apikey={config['AlphaAvantage_api_key']}"

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

if __name__=="__main__":
    print(get_stock__data("AAPL"))


