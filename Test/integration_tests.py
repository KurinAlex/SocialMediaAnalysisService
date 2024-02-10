from datetime import datetime, timedelta

from unittest import TestCase, main
from parameterized import parameterized

from Frontend.api_keys import news_api_key, event_registry_api_key
from Backend.data_providers import NewsApiDataProvider, EventRegistryDataProvider


class ProvidersIntegrationTests(TestCase):
    @parameterized.expand([50, 100])
    def test_load_data(self, max_items):
        # arrange
        providers = [NewsApiDataProvider(news_api_key), EventRegistryDataProvider(event_registry_api_key)]
        min_date = datetime.now().date() - timedelta(days=7)

        # act
        data_array = \
            [provider.load_data('test', min_date, max_items=max_items) for provider in providers]

        # assert
        for data in data_array:
            self.assertLessEqual(len(data), max_items)
            for d in data:
                self.assertGreaterEqual(d.date, min_date)
                self.assertIsNotNone(d.text)


if __name__ == '__main__':
    main()
