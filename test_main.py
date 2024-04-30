import unittest
from unittest.mock import patch
from main import *


class TestWeatherApp(unittest.TestCase):
    def test_setup_logging(self):
        setup_logging()

        root_logger = logging.getLogger()
        handlers = root_logger.handlers

        self.assertTrue(handlers)

        # self.assertIsInstance(handlers[0], logging.handlers.RotatingFileHandler)

    @patch('requests.get')
    def test_get_weather(self, mock_get):
        mock_response_success = unittest.mock.Mock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = {'cod': '200', 'list': []}

        mock_response_failure = unittest.mock.Mock()
        mock_response_failure.status_code = 404

        mock_get.return_value = mock_response_success
        weather_data_success = get_weather("18031", api_key)
        self.assertIsNotNone(weather_data_success)

        # mock_get.return_value = mock_response_failure
        # weather_data_failure = get_weather("90733", api_key)
        # self.assertIsNone(weather_data_failure)


if __name__ == '__main__':
    unittest.main()
