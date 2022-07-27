import dash_mantine_components as dmc
from dash_iconify import DashIconify

from pages.accounts import viagounet

cards = viagounet.cards

add_card = dmc.Paper([(dmc.Col(dmc.Button(
            "Add card",
            leftIcon=[DashIconify(icon="ic:baseline-post-add")],
        ), span=3))], shadow="xs", radius=10, withBorder=True, p=10)
cards = dmc.Col(
    dmc.Grid(
        [dmc.Col(card.render, span=3) for card in cards] + [add_card],
        grow=True,
    ))
