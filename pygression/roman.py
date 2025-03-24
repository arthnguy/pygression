from .consts import Accidental, AS_NOTATION, ROMAN

class Roman:
    def __init__(self, degree, accidental: Accidental=Accidental.NATURAL):
        if type(degree) != int:
            raise TypeError(f"degree must be int, not {type(degree).__name__}")
        elif degree < 1 or degree > 7:
            raise ValueError("invalid degree")
        if type(accidental) != Accidental:
            raise TypeError(f"accidental must be accidental, not {type(accidental).__name__}")

        self._degree = degree
        self._accidental = accidental

    def __int__(self):
        return (self._degree + self._accidental.value) % 12

    def __repr__(self):
        return ROMAN[self._degree - 1] + AS_NOTATION[self._accidental]

    def __str__(self):
        return ROMAN[self._degree - 1] + AS_NOTATION[self._accidental]
    
    # Accidental change
    def __iadd__(self, semitones: int):
        if type(semitones) != int:
            raise TypeError(f"semitones must be int, not {type(semitones).__name__}")

        self._accidental = Accidental(self._accidental.value + semitones)

        return self
    
    def __add__(self, semitones: int):
        if type(semitones) != int:
            raise TypeError(f"semitones must be int, not {type(semitones).__name__}")

        return Roman(self._degree, Accidental(self._accidental.value + semitones))

    def __isub__(self, semitones: int):
        return self.__iadd__(-semitones)
    
    def __sub__(self, semitones: int):
        return self.__add__(-semitones)
    
    # Letter change
    def __rshift__(self, shift: int):
        return Roman((self._degree + shift) % 7 + 1, self._accidental)
    
    def __irshift__(self, shift: int):
        self._degree = (self._degree + shift) % 7 + 1
        return self
    
    def __lshift__(self, shift: int):
        return self.__rshift__(-shift)

    def __ilshift__(self, shift: int):
        return self.__irshift__(-shift)

    # Same or enharmonically equivalent
    def __eq__(self, other):
        if type(other) != Roman:
            raise TypeError(f"other must be roman, not {type(other).__name__}")

        return int(self) == int(other)
    
    def __ne__(self, other):
        if type(other) != Roman:
            raise TypeError(f"other must be roman, not {type(other).__name__}")

        return int(self) != int(other)
    
    @property
    def degree(self):
        return self._degree
    
    @property
    def accidental(self):
        return self._accidental