import dash_mantine_components as dmc
from dash import dcc
from dash_iconify import DashIconify


def create_home_link(label):
    return dmc.Text(
        label,
        size="xl",
        color="gray",
    )


header = dmc.Header(
    height=65,
    # fixed=True, # uncomment this line if you are using this example in your app
    p=5,
    children=[
        dmc.Container(
            fluid=True,
            children=dmc.Group(
                position="apart",
                align="flex-start",
                children=[
                    dmc.Center(
                        [
                            dmc.ThemeIcon(
                                DashIconify(
                                    icon="ic:baseline-school",
                                    width=35,
                                ),
                                radius=46,
                                size=46,
                            ),
                            dmc.Space(w=10),
                            dcc.Link(
                                [
                                    dmc.MediaQuery(
                                        create_home_link(dmc.Title("Cardomatic")),
                                        smallerThan="sm",
                                        styles={"display": "none"},
                                    ),
                                    dmc.MediaQuery(
                                        create_home_link("DMC"),
                                        largerThan="sm",
                                        styles={"display": "none"},
                                    ),
                                ],
                                href="/",
                                style={"paddingTop": 5, "textDecoration": "none"},
                            ),
                        ]
                    ),
                    dmc.Group(
                        position="right",
                        align="center",
                        spacing="xl",
                        children=[
                            dmc.Badge(
                                "Global level 1",
                                variant="gradient",
                                gradient={"from": "teal", "to": "lime", "deg": 105},
                            ),
                            dmc.Text("Ismaël"),
                            dmc.Tooltip(
                                dmc.ThemeIcon(
                                    DashIconify(
                                        icon="ic:baseline-account-circle",
                                        width=36,
                                    ),
                                    radius=30,
                                    size=36,
                                    variant="outline",
                                ),
                                label="My account",
                                position="bottom",
                            ),
                        ],
                    ),
                ],
            ),
            mb=20
        )])
