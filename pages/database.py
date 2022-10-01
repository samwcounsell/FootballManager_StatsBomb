import pandas as pd
from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np, math

from app_components.navbar import create_navbar
# from functions.position_grid import call_data

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Reading in app components and data
navbar = create_navbar()

# Page Layout
layout = html.Div([

    navbar,

    html.H1("DATABASE")

])