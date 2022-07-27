from structure.card import Card
from structure.user import User

time = Card(title="time", words=["hoy", "ahora", "antés", "depués", "ayer"])
ordinador = Card(title="ordenador", words=["ordenador", "ratón", "teclado", "red"])

ordinador.save("viagounet")
time.save("viagounet")

viagounet = User("viagounet", [time, ordinador])
