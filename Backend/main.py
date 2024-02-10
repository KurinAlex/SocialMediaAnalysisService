from textblob import TextBlob
from datetime import date, timedelta, datetime
from Backend.Entries import AnalysisEntry
from Backend.DataProviders import NewsApiDataProvider, EventRegistryDataProvider, DataProvider
from collections import Counter
from logging import basicConfig, DEBUG


default_data_providers = [
    NewsApiDataProvider('e9e5d64799184c1cb15e53c9dc284e19'),
    EventRegistryDataProvider('cf2085b4-29da-4055-b75f-34d23549993a')
]

default_max_items_per_provider = 100


def get_default_analysis(keyword: str, min_post_date: date) -> dict:
    return get_analysis(keyword, min_post_date, default_data_providers, default_max_items_per_provider)


def get_analysis(keyword: str,
                 min_post_date: date,
                 data_providers: list[DataProvider],
                 max_items_per_provider: int) -> dict:

    entries = sum([provider.load_data(keyword, min_post_date, max_items_per_provider)
                   for provider in data_providers], [])

    total_entry = AnalysisEntry()
    dates_entries = {}
    noun_phrases = []
    for data_entry in entries:
        entry = dates_entries.setdefault(data_entry.date, AnalysisEntry())

        blob = TextBlob(data_entry.text)
        if blob.sentiment.polarity > 0:
            entry.positive_count += 1
            total_entry.positive_count += 1
        elif blob.sentiment.polarity < 0:
            entry.negative_count += 1
            total_entry.negative_count += 1
        else:
            entry.neutral_count += 1
            total_entry.neutral_count += 1

        entry.total_count += 1
        total_entry.total_count += 1

        noun_phrases += blob.noun_phrases

    dates_entries = dict(sorted(dates_entries.items()))

    return {
        'total': {
            'count': total_entry.total_count,
            'positive': total_entry.positive_count,
            'negative': total_entry.negative_count,
            'neutral': total_entry.neutral_count
        },
        'daily': {
            'dates': [published_date for published_date in dates_entries.keys()],
            'count': [entry.total_count for entry in dates_entries.values()],
            'positive': [entry.positive_count for entry in dates_entries.values()],
            'negative': [entry.negative_count for entry in dates_entries.values()],
            'neutral': [entry.neutral_count for entry in dates_entries.values()],
        },
        'top20_nouns': Counter(noun_phrases).most_common(20)
    }


if __name__ == '__main__':
    basicConfig(level=DEBUG)
    data = get_default_analysis('Ukraine', (datetime.now() - timedelta(days=7)).date())
    print(data)
