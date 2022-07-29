from random import shuffle
from math import log
import json
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from structure.card_test import CardTest
from structure.word import WordFromFile, Word
from utility.func import level_mapping


def gen_lists(words):
    fr_item_list = []
    es_item_list = []
    for word in words:

        # Managing None values
        if word.translation is None:
            word.translation = ""
        if word.string is None:
            word.string = ""

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
    return es_list, fr_list


class Card:
    def __init__(self, title, words, user):

        # Creating the words list with a list of String or a list of Word
        if type(words[0]) == str:
            self.words = [Word(word) for word in words]
        else:
            self.words = words

        self.title = title
        self.test = CardTest(self)
        self.user = user

    def shuffle(self):
        shuffle(self.words)

    @property
    def serialize(self):
        return {"title": self.title,
                "score": self.score,
                "words": [word.serialize for word in self.words]}

    def save(self):
        with open(f"data/{self.user}/cards/{self.title}.json", "w", encoding="utf-8") as fb:
            json.dump(self.serialize, fb)
        for word in self.words:
            word.save(self.user)

    @property
    def score(self):
        return sum([word.taor_score for word in self.words] + [word.orta_score for word in self.words])

    @property
    def level(self):
        return level_mapping(self.score)

    @property
    def render(self):
        header = [
            dmc.Group([dmc.Title(self.title.capitalize(), order=4),
                       dmc.Badge(
                           f"Lvl.{self.level}",
                           variant="gradient",
                           gradient={"from": "teal", "to": "lime", "deg": 105},
                       ),
                       ], align="center", id={"type": "card-title", "index": self.title}),
            dmc.Space(h=5),
            dmc.Divider(variant="dotted"),
            dmc.Space(h=15),
        ]
        es_list, fr_list = gen_lists(self.words)
        body = [dmc.Grid([
            dmc.Col(es_list, span=6),
            dmc.Col(fr_list, span=6),
        ],
            style={"height": "30vh", "overflow-y": "scroll"}, id={"type": "list-words", "index": self.title})]
        button = [html.Div([dmc.Divider(variant="dotted"),
                            dmc.Button("Take a test", id={
                                'type': 'test-button',
                                'index': self.title
                            })],
                           className="d-flex flex-column justify-content-center align-items-center",
                           style={"width": "100%", "display": "flex", "justify-content": "center",
                                  "align-items": "center"})]

        modal = [dmc.Modal(
            opened=False,
            title=f"Test : {self.title.capitalize()}",
            id={
                'type': 'test-modal',
                'index': self.title
            },
            children=[
                self.test.render,
                dmc.Space(h=20),
                dmc.Group(
                    [
                        dmc.Button("Confirm", id={"type": "confirm-button", "index": self.title}),
                        dmc.Button(
                            "Stop",
                            color="red",
                        ),
                        html.Div(dmc.Button("Next", id={"type": "next-button", "index": self.title}, ),
                                 style={"display": "none"}),
                    ],
                    position="right",
                ),
            ],
        )]
        return dmc.Paper(header + body + button + modal, shadow="xs", radius=10, withBorder=True, p=10,
                         id={"type": "vocab-card", "index": self.title})

    def __len__(self):
        return len(self.words)

    def __add__(self, other):
        if isinstance(other, Word):
            self.words.append(other)
        elif isinstance(other, Card):
            self.words = self.words + other.words


class CardFromFile(Card):
    def __init__(self, user, title):
        with open(f"data/{user}/cards/{title}.json", "r", encoding="utf-8") as fb:
            self.data = json.load(fb)
        self.words = [WordFromFile(user, word["string"]) for word in self.data["words"]]
        super(CardFromFile, self).__init__(self.data["title"], self.words, user)
        self.title = self.data["title"]
