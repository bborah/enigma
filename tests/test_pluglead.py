import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from enigma import PlugLead

def test_basic_swap():
    lead = PlugLead('AG')
    assert lead.encode('A') == 'G'
    assert lead.encode('G') == 'A'
    assert lead.encode('B') == 'B'
    print("Basic swap test passed")

def test_case_handling():
    lead = PlugLead('ag')
    assert lead.encode('a') == 'G'
    assert lead.encode('g') == 'A'
    print("Case handling test passed")

def test_invalid_pairs():
    try:
        PlugLead('AA')
        assert False, "Should not allow same letter"
    except ValueError:
        pass
    
    try:
        PlugLead('ABC')
        assert False, "Should not allow three letters"
    except ValueError:
        pass
    
    print("Invalid pairs test passed")

if __name__ == '__main__':
    test_basic_swap()
    test_case_handling()
    test_invalid_pairs()
    print("\nAll PlugLead tests passed!")
