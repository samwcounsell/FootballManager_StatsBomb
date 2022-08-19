from dash import dcc, html, Input, Output, callback, dash_table

from app_components.navbar import create_navbar
from functions.position_grid import call_data

# Reading in app components and data
navbar = create_navbar()
df = call_data()


# Page Layout
layout = html.Div([

    navbar,

    dash_table.DataTable(df.to_dict('records'),[{"name": i, "id": i} for i in df.columns], id='tbl')

])