from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[Email("Некорректный email")])
    psw = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=4, max=100,
                                                                       message="Пароль должен содержать от 4 до 100 символов")])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    name = StringField('Имя: ',
                       validators=[Length(min=1, max=100, message='В имени должно быть как минимум 3 символа')])
    surname = StringField('Фамилия: ',
                          validators=[Length(min=1, max=100, message='В фамилии должно быть как минимум 3 символа')])
    city: StringField = StringField('Город проживания: ',
                       validators=[Length(min=2, max=100, message='Название города как минимум из 2 символов')])
    age = IntegerField('Возраст: ',
                       validators=[NumberRange(min=6, max=150)])
    email = StringField('Email: ', validators=[Email("Некорректный email")])
    psw_1 = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=4, max=100,
                                                                         message="Пароль должен содержать от 4 до 100 символов")])
    psw_2 = PasswordField("Повтор пароля: ",
                          validators=[DataRequired(), EqualTo('psw_1', message="Пароли не совпадают")])
    submit = SubmitField("Регистрация")


class ExpensesForm(FlaskForm):
    category = StringField('Категория: ',
                       validators=[Length(min=1, max=100, message='Катего')])
    aim = StringField('Назначение платежа: ',
                          validators=[Length(min=1, max=250)])
    amount = DecimalField('Сумма: ', places=2)
    date = DateField('Дата платежа: ')
    submit = SubmitField("Добавить платеж")