import dash_bootstrap_components as dbc

# Creating the navbar for the top of every page within the app
def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu",
                children=[
                    dbc.DropdownMenuItem("Player Comparison", href='/'),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Player Graphs", href='/player_graphs'),
                    dbc.DropdownMenuItem("Database", href='/database'),
                ],
            ),
        ],
        brand="Football Manager Stats Bomb",
        brand_href="/home",
        sticky="top",
        color="indigo",
        dark=True
    )

    return navbar