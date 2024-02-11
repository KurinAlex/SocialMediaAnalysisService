# SocialMediaAnalysisService

## Installation

Copy this repository code to your project using any way you're used to.

After that run the following command in the project directory:

```
pip install -r requirements.txt
```

## Backend

Backend is represented as a Python module, which contains a lot of customizable functions and classes.

### Entries

Entries are the classes, that are used by API functions as data transfer objects:

- DataEntry represents article data, needed for NLP analysis.
- AnalysisEntry represents NLP analysis result data for articles, published on certain date.
- FeedEntry represents RSS Feed entry data.

### Data Providers

Data Providers are the classes, inherited from DataProvider class, which declares two useful methods that are used for retrieving data for NLP analysis and RSS Feed accordingly:

```
def load_data(
    self,
    keyword: str,
    min_published_date: date,
    max_items: int) -> list[DataEntry]

def load_feed(
    self,
    keyword: str,
    min_published_date: date,
    max_items: int) -> list[FeedEntry]
```

This provides a great flexibility for user to implement their own data providers for their needs.

Backend already have two implemented Data Providers: 
- NewsApiDataProvider for retrieving data from NewsAPI (https://newsapi.org/).
- EventRegistryDataProvider for retrieving data from EventRegistry (https://eventregistry.org/).

API keys for using them are located in file Backend/api_keys.py.

### Main Functions
- get_analysis function is used for getting NLP analysis of articles:

```
def get_analysis(
    keyword: str,
    min_post_date: date,
    data_providers: list[DataProvider],
    max_items_per_provider: int) -> dict:
```

- get_feed function is used for getting configurable RSS Feed string:

```
def get_feed(
    keyword: str,
    min_post_date: date,
    data_providers: list[DataProvider],
    max_items_per_provider: int,
    your_link: str) -> str
```

Please refer to Backend directory files for more documentation comments.

### Running

main.py file consists default program for getting RSS Feed for articles about Ukraine, published a week before request date.

In order to run it you can:
- use just Python:

```
python Backend/main.py
```

- or run program in Docker container:

```
docker build -t social-media-analysis-service-image .
docker run social-media-analysis-service-container
```

## Frontend

Frontend is represented as tkinter window application.

On a start it shows main page, which prompts user to enter keyword for search and minimum published date for articles.

After that user can press button 'Analyze' and process of data retrieving and NLP analysis will start.

It may take some time (up to about 30 seconds) for program to finish analysis and show dashboard containing three plots:
- line plot, showing trends of articles sentiment changes over the time interval.
- bar plot, showing top 20 nouns, that were the most frequent in requested articles.
- pie plot, showing distribution of all articles sentiment data.

### Running

In order to run the frontend, run the following shell command:

```
python Frontend/main.py
```

## Unit and Integration Tests

### Running

Run the following command to run unit and integration tests accordingly:

```
python Test/unit_tests.py
python Test/integration_tests.py
```
