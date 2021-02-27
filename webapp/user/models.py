from webapp.db import db
from flask import jsonify
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    status = db.Column(db.String(5), nullable=False)
    email = db.Column(db.String(128))

    def check_password(self, password):
        return jsonify(check_password_hash(self.password, password))

    @property
    def is_admin(self):
        return self.status == 'admin'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f'Пользователь {self.id} - {self.username}'
