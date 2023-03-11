import dash
from dash import Dash, html, dcc, dash_table, Input, Output, State, DiskcacheManager, MATCH
import plotly.express as px
import pandas as pd
import numpy as np
from movienight import MovieFinder
from movienight.datasets import load_tmdb

# Diskcache
import diskcache
cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)


# Use pre-loaded dataset from TMDB
movie_data = load_tmdb()

genres_dict = {
    "Action": 28,
    "Adventure": 12,
    "Animation": 16,
    "Comedy": 35,
    "Crime": 80,
    "Documentary": 99,
    "Drama": 18,
    "Family": 10751,
    "Fantasy": 14,
    "History": 36,
    "Horror": 27,
    "Music": 10402,
    "Mystery": 9648,
    "Romance": 10749,
    "SciFi" : 878,
    "TV_movie" : 10770,
    "Thriller": 53,
    "War": 10752,
    "Western": 37
}

# dash app
app = Dash(__name__)

app.layout = html.Div([
    
    html.H1(children='Find movie recommendations using NLP'),

    html.H4(children='''
        Enter a query to search for movie recommendations. The more specific the query, the better the recommendations will be.
    '''),

    html.H4(children='''
        Be aware that queries can take up to 30 seconds so please be patient while we scan thousands of movies. If timeout errors keep 
        occuring, try limiting the genres you search to 3-4 max.
    '''),

    html.Br(),

    dcc.Input(
            id='movie_query',
            placeholder='Enter query here',
            type='text',
            style={'width': '70%'}
    ),

    html.Br(),
    
    dcc.Checklist(
        [
            "Action",
            "Adventure",
            "Animation",
            "Comedy",
            "Crime",
            "Documentary",
            "Drama",
            "Family",
            "Fantasy",
            "History",
            "Horror",
            "Music",
            "Mystery",
            "Romance",
            "SciFi",
            "TV_movie",
            "Thriller",
            "War",
            "Western"
        ],
        ["Action", "Adventure"],
        id="genres", 
        inline=True
    ),
    
    html.Br(),

    dcc.RangeSlider(
        min=1900,
        max=2025,
        step=5,
        marks={i: '{:d}'.format(i) for i in range(1900,2025,5)}, 
        value=[2000, 2025], 
        id='year-range',
        allowCross=False
    ),

    html.Br(),

    html.Button('Submit', id='submit-button'),

    html.Br(),

    html.Div(id='min_year'),

    html.Br(),

    html.Div(id='max_year'),

    html.Br(),

    dash_table.DataTable(
        id='table',        
        columns=[{"name": i, "id": i} for i in ["title","overview"]],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'textAlign': 'left'
        }
    )
])

@dash.callback(
    Output(component_id='table', component_property='data'),
    Output(component_id='min_year', component_property='children'),
    Output(component_id='max_year', component_property='children'),
    Input(component_id='submit-button', component_property='n_clicks'),
    State(component_id='movie_query', component_property='value'),
    State(component_id='genres', component_property='value'),
    State(component_id='year-range', component_property='value'),
)

def update_output(submit_click, movie_query, genres, date_range):
    
    min_year, max_year = date_range

    date_mask = (movie_data["release_date"] > f'{str(min_year)}-01-01') & (movie_data["release_date"] < f'{str(max_year)}-12-31')

    movie_query = str(movie_query)

    genre_codes = [genres_dict[i] for i in genres]
    
    genres = ''.join(str(genre_codes))\
        .replace("[", "")\
        .replace("]", "")\
        .replace(", ", "|")
    
    m = MovieFinder()
    
    m.get_n_matches(
        query=movie_query,
        data=movie_data[date_mask].query(f'genre_ids.str.contains("{genres}")'),
        n=10)
    
    index_list = [i for i in m.top_n_index]
    
    indices = ''.join(str(index_list))
    
    result = movie_data[date_mask]\
        [["title","overview"]]\
        .iloc[m.top_n_index,:]\
        .to_dict('records')

    return result, min_year, max_year

if __name__ == '__main__':
    app.run_server(debug=True)