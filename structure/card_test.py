from math import exp
from random import choice, choices

import dash_mantine_components as dmc
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
        self.last_answer = ""
        self.card_score_at_start = self.card.score

    def start(self):
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
                return dmc.Alert("You're right!", title="Nice!", color="green")
            else:
                self.current_word.orta_score -= 1.5

                return dmc.Alert(f"Wrong answer. The correct answer was : {self.current_word.translation}",
                                 title="Oops!", color="red")
        elif self.src_lan == "taor":
            if user_input == self.current_word.string:
                self.current_word.taor_score += 1.5
                return dmc.Alert("You're right!", title="Good!", color="green")
            else:
                self.current_word.taor_score -= 1.5
                return dmc.Alert(f"Wrong answer. The correct answer was : {self.current_word.string}",
                                 title="Oops!", color="red")

        return dmc.Container(f"There has been a problem (wrong or no language provided) (lan={self.src_lan}")

    @property
    def score(self):
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
        print("Card Level : ", self.card.level)
        print("Card Score : ", self.card.score)
        self.state = "Finished"

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

    def ask(self):
        possible_words = []
        weights = []
        for word in self.card.words:
            possible_words.append([word, "orta"])
            possible_words.append([word, "taor"])
            weights.append(int(exp(-word.orta_score / 10) * 1000))
            weights.append(int(exp(-word.taor_score / 10) * 1000))

        print([(word[0].string, word[0].translation, score) for word, score in zip(possible_words, weights)])

        chosen_tuple = choices(possible_words, weights)[0]
        word, language = chosen_tuple
        word_string = ""
        return word, language
