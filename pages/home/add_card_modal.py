import dash_mantine_components as dmc
from dash import html, callback, Output, Input, State, ALL
from dash_iconify import DashIconify

from pages.accounts import viagounet
from structure.card import Card
from structure.word import Word


def block(n):
    return [
        dmc.Group(
            [
                dmc.ActionIcon(
                    DashIconify(icon="circle-flags:es", width=48),
                    size=48,
                ),
                dmc.TextInput(placeholder="Enter a word", id={"index": n, "type": "input-origin"}),
                dmc.Space(w=10),
                dmc.ActionIcon(
                    DashIconify(icon="circle-flags:fr", width=48),
                    size=48,
                ),
                dmc.TextInput(placeholder="Enter its translation", id={"index": n, "type": "input-translation"}),
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
                'align-items': 'center',
                'justify-content': 'center', },
        ),
        dmc.Space(h=30)
    ]


def gen_input_group(n):
    children = []
    for i in range(n):
        children += block(i)

    return children


header = [dmc.Group([dmc.Title("Card title : ", order=3), dmc.TextInput(placeholder="Title", id="card-title")])]

add_card_modal = dmc.Modal(
    opened=True,
    title=f"Add a new card",
    size="50%",
    id="add-card-modal",
    overflow="inside",
    children=header
             + [dmc.Space(h=50)]
             + [html.Div(gen_input_group(3), id="words-input-group")]
             + [
                 html.Div(
                     [
                         dmc.Button(
                             "Add word",
                             leftIcon=[DashIconify(icon="akar-icons:circle-plus-fill", color="white")],
                             id="add-word-button",
                         ),
                         dmc.Space(w=15),
                         dmc.Button(
                             "Add card",
                             leftIcon=[DashIconify(icon="bi:card-text", color="white")],
                             id="add-card-button",
                         ),
                     ],
                     style={
                         'display': 'flex',
                         'flex-direction': 'row',
                         'align-items': 'center',
                         'justify-content': 'center', },
                 ),
             ]
)


@callback(
    Output("words-input-group", "children"),
    [Input("add-word-button", "n_clicks")],
    [State("words-input-group", "children")],
    prevent_initial_call=True,
)
def add_word_button_callback(n_clicks, children):
    if n_clicks is None:
        return []
    return children + block(len(children) // 2)


@callback(
    Output("add-card-modal", "opened"),
    Input("add-card-button", "n_clicks"),
    State({"type": "input-origin", "index": ALL}, "value"),
    State({"type": "input-translation", "index": ALL}, "value"),
    State("card-title", "value"),
    prevent_initial_call=True,
)
def add_card_button_callback(n_clicks, values_origin, values_translation, title):
    if n_clicks is None:
        return True
    words = []
    for string, translation in zip(values_origin, values_translation):
        word = Word(string)
        word.translation = translation
        words.append(word)
    print(viagounet.cards)
    viagounet.add_new_card(title, words)
    print(viagounet.cards)
    return False
