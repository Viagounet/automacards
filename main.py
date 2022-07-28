import dash
from dash import Dash

from pages.accounts import viagounet
from pages.home.cards import cards
from pages.home.timeline import create_timeline
from pages.header import header
from dash import html, Output, Input, State, callback, MATCH

from structure.card import gen_lists
from utility.func import parse
from utility.dash_func import gen_elements

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
    Output({'type': 'test-modal', 'index': MATCH}, "title"),
    Input({'type': 'test-button', 'index': MATCH}, 'n_clicks'),
    Input({'type': 'next-button', 'index': MATCH}, 'n_clicks'),
    Input({'type': 'confirm-button', 'index': MATCH}, 'n_clicks'),
    State({'type': 'test-modal', 'index': MATCH}, "opened"),
    State({'type': 'test-modal', 'index': MATCH}, "children"),
    State({'type': 'user-text-input', 'index': MATCH}, "value"),
    prevent_initial_call=True,
)
def test_manager(n, n_, n__, opened, modal_children, input_value):
    ctx = dash.callback_context
    type, index = parse(ctx)
    card = account.get_card(index)
    card.test.ask()
    title = f"Test : {card.title.capitalize()}"

    if type == "test-button":
        card.test.start()
        top, bottom = gen_elements(card, type, input_value)
        return not opened, top + [card.test.render] + bottom, title

    if type == "confirm-button":
        card = account.get_card(index)
        top, bottom = gen_elements(card, type, input_value)
        return True, top + [card.test.render] + bottom, title

    if type == "next-button":
        card = account.get_card(index)

        if card.test.current_word.translation == "":
            card.test.current_word.translation = input_value
            card.save("viagounet")

        card.test.next()
        top, bottom = gen_elements(card, type, input_value)

        if card.test.state == "Not started yet":
            return False, top + [card.test.render] + bottom, title
        return True, top + [card.test.render] + bottom, title


# todo: Change the input for a detection of change in the json
@callback(
    Output({'type': 'list-words', 'index': MATCH}, "children"),
    Input({'type': 'test-modal', 'index': MATCH}, "opened"),
    State({'type': 'list-words', 'index': MATCH}, "children"),
    prevent_initial_call=True,
)
def update_card_after_next(opened, current):
    ctx = dash.callback_context
    type, index = parse(ctx)
    card = account.get_card(index)
    if opened:
        return dmc.Container(dmc.Title("Currently testing for this card", order=4, align="center"))
    else:
        es_list, fr_list = gen_lists(card.words)
        return dmc.Grid([
            dmc.Col(es_list, span=6),
            dmc.Col(fr_list, span=6),
        ])


if __name__ == "__main__":
    app.run_server()