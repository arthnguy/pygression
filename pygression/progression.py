# Basically a list specifically tailored to chord progressions
from typing import List
from copy import deepcopy
from .chord import Chord
from .roman import Roman
from .romanchord import RomanChord
from .note import Note
from .consts import Accidental, Mode
from .quality.triad import *

class Progression:
    def __init__(self, items=None, mode: Mode=Mode.ION, relative_to: Mode=Mode.ION):
        if type(mode) != Mode:
            raise TypeError(f"mode must be mode, not {type(mode).__name__}")
        if type(relative_to) != Mode:
            raise TypeError(f"relative_to must be mode, not {type(relative_to).__name__}")
        if items != None and type(items) != list:
            raise TypeError(f"items must be list, not {type(items).__name__}")
            
        self._mode = mode
        self._relative_to = relative_to
        self._chords = []

        for item in items:
            self.append(item)

    # Get notes for scale in the specified mode
    def _calculate_scale(self, mode: Mode) -> List[Note]:
        scale = []
        for i in range(7):
            scale.append(self._key >> i)

        # Apply accidentals
        for i in range(7):
            semitones = (mode.value[i] + int(self._key) - int(scale[i])) % 12
            if semitones > 2:
                semitones -= 12
                
            scale[i] += semitones
        
        return scale
    
    def __repr__(self) -> str:
        return str(self._chords)

    def __str__(self) -> str:
        return str(self._chords)

    def __add__(self, prog: "Progression") -> "Progression":
        new_prog = deepcopy(self)
        new_prog._chords += prog._chords

        return new_prog
    
    def __iadd__(self, prog: "Progression") -> "Progression":
        self._chords += prog._chords
        return self

    def __getitem__(self, index: int) -> RomanChord:
        if index >= len(self._chords) or index < -len(self._chords):
            raise IndexError("progression index out of range")

        return self._chords[index]
    
    def __setitem__(self, index: int, new_chord: RomanChord):
        if index >= len(self._chords) or index < -len(self._chords):
            raise IndexError("progression index out of range")

        self._chords[index] = new_chord
    
    @property
    def mode(self) -> Mode:
        return self._mode
    
    # Mode change
    @mode.setter
    def mode(self, new_mode: Mode):
        if type(new_mode) != Mode:
            raise TypeError(f"must be mode, not {type(new_mode).__name__}")

        self._mode = new_mode
    
    @property
    def relative_to(self) -> Mode:
        return self._relative_to
    
    @relative_to.setter
    def relative_to(self, new_mode: Mode):
        if type(new_mode) != Mode:
            raise TypeError(f"must be mode, not {type(new_mode).__name__}")

        for chord in self._chords:
            chord.roman += new_mode - self._relative_to

            if chord._target != None:
                chord._target.roman += new_mode - self._relative_to

        self._relative_to = new_mode
    
    @property
    def chords(self) -> List[Chord]:
        return self._chords
    
    def _append_degree(self, degree: int):
        if degree < 1 or degree > 7:
            raise ValueError("degree must be between 1 and 7")

        scale = self._mode.value
        integers = [int(scale[degree - 1]), int(scale[(degree + 1) % 7]), int(scale[(degree + 3) % 7])]
        integers[1] -= integers[0]
        integers[1] %= 12
        integers[2] -= integers[0]
        integers[2] %= 12
        integers[0] = 0

        quality = None

        if integers == Major.get_integers():
            quality = Major()
        elif integers == Minor.get_integers():
            quality = Minor()
        elif integers == Diminished.get_integers():
            quality = Diminished()
        elif integers == Augmented.get_integers():
            quality = Augmented()

        self._chords.append(RomanChord(Roman(degree, accidental=Accidental(self._mode.value[degree - 1] - self._relative_to.value[degree - 1])), quality=quality))

    def _append_chord(self, chord: Chord):
        self._chords.append(chord)
    
    def _insert_degree(self, degree: int, index: int):
        if degree < 1 or degree > 7:
            raise ValueError("degree must be between 1 and 7")

        scale = self._mode.value
        integers = [int(scale[degree - 1]), int(scale[(degree + 1) % 7]), int(scale[(degree + 3) % 7])]
        integers[1] -= integers[0]
        integers[1] %= 12
        integers[2] -= integers[0]
        integers[2] %= 12
        integers[0] = 0

        quality = None

        if integers == Major.get_integers():
            quality = Major()
        elif integers == Minor.get_integers():
            quality = Minor()
        elif integers == Diminished.get_integers():
            quality = Diminished()
        elif integers == Augmented.get_integers():
            quality = Augmented()
        
        self._chords.insert(index, RomanChord(Roman(degree, accidental=Accidental(self._mode.value[degree - 1] - self._relative_to.value[degree - 1])), quality=quality))
    
    def _insert_chord(self, chord: Chord, index: int):
        self._chords.insert(index, chord)

    def append(self, item):
        if type(item) == int:
            self._append_degree(item)
        elif type(item) == RomanChord:
            self._append_chord(item)
        else:
            raise TypeError(f"item must be int or Chord, not {type(item).__name__}")
    
    def insert(self, index: int, item):
        if type(item) == int:
            self._insert_degree(item, index)
        elif type(item) == RomanChord:
            self._insert_chord(item, index)
        else:
            raise TypeError(f"item must be int or Chord, not {type(item).__name__}")
    
    def pop(self, index: int=-1) -> Chord:
        return self._chords.pop(index)
    
    def chords_in(self, key: Note) -> List[Chord]:
        if key.accidental.value < -1 or key.accidental.value > 1:
            raise ValueError("cannot have double accidentals as key")

        chords = []
        scale = self._relative_to.value

        for chord in self._chords:
            degree = (chord.roman.degree + (0 if chord._target == None else chord._target.roman.degree - 1)) % 7

            root = Note(key.letter) >> (degree - 1)
            accidental = scale[degree - 1] + chord.roman.accidental.value + (chord._target.roman.accidental.value if chord._target != None else 0) - (int(root) - int(key))
            if accidental > 2:
                accidental -= 12
            root.accidental = Accidental(accidental)
            
            new_chord = Chord(root, quality=chord.quality) >> chord._inversion
            new_chord.modifiers = deepcopy(chord._modifiers)

            chords.append(new_chord)

        return chords