from flask import render_template, Flask
import io
import base64

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from math import *

app = Flask(__name__)

@app.route("/", methods=["GET"])
def mainpage():
    # Generate plot
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
        func_value[i] = eval('sin(x**2)')
        args_value[i] = x
        x += x_delta

    curve.plot(args_value, func_value, "ro-")

    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)

    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')

    return render_template("main.html", image=pngImageB64String)

if __name__ == '__main__':
   app.run(port=8000, host='127.0.0.1')
# In the image.html jinja2 template use the following <img> to add the plot:
# <img src="{{ image }}"/>
