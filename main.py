import dash
from dash import Dash

from pages.accounts import viagounet
from pages.home.cards import cards
from pages.home.timeline import create_timeline
from pages.header import header
from dash import html, Output, Input, State, callback, MATCH
from utility.func import parse

app = Dash(__name__)

import dash_mantine_components as dmc

account = viagounet

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
    Output({'type': 'test-modal', 'index': MATCH}, "children"),
    Input({'type': 'test-button', 'index': MATCH}, 'n_clicks'),
    Input({'type': 'next-button', 'index': MATCH}, 'n_clicks'),
    Input({'type': 'confirm-button', 'index': MATCH}, 'n_clicks'),
    State({'type': 'test-modal', 'index': MATCH}, "opened"),
    State({'type': 'test-modal', 'index': MATCH}, "children"),
    prevent_initial_call=True,

)
def my_test(n, n_, n__, opened, modal_children):
    ctx = dash.callback_context
    type, index = parse(ctx)
    if type == "test-button":
        card = account.get_card(index)
        card.test.start()
        return not opened, modal_children

    if type == "confirm-button":
        card = account.get_card(index)
        bottom = [dmc.Space(h=10),
                  card.test.render_correction("Hello"),
                  dmc.Space(h=10),
                  dmc.Divider(),
                  dmc.Group(
                      [
                          html.Div(dmc.Button("Confirm", id={"type": "confirm-button", "index": card.title}, ),
                                   style={"display": "none"}),
                          dmc.Button("Next", id={"type": "next-button", "index": card.title}),
                          dmc.Button(
                              "Stop",
                              color="red",
                          ),
                      ],
                      position="right",
                  ),

                  ]
        if card.test.state == "Not started yet":
            return False, [card.test.render] + bottom
        return True, [card.test.render] + bottom

    if type == "next-button":
        card = account.get_card(index)
        card.test.next()

        bottom = [dmc.Space(h=20),
                  dmc.Group(
                      [
                          html.Div(dmc.Button("Next", id={"type": "next-button", "index": card.title}, ),
                                   style={"display": "none"}),
                          dmc.Button("Confirm", id={"type": "confirm-button", "index": card.title}),

                          dmc.Button(
                              "Stop",
                              color="red",
                          ),
                      ],
                      position="right",
                  )]

        if card.test.state == "Not started yet":
            return False, [card.test.render] + bottom
        return True, [card.test.render] + bottom


if __name__ == "__main__":
    app.run_server(debug=True)
