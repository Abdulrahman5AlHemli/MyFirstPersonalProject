# -------------------------------
# Absolute Chord Builder (Semitone Based)
# -------------------------------

# Define the chromatic scale (12 semitones).
CHROMATIC = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Dictionary mapping chord type names to their semitone offsets from the root note.
CHORD_SEMITONE_PATTERNS = {
    # Triads:
    "maj": [0, 4, 7],       # Major triad: root, major 3rd (4 semitones), perfect 5th (7 semitones)
    "min": [0, 3, 7],       # Minor triad: root, minor 3rd (3 semitones), perfect 5th (7 semitones)
    "dim": [0, 3, 6],       # Diminished triad: root, minor 3rd (3 semitones), diminished 5th (6 semitones)
    "aug": [0, 4, 8],       # Augmented triad: root, major 3rd (4 semitones), augmented 5th (8 semitones)

    # Seventh Chords:
    "maj7": [0, 4, 7, 11],  # Major 7th: add a major 7th (11 semitones)
    "7":    [0, 4, 7, 10],  # Dominant 7th: add a minor 7th (10 semitones)
    "min7": [0, 3, 7, 10],  # Minor 7th: minor triad plus minor 7th
    "m(maj7)": [0, 3, 7, 11],  # Minor/major 7th: minor triad plus major 7th
    "dim7": [0, 3, 6, 9],   # Fully diminished 7th: diminished triad plus diminished 7th (9 semitones)
    "halfdim7": [0, 3, 6, 10],  # Half-diminished (m7b5): diminished triad plus minor 7th
    # Extended chords (example):
    "9": [0, 4, 7, 10, 14],     # Dominant 9th: add a 9th (14 semitones; note 14 mod 12 = 2, so be mindful of naming)
    # Additional chord types can be added here.
}

def build_chord(root: str, chord_type: str) -> list:
    """
    Build an absolute chord from a root note and chord type by using semitone offsets.
    
    Parameters:
        root (str): The chord's root note (e.g., 'C', 'D#').
        chord_type (str): A chord type key from CHORD_SEMITONE_PATTERNS (e.g., 'min', 'maj7').
        
    Returns:
        list: A list of note names that form the chord.
    """
    chord_type = chord_type.lower()
    if chord_type not in CHORD_SEMITONE_PATTERNS:
        raise ValueError("Chord type not recognized. Options: " + ", ".join(CHORD_SEMITONE_PATTERNS.keys()))
    
    offsets = CHORD_SEMITONE_PATTERNS[chord_type]
    
    try:
        root_index = CHROMATIC.index(root)
    except ValueError:
        raise ValueError(f"Invalid root note '{root}'. Must be one of: {', '.join(CHROMATIC)}")
    
    chord_notes = []
    for offset in offsets:
        note_index = (root_index + offset) % 12
        chord_notes.append(CHROMATIC[note_index])
    return chord_notes

# -------------------------------
# Diatonic Key (Scale-Based) Classes
# -------------------------------

class Key:
    """
    Base class representing a musical key by its diatonic scale.
    A Key is defined by a root note and a series of intervals (in semitones)
    that generate the scale.
    """
    def __init__(self, root: str, scale_intervals: list, key_name: str):
        """
        Parameters:
            root (str): The key's root note (e.g., 'C', 'A').
            scale_intervals (list): The interval pattern (in semitones) for the scale.
                                  For example, a major scale uses [2,2,1,2,2,2,1].
            key_name (str): A descriptive name for the key (e.g., "Major Key").
        """
        self.root = root
        self.scale_intervals = scale_intervals
        self.key_name = key_name
        self.scale_notes = self._generate_scale_notes()  # Full scale, including octave

    def _generate_scale_notes(self) -> list:
        """
        Generate the full scale (including the octave) starting from the root,
        using the provided interval pattern.
        """
        try:
            start = CHROMATIC.index(self.root)
        except ValueError:
            raise ValueError("Invalid root note for key. Choose from: " + ", ".join(CHROMATIC))
        
        notes = [self.root]
        current_index = start
        for interval in self.scale_intervals:
            current_index = (current_index + interval) % 12
            notes.append(CHROMATIC[current_index])
        return notes

    def get_scale_degrees(self) -> list:
        """
        Return the unique scale degrees (diatonic scale) by dropping the duplicate octave.
        """
        notes = self.scale_notes[:]
        if notes[-1] == notes[0]:
            notes = notes[:-1]
        return notes

    def get_diatonic_triad(self, degree: int) -> list:
        """
        Build a triad (3-note chord) on a specified scale degree within the key.
        
        Parameters:
            degree (int): The 0-indexed degree on which to build the chord.
                For instance, 0 for the I chord, 1 for the ii chord, etc.
                
        Returns:
            list: The list of note names for the triad.
        """
        scale_degrees = self.get_scale_degrees()
        # Construct the triad by taking every other note:
        chord = [
            scale_degrees[degree % len(scale_degrees)],
            scale_degrees[(degree + 2) % len(scale_degrees)],
            scale_degrees[(degree + 4) % len(scale_degrees)]
        ]
        return chord

    def get_diatonic_seventh(self, degree: int) -> list:
        """
        Build a seventh chord (4-note chord) on a specified scale degree within the key.
        
        Parameters:
            degree (int): The 0-indexed degree for the chord.
            
        Returns:
            list: The list of note names for the seventh chord.
        """
        scale_degrees = self.get_scale_degrees()
        chord = [
            scale_degrees[degree % len(scale_degrees)],
            scale_degrees[(degree + 2) % len(scale_degrees)],
            scale_degrees[(degree + 4) % len(scale_degrees)],
            scale_degrees[(degree + 6) % len(scale_degrees)]
        ]
        return chord

class MajorKey(Key):
    """
    Represents a major key (diatonic). The interval pattern for a major scale is:
    2, 2, 1, 2, 2, 2, 1.
    """
    def __init__(self, root: str):
        super().__init__(root, [2, 2, 1, 2, 2, 2, 1], "Major Key")

class HarmonicMinorKey(Key):
    """
    Represents a harmonic minor key. Its interval pattern is:
    2, 1, 2, 2, 1, 3, 1.
    """
    def __init__(self, root: str):
        super().__init__(root, [2, 1, 2, 2, 1, 3, 1], "Harmonic Minor Key")

class MelodicMinorKey(Key):
    """
    Represents an ascending melodic minor key. Its interval pattern is:
    2, 1, 2, 2, 2, 2, 1.
    Note: In actual practice, the descending melodic minor is often identical to the natural minor.
    """
    def __init__(self, root: str):
        super().__init__(root, [2, 1, 2, 2, 2, 2, 1], "Melodic Minor Key (Ascending)")

# -------------------------------
# Example Usage
# -------------------------------
if __name__ == "__main__":
    # -------------------------------
    # Absolute chord building examples:
    # -------------------------------
    print("Absolute Chord Building (Semitone Based):")
    print("D minor triad:", build_chord("D", "min"))    # Expected: ['D', 'F', 'A']
    print("D major triad:", build_chord("D", "maj"))      # Expected: ['D', 'F#', 'A']
    print("G7 chord:", build_chord("G", "7"))             # Expected: ['G', 'B', 'D', 'F']
    print("Cmaj7 chord:", build_chord("C", "maj7"))       # Expected: ['C', 'E', 'G', 'B']
    print()

    # -------------------------------
    # Diatonic key examples:
    # -------------------------------
    print("Diatonic Key-Based (Scale-Based) Chord Building:")
    # C Major Key:
    key_c = MajorKey("C")
    print("C Major Scale:", key_c.get_scale_degrees())
    for i in range(7):
        triad = key_c.get_diatonic_triad(i)
        print(f"Triad on degree {i+1} of C Major:", triad)
        
    print()
    # A Harmonic Minor Key:
    key_a_hmin = HarmonicMinorKey("A")
    print("A Harmonic Minor Scale:", key_a_hmin.get_scale_degrees())
    for i in range(7):
        triad = key_a_hmin.get_diatonic_triad(i)
        print(f"Triad on degree {i+1} of A Harmonic Minor:", triad)
        
    print()
    # A Melodic Minor Key:
    key_a_mmin = MelodicMinorKey("A")
    print("A Melodic Minor Scale (Ascending):", key_a_mmin.get_scale_degrees())
    for i in range(7):
        triad = key_a_mmin.get_diatonic_triad(i)
        print(f"Triad on degree {i+1} of A Melodic Minor:", triad)
    print(build_chord("F","halfdim7"))