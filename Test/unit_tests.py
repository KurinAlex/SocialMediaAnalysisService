from datetime import date
from unittest import TestCase, main
from unittest.mock import patch

from eventregistry import QueryArticlesIter
from newsapi import NewsApiClient

from Backend.data_providers import NewsApiDataProvider, EventRegistryDataProvider
from Backend.entries import DataEntry, AnalysisEntry, FeedEntry
from Backend.main import get_analysis

newsapi_test_data = [
    {
        'articles': [
            {
                'publishedAt': '2022-01-01T12:00:00Z',
                'description': 'Test description 1',
                'content': 'Test content 1'
            }
        ],
        'totalResults': 3
    },
    {
        'articles': [
            {
                'publishedAt': '2022-01-02T12:00:00Z',
                'description': 'Test description 2',
                'content': None
            }
        ],
        'totalResults': 3
    },
    {
        'articles': [
            {
                'publishedAt': '2022-01-03T12:00:00Z',
                'description': None,
                'content': 'Test content 3'
            }
        ],
        'totalResults': 3
    }
]

eventregistry_test_data = [
    {'date': '2022-01-01T12:00:00Z', 'body': 'Test article'},
    {'date': '2022-01-02T12:00:00Z', 'body': 'Test article 2'},
    {'date': '2022-01-03T12:00:00Z', 'body': 'Test article 3'}
]

entries_test_data = [
    DataEntry(date(2022, 1, 1), 'Test text 1'),
    DataEntry(date(2022, 1, 2), 'Test text 2'),
    DataEntry(date(2022, 1, 3), 'Test text 3'),
]


class DataEntryTests(TestCase):
    def test_data_entry_creation(self):
        data_entry = DataEntry(date(2022, 1, 1), 'Test text')
        self.assertEqual(data_entry.date, date(2022, 1, 1))
        self.assertEqual(data_entry.text, 'Test text')


class AnalysisEntryTests(TestCase):
    def test_data_entry_creation(self):
        data_entry = AnalysisEntry()
        self.assertEqual(data_entry.total_count, 0)
        self.assertEqual(data_entry.positive_count, 0)
        self.assertEqual(data_entry.neutral_count, 0)
        self.assertEqual(data_entry.negative_count, 0)


class FeedEntryTests(TestCase):
    def test_feed_entry_creation(self):
        feed_entry = FeedEntry('Title', 'URL', 'Description', date(2020, 1, 1))
        self.assertEqual(feed_entry.title, 'title')
        self.assertEqual(feed_entry.url, 'URL')
        self.assertEqual(feed_entry.description, 'Description')
        self.assertEqual(feed_entry.pubdate, date(2020, 1, 1))


class NewsApiDataProviderTests(TestCase):
    @patch.object(NewsApiClient, 'get_everything')
    def test_load_data(self, mock_get_everything):
        # arrange
        mock_get_everything.side_effect = newsapi_test_data
        news_api_data_provider = NewsApiDataProvider(api_key='api key')

        # act
        data_entries = news_api_data_provider.load_data(
            'test',
            date(2022, 1, 1),
            10)

        # assert
        self.assertEqual(len(data_entries), 3)
        self.assertEqual(data_entries[0].date, date(2022, 1, 1))
        self.assertEqual(data_entries[0].text, 'Test description 1')
        self.assertEqual(data_entries[1].date, date(2022, 1, 2))
        self.assertEqual(data_entries[1].text, 'Test description 2')
        self.assertEqual(data_entries[2].date, date(2022, 1, 3))
        self.assertEqual(data_entries[2].text, 'Test content 3')
        for p in range(1, 3):
            mock_get_everything.asser_any_call(
                q='test',
                from_param=date(2022, 1, 1),
                page=p,
                language='en')

    @patch.object(NewsApiClient, 'get_everything')
    def test_load_data_max_items_overflow(self, mock_get_everything):
        # arrange
        mock_get_everything.side_effect = newsapi_test_data
        news_api_data_provider = NewsApiDataProvider(api_key='api key')

        # act
        data_entries = news_api_data_provider.load_data(
            'test',
            date(2022, 1, 1),
            2)

        # assert
        self.assertEqual(len(data_entries), 2)
        for p in range(1, 2):
            mock_get_everything.asser_any_call(
                q='test',
                from_param=date(2022, 1, 1),
                page=p,
                language='en')


class EventRegistryDataProviderTests(TestCase):
    @patch.object(QueryArticlesIter, 'execQuery', return_value=eventregistry_test_data)
    def test_load_data(self, mock_exec_query):
        # arrange
        event_registry_data_provider = EventRegistryDataProvider('api key')

        # act
        data_entries = event_registry_data_provider.load_data(
            'test',
            date(2022, 1, 1),
            10)

        # assert
        self.assertEqual(len(data_entries), 3)
        self.assertEqual(data_entries[0].date, date(2022, 1, 1))
        self.assertEqual(data_entries[0].text, 'Test article')
        self.assertEqual(data_entries[1].date, date(2022, 1, 2))
        self.assertEqual(data_entries[1].text, 'Test article 2')
        self.assertEqual(data_entries[2].date, date(2022, 1, 3))
        self.assertEqual(data_entries[2].text, 'Test article 3')


class MainTests(TestCase):
    @patch('Backend.DataProviders.NewsApiDataProvider')
    @patch('Backend.DataProviders.EventRegistryDataProvider')
    def test_get_analysis(self, newsapi_provider_mock, eventregistry_mock):
        # arrange
        mock_newsapi_instance = newsapi_provider_mock.return_value
        mock_event_registry_instance = eventregistry_mock.return_value
        mock_newsapi_instance.load_data.return_value = entries_test_data
        mock_event_registry_instance.load_data.return_value = entries_test_data

        # act
        data_entries = get_analysis(
            'test',
            date(2022, 1, 1),
            [mock_newsapi_instance, mock_event_registry_instance],
            10
        )

        # assert
        self.assertEqual(data_entries['total']['count'], 6)
        self.assertEqual(len(data_entries['daily']['dates']), 3)
        self.assertEqual(len(data_entries['daily']['count']), 3)
        self.assertLessEqual(len(data_entries['top20_nouns']['nouns']), 20)
        self.assertLessEqual(len(data_entries['top20_nouns']['count']), 20)


if __name__ == '__main__':
    main()
