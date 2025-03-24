# Dictates how the chord is built
from abc import ABC, abstractmethod
from ..note import Note
from ..consts import Letter
from ..utils import nth_letter_from

class Quality(ABC):
    @abstractmethod
    def __str__(self):
        pass
    
    # Notes of the chord as integers
    @staticmethod
    @abstractmethod
    def get_integers(self) -> [int]:
        pass
    
    # For Roman numeral analysis
    @abstractmethod
    def figured_bass(self) -> str:
        pass

    def build_core(self, root: Note) -> [Note]:
        notes = []
        integers = self.get_integers()

        for i in range(len(integers)):
            notes.append(Note.note_relative_to(nth_letter_from(root.letter, i * 2), root, integers[i]))

        return notes