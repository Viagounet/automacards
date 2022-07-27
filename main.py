import dash
from dash import Dash
from dash_iconify import DashIconify

from pages.accounts import viagounet
from pages.home.cards import cards
from pages.home.timeline import create_timeline
from pages.header import header
from dash import html, Output, Input, State, callback, MATCH

from structure.card import gen_lists
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


def hidden(widget):
    return html.Div(children=widget, style={"display": "none"})


def gen_elements(card, type, input):
    string = "Next"
    if card.test.i+1 == card.test.limit:
        string = "Finish"
    if card.test.src_lan == "new":
        buttons = [
            dmc.Button(string, id={"type": "next-button", "index": card.title}),
            hidden(dmc.Button("Confirm", id={"type": "confirm-button", "index": card.title})),
            dmc.Button("Stop", color="red")]
        top = [dmc.Alert("This is a new word, make sure the translation is correct.", title="New word",
                         color="blue"), dmc.Space(h=15)]
        bottom = [
            dmc.Space(h=15),
            dmc.Group(
                buttons,
                position="right",
            ),

        ]

    else:
        top = [html.Div([])]
        if type == "confirm-button":
            buttons = [
                dmc.Button(string, id={"type": "next-button", "index": card.title}),
                hidden(dmc.Button("Confirm", id={"type": "confirm-button", "index": card.title})),
                dmc.Button("Stop", color="red")]
            bottom = [dmc.Space(h=10),
                      card.test.render_correction(input),
                      dmc.Space(h=10),
                      dmc.Divider(),
                      dmc.Group(
                          buttons,
                          position="right",
                      )]
        elif type == "test-button":
            buttons = [
                hidden(dmc.Button(string, id={"type": "next-button", "index": card.title})),
                dmc.Button("Confirm", id={"type": "confirm-button", "index": card.title}),
                dmc.Button("Stop", color="red")]

            bottom = [
                dmc.Space(h=15),
                dmc.Group(
                    children=buttons,
                    position="right",
                )]
        else:
            buttons = [
                hidden(dmc.Button(string, id={"type": "next-button", "index": card.title})),
                dmc.Button("Confirm", id={"type": "confirm-button", "index": card.title}),
                dmc.Button("Stop", color="red")]
            bottom = [
                dmc.Group(
                    buttons,
                    position="right",
                ),
            ]
    return top, bottom


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
def my_test(n, n_, n__, opened, modal_children, input_value):
    ctx = dash.callback_context
    type, index = parse(ctx)
    card = account.get_card(index)

    title = f"Test : {card.title.capitalize()} (Word {card.test.i+1}/{card.test.limit})"

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

        top, bottom = gen_elements(card, type, input_value)
        card.test.next()

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
    app.run_server(debug=True)

"""fr_item_list = []
        es_item_list = []
        for word in card.words:
            if word.translation == "":
                fr_item_list.append(dmc.ListItem(dmc.Text("n/a")))
                es_item_list.append(dmc.ListItem(dmc.Text(word.string)))
            else:
                fr_item_list.append(dmc.ListItem(word.translation.capitalize()))
                es_item_list.append(dmc.ListItem(dmc.Text(word.string)))

        es_list = dmc.List(
            icon=[
                dmc.ThemeIcon(
                    DashIconify(icon="circle-flags:es", width=24),
                    radius="xl",
                    color="gray",
                    size=24,
                )
            ],
            size="sm",
            spacing="sm",
            children=es_item_list)

        fr_list = dmc.List(
            icon=[
                dmc.ThemeIcon(
                    DashIconify(icon="circle-flags:fr", width=24),
                    radius="xl",
                    color="dark",
                    size=24,
                )
            ],
            size="sm",
            spacing="sm",
            children=fr_item_list)
        return [
            dmc.Col(es_list, span=6),
            dmc.Col(fr_list, span=6),
        ]"""
