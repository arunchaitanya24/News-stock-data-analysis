import re
from textblob import TextBlob
import csv
import requests
from requests.compat import urljoin
import urllib


def clean_article(article):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", article).split())


def get_article_sentiment(article):
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_article(article))
    print(analysis.sentiment)
    if analysis.sentiment.polarity > 0:
        sentiment = 'positive'
    elif analysis.sentiment.polarity == 0:
        sentiment = 'neutral'
    else:
        sentiment = 'negative'

    return [sentiment, analysis.sentiment.polarity, analysis.sentiment.subjectivity]


def get_article_entity_symbols(ents):
    article_entites = ents.split(',')
    symbols = []
    for entity in article_entites:
        stock_symbol = get_stock_name_for_company(entity)
        if stock_symbol:
            symbols.append(stock_symbol)

    if len(symbols) > 0:
        if len(symbols) > 1:
            return ",".join(symbols)
        else:
            return symbols[0]


def get_stock_name_for_company(entity):
    base = 'https://query2.finance.yahoo.com/v1/finance/search'
    other_query = "&quotesCount=3&newsCount=0&quotesQueryId=tss_match_phrase_query&" \
                   "multiQuoteQueryId=multi_quote_single_token_query&newsQueryId=news_ss_symbols" \
                   "&enableCb=false&enableNavLinks=false"
    encode_entity = urllib.parse.quote(entity)
    url_query = urljoin(base, '?q='+encode_entity+other_query)
    print(url_query)
    request = requests.get(url_query)
    if request.status_code == 200:
        data = request.json()
        if data['quotes']:
            quotes = data['quotes']
            for quote in quotes:
                if quote['quoteType']:
                    quote_type = quote['quoteType']
                    if quote_type == 'EQUITY':
                        return quote['symbol']
                        exit()
        else:
            print('no data returned')


# get articles from `.csv` and returns an `order_dictonary_list`
def get_articles():
    with open('sample_ent.csv', newline='') as csvfile:
        articles_data = csv.DictReader(csvfile)
        articles_list = []
        for article in articles_data:
            articles_list.append(article)
    return articles_list


def perform_analysis():
    # Get articles list
    articles = get_articles()

    # An array of entity recognised articles.
    analyse_articles = []
    i = 0
    # Looping articles for sentiment analysis
    for article in articles:
        i = i + 1
        print(i)
        entity_symbols = get_article_entity_symbols(article['ents'])
        if entity_symbols:
            article["symbol"] = entity_symbols
            # Get summary from article
            summary = article["summary"]
            # print(get_article_sentiment(summary))
            article_sentiment = get_article_sentiment(summary)
            article["sentiment"] = article_sentiment[0]
            article["polarity"] = article_sentiment[1]
            article["subjectivity"] = article_sentiment[2]
            analyse_articles.append(article)

    return analyse_articles


# Main

analysed_articles = perform_analysis()
# Get Keys to est header to csv
keys = analysed_articles[0].keys()
# Create a new csv with entity list
with open('sample_analysed_articles.csv', 'w+') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(analysed_articles)
