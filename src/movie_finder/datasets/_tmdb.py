import json
import requests
import pandas as pd
from pathlib import Path

def _get_tmdb(
    url=["https://api.themoviedb.org/3/movie/popular","https://api.themoviedb.org/3/movie/top_rated"],
    api_key = '87a6e64caf61f2a624fdf65c58337921',
    n_pages = 100,
    col_names = [
        "id",
        "title",
        "overview",
        "adult",
        "genre_ids",
        "release_date"
    ]
):

    # empty dataframe to populate
    movie_data = pd.DataFrame()

    # looping through endpoints and pages
    for i in url:
        for j in range(n_pages):
            page_num = j+1
            payload = {
                "api_key" : api_key,
                "region" : "US",
                "page" : page_num
            }
            r = requests.get(i, params=payload)
            results = r.json()
            movie_data = pd.concat([movie_data, pd.json_normalize(results['results'])[col_names]])\
                .drop_duplicates(subset='id')\
                .reset_index(drop=True)
    return movie_data

if __name__ == "__main__":
    filepath_ = Path("src/movie_finder/datasets/data/tmdb.csv")
    data_ = _get_tmdb()
    data_.to_csv(filepath_, index=False)