from dash import Dash, dcc, html, Input, Output
import numpy as np
import pandas as pd
from movienight import MovieFinder
from movienight.datasets import load_tmdb

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(
        id="search-query",
        type="text",
        value="Describe the movie you want to watch here. The more descriptive the better!"
    ),
    html.Table([
        html.Tr([html.Td("Movie 1"), html.Td(id='m1')]),
        html.Tr([html.Td("Movie 2"), html.Td(id='m2')]),
        html.Tr([html.Td("Movie 3"), html.Td(id='m3')]),
        html.Tr([html.Td("Movie 4"), html.Td(id='m4')]),
        html.Tr([html.Td("Movie 5"), html.Td(id='m5')]),
    ]),
])


@app.callback(
    Output('m1', 'children'),
    Output('m2', 'children'),
    Output('m3', 'children'),
    Output('m4', 'children'),
    Output('m5', 'children'),
    Input('search-query', 'value'))

def callback_a(query):
    # Use pre-loaded dataset from TMDB
    movie_data = load_tmdb()
    # load MovieFinder
    m = MovieFinder()
    moviefinder_parameters = {
        "data" : movie_data,
        "n" : 10
    }
    m.get_n_matches(query=query, **moviefinder_parameters)
    results = movie_data.iloc[m.top_n_index,:][["title"]]
    return results[0],results[1],results[2],results[3],results[4]


if __name__ == '__main__':
    app.run_server(debug=True)