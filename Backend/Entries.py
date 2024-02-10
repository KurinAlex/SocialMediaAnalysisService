from datetime import date


class DataEntry:
    def __init__(self, post_date: date, text: str):
        self.date = post_date
        self.text = text


class AnalysisEntry:
    def __init__(self):
        self.total_count = 0
        self.positive_count = 0
        self.neutral_count = 0
        self.negative_count = 0
