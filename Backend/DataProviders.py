from pandas import DataFrame, to_datetime
from datetime import date
from newsapi import NewsApiClient
from Backend.Entries import DataEntry
from eventregistry import EventRegistry, QueryArticlesIter


class DataProvider:
    def load_data(self, keyword: str, min_published_date: date, max_items: int) -> list[DataEntry]:
        pass


class NewsApiDataProvider(DataProvider):
    def __init__(self, api_key: str) -> None:
        self.client = NewsApiClient(api_key=api_key)

    def load_data(self, keyword: str, min_published_date: date, max_items: int) -> list[DataEntry]:
        articles = []
        page = 1

        while True:
            data = self.client.get_everything(q=keyword,
                                              from_param=min_published_date,
                                              page=page,
                                              language='en')

            articles += data['articles']
            page += 1

            articles_len = len(articles)
            if articles_len >= data['totalResults'] or articles_len >= max_items:
                break

        df = DataFrame(articles)
        df['date'] = to_datetime(df['publishedAt']).dt.date
        df['text'] = df['description'].fillna(df['content'])
        return [DataEntry(r['date'], r['text']) for _, r in df.iterrows()]


class EventRegistryDataProvider(DataProvider):
    def __init__(self, api_key: str) -> None:
        self.event_registry = EventRegistry(apiKey=api_key)

    def load_data(self, keyword: str, min_published_date: date, max_items: int) -> list[DataEntry]:
        q = QueryArticlesIter(keywords=keyword,
                              lang='eng',
                              dateStart=min_published_date.strftime('%Y-%m-%d'))
        articles = list(q.execQuery(self.event_registry, maxItems=max_items))

        df = DataFrame(articles)
        df['date'] = to_datetime(df['date']).dt.date
        return [DataEntry(r['date'], r['body']) for _, r in df.iterrows()]
