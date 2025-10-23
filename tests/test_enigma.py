import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from enigma import build_enigma

def test_basic_encoding():
    machine = build_enigma(['I', 'II', 'III'], 'B', 'AAZ')
    result = machine.process_text('A')
    assert result == 'U', f"Expected U, got {result}"
    print("Basic encoding test passed")

def test_message_encoding():
    pairs = ['HL', 'MO', 'AJ', 'CX', 'BZ', 'SR', 'NI', 'YW', 'DG', 'PK']
    machine = build_enigma(['I', 'II', 'III'], 'B', 'AAZ', (1,1,1), pairs)
    result = machine.process_text('HELLOWORLD')
    assert result == 'RFKTMBXVVW', f"Expected RFKTMBXVVW, got {result}"
    print("Message encoding test passed")

def test_different_positions():
    machine = build_enigma(['I', 'II', 'III'], 'B', 'AAA')
    result = machine.process_text('A')
    assert result == 'B', f"Expected B, got {result}"
    print("Different positions test passed")

def test_ring_settings():
    machine = build_enigma(['IV', 'V', 'BETA'], 'B', 'AAA', (14, 9, 24))
    result = machine.process_text('H')
    assert result == 'Y', f"Expected Y, got {result}"
    print("Ring settings test passed")

def test_four_rotors():
    machine = build_enigma(['I', 'II', 'III', 'IV'], 'C', 'QEVZ', (7, 11, 15, 19))
    result = machine.process_text('Z')
    assert result == 'V', f"Expected V, got {result}"
    print("Four rotors test passed")

def test_long_message():
    pairs = ['PC', 'XZ', 'FM', 'QA', 'ST', 'NB', 'HY', 'OR', 'EV', 'IU']
    machine = build_enigma(['IV', 'V', 'BETA', 'I'], 'A', 'EZGP', (18, 24, 3, 5), pairs)
    cipher = 'BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI'
    result = machine.process_text(cipher)
    expected = 'CONGRATULATIONSONPRODUCINGYOURWORKINGENIGMAMACHINESIMULATOR'
    assert result == expected, f"Expected {expected}, got {result}"
    print("Long message test passed")

def test_reciprocal():
    machine1 = build_enigma(['I', 'II', 'III'], 'B', 'AAA')
    encrypted = machine1.process_text('TESTMESSAGE')
    
    machine2 = build_enigma(['I', 'II', 'III'], 'B', 'AAA')
    decrypted = machine2.process_text(encrypted)
    
    assert decrypted == 'TESTMESSAGE', f"Expected TESTMESSAGE, got {decrypted}"
    print("Reciprocal test passed")

if __name__ == '__main__':
    test_basic_encoding()
    test_message_encoding()
    test_different_positions()
    test_ring_settings()
    test_four_rotors()
    test_long_message()
    test_reciprocal()
    print("\nAll Enigma machine tests passed!")
