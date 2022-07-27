from structure.card import Card, CardFromFile
from structure.user import User

time = CardFromFile("viagounet", "time")
ordenador = CardFromFile("viagounet", "ordenador")

ordenador.save("viagounet")
time.save("viagounet")

viagounet = User("viagounet", [time, ordenador])
