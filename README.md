Stats 418 Final Project
============

This repository holds all code relevant to the final project for Stats 418.


    ├── src
    │   ├── movie_finder/
    │   │   ├── _MovieFinder.py       <- Holds all classes and functions relevant to MovieFinder
    │   │   └── datasets/        
    │   │       ├── _base.py          <- Utility function to load tmdb dataset
    │   │       ├── _tmdb.py          <- Script used to query TMDB api
    │   │       └── data              <- Holds datasets used by MovieFinder
    │   └── Nrl/
    │       └── _Nrl.py               <- Holds all classes and functions relevant to neural network model
    │
    ├── STAT 418 Dashboard v3.ipynb   <- Dashboard that contains all outputs for the project
    ├── Movie_Finder_demo.ipynb       <- Notebook used to test MovieFinder functionality
    └── README.md

Quick Start
------------
This project uses ```poetry``` to manage dependencies. Download ```poetry``` following the instructions found [here](https://python-poetry.org/docs/), then navigate to the directory that contains the ```pyproject.toml``` file and run:

```
poetry install
```

Once all dependencies are installed, run the entirety of ```STAT 418 Dashboard v3.ipynb``` to create a dashboard that runs locally.