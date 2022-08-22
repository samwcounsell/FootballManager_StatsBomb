import pandas as pd
from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np

from app_components.navbar import create_navbar
# from functions.position_grid import call_data

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Reading in app components and data
navbar = create_navbar()

#TODO: Un-hashtag later
# df = call_data()

# TODO: Temporary as position grid is slower and can use this output csv for testing
df = pd.read_csv('./output.csv')
compare_df = pd.DataFrame([])

# TODO: Move adding new stats to hidden function
df['Gls/xG'] = df['Gls'] / df['xG']
df['Gls/90'] = df['Gls'] * df['Mins'] / 90
df['FA/90'] = df['FA'] * df['Mins'] / 90
df['Gls/90'] = df['Gls'] * df['Mins'] / 90
df['Dist/90'] = df['Distance'] * df['Mins'] / 90
df['xG/90'] = df['xG'] * df['Mins'] / 90
df['Off/90'] = df['Off'] * df['Mins'] / 90
df = df.round(decimals=3)

df.replace([np.inf, -np.inf], 0, inplace=True)
df = df.fillna(0)

# TODO: Move adding skillset ratings to hidden function
skillsets = ['Finishing', 'Dribbling', 'Aerial', 'Assisting', 'Pressing', 'Movement']

df['Finishing'] = (df['Gls/xG'] ** 2) * df['Shot %'] * df['Gls/90']
df['Dribbling'] = df['Drb/90'] * df['FA/90']
# Fix these after proof of working
df['Aerial'] = df['Height'] * df['Weight'] * df['Hdr %'] * df['Hdrs W/90'] * df['Aer A/90']
df['Assisting'] = df['Asts/90'] * df['Ch C/90'] * df['K Ps/90'] * df['Pas %']
df['Pressing'] = df['Dist/90'] * df['Tck'] * df['Int/90']
df['Movement'] = df['xG/90'] + df['Shot/90'] + df['Off/90']

# Required lists/dicts/etc.,
positions = ['GK', 'DL', 'DC', 'DR', 'WBL', 'DM', 'WBR', 'ML', 'MC', 'MR', 'AML', 'AMC', 'AMR', 'ST']
players = df['Name']

# TODO: Positions roles and role stats (potentially move to other file later)
position_roles = {
    'GK': ['Goalkeeper', 'Sweeper Keeper'],
    'DL': ['Fullback', 'Wingback', 'Complete Wingback'],
    'DC': ['Central Defender', 'Ballplaying Defender'],
    'DR': ['Central Defender', 'Ballplaying Defender'],
    'WBL': ['Wingback', 'Complete Wingback', 'Inverted Wingback'],
    'WBR': ['Wingback', 'Complete Wingback', 'Inverted Wingback'],
    'DM': ['Defensive Midfielder', 'Anchor Man', 'Deeplying Playmaker'],
    'ML': ['Defensive Winger', 'Winger', 'Inverted Winger'],
    'MC': ['Deeplying Playmaker', 'Advanced Playmaker', 'Box-to-Box', 'Ballwinning Midfielder', 'Mezzala', 'Central '
           'Midfielder (At)'],
    'MR': ['Defensive Winger', 'Winger', 'Inverted Winger'],
    'AML': ['Winger', 'Inverted Winger', 'Inside Forward'],
    'AMC': ['Attacking Midfielder', 'Advanced Playmaker', 'Shadow Striker'],
    'AML': ['Winger', 'Inverted Winger', 'Inside Forward'],
    'ST': ['Advanced Forward', 'False Nine', 'Poacher', 'Target Forward', 'Pressing Forward']
}

position_skills = {
    'GK': ['Finishing', 'Dribbling', 'Aerial', 'Assisting', 'Pressing', 'Movement'],
    'DL': ['Finishing', 'Dribbling', 'Aerial', 'Assisting', 'Pressing', 'Movement'],
    'DC': ['Finishing', 'Dribbling', 'Aerial', 'Assisting', 'Pressing', 'Movement'],
    'DR': ['Finishing', 'Dribbling', 'Aerial', 'Assisting', 'Pressing', 'Movement'],
    'WBL': ['Finishing', 'Dribbling', 'Aerial', 'Assisting', 'Pressing', 'Movement'],
    'WBR': ['Finishing', 'Dribbling', 'Aerial', 'Assisting', 'Pressing', 'Movement'],
    'DM': ['Finishing', 'Dribbling', 'Aerial', 'Assisting', 'Pressing', 'Movement'],
    'ML': ['Finishing', 'Dribbling', 'Aerial', 'Assisting', 'Pressing', 'Movement'],
    'MC': ['Finishing', 'Dribbling', 'Aerial', 'Assisting', 'Pressing', 'Movement'],
    'MR': ['Finishing', 'Dribbling', 'Aerial', 'Assisting', 'Pressing', 'Movement'],
    'AML': ['Finishing', 'Dribbling', 'Aerial', 'Assisting', 'Pressing', 'Movement'],
    'AMC': ['Finishing', 'Dribbling', 'Aerial', 'Assisting', 'Pressing', 'Movement'],
    'AML': ['Finishing', 'Dribbling', 'Aerial', 'Assisting', 'Pressing', 'Movement'],
    'ST': ['Finishing', 'Dribbling', 'Aerial', 'Assisting', 'Pressing', 'Movement']
}

role_stats = {
    'Goalkeeper': ['Drb', 'Height'],
    'Sweeper Keeper': ['Hdrs', 'FA'],
    'Fullback': ['Fls', 'Tck'],
    'Wingback': [],
    'Complete Wingback': [],
    'Central Defender': [],
    'Ballplaying Defender': [],
    'Inverted Wingback': [],
    'Defensive Midfielder': [],
    'Anchor Man': [],
    'Deeplying Playmaker': [],

    'Advanced Forward': ['xG', 'Gls', 'Gls/xG', 'Drb/90', 'Ch C/90', 'Asts/90']
}

# Page Layout
layout = html.Div([

    navbar,

    html.H1(children='', style={'textAlign': 'center', 'padding': 15}),

    # Top Row Dropdowns
    dbc.Row([
        dbc.Col([
            html.P(children='Please Select Input: Position'),
            dcc.Input(id='position_dropdown', list='suggested_positions', value=positions[0], type='text'),
            ]),
        dbc.Col([
            #TODO: Make roles option dependent on position selected (using callback)
            html.P(children='Please Select Input: Player Role'),
            dcc.Input(id='role_dropdown', list='suggested_roles', value=list(role_stats.keys())[0], type='text'),
            ]),
        dbc.Col([
            # TODO: Make these auto-fill in as in previous iteration
            html.P(children='Please Select Input: Player A'),
            dcc.Input(id='playerA_dropdown', list='suggested_names', value=players[0], type='text'),
            ]),
        dbc.Col([
            html.P(children='Please Select Input: Player B'),
            dcc.Input(id='playerB_dropdown', list='suggested_names', value=players[2], type='text'),
            ]),
        dbc.Col([
            html.P(children=' ')
        ]),
    ], style={"display": "grid", "grid-template-columns": "10% 10% 10% 10% 60%", 'fontSize': 11, 'padding-left': 15, 'padding-bottom': 25}),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Hexagon'),
                    dcc.Graph(id='polygon')
                ], className='text-center')
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div(id='compare_table')
                        ], className='text-center')
                    ])
                ], xs=12)
            ], className='pt-1')
        ], xs=6),
        dbc.Col([

            # Range Sliders

            dbc.Card([
                dbc.CardBody([
                    html.H4('Range Sliders / Inputs'),
                    dbc.Row([
                        html.P('Age: '),
                        dcc.RangeSlider(id='age_slider', min=15, max=45, marks={15: '15', 20: '20',25: '25',30: '30',35: '35',40: '40',45: '45'}, value=[15, 45])
                    ], style={"display": "grid", "grid-template-columns": "15% 85%", 'fontSize': 11}),
                    dbc.Row([
                        html.P('Minutes: '),
                        dcc.RangeSlider(0, 6000, 200, value=[200, 6000], marks={0: '0', 1000: '1000', 2000: '2000', 3000: '3000', 4000: '4000', 5000: '5000', 6000: '6000'}, id='minutes_slider')
                    ], style={"display": "grid", "grid-template-columns": "15% 85%", 'fontSize': 11}),
                ])
            ], className='h-100 text-center')
        ], xs=3),

        # Recommendations

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Top Reccomendations'),
                ])
            ], className='h-100 text-center')
        ], xs=3),
    ]),

    # Active dataframes and datalists
    dcc.Store(id='active_data'),
    html.Datalist(id='suggested_names', children=[html.Option(value=player) for player in players]),
    html.Datalist(id='suggested_positions', children=[html.Option(value=position) for position in positions]),
    html.Datalist(id='suggested_roles', children=[html.Option(value=role) for role in role_stats]),

])



####### Callbacks

### Data Callbacks

# Big Data callbacks
@callback(
    Output('active_data', 'data'),
    [Input('position_dropdown', 'value'),
     Input('age_slider', 'value'),
     Input('minutes_slider', 'value'),
     ],
)
def filter_data(position, age, minutes):

    # Position filter
    new_df = df[df[position] == 1]

    # Age Filter
    age_min, age_max = age
    new_df = new_df[new_df['Age'].between(age_min, age_max)]

    # Minutes Filter
    minutes_min, minutes_max = minutes
    new_df = new_df[new_df['Mins'].between(minutes_min, minutes_max)]

    return new_df.to_json(orient='split')

# Player Stats Callbacks
@callback(
    Output('compare_table', 'children'),
    [Input('position_dropdown', 'value'),
    Input('role_dropdown', 'value'),
    Input('playerA_dropdown', 'value'),
    Input('playerB_dropdown', 'value')]
)
def update_compare(position, role, playerA, playerB):

    stats = ['Mins', 'Av Rat'] + role_stats[role]
    names = [playerA, playerB]

    compare_table = df[df['Name'].isin(names)].set_index('Name')
    compare_table = compare_table[stats]
    compare_table = compare_table.T.reset_index()

    return dash_table.DataTable(compare_table.to_dict('records'), [{"name": i, "id": i} for i in compare_table.columns])

### Dropdown / Input Callbacks

# Role Callbacks
@callback(
    [Output('suggested_roles', 'children'),
    Output('role_dropdown', 'value')],
    Input('position_dropdown', 'value')
)
def update_roles_list(position):

    roles = position_roles[position]

    return [html.Option(value=role) for role in roles], roles[0]

# Player Input Callbacks
@callback(
    Output('suggested_names', 'children'),
    Output('playerA_dropdown', 'value'),
    Output('playerB_dropdown', 'value'),
    Input('active_data', 'data')
)
def update_player_list(df):

    df = pd.read_json(df, orient='split')
    players = list(df.Name.values)

    return [html.Option(value=word) for word in players], players[0], players[2]

### Graph Callbacks

# Hexagon Callback
@callback(
    Output('polygon', 'figure'),
    [Input('active_data', 'data'),
     Input('position_dropdown', 'value'),
     Input('playerA_dropdown', 'value'),
     Input('playerB_dropdown', 'value')]
)
def update_polygon(df, position, playerA, playerB):

    df = pd.read_json(df, orient='split')
    df = df.set_index('Name')

    for skill in skillsets:
        df[skill] = df[skill].rank(pct=True)

    skills = position_skills[position]

    polygon = go.Figure()
    polygon.add_trace(go.Scatterpolar(
        r=[df[position_skills[position][0]][playerA], df[position_skills[position][1]][playerA], df[position_skills[position][2]][playerA],
           df[position_skills[position][3]][playerA], df[position_skills[position][4]][playerA], df[position_skills[position][5]][playerA],
           df[position_skills[position][0]][playerA]],
        theta=[0, 60, 120, 180, 240, 300, 0],
        fill="toself",
        name=playerA,
        marker=dict(size=1, color="indigo")))
    polygon.add_trace(go.Scatterpolar(
        r=[df[position_skills[position][0]][playerB], df[position_skills[position][1]][playerB], df[position_skills[position][2]][playerB],
           df[position_skills[position][3]][playerB], df[position_skills[position][4]][playerB], df[position_skills[position][5]][playerB],
           df[position_skills[position][0]][playerB]],
        theta=[0, 60, 120, 180, 240, 300, 0],
        fill="toself",
        name=playerB,
        marker=dict(size=1, color="thistle")))
    polygon.update_layout(
        polar=dict(
            radialaxis=dict(visible=False, tickangle=0),
            angularaxis=dict(
                thetaunit="degrees",
                dtick=60,
                direction="clockwise",
                tickmode="array",
                tickvals=[0, 60, 120, 180, 240, 300],
                ticktext=skills,
            )
        ), hovermode='x unified')

    return polygon

