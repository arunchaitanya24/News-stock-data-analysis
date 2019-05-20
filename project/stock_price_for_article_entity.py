import requests
from requests.compat import urljoin
import pytz
import datetime


def get_stock(symbol, published_date):
    timestamp = convert_date_to_timestamp(published_date)
    base = 'https://query2.finance.yahoo.com/v8/finance/chart/'
    other_query = "?formatted=true&lang=en-US&region=us&"
    period1 = 'period1='+timestamp
    period2 = '&period2='+timestamp+'&interval=1d'
    url_query = urljoin(base, symbol+other_query+period1+period2)
    print(url_query)
    request = requests.get(url_query)
    if request.status_code == 200:
        map_stock_data(request)
    else:
        print('request: no data return')


def map_stock_data(request):
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
                        percentage_change_in_stock(stock_quote['open'], stock_quote['close'])
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

    change_in_stocks = closing_price/opening_price
    print(opening_price, ",", closing_price)
    if change_in_stocks < 1:
        print('neg')
    if change_in_stocks > 1:
        print('pos')

    print(change_in_stocks)
    print(1 - change_in_stocks)


def convert_date_to_timestamp(date):
    date_obj = datetime.datetime.strptime(date, '%b %d %Y')
    zone = pytz.timezone('America/New_York')
    timezone_date_time_obj = zone.localize(date_obj).timestamp()
    timestamp = int(timezone_date_time_obj)
    return str(timestamp)


get_stock("", 'May 17 2019')

