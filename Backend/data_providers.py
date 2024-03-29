from datetime import date

from eventregistry import EventRegistry, QueryArticlesIter
from newsapi import NewsApiClient
from pandas import DataFrame, to_datetime

from Backend.entries import DataEntry, FeedEntry


class DataProvider:
    """
    Provides a base class for all news posts data providers.
    """

    def load_data(self, keyword: str, min_published_date: date, max_items: int) -> list[DataEntry]:
        """
        Loads data from underlying API and returns data as a list of DataEntry objects.

        :param keyword: keyword/phrase to do search on
        :param min_published_date: minimum published date for articles
        :param max_items: max number of articles to retrieve
        :return: list of DataEntry objects
        """
        pass

    def load_feed(self, keyword: str, min_published_date: date, max_items: int) -> list[FeedEntry]:
        """
        Loads data from underlying API and returns data as a list of FeedEntry objects.

        :param keyword: keyword/phrase to do search on
        :param min_published_date: minimum published date for articles
        :param max_items: max number of articles to retrieve
        :return: list of FeedEntry objects
        """
        pass


class NewsApiDataProvider(DataProvider):
    """
    Encapsulates data retrieving from NewsAPI (https://newsapi.org/).

    Attributes:
    - client (NewsApiClient): API Client for NewsAPI.
    """

    def __init__(self, api_key: str):
        """
        Constructor for NewsApiDataProvider. Inits NewsApiClient from provided API key.

        :param api_key: API key for NewsAPI.
        """

        self.client = NewsApiClient(api_key=api_key)

    def load_data(self, keyword: str, min_published_date: date, max_items: int) -> list[DataEntry]:
        # construct data frame from all articles
        articles = self.get_articles(keyword, min_published_date, max_items)
        df = DataFrame(articles)

        # transform articles text and date data
        df['date'] = to_datetime(df['publishedAt']).dt.date
        df = df[df['date'] >= min_published_date]
        df['text'] = df['description'].fillna(df['content'])
        return [DataEntry(r['date'], r['text']) for _, r in df.iterrows()]

    def load_feed(self, keyword: str, min_published_date: date, max_items: int) -> list[FeedEntry]:
        # construct data frame from all articles
        articles = self.get_articles(keyword, min_published_date, max_items)
        df = DataFrame(articles)

        # transform articles text and date data
        df['date'] = to_datetime(df['publishedAt']).dt.date
        df['description'] = df['description'].fillna(df['content'])
        return [FeedEntry(r['title'], r['url'], r['description'], r['date']) for _, r in df.iterrows()]

    def get_articles(self, keyword: str, min_published_date: date, max_items: int) -> list[dict]:
        articles = []  # list of all retrieved articles
        page = 1  # current page

        # because of pagination, we do get requests until we loaded max_items articles or loaded them all
        while True:

            # request for current page
            data = self.client.get_everything(q=keyword,
                                              from_param=min_published_date,
                                              page=page,
                                              page_size=min(100, max_items - len(articles)),
                                              language='en')

            # add articles and move to the next page
            articles += data['articles']
            page += 1

            # break if we loaded all available articles or reached the max_items limit
            articles_len = len(articles)
            if articles_len >= data['totalResults'] or articles_len >= max_items:
                break

        return articles


class EventRegistryDataProvider(DataProvider):
    """
    Encapsulates data retrieving from EventRegistry (https://eventregistry.org/)

    Attributes:
    - event_registry (EventRegistry): API Client for EventRegistry.
    """

    def __init__(self, api_key: str) -> None:
        """
        Constructor for EventRegistry. Inits EventRegistry from provided API key.

        :param api_key: API key for EventRegistry.
        """

        self.event_registry = EventRegistry(apiKey=api_key)

    def load_data(self, keyword: str, min_published_date: date, max_items: int) -> list[DataEntry]:
        # construct data frame from all articles
        articles = self.get_articles(keyword, min_published_date, max_items)
        df = DataFrame(articles)

        # transform articles date data
        df['date'] = to_datetime(df['date']).dt.date
        df = df[df['date'] >= min_published_date]
        return [DataEntry(r['date'], r['body']) for _, r in df.iterrows()]

    def load_feed(self, keyword: str, min_published_date: date, max_items: int) -> list[FeedEntry]:
        # construct data frame from all articles
        articles = self.get_articles(keyword, min_published_date, max_items)
        df = DataFrame(articles)

        # transform articles date data
        df['date'] = to_datetime(df['date']).dt.date
        return [FeedEntry(r['title'], r['url'], r['body'], r['date']) for _, r in df.iterrows()]

    def get_articles(self, keyword: str, min_published_date: date, max_items: int) -> list[dict]:
        # create query parameters
        q = QueryArticlesIter(keywords=keyword,
                              lang='eng',
                              dateStart=min_published_date.strftime('%Y-%m-%d'))

        # execute query and move all received articles to list
        return list(q.execQuery(self.event_registry, maxItems=max_items))
