from random import choice

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

"""dmc.Group([dmc.ThemeIcon(
                DashIconify(icon="circle-flags:es", width=32),
                radius="xl",
                color="gray",
                size=32,
            ), dmc.Text(card.card_info["words"][i]["string"])]),
            dmc.Space(h=15),
            dmc.Group([dmc.ThemeIcon(
                DashIconify(icon="circle-flags:fr", width=32),
                radius="xl",
                color="gray",
                size=32,
            ), dmc.TextInput(placeholder="Answer")])"""


class CardTest:
    def __init__(self, card):
        self.card = card
        self.i = 0
        self.state = "Not started yet"

    def start(self):
        self.card.shuffle()
        self.state = "Running"

    def next(self):
        self.i += 1

    def stop(self):
        self.i = 0
        self.state = "Not started yet"

    def render_clear_text(self, language):
        print(language, self.current_word.string)
        if language == "or":
            return dmc.Group([dmc.ThemeIcon(
                DashIconify(icon="circle-flags:es", width=32),
                radius="xl",
                color="gray",
                size=32,
            ), dmc.Text(self.current_word.string)])
        elif language == "ta":
            return dmc.Group([dmc.ThemeIcon(
                DashIconify(icon="circle-flags:fr", width=32),
                radius="xl",
                color="gray",
                size=32,
            ), dmc.Text(self.current_word.string)])
        return dmc.Container("There has been a problem (wrong or no language provided)")

    @staticmethod
    def render_input(language):
        if language == "or":
            return dmc.Group([dmc.ThemeIcon(
                DashIconify(icon="circle-flags:es", width=32),
                radius="xl",
                color="gray",
                size=32,
            ), dmc.TextInput(placeholder="Answer")])

        elif language == "ta":
            return dmc.Group([dmc.ThemeIcon(
                DashIconify(icon="circle-flags:fr", width=32),
                radius="xl",
                color="gray",
                size=32,
            ), dmc.TextInput(placeholder="Answer")])
        return dmc.Container("There has been a problem (wrong or no language provided)")

    @property
    def current_word(self):
        return self.card.words[self.i]

    @property
    def render(self):
        src_language = choice(["or", "ta"])
        if self.current_word.translation == "":
            return html.Div([dmc.Alert("This is a new word, make sure the translation is correct.", title="New word",
                                       color="blue"),
                             dmc.Space(h=15),
                             dmc.Group([self.render_clear_text("or"), dmc.Space(h=15), self.render_input("ta")])
                             ])
        if src_language == "or":
            return dmc.Group([self.render_clear_text("or"), dmc.Space(h=15), self.render_input("ta")])
        elif src_language == "ta":
            return dmc.Group([self.render_clear_text("ta"), dmc.Space(h=15), self.render_input("or")])
        return dmc.Container("There has been a problem (wrong or no language provided)")
