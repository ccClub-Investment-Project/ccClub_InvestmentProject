from app import app
from flask import render_template
from app.plot_utils import create_plot


@app.route('/')
def index():
    graphJSON = create_plot()
    return render_template('app_0619_merge.html', graphJSON=graphJSON)
