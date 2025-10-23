"""
Code breaking script for Enigma assignment
Uses the enigma.py implementation to crack all 5 codes
"""
from enigma import build_enigma
from itertools import product, permutations, combinations


def test_reflectors(cipher, crib, rotors, positions, rings, pairs):
    """Try all reflectors A, B, C"""
    for reflector in ['A', 'B', 'C']:
        try:
            machine = build_enigma(rotors, reflector, positions, rings, pairs)
            plaintext = machine.process_text(cipher)
            if crib in plaintext:
                return {
                    'plaintext': plaintext,
                    'reflector': reflector,
                    'rotors': rotors,
                    'positions': positions,
                    'rings': rings,
                    'pairs': pairs
                }
        except:
            continue
    return None


def test_positions(cipher, crib, rotors, reflector, rings, pairs):
    """Try all possible 3-letter position combinations"""
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    count = 0
    for combo in product(letters, repeat=3):
        count += 1
        if count % 1000 == 0:
            print(f"  Tried {count} positions...", end='\r')
        
        positions = ''.join(combo)
        try:
            machine = build_enigma(rotors, reflector, positions, rings, pairs)
            plaintext = machine.process_text(cipher)
            if crib in plaintext:
                print(f"\n  Found after {count} attempts!")
                return {
                    'plaintext': plaintext,
                    'reflector': reflector,
                    'rotors': rotors,
                    'positions': positions,
                    'rings': rings,
                    'pairs': pairs
                }
        except:
            continue
    return None


def test_rotor_ring_reflector(cipher, crib, position, pairs, rotor_choices, ring_choices):
    """Try combinations of rotors, rings, and reflectors"""
    count = 0
    total = len(list(permutations(rotor_choices, 3))) * len(list(product(ring_choices, repeat=3))) * 3
    print(f"  Total combinations to try: {total}")
    
    for rotor_combo in permutations(rotor_choices, 3):
        for ring_combo in product(ring_choices, repeat=3):
            for reflector in ['A', 'B', 'C']:
                count += 1
                if count % 100 == 0:
                    print(f"  Progress: {count}/{total} ({100*count//total}%)", end='\r')
                
                try:
                    rotors = [r.upper() for r in rotor_combo]
                    machine = build_enigma(rotors, reflector, position, ring_combo, pairs)
                    plaintext = machine.process_text(cipher)
                    if crib in plaintext:
                        print(f"\n  Found after {count} attempts!")
                        return {
                            'plaintext': plaintext,
                            'reflector': reflector,
                            'rotors': rotors,
                            'positions': position,
                            'rings': ring_combo,
                            'pairs': pairs
                        }
                except:
                    continue
    return None


def test_missing_pairs(cipher, crib, rotors, reflector, positions, rings, known_pairs, unknown_pairs):
    """Find missing plugboard pairs where one letter is known"""
    # Get letters already used
    used = set(''.join(known_pairs))
    
    # Get available letters for pairing
    available = [c for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if c not in used]
    
    count = 0
    # Try all combinations of available letters for the two unknown pairs
    for a_partner in available:
        for i_partner in available:
            if a_partner == i_partner:
                continue
            
            count += 1
            if count % 100 == 0:
                print(f"  Tried {count} combinations...", end='\r')
            
            # Build complete pairs list
            test_pairs = known_pairs + ['A' + a_partner, 'I' + i_partner]
            
            try:
                machine = build_enigma(rotors, reflector, positions, rings, test_pairs)
                plaintext = machine.process_text(cipher)
                if crib in plaintext:
                    print(f"\n  Found after {count} attempts!")
                    return {
                        'plaintext': plaintext,
                        'reflector': reflector,
                        'rotors': rotors,
                        'positions': positions,
                        'rings': rings,
                        'pairs': test_pairs
                    }
            except:
                continue
    return None

def code_1():
    print("=" * 70)
    print("CODE 1: Finding unknown reflector")
    print("=" * 70)
    
    result = test_reflectors(
        cipher='DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ',
        crib='SECRETS',
        rotors=['BETA', 'GAMMA', 'V'],
        positions='MJM',
        rings=(4, 2, 14),
        pairs=['KI', 'XN', 'FL']
    )
    
    if result:
        print(f"✓ Decoded: {result['plaintext']}")
        print(f"✓ Reflector: {result['reflector']}")
    else:
        print("✗ Failed to crack")
    print()
    return result


def code_2():
    print("=" * 70)
    print("CODE 2: Finding starting positions")
    print("=" * 70)
    
    result = test_positions(
        cipher='CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH',
        crib='UNIVERSITY',
        rotors=['BETA', 'I', 'III'],
        reflector='B',
        rings=(23, 2, 10),
        pairs=['VH', 'PT', 'ZG', 'BJ', 'EY', 'FS']
    )
    
    if result:
        print(f"✓ Decoded: {result['plaintext']}")
        print(f"✓ Positions: {result['positions']}")
    else:
        print("✗ Failed to crack")
    print()
    return result


def code_3():
    print("=" * 70)
    print("CODE 3: Finding rotors, rings, and reflector (even numbers only)")
    print("=" * 70)
    print("This will take 2-5 minutes...")
    
    # Even rotors only: II, IV, Beta, Gamma
    rotor_choices = ['ii', 'iv', 'beta', 'gamma']
    
    # Ring settings with all even digits
    ring_choices = [2, 4, 6, 8, 20, 22, 24, 26]
    
    result = test_rotor_ring_reflector(
        cipher='ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY',
        crib='THOUSANDS',
        position='EMY',
        pairs=['FH', 'TS', 'BE', 'UQ', 'KD', 'AL'],
        rotor_choices=rotor_choices,
        ring_choices=ring_choices
    )
    
    if result:
        print(f"✓ Decoded: {result['plaintext']}")
        print(f"✓ Rotors: {result['rotors']}")
        print(f"✓ Reflector: {result['reflector']}")
        print(f"✓ Rings: {result['rings']}")
    else:
        print("✗ Failed to crack")
    print()
    return result


def code_4():
    print("=" * 70)
    print("CODE 4: Finding missing plugboard pairs")
    print("=" * 70)
    
    result = test_missing_pairs(
        cipher='SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW',
        crib='TUTOR',
        rotors=['V', 'III', 'IV'],
        reflector='A',
        positions='SWU',
        rings=(24, 12, 10),
        known_pairs=['WP', 'RJ', 'VF', 'HN', 'CG', 'BS'],
        unknown_pairs=['A?', 'I?']  # A and I need partners
    )
    
    if result:
        print(f"✓ Decoded: {result['plaintext']}")
        print(f"✓ Complete plugboard: {result['pairs']}")
    else:
        print("✗ Failed to crack")
    print()
    return result


def test_modified_reflectors(cipher, crib, rotors, positions, rings, pairs):
    """Try all standard reflectors with double wire swaps (2 swap operations)"""
    from enigma import RotorAssembly
    from itertools import combinations

    expected = 'YOUCANFOLLOWMYDOGONINSTAGRAMATTALESOFHOFFMANN'

    # Try each reflector
    for base_ref in ['A', 'B', 'C']:
        print(f"\n  Testing reflector {base_ref}...")
        original_wiring = RotorAssembly.REFLECTOR_CONFIGS[base_ref]

        # Extract pairs
        pairs_list = []
        used = set()
        for i, letter in enumerate(original_wiring):
            if chr(i + ord('A')) not in used:
                let1 = chr(i + ord('A'))
                let2 = letter
                pairs_list.append((let1, let2))
                used.add(let1)
                used.add(let2)

        count = 0
        # Choose 4 pairs total (for 2 separate swap operations)
        for four_pair_indices in combinations(range(len(pairs_list)), 4):
            # Split into two groups of 2 for the two swap operations
            for split in [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]:
                swap1_indices = (four_pair_indices[split[0][0]], four_pair_indices[split[0][1]])
                swap2_indices = (four_pair_indices[split[1][0]], four_pair_indices[split[1][1]])

                p1, p2 = pairs_list[swap1_indices[0]], pairs_list[swap1_indices[1]]
                p3, p4 = pairs_list[swap2_indices[0]], pairs_list[swap2_indices[1]]

                # Try all swap combinations for both swaps
                for swap1_type in range(3):
                    for swap2_type in range(3):
                        count += 1
                        if count % 1000 == 0:
                            print(f"    Progress: {count} combinations tested...", end='\r')

                        # Apply both swaps
                        modified = list(original_wiring)

                        # First swap
                        if swap1_type == 0:
                            new_p1, new_p2 = (p1[0], p2[1]), (p2[0], p1[1])
                        elif swap1_type == 1:
                            new_p1, new_p2 = (p1[0], p2[0]), (p1[1], p2[1])
                        else:
                            new_p1, new_p2 = (p1[1], p2[0]), (p1[0], p2[1])

                        modified[ord(new_p1[0]) - ord('A')] = new_p1[1]
                        modified[ord(new_p1[1]) - ord('A')] = new_p1[0]
                        modified[ord(new_p2[0]) - ord('A')] = new_p2[1]
                        modified[ord(new_p2[1]) - ord('A')] = new_p2[0]

                        # Second swap
                        if swap2_type == 0:
                            new_p3, new_p4 = (p3[0], p4[1]), (p4[0], p3[1])
                        elif swap2_type == 1:
                            new_p3, new_p4 = (p3[0], p4[0]), (p3[1], p4[1])
                        else:
                            new_p3, new_p4 = (p3[1], p4[0]), (p3[0], p4[1])

                        modified[ord(new_p3[0]) - ord('A')] = new_p3[1]
                        modified[ord(new_p3[1]) - ord('A')] = new_p3[0]
                        modified[ord(new_p4[0]) - ord('A')] = new_p4[1]
                        modified[ord(new_p4[1]) - ord('A')] = new_p4[0]

                        modified_str = ''.join(modified)

                        # Test
                        try:
                            from enigma import Enigma, Plugboard, PlugLead, Reflector, RotorAssembly

                            machine = Enigma()
                            machine.plugboard = Plugboard()
                            for pp in pairs:
                                machine.plugboard.add(PlugLead(pp))

                            machine.rotor_assembly = RotorAssembly(rotors, 'B', positions, rings)
                            machine.rotor_assembly.reflector = Reflector(modified_str)

                            result = machine.process_text(cipher)

                            if result == expected or 'INSTAGRAM' in result:
                                print(f"\n  ✓ Found it after {count} attempts!")
                                return {
                                    'plaintext': result,
                                    'base_reflector': base_ref,
                                    'original_wiring': original_wiring,
                                    'modified_wiring': modified_str,
                                    'swap1_original': (p1, p2),
                                    'swap1_modified': (new_p1, new_p2),
                                    'swap2_original': (p3, p4),
                                    'swap2_modified': (new_p3, new_p4),
                                    'rotors': rotors,
                                    'positions': positions,
                                    'rings': rings,
                                    'pairs': pairs
                                }
                        except:
                            pass

        print(f"\n  Tested {count} combinations for reflector {base_ref}")

    return None

def code_5():
    print("=" * 70)
    print("CODE 5: Custom reflector with TWO wire swaps")
    print("=" * 70)
    print("Testing reflectors with double wire-swap modifications...")
    print("(This may take a few minutes...)")
    print()

    result = test_modified_reflectors(
        cipher='HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX',
        crib='INSTAGRAM',
        rotors=['V', 'II', 'IV'],
        positions='AJL',
        rings=(6, 18, 7),
        pairs=['UG', 'IE', 'PO', 'NX', 'WT']
    )

    if result:
        print(f"Decoded: {result['plaintext']}")
        print(f"Base reflector: {result['base_reflector']}")
        print(f"First swap:")
        print(f"    Original: {result['swap1_original'][0]} and {result['swap1_original'][1]}")
        print(f"    Modified: {result['swap1_modified'][0]} and {result['swap1_modified'][1]}")
        print(f"Second swap:")
        print(f"    Original: {result['swap2_original'][0]} and {result['swap2_original'][1]}")
        print(f"    Modified: {result['swap2_modified'][0]} and {result['swap2_modified'][1]}")
    else:
        print("Failed to crack")
        print("Expected: YOUCANFOLLOWMYDOGONINSTAGRAMATTALESOFHOFFMANN")
    print()
    return result


if __name__ == '__main__':
    print("\n" + "*" * 70)
    print(" ENIGMA CODE BREAKING")
    print("*" * 70 + "\n")

    results = []
    results.append(code_1())
    results.append(code_2())
    results.append(code_3())
    results.append(code_4())
    results.append(code_5())

    print("*" * 70)
    print(" SUMMARY")
    print("*" * 70)
    successful = sum(1 for r in results if r is not None)
    print(f"Successfully cracked: {successful}/5 codes")
    print("*" * 70 + "\n")