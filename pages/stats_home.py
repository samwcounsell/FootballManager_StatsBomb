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

#TODO: Un-hashtag later
# df = call_data()

# TODO: Temporary as position grid is slower and can use this output csv for testing
df = pd.read_csv('./new_output.csv', dtype={"Personality": "string"})
df['Personality'] = df['Personality'].fillna('-')
compare_df = pd.DataFrame([])

# TODO: Move adding new stats to hidden function
df['Gls/xG'] = df['Gls'] / df['xG']
df['Gls/90'] = df['Gls'] * df['Mins'] / 90
df['FA/90'] = df['FA'] * df['Mins'] / 90
df['Gls/90'] = df['Gls'] * df['Mins'] / 90
df['Dist/90'] = df['Distance'] * df['Mins'] / 90
df['xG/90'] = df['xG'] * df['Mins'] / 90
df['Off/90'] = df['Off'] * df['Mins'] / 90
df['Cr/90'] = df['Cr A'] * df['Mins'] / 90
df['K Tck/90'] = df['K Tck'] * df['Mins'] / 90
df['Fls/90'] = df['Fls'] * df['Mins'] / 90
df = df.round(decimals=3)

df.replace([np.inf, -np.inf], 0, inplace=True)
df = df.fillna(0)

# TODO: Move adding skillset ratings to hidden function
skillsets = ['Finishing', 'Dribbling', 'Aerial', 'Assisting', 'Pressing', 'Movement', 'Crossing', 'Work Rate',
             'Passing', 'Tackling', 'Intercepting', 'Goalkeeping']

df['Finishing'] = (df['Gls/xG'] ** 2) * df['Shot %'] * df['Gls/90']
df['Dribbling'] = df['Drb/90'] * df['FA/90']
# Fix these after proof of working
df['Aerial'] = df['Height'] * (df['Weight'] ** 0.5) * df['Hdr %'] * df['Hdrs W/90'] * df['Aer A/90']
df['Assisting'] = df['Asts/90'] * df['Ch C/90'] * df['K Ps/90'] * df['Pas %']
df['Pressing'] = df['Dist/90'] * df['Tck'] * df['Int/90']
df['Movement'] = df['xG/90'] + df['Shot/90'] + df['Off/90']
df['Crossing'] = df['Cr/90'] * (df['Cr C/A'] ** 2) * df['Asts/90']
df['Work Rate'] = df['Dist/90'] * df['Mins/Gm']
df['Passing'] = df['Ps A/90'] * df['Pas %'] * df['K Ps/90']
df['Tackling'] = df['K Tck/90'] * df['Tck'] * df['Tck R'] / df['Fls/90']
df['Intercepting'] = (df['Int/90'] ** 2) * df['Dist/90']
df['Goalkeeping'] = df['Sv %']

# Required lists/dicts/etc.,
positions = ['GK', 'DL', 'DC', 'DR', 'WBL', 'DM', 'WBR', 'ML', 'MC', 'MR', 'AML', 'AMC', 'AMR', 'ST']
players = df['Name']

# TODO: Positions roles and role stats (potentially move to other file later)
position_roles = {
    'GK': ['Goalkeeper', 'Sweeper Keeper'],
    'DL': ['Fullback', 'Wingback', 'Complete Wingback'],
    'DC': ['Central Defender', 'Ballplaying Defender'],
    'DR': ['Fullback', 'Wingback', 'Complete Wingback'],
    'WBL': ['Wingback', 'Complete Wingback', 'Inverted Wingback'],
    'WBR': ['Wingback', 'Complete Wingback', 'Inverted Wingback'],
    'DM': ['Defensive Midfielder', 'Anchor Man', 'Deeplying Playmaker'],
    'ML': ['Defensive Winger', 'Winger', 'Inverted Winger'],
    'MC': ['Deeplying Playmaker', 'Advanced Playmaker', 'Box-to-Box', 'Ballwinning Midfielder', 'Mezzala', 'Central '
           'Midfielder (At)'],
    'MR': ['Defensive Winger', 'Winger', 'Inverted Winger'],
    'AML': ['Winger', 'Inverted Winger', 'Inside Forward'],
    'AMC': ['Attacking Midfielder', 'Advanced Playmaker', 'Shadow Striker'],
    'AMR': ['Winger', 'Inverted Winger', 'Inside Forward'],
    'ST': ['Advanced Forward', 'False Nine', 'Poacher', 'Target Forward', 'Pressing Forward']
}

position_skills = {
    'GK': ['Finishing', 'Dribbling', 'Aerial', 'Assisting', 'Pressing', 'Movement'],
    'DL': ['Crossing', 'Dribbling', 'Aerial', 'Assisting', 'Work Rate', 'Tackling'],
    'DC': ['Passing', 'Pressing', 'Aerial', 'Finishing', 'Intercepting', 'Tackling'],
    'DR': ['Crossing', 'Dribbling', 'Aerial', 'Assisting', 'Work Rate', 'Tackling'],
    'WBL': ['Crossing', 'Dribbling', 'Passing', 'Assisting', 'Work Rate', 'Tackling'],
    'WBR': ['Crossing', 'Dribbling', 'Passing', 'Assisting', 'Work Rate', 'Tackling'],
    'DM': ['Passing', 'Work Rate', 'Aerial', 'Assisting', 'Intercepting', 'Tackling'],
    'ML': ['Dribbling', 'Passing', 'Assisting', 'Work Rate', 'Movement', 'Tackling'],
    'MC': ['Finishing', 'Dribbling', 'Tackling', 'Assisting', 'Passing', 'Work Rate'],
    'MR': ['Dribbling', 'Passing', 'Assisting', 'Work Rate', 'Movement', 'Tackling'],
    'AML': ['Finishing', 'Dribbling', 'Crossing', 'Assisting', 'Work Rate', 'Movement'],
    'AMC': ['Finishing', 'Dribbling', 'Passing', 'Assisting', 'Crossing', 'Movement'],
    'AMR': ['Finishing', 'Dribbling', 'Crossing', 'Assisting', 'Work Rate', 'Movement'],
    'ST': ['Finishing', 'Dribbling', 'Aerial', 'Assisting', 'Pressing', 'Movement']
}

role_stats = {
    'Goalkeeper': ['Sv %'],
    'Sweeper Keeper': ['Sv %'],
    'Fullback': ['Fls', 'Tck'],
    'Wingback': [],
    'Complete Wingback': [],
    'Central Defender': [],
    'Ballplaying Defender': [],
    'Inverted Wingback': [],
    'Defensive Midfielder': [],
    'Anchor Man': [],
    'Deeplying Playmaker': [],
    'Advanced Playmaker': [''],
    'Box-to-Box': [],
    'Ballwinning Midfielder': [],
    'Mezzala': [],
    'Central Midfielder (At)': [],
    'Defensive Winger': [],
    'Winger': [],
    'Inverted Winger': [],
    'Inside Forward': [],
    'Attacking Midfielder': [],
    'Advanced Playmaker': ['Ast', 'Asts/90', 'K Ps/90', 'Pas %', 'Ps C/90', 'Drb/90'],
    'Shadow Striker': [],
    'Advanced Forward': ['xG', 'Gls', 'Gls/xG', 'Drb/90', 'Ch C/90', 'Asts/90'],
    'False Nine': [],
    'Poacher': [],
    'Target Forward': [],
    'Pressing Forward': [],
}

#Nations
nations = ['Any'] + df['Nat'].to_list()
nations = list(set(nations))

# Leagues
leagues= ['Any'] + df['Based'].to_list()
leagues = list(set(leagues))

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
        ], xs=4),
        dbc.Col([

            # Range Sliders

            dbc.Card([
                dbc.CardBody([
                    html.H4('Range Sliders / Inputs'),
                    dbc.Row([
                        html.P('Age: '),
                        dcc.RangeSlider(15, 45, 1, marks={15: '15', 20: '20',25: '25',30: '30',35: '35',40: '40',45: '45'}, value=[15, 45], id='age_slider')
                    ], style={"display": "grid", "grid-template-columns": "15% 85%", 'fontSize': 11, 'padding': 10}),
                    dbc.Row([
                        html.P('Minutes: '),
                        dcc.RangeSlider(0, 6000, 200, value=[200, 6000], marks={0: '0', 1000: '1000', 2000: '2000', 3000: '3000', 4000: '4000', 5000: '5000', 6000: '6000'}, id='minutes_slider')
                    ], style={"display": "grid", "grid-template-columns": "15% 85%", 'fontSize': 11, 'padding': 10}),
                    dbc.Row([
                        html.P('Nation: '),
                        dcc.Input(id='nation_dropdown', list='suggested_nations', value='Any', type='text')
                    ], style={"display": "grid", "grid-template-columns": "15% 85%", 'fontSize': 11, 'padding': 10}),
                    dbc.Row([
                        html.P('League: '),
                        dcc.Input(id='league_dropdown', list='suggested_leagues', value='Any', type='text')
                    ], style={"display": "grid", "grid-template-columns": "15% 85%", 'fontSize': 11, 'padding': 10}),
                ])
            ], className='h-100 text-center')
        ], xs=3),

        # Recommendations

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Top Reccomendations'),
                    html.Div(id='recommendation_table')

                ])
            ], className='h-100 text-center')
        ], xs=5),
    ]),

    # Active dataframes and datalists
    dcc.Store(id='active_data'),
    html.Datalist(id='suggested_names', children=[html.Option(value=player) for player in players]),
    html.Datalist(id='suggested_positions', children=[html.Option(value=position) for position in positions]),
    html.Datalist(id='suggested_roles', children=[html.Option(value=role) for role in role_stats]),
    html.Datalist(id='suggested_nations', children=[html.Option(value=nation) for nation in nations]),
    html.Datalist(id='suggested_leagues', children=[html.Option(value=league) for league in leagues]),

])



####### Callbacks

### Data Callbacks

# Big Data callbacks
@callback(
    Output('active_data', 'data'),
    [Input('position_dropdown', 'value'),
    Input('age_slider', 'value'),
    Input('minutes_slider', 'value'),
    Input('nation_dropdown', 'value'),
    Input('league_dropdown', 'value')],
)
def filter_data(position, age, minutes, nation, league):

    # Position filter
    new_df = df[df[position] == 1]

    # Age Filter
    age_min, age_max = age
    new_df = new_df[new_df['Age'].between(age_min, age_max)]

    # Minutes Filter
    minutes_min, minutes_max = minutes
    new_df = new_df[new_df['Mins'].between(minutes_min, minutes_max)]

    # Nation Filter
    if nation == 'Any':
        new_df = new_df
    else:
        new_df = new_df[(new_df['Nat'] == nation) | (new_df['2nd Nat'] == nation)]
        print(new_df)

    # League/Club Filters
    if league == 'Any':
        new_df = new_df
    else:
        new_df = new_df[new_df['Based'] == league]

    return new_df.to_json(orient='split')

### Table Callbacks

# Player Compare Table
@callback(
    Output('compare_table', 'children'),
    [Input('active_data', 'data'),
    Input('position_dropdown', 'value'),
    Input('role_dropdown', 'value'),
    Input('playerA_dropdown', 'value'),
    Input('playerB_dropdown', 'value')]
)
def update_compare(df, position, role, playerA, playerB):

    df = pd.read_json(df, orient='split')

    stats = ['Age', 'Nat', 'Club', 'Height', 'Weight', 'Left Foot', 'Right Foot', 'Mins', 'Av Rat'] + role_stats[role]
    names = [playerA, playerB]

    compare_table = df[df['Name'].isin(names)].set_index('Name')
    compare_table = compare_table[stats]
    compare_table = compare_table.T.reset_index()

    return dash_table.DataTable(compare_table.to_dict('records'), [{"name": i, "id": i} for i in compare_table.columns],
                                style_cell={'fontSize': 10, 'font-family': 'sans-serif'},)

# Recommendations Table
@callback(
    Output('recommendation_table', 'children'),
    [Input('active_data', 'data'),
    Input('position_dropdown', 'value')]
)
def update_recommend(df, position):

    df = pd.read_json(df, orient='split')

    for skill in skillsets:
        df[skill] = df[skill].rank(pct=True)

    # Later change this to sum for role skills rather than position skills
    df['Sum'] = df[position_skills[position]].sum(1)

    df = df.round(decimals=2).sort_values(by='Sum', ascending=False)
    skills = ['Name'] + ['Sum'] + position_skills[position]
    table = df[skills]

    return dash_table.DataTable(table.to_dict('records'), [{"name": i, "id": i} for i in table.columns],
                                sort_action="native",
                                sort_mode="multi",
                                style_cell={'fontSize': 10, 'font-family': 'sans-serif'},
                                style_data={'height': 'auto', 'width': 'auto'}
                                )

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
    [Output('suggested_names', 'children'),
    Output('playerA_dropdown', 'value'),
    Output('playerB_dropdown', 'value')],
    Input('active_data', 'data')
)
def update_player_list(df):

    df = pd.read_json(df, orient='split')
    players = list(df.Name.values)

    return [html.Option(value=word) for word in players], players[0], players[1]

# Nation Callback
# League / Club Callbacks
@callback(
    [Output('suggested_nations', 'children'),
    Output('nation_dropdown', 'value')],
    Input('active_data', 'data')
)
def update_league_list():

    nations = ['Any'] + df['Nat'].to_list()
    nations = list(set(nations))

    return [html.Option(value=nation) for nation in nations]

# League / Club Callbacks
@callback(
    [Output('suggested_leagues', 'children'),
    Output('leagues_dropdown', 'value')],
    Input('active_data', 'data')
)
def update_league_list(df):

    leagues = ['Any'] + df['Based'].to_list()
    leagues = list(set(leagues))

    return [html.Option(value=league) for league in leagues]


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
            radialaxis=dict(range=[0,1], visible=False, tickangle=0),
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

