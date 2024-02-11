from datetime import date


class DataEntry:
    """
    A class for holding data for single news post.

    Attributes:
    - date (datetime.date): Publishing date of news post.
    - text (datetime.date): Main text of news post.
    """

    def __init__(self, post_date: date, text: str):
        """
        Constructor for DataEntry.

        :param post_date: Publishing date of news post.
        :param text: Main text of news post.
        """

        self.date = post_date
        self.text = text


class AnalysisEntry:
    """
    A class for holding NLP analysis results for certain date.

    Attributes:
    - total_count (int): Total count of news posts.
    - positive_count (int): Number of posts with positive sentiment.
    - neutral_count (int): Number of posts with neutral sentiment.
    - negative_count (int): Number of posts with negative sentiment.
    """

    def __init__(self):
        """
        Constructor for DataEntry. Sets all attributes to 0.
        """

        self.total_count = 0
        self.positive_count = 0
        self.neutral_count = 0
        self.negative_count = 0


class FeedEntry:
    """
    A class for RSS Feed entry data.

    Attributes:
    - title (str): Article title.
    - link (str): Article link.
    - description (str): Article description.
    - pubdate (datetime.date): Article date of publishing.
    """

    def __init__(self, title: str, link: str, description: str, pubdate: date):
        """
        Constructor for DataEntry. Sets all attributes to 0.
        """

        self.title = title
        self.url = link
        self.description = description
        self.pubdate = pubdate
