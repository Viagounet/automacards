import dash_mantine_components as dmc
from dash_iconify import DashIconify

from structure.card import Card


time = Card(title="time", words=["hoy", "ahora", "antés", "depués", "ayer"])
ordinador = Card(title="ordenador", words=["ordenador", "ratón", "teclado", "red"])
ordinador.save("viagounet")
time.save("viagounet")

cards = [ordinador, time]
add_card = dmc.Paper([(dmc.Col(dmc.Button(
            "Add card",
            leftIcon=[DashIconify(icon="ic:baseline-post-add")],
        ), span=3))], shadow="xs", radius=10, withBorder=True, p=10)
cards = dmc.Col(
    dmc.Grid(
        [dmc.Col(card.render, span=3) for card in cards] + [add_card],
        grow=True,
    ))
