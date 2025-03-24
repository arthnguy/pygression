from .base import Quality

class Triad(Quality):
    def figured_bass(self, inversion: int) -> str:
        bass = ""

        if inversion == 1:
            bass = "6"
        elif inversion == 2:
            bass = "6/4"

        return bass

class Major(Triad):
    def __str__(self):
        return ""

    @staticmethod
    def get_integers() -> [int]:
        return [0, 4, 7]

class Minor(Triad):
    def __str__(self):
        return "m"

    @staticmethod
    def get_integers() -> [int]:
        return [0, 3, 7]

class Augmented(Triad):
    def __str__(self):
        return "+"

    @staticmethod
    def get_integers() -> [int]:
        return [0, 4, 8]

class Diminished(Triad):
    def __str__(self):
        return "o"

    @staticmethod
    def get_integers() -> [int]:
        return [0, 3, 6]