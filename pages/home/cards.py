import dash_mantine_components as dmc
from dash_iconify import DashIconify

from structure.card import Card

ordinador = Card(title="ordenador", words=["ordenador", "ratón", "teclado", "red"])
ordinador.save("viagounet")

cards = [ordinador]

cards = dmc.Col(
    dmc.Grid(
        [dmc.Col(card.render, span=3) for card in cards] + [dmc.Paper([(dmc.Col(dmc.Button(
            "Add card",
            leftIcon=[DashIconify(icon="ic:baseline-post-add")],
        ), span=3))], shadow="xs", radius=10, withBorder=True, p=10)],
        grow=True,
    ))
