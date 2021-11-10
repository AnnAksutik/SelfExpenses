from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

menu = [{'url': '/', 'title': 'Главная'},
        {'url': '/about', 'title': 'О сайте'},
        {'url': '/login', 'title': 'Авторизация'}]

# configuration
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
MAX_CONTENT_LENGTH = 1024 * 1024
SQLALCHEMY_DATABASE_URI = 'sqlite:///selfexp.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(__name__)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"

db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).get(user_id)


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    pr = db.relationship('Profiles', backref='users', uselist=False)

    def __repr__(self):
        return f"<users {self.id}>"


class Profiles(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    surname = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer)
    city = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<profiles {self.id}>"


@app.route('/')
def index():
    return render_template('base.html', menu=menu)


@app.route('/about')
def about():
    return 'ЗДЕСЬ ДОЛЖНО БЫТЬ ЧТО-ТО О САЙТЕ'


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.psw, form.psw.data):
            rm = form.remember.data
            login_user(user, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))
        flash("Неверная пара логин/пароль", "error")

    return render_template('login.html', form=form, menu=menu, title="Авторизация")


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            hash = generate_password_hash(form.psw_1.data)
            u = Users(email=form.email.data, psw=hash)
            db.session.add(u)
            db.session.flush()
            p = Profiles(name=form.name.data, surname=form.surname.data, age=form.age.data,
                         city=form.city.data, user_id=u.id, )
            db.session.add(p)
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")
            flash("Ошибка добавления в БД", 'error')
        flash("Вы успешно зарегистрированы", "success")
        return redirect(url_for('login'))

    return render_template('/register.html', form=form, menu=menu, title="Регистрация")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", menu=menu, title="Мой профиль", name=Profiles.query.get(current_user.id).name)




if __name__ == "__main__":
    app.run(debug=True)
