import requests
import pytz
import csv
import datetime
from requests.compat import urljoin


def get_stock(symbol, published_date):
    timestamp = convert_date_to_timestamp(published_date)
    base = 'https://query2.finance.yahoo.com/v8/finance/chart/'
    other_query = "?formatted=true&lang=en-US&region=us&"
    period1 = 'period1='+timestamp
    period2 = '&period2='+timestamp+'&interval=1d'
    url_query = urljoin(base, symbol+other_query+period1+period2)
    print(symbol)
    request = requests.get(url_query)
    if request.status_code == 200:
        return map_stock_data(request, symbol)
    else:
        print('request: no data return')


# Splits the multiple entity names and sets the symbols
# After getting the symbols join them with ',' and return a string.
def get_stock_movement(symbols, published_date):
    entities_symbol = symbols.split(',')
    stock_data = []
    for symbol in entities_symbol:
        stock = get_stock(symbol, published_date)
        if stock:
            stock_data.append(stock)
    return stock_data


def map_stock_data(request, symbol):
    data = request.json()
    if data['chart']:
        stock_data = data['chart']
        if stock_data['result']:
            result = stock_data['result'][0]
            if result['indicators']:
                stock_indicator = result['indicators']
                if stock_indicator['quote']:
                    quote = stock_indicator['quote']
                    if quote[0]:
                        stock_quote = map_stock_quote(quote[0])
                        change = percentage_change_in_stock(stock_quote['open'], stock_quote['close'])
                        return {
                            'symbol': symbol,
                            'open_quote': stock_quote['open'],
                            'close_quote': stock_quote['close'],
                            'percentage_change': change[1],
                            'movement': change[0]
                        }
                    else:
                        print('Quote: empty')
                else:
                    print('Indicator: empty')


# returns stock quote eg:-
# high quote on the day.
# low quote on the day.
# opening quote on the day.
# closing quote on the day.
def map_stock_quote(quote):

    stock_quote = {}

    if quote['high']:
        high_quote = quote['high'][0]
        stock_quote['high'] = high_quote
    else:
        print('high quote: not returned')

    if quote['open']:
        open_quote = quote['open'][0]
        stock_quote['open'] = open_quote
    else:
        exit()
        print('high quote: not returned')

    if quote['low']:
        low_quote = quote['low'][0]
        stock_quote['low'] = low_quote
    else:
        print('low quote: not returned')

    if quote['close']:
        close_quote = quote['close'][0]
        stock_quote['close'] = close_quote
    else:
        print('low quote: not returned')

    return stock_quote


def percentage_change_in_stock(opening_price, closing_price):
    change_in_stocks = ((closing_price - opening_price) / opening_price) * 100
    # print(opening_price, ",", closing_price)
    stock_movement = ''
    if change_in_stocks < 0:
        stock_movement = 'neg'
    if change_in_stocks > 0:
        stock_movement = 'pos'
    return stock_movement, "%.3f" % change_in_stocks


def convert_date_to_timestamp(date):
    date_obj = datetime.datetime.strptime(date, '%b %d %Y')
    zone = pytz.timezone('America/New_York')
    timezone_date_time_obj = zone.localize(date_obj).timestamp()
    timestamp = int(timezone_date_time_obj)
    return str(timestamp)


# get articles from `.csv` and returns an `order dictionary list`.
def get_articles():
    with open('data/analysed_art_symbols_sentiment.csv', newline='') as csvfile:
        articles_data = csv.DictReader(csvfile)
        articles_list = []
        for article in articles_data:
            articles_list.append(article)
    return articles_list


# Perform sentiment analysis only when entity symbol identified.
def perform_analysis():
    # Get articles list
    articles = get_articles()

    # An array of entity recognised articles.
    analyse_articles = []
    i = 0
    # Looping articles for sentiment analysis
    for article in articles:
        i = i + 1
        print('\n' ,i)
        stock_data = get_stock_movement(article['symbol'], article['time'])
        for data in stock_data:
            art_new = {}
            # print(data)
            if data:
                print(article)
                art_new['title'] = article['title']
                art_new['summary'] = article['summary']
                art_new['time'] = article['time']
                art_new['entities'] = article['ents']
                art_new['sentiment'] = article['sentiment']
                art_new['polarity'] = article['polarity']
                art_new['subjectivity'] = article['subjectivity']
                art_new["symbol"] = data['symbol']
                art_new["open_quote"] = data['open_quote']
                art_new["close_quote"] = data['close_quote']
                art_new["percentage_change"] = data['percentage_change']
                art_new['movement'] = data['movement']
                analyse_articles.append(art_new)
    return analyse_articles


# Main
analysed_articles = perform_analysis()
# Get Keys to est header to csv
keys = analysed_articles[0].keys()
# Create a new csv with entity list
with open('quote_listed_articles.csv', 'w+') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(analysed_articles)
    print('Success')
    
