# News-stock-data-analysis

  The aim of this project to coorelate the change in stock price of respective entity, to news article published on the same day.
 
 ![alt text](https://github.com/arunchaitanya24/News-stock-data-analysis/blob/develop/project/System_framework.png)

Minor thesis is published in ADMA 2019 under short paper category [Article Link](https://link.springer.com/chapter/10.1007/978-3-030-35231-8_24)
## Web scraping for news articles.

  For getting news articles, REUTERS site is been scraped to getting around 19000 news article data set.
  please refere `reuters_web_scraping.py`
  
## Name Entity Recognition - NER

  To perform NER [spaCy](https://spacy.io/) an NLP pipe line is used to extract the company names listed in the new articles.
  
## Sentiment Analysis

[TextBlob](https://textblob.readthedocs.io/en/dev/#) is used to identify the polaity of the sentences.

## Yahoo Finance API

- Searching Entity Symbols : [Example Symbol Search for Apple](https://query2.finance.yahoo.com/v1/finance/search?q=Apple&quotesCount=3&newsCount=0&quotesQueryId=tss_match_phrase_query&multiQuoteQueryId=multi_quote_single_token_query&newsQueryId=news_ss_symbols&enableCb=false&enableNavLinks=false)

  To get the stock quote, first the extracted names from the articles are searched in yahoo finance for the symbols of the stock listed on stock markets.

- Getting stock quote: [Example Stock qoute for apple news article published on April 3 2019](https://query2.finance.yahoo.com/v8/finance/chart/AAPL?formatted=true&lang=en-US&region=us&period1=1554210000&period2=1554210000&interval=1d)

  After fetching the stock symbols stock quote of the entities are fetched on the day new article is published using yahoo historical finance data.

## Analysis

  Data Cleansing and transformation are peformed on the data to acqurie data normalisation for performing correlation analysis on the data. To perform correlation analysis, to establish the relation between change in stock price and news article polarity of the news article three types of correlation methods are employeed as following:
      
- Pearson's Correlation
- Kendall's Correlation
- Spearman's Correlation
  
##### Note: This project is done for academic thesis purpose
