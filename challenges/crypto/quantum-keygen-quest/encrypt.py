import random

def generate_bits_and_gates(original_key):
    result_key = []
    alice_result_gates = []
    bob_result_gates = []

    goal_length = len(original_key) * 4  # Estimate from https://pdfs.semanticscholar.org/924b/ac4f2bc31df18d673913dfddee90d3f3e11a.pdf

    # Generate random bits for the result_key
    result_key = [random.choice(['0', '1']) for _ in range(goal_length)]

    # Place our original key in the result_key
    orig_index = 0
    for i in range(goal_length):
        # Randomly place original key in result_key
        if orig_index < len(original_key) and random.random() < len(original_key) / goal_length:
            result_key[i] = original_key[orig_index]
            orig_index += 1

            # Generate random gates for Alice and Bob
            resulting_gate = random.choice(['H', 'X'])
            alice_result_gates += resulting_gate
            bob_result_gates += resulting_gate

        else:
            # They don't match, so we need to apply a random gate to Alice and Bob
            resulting_gate = random.choice(['H', 'X'])

            alice_result_gates += resulting_gate

            if resulting_gate == 'H':
                bob_result_gates += 'X'
            else:
                bob_result_gates += 'H'

    # Just in case we didn't use all of the original key
    if orig_index < len(original_key):
        result_key += original_key[orig_index:]

    return result_key, alice_result_gates, bob_result_gates

def string_to_binary(string):
    """Convert ASCII string to binary string"""
    return ''.join(format(ord(x), '08b') for x in string)

# This main method will be reversing the process of Quantum Key Distribution
# Essentially, we want to say Adam and Bob ended with our result_key, and we will need to work backwards to get what
    # things they started with and what gates they applied to end up with that shared key
def main():
    # Original flag
    flag = "vikeCTF{QU4N7UM_C0MPU71N6_15_C001}"

    # Shared key at the end that we want to reverse
    result_key = ''.join(format(ord(x), '08b') for x in flag)

    S_A, G_A, G_B = generate_bits_and_gates(result_key)

    # What Alice and Bob started with
    print(f'S_A: {"".join(S_A)}')
    print(f'G_A: {"".join(G_A)}')
    print(f'G_B: {"".join(G_B)}')

if __name__ == "__main__":
    main()
