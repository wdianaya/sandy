import io
import base64
import calc_fft
from data import db_session
from forms.login import LoginForm
from forms.register import RegisterForm
from data.users import User
from flask import Flask, render_template, redirect, request, make_response, abort, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms.main_form import MainForm
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from math import *
import mpld3


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/sandy.db")
    db_sess = db_session.create_session()
    app.run(port=8000, host='127.0.0.1')


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("base.html")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/graf", methods=['GET', 'POST'])
def mainpage():
    form = MainForm()
    if request.method == 'POST':
        try:
            function = request.form['function']  # так берётся текст введенной функции
            # start_dot = request.form['start_dot']  # начальная
            # end_dot = request.form['end_dot']  # конечная
            # amount = request.form['count']  # количество точек
            if function:
                fig = Figure(figsize=(15, 7.78))
                curve = fig.add_subplot(1, 1, 1)
                graph_dot_count = 100
                func_value = [0] * graph_dot_count
                args_value = [0] * graph_dot_count
                x_start = 0
                x_end = 10
                x_delta = (x_end - x_start) / graph_dot_count
                x = x_start
                for i in range(graph_dot_count):
                    try:
                        func_value[i] = eval(function)
                    except ZeroDivisionError:
                        pass
                    args_value[i] = x
                    x += x_delta

                curve.plot(args_value, func_value, "ro-")
                curve.grid(True)

                html_str = mpld3.fig_to_html(fig)
                Html_file = open("index.html", "w")
                Html_file.write(html_str)
                Html_file.close()

                spectre_fig = Figure(figsize=(3, 3))
                spectre = spectre_fig.add_subplot(1, 1, 1)
                y = calc_fft.calc_fft(func_value)

                spectre.plot(abs(y), "ro-")

                html_spec = mpld3.fig_to_html(spectre_fig)
                Html_spec = open("spec.html", "w")
                Html_spec.write(html_str)
                Html_spec.close()

                return render_template("main.html", title=function, html_fig=html_str, html_spec=html_spec, form=form)
        except Exception:
            raise Exception
    return render_template("main.html", image=None, form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Password or login is incorrect",
                               form=form)
    return render_template('login.html', form=form)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


if __name__ == '__main__':
    main()

# In the image.html jinja2 template use the following <img> to add the plot:
# <img src="{{ image }}"/>