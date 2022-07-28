from random import choice, choices

import dash_mantine_components as dmc
from dash_iconify import DashIconify


class CardTest:
    def __init__(self, card):
        self.card = card
        self.state = "Not started yet"
        self.src_lan = choice(["orta", "taor"])
        self.current_word = self.card.words[0]
        self.limit = len(self.card)

        self.score = 0
        self.score_objective = 100
        self.nb_trials = 0

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
                self.score += 10
                return dmc.Alert("You're right!", title="Good!", color="green")
            else:
                self.score -= 10
                if self.score <= 0:
                    self.score = 0

                return dmc.Alert(f"Wrong answer. The correct answer was : {self.current_word.translation}",
                                 title="Oops!", color="red")
        elif self.src_lan == "taor":
            if user_input == self.current_word.string:
                self.score += 10
                return dmc.Alert("You're right!", title="Good!", color="green")
            else:
                self.score -= 10
                return dmc.Alert(f"Wrong answer. The correct answer was : {self.current_word.string}",
                                 title="Oops!", color="red")

        return dmc.Container(f"There has been a problem (wrong or no language provided) (lan={self.src_lan}")

    def next(self):
        if self.score >= self.score_objective:
            self.stop()

        else:
            self.nb_trials += 1
            self.current_word, self.src_lan = self.ask()
            if self.current_word.translation == "":
                self.src_lan = "new"

    def stop(self):
        self.state = "Finished"

    @property
    def render_clear_text(self):
        print(self.src_lan, self.current_word.string, self.current_word.translation)
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
        if self.src_lan == "orta" or self.src_lan == "new":
            return dmc.Group([dmc.ThemeIcon(
                DashIconify(icon="circle-flags:fr", width=32),
                radius="xl",
                color="gray",
                size=32,
            ), dmc.TextInput(placeholder="Answer", id={"type": "user-text-input", "index": self.card.title})])

        elif self.src_lan == "taor":
            return dmc.Group([dmc.ThemeIcon(
                DashIconify(icon="circle-flags:es", width=32),
                radius="xl",
                color="gray",
                size=32,
            ), dmc.TextInput(placeholder="Answer", id={"type": "user-text-input", "index": self.card.title})])
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
            weights.append(word.orta_score)
            weights.append(word.taor_score)

        chosen_tuple = choices(possible_words, weights)[0]
        word, language = chosen_tuple
        word_string = ""
        return word, language
