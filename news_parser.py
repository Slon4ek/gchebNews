from typing import Dict

import requests
from bs4 import BeautifulSoup

st_accept = "text/html"
st_useragent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15")

HEADERS = {
    "Accept": st_accept,
    "User-Agent": st_useragent
}


def get_news_text(url):
    response = requests.get(url, headers=HEADERS, timeout=5)
    soup = BeautifulSoup(response.text, 'lxml')
    text = soup.find_all('div', class_='news_text')
    news_text = text[0].text
    return news_text


def get_news() -> Dict:
    response = requests.get('https://gcheb.cap.ru/news/?type=news', headers=HEADERS)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        news = soup.find_all('div', class_='item_news')
        full_news: Dict[int, Dict] = dict()
        count = 1
        for n in news:
            href = n.find('a')['href']
            date = n.find('div', {'class': 'news-list_date'}).text
            title = n.find('a', {'class': 'news-list_title'}).text

            full_href = 'https://gcheb.cap.ru' + href
            news_text = get_news_text(full_href)
            full_news[count] = {
                'title': title,
                'href': full_href,
                'date': date,
                'news_text': news_text
            }
            count += 1
        return full_news
