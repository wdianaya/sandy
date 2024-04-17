import io
import base64
import calc_fft
from convert_img import save_picture_post
from data import db_session
from forms.login import LoginForm
from forms.register import RegisterForm
from forms.post_forms import PostForm, Comment
from data.users import User
from data.post import Post
from data.comments import Comments
from flask import Flask, render_template, redirect, request, make_response, abort, jsonify, flash, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms.main_form import MainForm
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from math import *
import mpld3
from forms.raspr import RasprForm
import rand_signal
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/sandy.db")
    db_sess = db_session.create_session()
    app.run(port=8000, host='127.0.0.1')


@app.route("/", methods=['GET', 'POST'])
@app.route("/forum")
def forum():
    session = db_session.create_session()

    posts = session.query(Post).all()
    if posts:
        page = request.args.get('page', 1, type=int)
        # posts = session.query(Post).query.order_by(Post.start_date.desc()).paginate(page=page, per_page=2)

    
        return render_template("index.html", title='Математический форум',
                           posts=posts)
    return render_template("index.html", title='Математический форум', either="Пока ещё не опубликовано ни одного поста")
    


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def error_500(error):
    return make_response(jsonify({'error': 'Were experiencing some trouble on our end.'
                                           ' Please try again in near future'}), 500)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/raspr", methods=['GET', 'POST'])
def raspredelen():
    form = RasprForm()
    if request.method == 'POST':
        dot_count = int(request.form['raspr_dot_count'])
        raspr_name = str(request.form['raspr_name'])
        rfig = Figure(figsize=(15, 7.78))
        rasp = rfig.add_subplot(1, 1, 1)
        hfig = Figure(figsize=(3, 3))
        hist = hfig.add_subplot(1, 1, 1)
        if raspr_name.lower() == 'равномерное':
            y = rand_signal.rand_uniform(dot_count)
            rasp.plot(y, "ro-")
            rasp.grid(True)
            hist.hist(y)
        elif raspr_name.lower()== 'треугольное':
            y = rand_signal.rand_triang(dot_count)
            rasp.plot(y, "ro-")
            rasp.grid(True)
            hist.hist(y)
        elif raspr_name.lower()== 'бета':
            y = rand_signal.rand_beta(dot_count)
            rasp.plot(y, "ro-")
            rasp.grid(True)
            hist.hist(y)
        elif raspr_name.lower()== 'экспоненциальное':
            y = rand_signal.rand_expo(dot_count)
            rasp.plot(y, "ro-")
            rasp.grid(True)
            hist.hist(y)
        elif raspr_name.lower()== 'гамма':
            y = rand_signal.rand_gamma(dot_count)
            rasp.plot(y, "ro-")
            rasp.grid(True)
            hist.hist(y)
        elif raspr_name.lower()== 'нормальное':
            y = rand_signal.rand_gauss(dot_count)
            rasp.plot(y, "ro-")
            rasp.grid(True)
            hist.hist(y)
        elif raspr_name.lower()== 'логнормальное':
            y = rand_signal.rand_lognorm(dot_count)
            rasp.plot(y, "ro-")
            rasp.grid(True)
            hist.hist(y)
        elif raspr_name.lower()== 'парето':
            y = rand_signal.rand_pareto(dot_count)
            rasp.plot(y, "ro-")
            rasp.grid(True)
            hist.hist(y)



        html_rand = mpld3.fig_to_html(rfig)
        Html_rand = open("raspr.html", "w")
        Html_rand.write(html_rand)
        Html_rand.close()

        html_hist = mpld3.fig_to_html(hfig)
        Html_hist = open("raspr.html", "w")
        Html_hist.write(html_hist)
        Html_hist.close()

        return render_template("raspr.html", html_rand=html_rand, html_hist=html_hist, form=form)
    return render_template("raspr.html", image=None, form=form)

@app.route("/graf", methods=['GET', 'POST'])
def mainpage():
    form = MainForm()
    if request.method == 'POST':
        try:
            function = request.form['function']  # так берётся текст введенной функции
            start_dot = request.form['start_dot']  # начальная
            end_dot = request.form['end_dot']  # конечная
            amount = request.form['count']  # количество точек
            if function:
                fig = Figure(figsize=(15, 7.78))
                curve = fig.add_subplot(1, 1, 1)
                graph_dot_count = int(amount)
                func_value = [0] * graph_dot_count
                args_value = [0] * graph_dot_count
                x_start = float(start_dot)
                x_end = float(end_dot)
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


@app.route('/post', methods=['GET', 'POST'])
def adding_post():
    form = PostForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        post = Post()
        post.team_leader = current_user.id
        post.posts = form.content.data
        post.title = form.title.data
        if form.picture.data:
            picture_file = save_picture_post(form.picture.data, post)
            post.image_post = picture_file
        post.start_date = datetime.datetime.now()
        try:
            session.add(post)
            session.commit()
        except Exception as e:
            ok, message = False, "Error was occurred. Please, try again"
        else:
            ok, message = True, ""
        if ok:
            flash('Пост был опубликован!', 'alert-success')
            return redirect('/')
        else:
            flash('Произошла ошибка при создании поста. Попробуйте ещё раз', 'alert-danger')
            return
        # image_file = url_for('static', filename=f'img/post_images/' + current_user.image_file) - для аватарок
    return render_template("create_post.html", title="New Post", form=form) # image_file=image_file


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def look_post(post_id):
    db_sess = db_session.create_session()
    form = Comment()
    comments = db_sess.query(Comments).filter(Comments.post_id == post_id).all()
    post = db_sess.query(Post).filter(Post.id == post_id).first()
    if not post:
        abort(404)

    if request.method == 'POST' and form.validate_on_submit():
        if current_user.is_authenticated:
            user_id = current_user.id
            comment = Comments()
            comment.user_id = user_id
            comment.post_id = post_id
            comment.text_com = form.text.data
            comment.start_date = datetime.datetime.now()
            db_sess.add(comment)
            db_sess.commit()
            flash('Комментарий к посту был добавлен', "alert-success")
            return redirect(url_for('look_post', post_id=post.id))
        flash('Вы должны быть авторизированы, чтобы оставлять вопросы на SANDY', "alert-warning")
        return redirect('/register')

    # image_file = url_for('static',
    #                      filename=f'profile_pics/' + 'users/' + post.author.username + '/post_images/' + post.image_post)
    return render_template('post.html', title=post.title, post=post,
                           form_comment=form, comments=comments) # image_file=image_file,


@app.route('/post_delete/<int:post_id>', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.id == post_id).first()
    if post.team_leader != current_user.id:
        flash('У вас нет прав доступа для выполнения данного действия', "alert-danger")
        return redirect('/')
    try:
        os.unlink(
            os.path.join(current_app.root_path,
                         f'static/img/post_images/{post.image_post}'))
        db_sess.delete(post)
    except:
        db_sess.delete(post)

    db_sess.commit()
    flash('Данный пост был удален', 'alert-success')
    return redirect('/')


@app.route('/comment_delete/<int:com_id>', methods=['POST', 'GET'])
@login_required
def delete_comment(com_id):
    db_sess = db_session.create_session()
    comment = db_sess.query(Comments).filter(Comments.id == com_id).first()
    post_id = comment.post_id
    if comment.user_id != current_user.id:
        flash('У вас нет прав доступа для выполнения данного действия', "alert-danger")
        return redirect('/')

    db_sess.delete(comment)
    db_sess.commit()
    flash('Данный комментарий был удален', 'alert-success')
    return redirect('/post/' + str(post_id))


@app.route("/job/<int:job_id>", methods=["GET", "POST"])
@login_required
def edit_job(job_id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
        if job:
            if current_user.id != 1 and current_user.id != job.team_leader:
                abort(403)
            form.name.data = job.job
            form.team_leader.data = job.team_leader
            form.hours.data = job.work_size
            form.collaborators.data = job.collaborators
            form.category.data = job.category
            form.finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
        if job:
            if current_user.id != 1 and current_user.id != job.team_leader:
                abort(403)
            job.job = form.name.data
            job.team_leader = form.team_leader.data
            job.work_size = form.hours.data
            job.collaborators = form.collaborators.data
            job.category = form.category.data
            if form.finished.data:
                job.end_date = datetime.datetime.now()
                job.is_finished = form.finished.data
            else:
                job.end_date = None
                job.is_finished = form.finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template("jobs.html", title="Editing a Job", form=form)


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