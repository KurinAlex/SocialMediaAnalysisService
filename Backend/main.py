from collections import Counter
from datetime import date, timedelta
from feedgenerator import Rss201rev2Feed

from textblob import TextBlob

from Backend.api_keys import news_api_key, event_registry_api_key
from Backend.data_providers import DataProvider, NewsApiDataProvider, EventRegistryDataProvider
from Backend.entries import AnalysisEntry


def get_analysis(
        keyword: str,
        min_post_date: date,
        data_providers: list[DataProvider],
        max_items_per_provider: int) -> dict:
    """
    Loads data from data providers, does NLP analysis on it and returns summary results of analysis.

    :param keyword: keyword/phrase to do search on.
    :param min_post_date: minimum published date for articles.
    :param data_providers: list of DataProvider object, from which data must be loaded.
    :param max_items_per_provider: max number of articles to retrieve from every data providers.
    :return: dictionary in format:
     {
        'total':
        {
            'count': int,
            'positive': int,
            'negative': int,
            'neutral': itn
        },
        'daily':
        {
            'dates': [datetime.date],
            'count': [int],
            'positive': [int],
            'negative': [int],
            'neutral': [int],
        },
        'top20_nouns':
        {
            'nouns': [str],
            'count': [int],
        }
    }
    """

    # load DataEntry lists from every provider and concatenate them
    entries = sum([provider.load_data(keyword, min_post_date, max_items_per_provider)
                   for provider in data_providers], [])

    total_entry = AnalysisEntry()  # entry for holding total statistics data
    dates_entries = {}  # dictionary of AnalysisEntry for every date
    noun_phrases = []  # list of all nouns, recognized in articles

    # do analysis for every DataEntry
    for data_entry in entries:
        # receive or create new DataEntry for certain day
        entry = dates_entries.setdefault(data_entry.date, AnalysisEntry())

        # do NLP analysis for article text
        blob = TextBlob(data_entry.text)

        # get text sentiment data
        if blob.sentiment.polarity > 0.2:
            entry.positive_count += 1
            total_entry.positive_count += 1
        elif blob.sentiment.polarity < -0.2:
            entry.negative_count += 1
            total_entry.negative_count += 1
        else:
            entry.neutral_count += 1
            total_entry.neutral_count += 1

        # increase total counts
        entry.total_count += 1
        total_entry.total_count += 1

        # add recognized nouns to nouns list
        noun_phrases += blob.noun_phrases

    # sort dates_entries by date
    dates_entries = dict(sorted(dates_entries.items()))
    most_common_nouns = Counter(noun_phrases).most_common(20)

    # return summary data of NLP
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
        'top20_nouns': {
            'nouns': [item[0] for item in most_common_nouns],
            'count': [item[1] for item in most_common_nouns],
        }
    }


def get_feed(
        keyword: str,
        min_post_date: date,
        data_providers: list[DataProvider],
        max_items_per_provider: int,
        your_link: str) -> str:
    """
    Loads data from data providers and builds RSS Feed out of articles data.

    :param keyword: keyword/phrase to do search on.
    :param min_post_date: minimum published date for articles.
    :param data_providers: list of DataProvider object, from which data must be loaded.
    :param max_items_per_provider: max number of articles to retrieve from every data providers.
    :param your_link: link to you RSS feed page.
    :return: RSS Feed string
    """

    feed = Rss201rev2Feed(
        title=f'{keyword} articles',
        link=your_link,
        description=f'Feed for articles, mentioning {keyword} since {min_post_date}.',
        language='en'
    )

    # load DataEntry lists from every provider and concatenate them
    entries = sum([provider.load_feed(keyword, min_post_date, max_items_per_provider)
                   for provider in data_providers], [])

    for entry in entries:
        feed.add_item(
            title=entry.title,
            link=entry.url,
            description=entry.description,
            pubdate=entry.pubdate,
        )

    return feed.writeString('utf-8')


if __name__ == '__main__':
    default_keyword = 'Ukraine'
    date = date.today() - timedelta(days=7)
    providers = [NewsApiDataProvider(news_api_key), EventRegistryDataProvider(event_registry_api_key)]
    rss_feed = get_feed(default_keyword, date, providers, 100, '/articles/')
    print(rss_feed)
