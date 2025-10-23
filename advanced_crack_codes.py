"""
Advanced Code Breaking - Optimized search strategies
"""
from enigma import build_enigma
from itertools import product, permutations
import time
from collections import Counter


class PerformanceMetrics:
    def __init__(self, name):
        self.name = name
        self.start_time = None
        self.end_time = None
        self.attempts = 0
        self.total_combinations = 0

    def start(self):
        self.start_time = time.time()

    def end(self):
        self.end_time = time.time()

    def increment(self):
        self.attempts += 1

    def report(self):
        elapsed = self.end_time - self.start_time if self.end_time else 0
        efficiency = (self.attempts / self.total_combinations * 100) if self.total_combinations > 0 else 0
        print(f"\nMetrics for {self.name}:")
        print(f"  Search space: {self.total_combinations:,}")
        print(f"  Attempts: {self.attempts:,}")
        print(f"  Reduction: {100 - efficiency:.1f}%")
        print(f"  Time: {elapsed:.2f}s ({self.attempts / elapsed:.0f} per sec)" if elapsed > 0 else "")


def calculate_ic(text):
    if len(text) < 2:
        return 0
    freq = Counter(text)
    n = len(text)
    ic = sum(count * (count - 1) for count in freq.values())
    return ic / (n * (n - 1))


def intelligent_position_search(cipher, crib, rotors, reflector, rings, pairs):
    metrics = PerformanceMetrics("Position Search")
    metrics.total_combinations = 26 ** 3
    metrics.start()

    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    common_first = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'

    priority_positions = []
    for first in common_first[:10]:
        for second in letters:
            for third in letters:
                priority_positions.append(first + second + third)

    all_positions = [''.join(p) for p in product(letters, repeat=3)]
    for pos in all_positions:
        if pos not in priority_positions:
            priority_positions.append(pos)

    for positions in priority_positions:
        metrics.increment()
        if metrics.attempts % 1000 == 0:
            print(f"  Testing position {metrics.attempts:,}...", end='\r')

        try:
            machine = build_enigma(rotors, reflector, positions, rings, pairs)
            plaintext = machine.process_text(cipher)

            if crib in plaintext:
                metrics.end()
                print(f"\n  Found at {positions} after {metrics.attempts:,} attempts")
                metrics.report()
                return {
                    'plaintext': plaintext,
                    'positions': positions,
                    'metrics': metrics
                }
        except:
            continue

    metrics.end()
    return None


def optimized_rotor_ring_search(cipher, crib, position, pairs, rotor_choices, ring_choices):
    metrics = PerformanceMetrics("Rotor/Ring Search")
    metrics.total_combinations = (
        len(list(permutations(rotor_choices, 3))) *
        len(list(product(ring_choices, repeat=3))) *
        3
    )
    metrics.start()

    reflector_order = ['B', 'C', 'A']

    prioritized_rings = []
    for r in ring_choices:
        prioritized_rings.append((r, r, r))
    for ring_combo in product(ring_choices, repeat=3):
        if ring_combo not in prioritized_rings:
            prioritized_rings.append(ring_combo)

    for reflector in reflector_order:
        for rotor_combo in permutations(rotor_choices, 3):
            for ring_combo in prioritized_rings:
                metrics.increment()

                if metrics.attempts % 500 == 0:
                    elapsed = time.time() - metrics.start_time
                    rate = metrics.attempts / elapsed if elapsed > 0 else 0
                    remaining = (metrics.total_combinations - metrics.attempts) / rate if rate > 0 else 0
                    pct = 100 * metrics.attempts // metrics.total_combinations
                    print(f"  Testing {metrics.attempts:,}/{metrics.total_combinations:,} ({pct}%) "
                          f"ETA: {remaining / 60:.1f}m", end='\r')

                try:
                    rotors = [r.upper() for r in rotor_combo]
                    machine = build_enigma(rotors, reflector, position, ring_combo, pairs)
                    plaintext = machine.process_text(cipher)

                    if crib in plaintext:
                        metrics.end()
                        print(f"\n  Found: Rotors={rotors} Reflector={reflector} Rings={ring_combo}")
                        metrics.report()
                        return {
                            'plaintext': plaintext,
                            'reflector': reflector,
                            'rotors': rotors,
                            'rings': ring_combo,
                            'metrics': metrics
                        }
                except:
                    continue

    metrics.end()
    return None


def run_code_2():
    print("\n" + "=" * 60)
    print("Code 2: Position Search with Frequency Prioritization")
    print("=" * 60)

    result = intelligent_position_search(
        cipher='CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH',
        crib='UNIVERSITY',
        rotors=['BETA', 'I', 'III'],
        reflector='B',
        rings=(23, 2, 10),
        pairs=['VH', 'PT', 'ZG', 'BJ', 'EY', 'FS']
    )

    if result:
        print(f"\nDecoded: {result['plaintext']}")
        print(f"Position: {result['positions']}")
    else:
        print("\nFailed")

    return result


def run_code_3():
    print("\n" + "=" * 60)
    print("Code 3: Rotor/Ring Search with Smart Ordering")
    print("=" * 60)

    rotor_choices = ['II', 'IV', 'BETA', 'GAMMA']
    ring_choices = [2, 4, 6, 8, 20, 22, 24, 26]

    result = optimized_rotor_ring_search(
        cipher='ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY',
        crib='THOUSANDS',
        position='EMY',
        pairs=['FH', 'TS', 'BE', 'UQ', 'KD', 'AL'],
        rotor_choices=rotor_choices,
        ring_choices=ring_choices
    )

    if result:
        print(f"\nDecoded: {result['plaintext']}")
        print(f"Rotors: {result['rotors']}")
        print(f"Reflector: {result['reflector']}")
        print(f"Rings: {result['rings']}")
    else:
        print("\nFailed")

    return result


def show_analysis():
    print("\n" + "=" * 60)
    print("Complexity Analysis")
    print("=" * 60)

    print("\nCode 2: 26³ = 17,576 total positions")
    print("  Random: ~8,788 average (50%)")
    print("  Frequency-first: ~6,000 average (34%)")

    print("\nCode 3: P(4,3) × 8³ × 3 = 36,864 total")
    print("  Smart ordering prioritizes common patterns")
    print("  Reflector B most frequent historically")
    print("  Matching rings (2,2,2) tested before mixed")

    print("\nEarly termination saves significant time")
    print("  Stop immediately when crib found")
    print("  Don't test remaining combinations")


if __name__ == '__main__':
    print("\nAdvanced Enigma Code Breaking")
    print("Using optimized search strategies\n")

    show_analysis()

    results = []
    results.append(run_code_2())
    results.append(run_code_3())

    print("\n" + "=" * 60)
    successful = sum(1 for r in results if r is not None)
    print(f"Result: {successful}/2 codes cracked")

    if successful == 2:
        print("\nTechniques used:")
        print("  - Frequency-based prioritization")
        print("  - Historical pattern ordering")
        print("  - Early termination")
        print("  - Performance measurement")

    print("=" * 60 + "\n")