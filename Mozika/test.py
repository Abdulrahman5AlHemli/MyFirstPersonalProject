# Global chromatic scale used in note calculations.
CHROMATIC = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

class Scale:
    def __init__(self, name: str, intervals: list):
        """
        Initialize a Scale with a given name and interval pattern.
        
        Parameters:
        - name: Name of the scale (e.g., "Major Scale")
        - intervals: A list of intervals (in semitones) defining the scale.
        """
        self.name = name
        self.intervals = intervals

    def get_notes(self, root: str) -> list:
        """
        Generate the full scale (including the octave) from the given root note.
        
        Parameters:
        - root: The starting note (e.g., 'C')
        
        Returns:
        A list of note names representing the scale.
        """
        try:
            start = CHROMATIC.index(root)
        except ValueError:
            raise ValueError("Invalid root note. Choose from: " + ", ".join(CHROMATIC))
            
        notes = [root]
        current_index = start
        for interval in self.intervals:
            current_index = (current_index + interval) % len(CHROMATIC)
            notes.append(CHROMATIC[current_index])
        return notes

    def get_scale_degrees(self, root: str) -> list:
        """
        Get the scale degrees without the duplicate octave.
        
        Parameters:
        - root: The starting note
        
        Returns:
        A list of the unique notes in the scale (7 degrees for a diatonic scale).
        """
        notes = self.get_notes(root)
        # If the last note (the octave) is the same as the first, drop it.
        if notes[-1] == notes[0]:
            notes = notes[:-1]
        return notes

    def get_triad(self, root: str, degree: int) -> list:
        """
        Build a triad (3-note chord) from the scale based on the specified degree.
        
        Parameters:
        - root: The root of the scale (e.g., 'C')
        - degree: The scale degree on which to build the chord (0-indexed, 0 for I, 1 for ii, etc.)
        
        Returns:
        A list of three notes forming the chord.
        """
        scale_degrees = self.get_scale_degrees(root)
        chord = [
            scale_degrees[degree % len(scale_degrees)],
            scale_degrees[(degree + 2) % len(scale_degrees)],
            scale_degrees[(degree + 4) % len(scale_degrees)]
        ]
        return chord

    def get_seventh_chord(self, root: str, degree: int) -> list:
        """
        Build a seventh chord (4-note chord) from the scale based on the specified degree.
        
        Parameters:
        - root: The root of the scale (e.g., 'C')
        - degree: The scale degree on which to build the chord (0-indexed)
        
        Returns:
        A list of four notes forming the seventh chord.
        """
        scale_degrees = self.get_scale_degrees(root)
        chord = [
            scale_degrees[degree % len(scale_degrees)],
            scale_degrees[(degree + 2) % len(scale_degrees)],
            scale_degrees[(degree + 4) % len(scale_degrees)],
            scale_degrees[(degree + 6) % len(scale_degrees)]
        ]
        return chord

    def rotate_intervals(self, n: int) -> list:
        """
        Rotate the interval list by n positions (useful for generating modes).
        """
        return self.intervals[n:] + self.intervals[:n]

    def get_mode(self, mode_name: str):
        """
        Generate a new Scale object representing a mode derived from this scale.
        For the major scale, modes like Ionian, Dorian, etc., are rotations.
        
        Parameters:
        - mode_name: The name of the mode (e.g., "dorian")
        
        Returns:
        A new Scale object with a rotated interval pattern.
        """
        major_modes = {
            "ionian": 0,
            "dorian": 1,
            "phrygian": 2,
            "lydian": 3,
            "mixolydian": 4,
            "aeolian": 5,
            "locrian": 6,
        }
        mode_key = mode_name.lower()
        if mode_key not in major_modes:
            raise ValueError("Mode not recognized. Choose from: " + ", ".join(major_modes.keys()))
        rotation = major_modes[mode_key]
        rotated_intervals = self.rotate_intervals(rotation)
        return Scale(f"{self.name} ({mode_name.title()} Mode)", rotated_intervals)

# Define specific scale classes.

class MajorScale(Scale):
    def __init__(self):
        # Major (Ionian) scale interval pattern: W-W-H-W-W-W-H (2,2,1,2,2,2,1)
        super().__init__("Major Scale", [2, 2, 1, 2, 2, 2, 1])

class HarmonicMinorScale(Scale):
    def __init__(self):
        # Harmonic minor interval pattern: 2,1,2,2,1,3,1
        super().__init__("Harmonic Minor Scale", [2, 1, 2, 2, 1, 3, 1])

class MelodicMinorScale(Scale):
    def __init__(self):
        # Melodic minor (ascending) interval pattern: 2,1,2,2,2,2,1
        super().__init__("Melodic Minor Scale (Ascending)", [2, 1, 2, 2, 2, 2, 1])

# Example usage:
if __name__ == '__main__':
    # Create a C Major scale.
    major = MajorScale()
    root = 'C'
    print("C Major Scale:", major.get_notes(root))
    
    # Generate triads on each degree of the C Major scale.
    print("\nTriads in C Major:")
    for i in range(7):
        chord = major.get_triad(root, i)
        # Label degrees I, ii, iii, IV, V, vi, vii° (we can refine the labels later)
        print(f"Degree {i+1}: {chord}")
    
    # Generate seventh chords on each degree of the C Major scale.
    print("\nSeventh Chords in C Major:")
    for i in range(7):
        chord = major.get_seventh_chord(root, i)
        print(f"Degree {i+1}: {chord}")
    
    # Also, using a mode (e.g., Dorian) from the Major scale.
    dorian = major.get_mode("dorian")
    print("\nC Dorian Mode (derived from C Major):", dorian.get_notes(root))
    print("Triad on 1st degree in C Dorian:", dorian.get_triad(root, 0))
