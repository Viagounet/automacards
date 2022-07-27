from random import choice

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


class CardTest:
    def __init__(self, card):
        self.card = card
        self.i = 0
        self.state = "Not started yet"
        self.src_lan = choice(["or", "ta"])
        self.limit = len(self.card)

    def start(self):
        self.card.shuffle()
        self.state = "Running"
        if self.current_word.translation == "":
            self.src_lan = "new"

    # todo: suppriner l'input vide il y a une erreur
    def render_correction(self, user_input):
        if self.src_lan == "or" or self.src_lan == "new":
            if user_input == self.current_word.translation:
                return dmc.Alert("You're right!", title="Good!", color="green")
            else:
                return dmc.Alert(f"Wrong answer. The correct answer was : {self.current_word.translation}",
                                 title="Oops!", color="red")
        elif self.src_lan == "ta":
            if user_input == self.current_word.string:
                return dmc.Alert("You're right!", title="Good!", color="green")
            else:
                return dmc.Alert(f"Wrong answer. The correct answer was : {self.current_word.string}",
                                 title="Oops!", color="red")

        return dmc.Container("There has been a problem (wrong or no language provided)")

    def next(self):
        if self.i == len(self.card) - 1:
            self.stop()
        else:
            self.i += 1
            print(self.i+1)
            if self.current_word.translation == "":
                self.src_lan = "new"

    def stop(self):
        self.i = 0
        self.state = "Finished"

    @property
    def render_clear_text(self):
        if self.src_lan == "or" or self.src_lan == "new":
            return dmc.Group([dmc.ThemeIcon(
                DashIconify(icon="circle-flags:es", width=32),
                radius="xl",
                color="gray",
                size=32,
            ), dmc.Text(self.current_word.string)])
        elif self.src_lan == "ta":
            return dmc.Group([dmc.ThemeIcon(
                DashIconify(icon="circle-flags:fr", width=32),
                radius="xl",
                color="gray",
                size=32,
            ), dmc.Text(self.current_word.string)])
        return dmc.Container("There has been a problem (wrong or no language provided)")

    @property
    def render_input(self):
        if self.src_lan == "or" or self.src_lan == "new":
            return dmc.Group([dmc.ThemeIcon(
                DashIconify(icon="circle-flags:fr", width=32),
                radius="xl",
                color="gray",
                size=32,
            ), dmc.TextInput(placeholder="Answer", id={"type": "user-text-input", "index": self.card.title})])

        elif self.src_lan == "ta":
            return dmc.Group([dmc.ThemeIcon(
                DashIconify(icon="circle-flags:es", width=32),
                radius="xl",
                color="gray",
                size=32,
            ), dmc.TextInput(placeholder="Answer", id={"type": "user-text-input", "index": self.card.title})])
        return dmc.Container("There has been a problem (wrong or no language provided)")

    @property
    def current_word(self):
        return self.card.words[self.i]

    @property
    def render(self):
        if self.src_lan == "or" or self.src_lan == "new":
            return dmc.Group([self.render_clear_text, dmc.Space(h=15), self.render_input])
        elif self.src_lan == "ta":
            return dmc.Group([self.render_clear_text, dmc.Space(h=15), self.render_input])
        return dmc.Container("There has been a problem (wrong or no language provided)")
