from flask import Flask, Blueprint

metric_point = Blueprint("metrics", __name__)

@metric_point.route("/metrics")
def metrics():
    sample_graph()
    return "This feature is not yet implimented"

def sample_graph():
    import numpy as np

    from bokeh.plotting import figure, show, output_file

    N = 500
    x = np.linspace(0, 10, N)
    y = np.linspace(0, 10, N)
    xx, yy = np.meshgrid(x, y)
    d = np.sin(xx)*np.cos(yy)

    p = figure(tooltips=[("x", "$x"), ("y", "$y"), ("value", "@image")])
    p.x_range.range_padding = p.y_range.range_padding = 0

    # must give a vector of image data for image parameter
    p.image(image=[d], x=0, y=0, dw=10, dh=10, palette="Spectral11")

    output_file("image.html", title="image.py example")

    show(p)