from getpass import getpass
from webapp import create_app
from webapp.db import db
from webapp.user.models import User
import sys

app = create_app()

with app.app_context():
    username = input('Введите имя пользователя: ')

    if User.query.filter(User.username == username).count():
        print('Такой пользователь уже есть')
        sys.exit(0)

    password = getpass('Введите пароль: ')
    password2 = getpass('Повторите пароль: ')
    if password == password2:
        new_user = User(username=username, status='user')
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        print(new_user.id)
