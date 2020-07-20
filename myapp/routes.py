from myapp import app
import json, plotly
from flask import render_template
from data.data import return_figures

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():

    figures = return_figures()[:5]

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON)
@app.route('/trade_view')
@app.route('/trade_view.html')
def trade_view():
    figures = return_figures()[-4:]

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('trade_view.html',
                           ids=ids,
                           figuresJSON=figuresJSON)
