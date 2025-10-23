import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from enigma import Plugboard, PlugLead

def test_empty_board():
    board = Plugboard()
    assert board.encode('A') == 'A'
    assert board.encode('Z') == 'Z'
    print("Empty board test passed")

def test_single_connection():
    board = Plugboard()
    board.add(PlugLead('SZ'))
    assert board.encode('S') == 'Z'
    assert board.encode('Z') == 'S'
    assert board.encode('A') == 'A'
    print("Single connection test passed")

def test_multiple_connections():
    board = Plugboard()
    board.add(PlugLead('SZ'))
    board.add(PlugLead('GT'))
    board.add(PlugLead('DV'))
    board.add(PlugLead('KU'))
    
    assert board.encode('K') == 'U'
    assert board.encode('U') == 'K'
    assert board.encode('A') == 'A'
    print("Multiple connections test passed")

def test_duplicate_rejection():
    board = Plugboard()
    board.add(PlugLead('AB'))
    
    try:
        board.add(PlugLead('AC'))
        assert False, "Should reject duplicate"
    except ValueError:
        pass
    
    print("Duplicate rejection test passed")

if __name__ == '__main__':
    test_empty_board()
    test_single_connection()
    test_multiple_connections()
    test_duplicate_rejection()
    print("\nAll Plugboard tests passed!")
