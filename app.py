from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

from pages import stats_home, database, player_graphs

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LUX])
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# App callback to switch between pages
@callback(Output('page-content', 'children'),
          Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/database':
        return database.layout
    elif pathname == '/player_graphs':
        return player_graphs.layout
    else:
        return stats_home.layout

if __name__ == '__main__':
    app.run_server(debug=False)



#TODO: ReadME (Delete final 4 columns in excel/libreofficecalc)