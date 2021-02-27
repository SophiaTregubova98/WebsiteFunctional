from flask_wtf import FlaskForm
from webapp.user.models import User
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()],
                           render_kw={'class': 'form-control'})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={'class': 'form-control'})
    remember_me = BooleanField('Запомнить меня', default=True,
                               render_kw={'class': 'form-check-input'})
    submit = SubmitField('Войти', render_kw={'class': 'btn btn-success'})


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()],
                           render_kw={'class': 'form-control'})
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={'class': 'form-control'})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={'class': 'form-control'})
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')],
                              render_kw={'class': 'form-control'})
    submit = SubmitField('Зарегистрироваться', render_kw={'class': 'btn btn-success'})

    def validate_username(self, username):
        users_count = User.query.filter_by(username=username.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с таким именем уже существует')

    def validate_email(self, email):
        users_count = User.query.filter_by(email=email.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с такой почтой уже существует')
