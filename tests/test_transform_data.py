# Using pytest helps to reduce boilerplate code compared to using purely unittest module,
# since now we just have to specify the "assert" keyword and don't need to do any inheritance

import unittest
from datetime import datetime
from unittest.mock import Mock, patch

import pytest
import requests

from pipeline.get_data import get_stock_data_alpha_vantage


class TestTransformData(unittest.TestCase):
    @patch('requests.get')
    def test_transform_data(self, mock_get):
        mock_response = Mock()
        response_dict = {
            'Meta Data': {
                '1. Information': 'Intraday (60min) open, high, low, close prices and volume',
                '2. Symbol': 'AAPL',
                '3. Last Refreshed': '2024-01-16 19:00:00',
                '4. Interval': '60min',
                '5. Output Size': 'Compact',
                '6. Time Zone': 'US/Eastern',
            },
            'Time Series (60min)': {
                '2024-01-16 19:00:00': {
                    '1. open': '183.2300',
                    '2. high': '183.4000',
                    '3. low': '183.0000',
                    '4. close': '183.0600',
                    '5. volume': '23893',
                },
                '2024-01-16 18:00:00': {
                    '1. open': '183.3150',
                    '2. high': '183.3800',
                    '3. low': '181.0700',
                    '4. close': '183.2000',
                    '5. volume': '20196',
                },
                '2024-01-16 17:00:00': {
                    '1. open': '183.4300',
                    '2. high': '219.3390',
                    '3. low': '153.3900',
                    '4. close': '183.3150',
                    '5. volume': '89113',
                },
            },
        }
        mock_response.status_code = 200
        mock_response.json.return_value = response_dict

        mock_get.return_value = mock_response

        user_data = get_stock_data_alpha_vantage("AAPL")

        expected_result = [
            {
                'open': 183.23,
                'high': 183.4,
                'low': 183.0,
                'close': 183.06,
                'volume': 23893,
                'datetime': datetime(2024, 1, 16, 19, 0),
                'symbol': 'AAPL',
            },
            {
                'open': 183.315,
                'high': 183.38,
                'low': 181.07,
                'close': 183.2,
                'volume': 20196,
                'datetime': datetime(2024, 1, 16, 18, 0),
                'symbol': 'AAPL',
            },
            {
                'open': 183.43,
                'high': 219.3390,
                'low': 153.39,
                'close': 183.315,
                'volume': 89113,
                'datetime': datetime(2024, 1, 16, 17, 0),
                'symbol': 'AAPL',
            },
        ]

        self.assertEqual(user_data, expected_result)


if __name__ == "__main__":
    unittest.main()
