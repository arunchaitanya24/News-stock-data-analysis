
from urllib.request import urlopen as urlRequest
from bs4 import BeautifulSoup
import pandas as pd


def get_articles_from_reuters(page_number):
    sn_url = 'https://www.reuters.com/news/archive/businessnews?view=page&page='+str(page_number)+'&pageSize=10'
    req = urlRequest(sn_url)
    page = req.read()
    scraping = BeautifulSoup(page, 'lxml')

    # Articles Div block
    article_list_div = scraping.findAll("div", {"class": "column1 col col-10"})[0]
    article_head_line_list = article_list_div.findAll("div", {"class": "news-headline-list"})[0]
    articles_list = []

    for story in article_head_line_list.findAll("article", {"class": "story"}):
        story_content = story.findAll("div", {"class": "story-content"})[0]
        article_data={}
        article_data["title"] = story_content.findAll("h3", {"class": "story-title"})[0].text.replace('\n', '')\
            .replace('\t', '')
        article_data["time"] = story_content.findAll("span", {"class": "timestamp"})[0].text
        article_data["summary"] = story_content.findAll("p")[0].text
        articles_list.append(article_data)

    return articles_list


# Main
if __name__ == '__main__':

    articlesData = {'title': [], 'summary': [], 'time': []}

    # This range can be adjusted to increase/decrease no of new articles.
    # 20 is chosen to nullify and new UI changes.
    for i in range(20, 2000):
        articles = get_articles_from_reuters(i)
        for article in articles:
            print(article)
            articlesData['title'].append(article.get("title", "none"))
            articlesData['summary'].append(article.get("summary", "none"))
            articlesData['time'].append(article.get("time", "none"))
    data = pd.DataFrame(articlesData)
    data.to_csv(r'news_articles.csv', index=False)
    print('Success')
