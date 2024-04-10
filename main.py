import io
import base64
import calc_fft

from flask import render_template, Flask, request
from forms.main_form import MainForm
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from math import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route("/", methods=['GET', 'POST'])
@app.route("/argentum")
def mainpage():
    form = MainForm()
    if request.method == 'POST':
        function = request.form['function']  # так берётся текст введенной функции
        if function:
            fig = Figure()
            curve = fig.add_subplot(1, 1, 1)
            graph_dot_count = 100
            func_value = [0] * graph_dot_count
            args_value = [0] * graph_dot_count
            x_start = 0
            x_end = 10
            x_delta = (x_end - x_start) / graph_dot_count
            x = x_start
            for i in range(graph_dot_count):
                func_value[i] = eval(function)
                args_value[i] = x
                x += x_delta

            curve.plot(args_value, func_value, "ro-")

            spectre_fig = Figure()
            spectre = spectre_fig.add_subplot(1, 1, 1)
            y = calc_fft.calc_fft(func_value)

            spectre.plot(abs(y), "ro-")


            # Convert plot to PNG image
            pngImage = io.BytesIO()
            FigureCanvas(fig).print_png(pngImage)

            pngImage_spectre = io.BytesIO()
            FigureCanvas(spectre_fig).print_png(pngImage_spectre)

            # Encode PNG image to base64 string
            pngImageB64String = "data:image/png;base64,"
            pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')

            pngImage_spectreB64String = "data:image/png;base64,"
            pngImage_spectreB64String += base64.b64encode(pngImage_spectre.getvalue()).decode('utf8')

            return render_template("main.html", title=function, image=pngImageB64String, image_spectre=pngImage_spectreB64String, form=form)
    return render_template("main.html", image=None, form=form)

if __name__ == '__main__':
   app.run(port=8000, host='127.0.0.1')
# In the image.html jinja2 template use the following <img> to add the plot:
# <img src="{{ image }}"/>
