import json
import urllib.error
import urllib.parse
import urllib.request

from .api import API, Article, Articles

class CoolBananasAPI(API):

    def query(self, rics, topics, start_date, end_date):
        params = {
            'InstrumentIDs': ','.join(rics),
            'TopicCodes': ','.join(topics),
            'StartDate': start_date,
            'EndDate': end_date
        }

        encoded = []
        for key, value in params.items():
            encoded.append(key + '=' + urllib.parse.quote(value))

        url = 'https://nickr.xyz/coolbananas/api/?' + '&'.join(encoded)

        try:
            with urllib.request.urlopen(url) as conn:
                raw = conn.read()
        except urllib.error.HTTPError as error:
            with error:
                raw = error.read().decode()

        data = json.loads(raw)

        if not data['success']: # something failed
            return Articles(False, error = data['error'])

        article_list = data['NewsDataSet']
        articles = []

        for article in article_list:
            rics = article['InstrumentIDs']
            topics = article['TopicCodes']
            timestamp = article['TimeStamp']
            headline = article['Headline']
            body = article['NewsText']
            articles.append(Article(rics, topics, timestamp, headline, body))

        return Articles(True, articles = articles, time = data['query_time'])