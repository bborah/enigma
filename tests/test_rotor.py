import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from enigma import Rotor

def test_rotor_creation():
    rotor = Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'A', 1, 'Q')
    assert rotor.position() == 'A'
    print("Rotor creation test passed")

def test_rotor_turning():
    rotor = Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'A', 1, 'Q')
    rotor.rotate()
    assert rotor.position() == 'B'
    rotor.rotate()
    assert rotor.position() == 'C'
    print("Rotor turning test passed")

def test_rotor_notch():
    rotor = Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'P', 1, 'Q')
    assert not rotor.at_turnover()
    rotor.rotate()
    assert rotor.at_turnover()
    print("Rotor notch test passed")

def test_forward_encoding():
    rotor = Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'A', 1, 'Q')
    result = rotor.encode_forward('A')
    assert result == 'E'
    print("Forward encoding test passed")

if __name__ == '__main__':
    test_rotor_creation()
    test_rotor_turning()
    test_rotor_notch()
    test_forward_encoding()
    print("\nAll Rotor tests passed!")
