from .base import Modifier
from ..note import Note
from ..utils import nth_letter_from

class No3(Modifier):
    def __str__(self):
        return "no3"
    
    def __repr__(self):
        return "no3"
    
    def _get_priority(self) -> int:
        return 9
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) != "sus2" and str(modifier) != "sus4"

    def _compatible_with_quality(self, quality) -> bool:
        return True
    
    def modify(self, root: Note, notes: [Note]) -> [Note]:
        modified_notes = notes.copy()
        modified_notes.pop(1)

        return modified_notes

class No5(Modifier):
    def __str__(self):
        return "no5"
    
    def __repr__(self):
        return "no3"
    
    def _get_priority(self) -> int:
        return 10
    
    def _compatible_with_mod(self, modifier) -> bool:
        return str(modifier) != "b5" and str(modifier) != "#5"
    
    def _compatible_with_quality(self, quality) -> bool:
        return True

    def modify(self, root: Note, notes: [Note]) -> [Note]:
        modified_notes = notes.copy()
        modified_notes.pop(2)

        return modified_notes