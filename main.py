import io
import base64
import calc_fft

from data import db_session
from flask import render_template, Flask, request
from forms.main_form import MainForm
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from math import *
import mpld3


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    # db_session.global_init("db/sandy.db")
    # db_sess = db_session.create_session()
    app.run(port=8000, host='127.0.0.1')


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("base.html")


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

if __name__ == '__main__':
    main()

# In the image.html jinja2 template use the following <img> to add the plot:
# <img src="{{ image }}"/>