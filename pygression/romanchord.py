from copy import deepcopy
from .roman import Roman
from .quality.base import Quality
from .quality.triad import Major, Minor
from .modifier.base import Modifier

class RomanChord:
    def __init__(self, roman: Roman, quality: Quality=Major()):
        if type(roman) != Roman:
            raise TypeError(f"roman must be roman, not {type(roman).__name__}")
        if not issubclass(type(quality), Quality):
            raise TypeError(f"quality must be quality, not {type(quality).__name__}")

        self._roman = roman
        self._quality = quality
        self._inversion = 0
        self._modifiers = []
        
        self._target = None
    
    def __repr__(self) -> str:
        s = str(self._roman)

        if str(self._quality) in ("m", "o", "ø"):
            s = s.lower()
        if str(self._quality) != "m":
            s += str(self._quality)

        return s + self._quality.figured_bass(self._inversion) + "".join(str(modifier) for modifier in self._modifiers) + ("/" + str(self._target) if self._target != None else "")

    def __str__(self) -> str:
        s = str(self._roman)

        if str(self._quality) in ("m", "o", "ø"):
            s = s.lower()
        if str(self._quality) != "m":
            s += str(self._quality)

        return s + self._quality.figured_bass(self._inversion) + "".join(str(modifier) for modifier in self._modifiers) + ("/" + str(self._target) if self._target != None else "")
    
    # Secondary chords
    def __idiv__(self, target: "RomanChord") -> "RomanChord":
        if target._roman != Roman(1):
            self._target = target
        else:
            self._target = None

        return self
    
    def __truediv__(self, target: "RomanChord") -> "RomanChord":
        chord = deepcopy(self)

        if target._roman != Roman(1):
            chord._target = target
        else:
            chord._target = None
        
        return chord
    
    # Inversions
    def __irshift__(self, inversions: int) -> "RomanChord":
        if type(inversions) != int:
            raise TypeError(f"must be int, not {type(inversions).__name__}")

        highest_inversion = 3
        if len(self._modifiers) > 0 and str(self._modifiers[-1]) in ("no3", "no5"):
            highest_inversion -= 1
        if len(self._modifiers) > 1 and str(self._modifiers[-2]) in ("no3", "no5"):
            highest_inversion -= 1

        self._inversion += inversions
        self._inversion %= highest_inversion
        
        return self

    def __rshift__(self, inversions: int) -> "RomanChord":
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
        
        return new_chord
    
    def __ilshift__(self, inversions: int) -> "RomanChord":
        return self.__irshift__(-inversions)

    def __lshift__(self, inversions: int) -> "RomanChord":
        return self.__rshift__(-inversions)
    
    # Add modifier
    def attach(self, new_modifier: Modifier) -> "RomanChord":
        if not issubclass(type(new_modifier), Modifier):
            raise TypeError(f"must be modifier, not {type(new_modifier).__name__}")
        if not new_modifier._compatible_with_quality(self._quality):
            raise TypeError(f"cannot apply {type(new_modifier).__name__} to {type(self._quality).__name__}")

        if new_modifier not in self._modifiers:
            self._modifiers.append(new_modifier)
        self._modifiers = [modifier for modifier in self._modifiers if new_modifier._compatible_with_mod(modifier)]

        return self

    # Remove modifier
    def detach(self, modifier: Modifier) -> "RomanChord":
        self._modifiers.remove(modifier)
        return self

    def with_mod(self, new_modifier: Modifier) -> "RomanChord":
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

    def without_mod(self, modifier: Modifier) -> "RomanChord":
        new_chord = deepcopy(self)
        new_chord._modifiers.remove(modifier)

        return new_chord
    
    @property
    def roman(self) -> Roman:
        return self._roman
    
    @roman.setter
    def roman(self, new_roman: Roman):
        if type(new_roman) != Roman:
            raise TypeError(f"must be roman, not {type(new_roman).__name__}")
        
        self._roman = new_roman
    
    @property
    def target(self) -> "RomanChord":
        if self._target != None:
            return self._target
        else:
            return RomanChord(Roman(1))
    
    @property
    def quality(self) -> Quality:
        return self._quality
    
    @quality.setter
    def quality(self, new_quality: Quality):
        if not issubclass(type(new_quality), Quality):
            raise TypeError(f"must be quality, not {type(new_quality).__name__}")

        self._quality = new_quality