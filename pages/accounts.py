from structure.card import Card, CardFromFile
from structure.user import User

"""time = CardFromFile("viagounet", "time")
ordenador = CardFromFile("viagounet", "ordenador")

ordenador.save("viagounet")
time.save("viagounet")
"""

verbos = Card(title="verbos", words=["probar", "desear", "decir"])
informatica = Card(title="informatica",
                   words=["ordenador", "red", "ratón", "teclado", "pantalla"])
informatica.save("viagounet")
verbos.save("viagounet")
viagounet = User("viagounet", [verbos, informatica])
