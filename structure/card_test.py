from math import exp
from random import choice, choices

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify
from numpy import interp


class CardTest:
    def __init__(self, card):
        self.card = card
        self.state = "Not started yet"
        self.src_lan = choice(["orta", "taor"])
        self.current_word = self.card.words[0]
        self.limit = len(self.card)
        self.nb_trials = 0
        self.good_answers = 0
        self.last_answer = ""
        self.card_score_at_start = self.card.score
        self.automatically_added_words = []

    def start(self):
        print("Current word:", self.current_word.string)
        self.nb_trials = 0
        self.good_answers = 0
        self.card.shuffle()
        self.state = "Running"
        if self.current_word.translation == "":
            self.src_lan = "new"
        self.next()

    # todo: suppriner l'input vide il y a une erreur
    def render_correction(self, user_input):
        if self.src_lan == "orta" or self.src_lan == "new":
            if user_input == self.current_word.translation:
                self.current_word.orta_score += 1.5
                self.good_answers += 1
                return dmc.Alert("You're right!", title="Nice!", color="green")
            else:
                self.current_word.orta_score -= 1.5

                return dmc.Alert(f"Wrong answer. The correct answer was : {self.current_word.translation}",
                                 title="Oops!", color="red")
        elif self.src_lan == "taor":
            if user_input == self.current_word.string:
                self.current_word.taor_score += 1.5
                self.good_answers += 1
                return dmc.Alert("You're right!", title="Good!", color="green")
            else:
                self.current_word.taor_score -= 1.5
                return dmc.Alert(f"Wrong answer. The correct answer was : {self.current_word.string}",
                                 title="Oops!", color="red")

        return dmc.Container(f"There has been a problem (wrong or no language provided) (lan={self.src_lan}")

    @property
    def score(self):
        print(self.card.title, self.card_score_at_start, self.card.score)
        return interp(self.card.score, [self.card_score_at_start, self.card_score_at_start * 1.5], [0, 100])

    def next(self):
        if self.score >= 100:
            self.stop()

        else:
            self.nb_trials += 1
            self.current_word, self.src_lan = self.ask()
            if self.current_word.translation == "":
                self.src_lan = "new"

    def stop(self):
        self.card_score_at_start = self.card.score
        self.card.save()
        self.automatically_added_words = self.card.user.dm.add_words_to(self.card)
        self.state = "Not started yet"

    @property
    def render_clear_text(self):
        if self.src_lan == "orta" or self.src_lan == "new":
            return dmc.Group([dmc.ThemeIcon(
                DashIconify(icon="circle-flags:es", width=32),
                radius="xl",
                color="gray",
                size=32,
            ), dmc.Text(self.current_word.string)])
        elif self.src_lan == "taor":
            return dmc.Group([dmc.ThemeIcon(
                DashIconify(icon="circle-flags:fr", width=32),
                radius="xl",
                color="gray",
                size=32,
            ), dmc.Text(self.current_word.translation)])
        return dmc.Container(f"There has been a problem (wrong or no language provided) (lan={self.src_lan}")

    @property
    def render_input(self):
        input_box = {
            "Not started yet": dmc.TextInput(placeholder="Answer",
                                             id={"type": "user-text-input", "index": self.card.title}),
            "Confirm": dmc.TextInput(placeholder="Answer",
                                     id={"type": "user-text-input", "index": self.card.title}),
            "Next": dmc.Text(self.last_answer, id={"type": "user-text-input", "index": self.card.title}),
            "starting": dmc.TextInput(placeholder="Answer",
                                      id={"type": "user-text-input", "index": self.card.title}),
            "Running": dmc.TextInput(placeholder="Translation",
                                     id={"type": "user-text-input", "index": self.card.title})}

        if self.src_lan == "new":
            return dmc.Group([dmc.ThemeIcon(
                DashIconify(icon="circle-flags:fr", width=32),
                radius="xl",
                color="gray",
                size=32,
            ), dmc.TextInput(placeholder="Translation",
                             id={"type": "user-text-input", "index": self.card.title})])

        elif self.src_lan == "orta":
            return dmc.Group([dmc.ThemeIcon(
                DashIconify(icon="circle-flags:fr", width=32),
                radius="xl",
                color="gray",
                size=32,
            ), input_box[self.state]])

        elif self.src_lan == "taor":
            return dmc.Group([dmc.ThemeIcon(
                DashIconify(icon="circle-flags:es", width=32),
                radius="xl",
                color="gray",
                size=32,
            ), input_box[self.state]])
        return dmc.Container(f"There has been a problem (wrong or no language provided) (lan={self.src_lan}")

    @property
    def render(self):
        if self.src_lan == "orta" or self.src_lan == "new":
            return dmc.Group([self.render_clear_text, dmc.Space(h=15), self.render_input])
        elif self.src_lan == "taor":
            return dmc.Group([self.render_clear_text, dmc.Space(h=15), self.render_input])
        return dmc.Container(f"There has been a problem (wrong or no language provided) (lan={self.src_lan}")

    @property
    def render_endscreen(self):
        return html.Div(
            [dmc.Title("Congratulations! You successfully completed this level!"),
             dmc.Text(f"You got a precision of {self.good_answers / self.nb_trials * 100:.2f}%"),
             dmc.Text(f"Because you're THAT good, we'll add a few more words in your card!"),
             dmc.Divider(),
             # Showing the new
             dmc.Text(f"The new words added to your card are :"),
             dmc.List([
                 dmc.ListItem(dmc.Text(word)) for word in self.automatically_added_words])],
            style={"display": "flex", "flex-direction": "column", "align-items": "center"})

    def ask(self):
        possible_words = []
        weights = []
        for word in self.card.words:
            possible_words.append([word, "orta"])
            possible_words.append([word, "taor"])
            weights.append(int(exp(-word.orta_score / 10) * 1000))
            weights.append(int(exp(-word.taor_score / 10) * 1000))

        chosen_tuple = choices(possible_words, weights)[0]
        word, language = chosen_tuple
        word_string = ""
        return word, language
