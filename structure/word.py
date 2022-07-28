import json


class Word:
    def __init__(self, string):
        self.string = string
        self.translation = ""
        self.orta_score = 1  # origin->target
        self.taor_score = 1

        self.orta_strikes = 0
        self.taor_strikes = 0

    @property
    def serialize(self):
        return {"string": self.string,
                "translation": self.translation,
                "orta_score": self.orta_score,
                "taor_score": self.taor_score}

    def save(self, user):
        with open(f"data/{user}/words/{self.string}.json", "w", encoding="utf-8") as fb:
            json.dump(self.serialize, fb)

    def __len__(self):
        return len(self.string)


class WordFromFile(Word):
    def __init__(self, user, string):
        with open(f"data/{user}/words/{string}.json", "r", encoding="utf-8") as fb:
            self.data = json.load(fb)
        super(WordFromFile, self).__init__(self.data["string"])
        self.translation = self.data["translation"]
        self.orta_score = self.data["orta_score"]  # origin->target
        self.taor_score = self.data["taor_score"]
