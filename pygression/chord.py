# Comprised of a note, quality, and modifiers, they are the building blocks of progressions
from copy import deepcopy
from .note import Note
from .utils import nth_letter_from
from .quality.base import Quality
from .quality.triad import Major, Minor
from .modifier.base import Modifier

class Chord:
    def __init__(self, root: Note, quality: Quality=Major()):
        if type(root) != Note:
            raise TypeError(f"root must be note, not {type(root).__name__}")
        if not issubclass(type(quality), Quality):
            raise TypeError(f"quality must be quality, not {type(quality).__name__}")

        self._root = root
        self._quality = quality
        self._inversion = 0
        self._modifiers = []
        self._notes = []

        self._calculate_notes()
    
    def __repr__(self):
        return str(self._root) + str(self._quality) + self._quality.figured_bass(0) + "".join(str(modifier) for modifier in self._modifiers) + ("/" + str(self._notes[0]) if self._inversion != 0 else "")

    def __str__(self):
        return str(self._root) + str(self._quality) + self._quality.figured_bass(0) + "".join(str(modifier) for modifier in self._modifiers) + ("/" + str(self._notes[0]) if self._inversion != 0 else "")
    
    # Add modifier
    def attach(self, new_modifier: Modifier):
        if not issubclass(type(new_modifier), Modifier):
            raise TypeError(f"must be modifier, not {type(new_modifier).__name__}")
        if not new_modifier._compatible_with_quality(self._quality):
            raise TypeError(f"cannot apply {type(new_modifier).__name__} to {type(self._quality).__name__}")

        if new_modifier not in self._modifiers:
            self._modifiers.append(new_modifier)
        self._modifiers = sorted([modifier for modifier in self._modifiers if new_modifier._compatible_with_mod(modifier)])
        self._calculate_notes()

        return self

    # Remove modifier
    def detach(self, modifier):
        self._modifiers.remove(modifier)
        return self

    def with_mod(self, new_modifier: Modifier):
        if not issubclass(type(new_modifier), Modifier):
            raise TypeError(f"must be modifier, not {type(new_modifier).__name__}")
        if not new_modifier._compatible_with_quality(self._quality):
            raise TypeError(f"cannot apply {type(new_modifier).__name__} to {type(self._quality).__name__}")
        
        new_chord = deepcopy(self)
        if new_modifier not in new_chord._modifiers:
            new_chord._modifiers.append(new_modifier)
        new_chord._modifiers = sorted([modifier for modifier in new_chord._modifiers if new_modifier._compatible_with_mod(modifier)])
        new_chord._calculate_notes()

        return new_chord            

    def without_mod(self, modifier):
        new_chord = deepcopy(self)
        new_chord._modifiers.remove(modifier)

        return new_chord

    # Inversions
    def __irshift__(self, inversions: int):
        if type(inversions) != int:
            raise TypeError(f"must be int, not {type(inversions).__name__}")

        highest_inversion = 3
        if len(self._modifiers) > 0 and str(self._modifiers[-1]) in ("no3", "no5"):
            highest_inversion -= 1
        if len(self._modifiers) > 1 and str(self._modifiers[-2]) in ("no3", "no5"):
            highest_inversion -= 1

        self._inversion += inversions
        self._inversion %= highest_inversion

        self._calculate_notes()
        
        return self

    def __rshift__(self, inversions: int):
        if type(inversions) != int:
            raise TypeError(f"must be int, not {type(inversions).__name__}")

        new_chord = deepcopy(self)
        
        highest_inversion = 3
        if len(new_chord._modifiers) > 0 and str(new_chord._modifiers[-1]) in ("no3", "no5"):
            highest_inversion -= 1
        if len(new_chord._modifiers) > 1 and str(new_chord._modifiers[-2]) in ("no3", "no5"):
            highest_inversion -= 1

        new_chord._inversion += inversions
        new_chord._inversion %= highest_inversion
        
        new_chord._calculate_notes()
        
        return new_chord
    
    def __ilshift__(self, inversions):
        return self.__irshift__(-inversions)

    def __lshift__(self, inversions):
        return self.__rshift__(-inversions)
    
    # Get nth note of chord
    def __getitem__(self, index) -> Note:
        return self._notes[index]
    
    # Same or enharmonically equivalent
    def __eq__(self, other) -> bool:
        if type(other) != Chord:
            raise TypeError(f"must be chord, not {type(other).__name__}")

        return self._notes == other._notes
    
    def __ne__(self, other) -> bool:
        if type(other) != Chord:
            raise TypeError(f"must be chord, not {type(other).__name__}")

        return self._notes != other._notes
    
    def __getitem__(self, index: int):
        return self._notes[index]

    # Slash chords, explicit inversion
    def __idiv__(self, note: Note):
        for _ in range(len(self._notes)):
            if self[0].letter == note.letter and self[0].accidental == note.accidental:
                return self
             
            self >>= 1
        
        raise ValueError("note doesn't exist in chord")
    
    def __truediv__(self, note: Note):
        test = deepcopy(self)

        for _ in range(len(test._notes)):
            if test[0].letter == note.letter and test[0].accidental == note.accidental:
                return test
             
            test >>= 1
        
        raise ValueError("note doesn't exist in chord")

    # Calculate the notes for the chord from the root, quality, and modifiers
    def _calculate_notes(self):
        '''
        Steps:
        1. Build core chord
        2. Apply modifiers
        3. Apply inversion
        '''
        self._notes = self._quality.build_core(self._root)

        for i in range(len(self._modifiers)):
            self._notes = self._modifiers[i].modify(self._root, self._notes)
        
        # Switch back to major if minor with a missing third or if only note (from no3no5 for some reason)
        if (type(self._quality) == Minor and len(self._notes) >= 2 and nth_letter_from(self._notes[0].letter, 2) != self._notes[1].letter) or (len(self._notes) == 1):
            self._quality = Major()

        self._inversion %= len(self._notes)
        for i in range(self._inversion):
            self._notes.append(self._notes.pop(0))
    
    @property
    def root(self) -> Note:
        return self._root
    
    @root.setter
    def root(self, new_root):
        if type(new_root) != Note:
            raise TypeError(f"must be note, not {type(new_root).__name__}")

        self._root = new_root
        self._calculate_notes()
    
    @property
    def quality(self) -> Quality:
        return self._quality
    
    @quality.setter
    def quality(self, new_quality):
        if not issubclass(type(new_quality), Quality):
            raise TypeError(f"must be quality, not {type(new_quality).__name__}")

        self._quality = new_quality
        self._calculate_notes()
    
    @property
    def inversion(self) -> int:
        return self._inversion
    
    @property
    def notes(self) -> str:
        return '-'.join(map(str, self._notes))
    
    @property
    def modifiers(self):
        return self._modifiers
    
    @modifiers.setter
    def modifiers(self, new_modifiers):
        self._modifiers = new_modifiers
        self._calculate_notes()