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


class Expenses(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=True)
    aim = db.Column(db.String(200), nullable=True)
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<expense {self.id}>"


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
    return render_template("profile.html", menu=menu, title="Мой профиль",
                           name=Profiles.query.get(current_user.id).name)

@app.route('/my_expenses')
@login_required
def my_expenses():
    categories = db.session.query(Expenses.category).filter(Expenses.user_id == current_user.id).group_by(Expenses.category)
    return render_template("myexpenses.html", menu=menu, title="Мои расходы", categories=categories)


@app.route("/my_expenses/<alias>")
@login_required
def show_expense(alias):
    expenses = db.session.query(Expenses).filter(Expenses.category == alias, Expenses.user_id == current_user.id).order_by(db.desc(Expenses.date)).all()
    result = 0
    for i in db.session.query(Expenses.amount).filter(Expenses.category == alias, Expenses.user_id == current_user.id):
        result += i.amount
    result = round(result, 2)
    return render_template('expenses_by_category.html', menu=menu, title='Мои расходы', expenses=expenses, title2=alias, result=result)


@app.route('/add_expense', methods=['POST', 'GET'])
@login_required
def add_expense():
    form = ExpensesForm()
    if form.validate_on_submit():
        try:
            expence = Expenses(category=form.category.data, aim=form.aim.data,
                           amount=form.amount.data, date=form.date.data, user_id=current_user.id)
            db.session.add(expence)
            db.session.flush()
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")
            flash("Ошибка добавления в БД", 'error')
        flash("Платеж внесен", "success")
        return redirect(url_for('my_expenses'))
    return render_template("add_expense.html", menu=menu, title="Мои расходы", form=form)


if __name__ == "__main__":
    app.run(debug=True)
