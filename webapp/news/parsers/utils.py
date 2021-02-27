from webapp.db import db
from webapp.news.models import News
import requests


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def save_news(url, title, date):
    check = News.query.filter(News.url == url).count()
    print(check)
    if not check:
        new_news = News(title=title, url=url, date=date)
        db.session.add(new_news)
        db.session.commit()
