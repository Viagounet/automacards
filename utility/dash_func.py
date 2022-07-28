from dash import html
import dash_mantine_components as dmc

def hidden(widget):
    return html.Div(children=widget, style={"display": "none"})

def gen_elements(card, type, input):
    string = "Next"
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
                dmc.Space(h=15),
                dmc.Group(
                    buttons,
                    position="right",
                ),
            ]

    bottom = bottom + [dmc.Space(h=15), dmc.Progress(value=card.test.score, color="pink")]
    return top, bottom
