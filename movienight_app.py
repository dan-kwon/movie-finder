import dash
from dash import Dash, html, dcc, dash_table, Input, Output, State, MATCH
import plotly.express as px
import pandas as pd
import numpy as np
from movienight import MovieFinder
from movienight.datasets import load_tmdb

# Use pre-loaded dataset from TMDB
movie_data = load_tmdb()

# dash app
app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Find movie recommendations using NLP'),

    html.Div(children='''
        Enter a query to search for movie recommendations. The more specific the query, the better the recommendations will be.
    '''),

    html.Br(),

    dcc.Input(
        id='input-query',
        placeholder='Search for a movie',
        type='text',
        value='',
        style={'width': '70%'}
    ),

    html.Br(),
    html.Br(),

    html.Button('Submit', id='submit-button'),
    
    html.Br(),
    html.Br(),
    
    dash_table.DataTable(
        data=movie_data.head(10).to_dict('records'),
        columns=[{"name": i, "id": i} for i in ["Title","Synopsis"]], id='table')
])

@app.callback(
    [Output("table", "data"), Output('table', 'columns')],
    [Input('submit-button', 'n_clicks')]
)
def update_top10_data(n_clicks):
    # Load MovieFinder instance
    m = MovieFinder()
    query = f"{n_clicks}"
    m.get_n_matches(
        query=query, 
        data=movie_data,
        n=10
    )

    if n_clicks is None:
        return movie_data.head(10).to_dict('records'), [{"name": i, "id": i} for i in ["Title","Synopsis"]]

    return movie_data.iloc[m.top_n_index,:][["title","overview"]].to_dict('records'), [{"name": i, "id": i} for i in ["Title","Synopsis"]]

if __name__ == '__main__':
    app.run_server(debug=True)
