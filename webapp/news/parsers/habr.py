from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from webapp.db import db
from webapp.news.models import News
from webapp.news.parsers.utils import get_html, save_news
import locale
import platform


def get_text():
    print('Собираю текста')
    news_without_text = News.query.filter(News.text.is_(None))
    for news in news_without_text:
        print(f'{news.id} - у нее нет текста')
        html = get_html(news.url)
        print(news.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            full = soup.find('div', class_='post__body post__body_full').decode_contents()
            if full:
                news.text = full
                db.session.add(news)
                db.session.commit()


def parse_page(url):
    print('пошел собирать заголовки')
    if platform.system() == 'Windows':
        locale.setlocale(locale.LC_ALL, 'russian')
    else:
        locale.setlocale(locale.LC_TIME, 'ru_RU')

    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('li', class_='content-list__item content-list__item_post shortcuts_item')
        for row in rows:
            try:
                url = row.find('h2').find('a')['href']
                title = row.find('h2').find('a').text
                date = row.find('header', class_='post__meta').find('span', class_='post__time').text
                if 'сегодня' in date:
                    today = datetime.now()
                    date = date.replace('сегодня', today.strftime('%d %B %Y'))
                elif 'вчера' in date:
                    yesterday = datetime.now() - timedelta(days=1)
                    date = date.replace('вчера', yesterday.strftime('%d %B %Y'))
                try:
                    date = datetime.strptime(date, '%d %B %Y в %H:%M')
                except ValueError:
                    date = datetime.now()
                save_news(url, title, date)
            except (AttributeError, TypeError):
                pass
