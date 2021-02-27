from celery import Celery
from celery.schedules import crontab
from webapp import create_app
from webapp.news.parsers import habr

flask_app = create_app()
celery_app = Celery('tasks', broker='redis://[::1]:6379/0')


@celery_app.task
def get_titles():
    with flask_app.app_context():
        habr.parse_page('https://habr.com/ru/news/')


@celery_app.task
def get_texts():
    with flask_app.app_context():
        habr.get_text()


@celery_app.on_after_configure.connect
def setup_period(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/1'), get_titles.s())
    sender.add_periodic_task(crontab(minute='*/2'), get_texts.s())
