from dash import Dash

from pages.home.cards import cards
from pages.home.timeline import create_timeline
from pages.header import header
from dash import html, Output, Input, State, callback, MATCH

app = Dash(__name__)

import dash_mantine_components as dmc


timeline = create_timeline(0)
tabs = dmc.Col(dmc.Tabs(
    color="red",
    orientation="vertical",
    children=[
        dmc.Tab(label="Cards", children=[cards]),
        dmc.Tab(label="Deck", children=[]),
        dmc.Tab(label="Stats", children=[]),
    ]
), span=9)
app.layout = html.Div(
    [header,
     dmc.Space(h=20),
     dmc.Grid(
         [
             tabs,
             dmc.Space(w=10),
             dmc.Col(dmc.Grid(
                 [
                     timeline
                 ],

             ), span=2)
         ],
     ),

     dmc.Affix(
         dmc.Button("Send me suggestions!"), position={"bottom": 20, "right": 20}
     )
     ],
)


@callback(
    Output({'type': 'test-modal', 'index': MATCH}, "opened"),
    Input({'type': 'test-button', 'index': MATCH}, 'n_clicks'),
    State({'type': 'test-modal', 'index': MATCH}, "opened"),
    prevent_initial_call=True,

)
def my_test(values, opened):
    return not opened

if __name__ == "__main__":
    app.run_server(debug=True)
