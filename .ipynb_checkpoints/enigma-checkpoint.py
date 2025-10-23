from string import ascii_uppercase
import subprocess
import os
import sys


class PlugLead:
    def __init__(self, mapping):
        if len(mapping) != 2:
            raise ValueError("Must connect exactly two letters")
        if mapping[0] == mapping[1]:
            raise ValueError("Cannot connect a letter to itself")
        self.first_letter = mapping[0].upper()
        self.second_letter = mapping[1].upper()
        self.encoding = {
            self.first_letter: self.second_letter,
            self.second_letter: self.first_letter
        }
    
    def encode(self, letter):
        letter = letter.upper()
        return self.encoding.get(letter, letter)


class Plugboard:
    def __init__(self):
        self.wire_map = {}
    
    def add(self, plug_lead):
        if plug_lead.first_letter in self.wire_map or plug_lead.second_letter in self.wire_map:
            raise ValueError("Letter already connected")
        self.wire_map[plug_lead.first_letter] = plug_lead.second_letter
        self.wire_map[plug_lead.second_letter] = plug_lead.first_letter
    
    def encode(self, letter):
        return self.wire_map.get(letter.upper(), letter.upper())


class Rotor:
    def __init__(self, wiring, position='A', ring_setting=1, notch=''):
        self.forward_wiring = wiring.upper()
        self.backward_wiring = self._create_reverse_wiring()
        self.turnover_position = notch.upper()
        self.ring_offset = ring_setting - 1
        self.current_offset = 0
        self._set_to_position(position.upper())
    
    def _create_reverse_wiring(self):
        reverse = [''] * 26
        for idx, char in enumerate(self.forward_wiring):
            reverse[ord(char) - ord('A')] = chr(idx + ord('A'))
        return ''.join(reverse)
    
    def _set_to_position(self, target_letter):
        target_value = ord(target_letter) - ord('A')
        while self.current_offset != target_value:
            self.current_offset = (self.current_offset + 1) % 26
    
    def position(self):
        return chr(self.current_offset + ord('A'))
    
    def rotate(self):
        self.current_offset = (self.current_offset + 1) % 26
    
    def at_turnover(self):
        if not self.turnover_position:
            return False
        return self.position() in self.turnover_position
    
    def encode_forward(self, input_letter):
        shift_in = (ord(input_letter) - ord('A') + self.current_offset - self.ring_offset) % 26
        mapped_letter = self.forward_wiring[shift_in]
        shift_out = (ord(mapped_letter) - ord('A') - self.current_offset + self.ring_offset) % 26
        return chr(shift_out + ord('A'))
    
    def encode_backward(self, input_letter):
        shift_in = (ord(input_letter) - ord('A') + self.current_offset - self.ring_offset) % 26
        mapped_letter = self.backward_wiring[shift_in]
        shift_out = (ord(mapped_letter) - ord('A') - self.current_offset + self.ring_offset) % 26
        return chr(shift_out + ord('A'))
    
    def encode_right_to_left(self, input_letter):
        return self.encode_forward(input_letter)
    
    def encode_left_to_right(self, input_letter):
        return self.encode_backward(input_letter)


class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring.upper()
    
    def encode(self, letter):
        position = ord(letter) - ord('A')
        return self.wiring[position]


class RotorAssembly:
    ROTOR_CONFIGS = {
        'I': ('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q'),
        'II': ('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E'),
        'III': ('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V'),
        'IV': ('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J'),
        'V': ('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z'),
        'BETA': ('LEYJVCNIXWPBQMDRTAKZGFUHOS', ''),
        'GAMMA': ('FSOKANUERHMBTIYCWLQPZXVGJD', ''),
    }
    
    REFLECTOR_CONFIGS = {
        'A': 'EJMZALYXVBWFCRQUONTSPIKHGD',
        'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
        'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
    }
    
    def __init__(self, rotor_types, reflector_type, start_positions='AAA', ring_settings=(1,1,1)):
        self.rotors = []
        for idx, rotor_name in enumerate(reversed(rotor_types)):
            wiring, notch = self.ROTOR_CONFIGS[rotor_name.upper()]
            pos_idx = len(rotor_types) - 1 - idx
            pos = start_positions[pos_idx] if pos_idx < len(start_positions) else 'A'
            ring = ring_settings[pos_idx] if pos_idx < len(ring_settings) else 1
            self.rotors.append(Rotor(wiring, pos, ring, notch))
        
        reflector_wiring = self.REFLECTOR_CONFIGS[reflector_type.upper()]
        self.reflector = Reflector(reflector_wiring)
    
    def perform_rotation(self):
        if len(self.rotors) >= 3:
            if self.rotors[1].at_turnover():
                self.rotors[1].rotate()
                self.rotors[2].rotate()
            elif self.rotors[0].at_turnover():
                self.rotors[1].rotate()
        
        self.rotors[0].rotate()
    
    def pass_through(self, input_letter):
        current = input_letter
        
        for rotor in self.rotors:
            current = rotor.encode_forward(current)
        
        current = self.reflector.encode(current)
        
        for rotor in reversed(self.rotors):
            current = rotor.encode_backward(current)
        
        return current


class Enigma:
    def __init__(self):
        self.plugboard = Plugboard()
        self.rotor_assembly = None
    
    def setup(self, rotor_list, reflector_type, positions='AAA', rings=(1,1,1), plug_pairs=None):
        self.rotor_assembly = RotorAssembly(rotor_list, reflector_type, positions, rings)
        
        if plug_pairs:
            for pair in plug_pairs:
                wire = PlugLead(pair)
                self.plugboard.add(wire)
    
    def press_key(self, letter):
        if not self.rotor_assembly:
            raise RuntimeError("Machine not configured")
        
        letter = letter.upper()
        
        self.rotor_assembly.perform_rotation()
        
        after_plugboard = self.plugboard.encode(letter)
        through_rotors = self.rotor_assembly.pass_through(after_plugboard)
        final_letter = self.plugboard.encode(through_rotors)
        
        return final_letter
    
    def process_text(self, text):
        output = []
        for char in text.upper():
            if char in ascii_uppercase:
                output.append(self.press_key(char))
        return ''.join(output)


def build_enigma(rotor_list, reflector_type, positions='AAA', rings=(1,1,1), plug_pairs=None):
    machine = Enigma()
    machine.setup(rotor_list, reflector_type, positions, rings, plug_pairs)
    return machine


def rotor_from_name(rotor_name):
    """Helper function to create a rotor from its name for demonstrations"""
    if rotor_name.upper() not in RotorAssembly.ROTOR_CONFIGS:
        raise ValueError(f"Unknown rotor: {rotor_name}")
    
    wiring, notch = RotorAssembly.ROTOR_CONFIGS[rotor_name.upper()]
    return Rotor(wiring, 'A', 1, notch)


def run_tests_sequentially():
    """Runs all test files located in the 'tests' subdirectory."""

    # Define the order of test files to run
    test_files = [
        'test_pluglead.py',
        'test_plugboard.py',
        'test_rotor.py',
        'test_enigma.py',
    ]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    tests_dir = os.path.join(script_dir, 'tests')

    print("--- Running Enigma Component Tests ---")

    if not os.path.isdir(tests_dir):
        print(f"ERROR: The 'tests' directory was not found at: {tests_dir}")
        return

    all_passed = True

    for filename in test_files:
        filepath = os.path.join(tests_dir, filename)

        try:
            # Run the test script using the absolute path
            result = subprocess.run(
                [sys.executable, filepath],
                capture_output=False,
                text=True,
                check=True  # Raise an exception for non-zero exit codes (test failures)
            )
            print(f"--- {filename} finished successfully ---")

        except FileNotFoundError:
            print(f"--- {filename} FAILED: Test file not found at {filepath} ---")
            all_passed = False
        except subprocess.CalledProcessError as e:
            print(f"--- {filename} FAILED with error code {e.returncode} ---")
            all_passed = False

    print("\n---------------------------------------")
    if all_passed:
        print("ALL ENIGMA TESTS PASSED!")
    else:
        print("SOME ENIGMA TESTS FAILED!")
    print("---------------------------------------")


if __name__ == '__main__':
    run_tests_sequentially()