# Comprised of a letter and accidental, used to denote the root in chords and key in progressions
from .utils import nth_letter_from
from .consts import Letter, Accidental, AS_NOTATION

class Note:
    def __init__(self, letter: Letter, accidental: Accidental=Accidental.NATURAL):
        if type(letter) != Letter:
            raise TypeError(f"letter must be letter, not {type(letter).__name__}")
        if type(accidental) != Accidental:
            raise TypeError(f"accidental must be accidental, not {type(accidental).__name__}")

        self._letter = letter
        self._accidental = accidental
    
    def __int__(self) -> int:
        return (self._letter.value + self._accidental.value) % 12

    def __repr__(self) -> str:
        return AS_NOTATION[self._letter] + AS_NOTATION[self._accidental]

    def __str__(self) -> str:
        return AS_NOTATION[self._letter] + AS_NOTATION[self._accidental]
    
    # Accidental change
    def __iadd__(self, semitones: int) -> "Note":
        if type(semitones) != int:
            raise TypeError(f"semitones must be int, not {type(semitones).__name__}")

        self._accidental = Accidental(self._accidental.value + semitones)

        return self
    
    def __add__(self, semitones: int) -> "Note":
        if type(semitones) != int:
            raise TypeError(f"semitones must be int, not {type(semitones).__name__}")

        return Note(self._letter, Accidental(self._accidental.value + semitones))

    def __isub__(self, semitones: int) -> "Note":
        return self.__iadd__(-semitones)
    
    def __sub__(self, semitones: int) -> "Note":
        return self.__add__(-semitones)
    
    # Letter change
    def __rshift__(self, shift: int) -> "Note":
        return Note(nth_letter_from(self._letter, shift), self._accidental)
    
    def __irshift__(self, shift: int) -> "Note":
        self._letter = nth_letter_from(self._letter, shift)
        return self
    
    def __lshift__(self, shift: int) -> "Note":
        return self.__rshift__(-shift)

    def __ilshift__(self, shift: int) -> "Note":
        return self.__irshift__(-shift)

    # Same or enharmonically equivalent
    def __eq__(self, other: "Note") -> bool:
        if type(other) != Note:
            raise TypeError(f"other must be note, not {type(other).__name__}")

        return int(self) == int(other)
    
    def __ne__(self, other: "Note") -> bool:
        if type(other) != Note:
            raise TypeError(f"other must be note, not {type(other).__name__}")

        return int(self) != int(other)
    
    @property
    def letter(self) -> Letter:
        return self._letter
    
    @letter.setter
    def letter(self, new_letter: Letter):
        self._letter = new_letter

    @property
    def accidental(self) -> Accidental:
        return self._accidental
    
    @accidental.setter
    def accidental(self, new_accidental: Accidental):
        self._accidental = new_accidental
    
    @staticmethod
    def note_relative_to(letter: Letter, root: "Note", semitones: int) -> "Note":
        accidental = (semitones - (letter.value - int(root) + root.accidental.value) % 12)
        if accidental > 2:
            accidental -= 12

        return Note(letter, Accidental(accidental + root.accidental.value))