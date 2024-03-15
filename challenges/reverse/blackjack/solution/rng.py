import math
import z3
import random

z3.set_param("parallel.enable", False)

A = 688885507887235759  # big prime
C = 128076673052050663  # big prime
BITS = 32
M = 2**BITS


DEFAULT_SEED = 123456789


def next_state(state):
    return (state * A + C) % M


def next_rand(state):
    REVEAL = 16
    mask = (1 << (REVEAL - 1)) - 1  # unsigned
    return (state >> REVEAL) & mask


def gen_cards(seed: int):
    state = seed

    def rng():
        nonlocal state
        state = next_state(state)
        return next_rand(state)

    cards_left = 0
    cards_bits = 0
    while True:
        if cards_left == 0:
            cards_bits = rng()
            cards_left = 2
        card = (cards_bits & 0xFF) % 52
        yield card
        cards_bits >>= 8
        cards_left -= 1


def break_rng(cards: list[int]):
    states = [
        z3.BitVec(f"state_{i}", BITS) for i in range(math.ceil(len(cards) / 2) + 1)
    ]

    s = z3.Solver()

    # model state transitions
    for i in range(1, len(states)):
        s.add(states[i] == next_state(states[i - 1]))

    # model outputs
    for i in range(len(cards)):
        i_state = (i // 2) + 1
        offset = (i % 2) * 8
        cards_bits = next_rand(states[i_state])
        card = z3.URem((cards_bits & (0xFF << offset)) >> offset, 52)
        s.add(card == cards[i])

    if s.check() == z3.sat:
        return s.model()[states[-1]].as_long()
    else:
        return None


if __name__ == "__main__":
    seed = random.randint(0, 2**32)
    N = 10

    # randomly generate N cards and never show internal state
    hidden_deck = gen_cards(seed)
    cards = [next(hidden_deck) % 52 for _ in range(N)]

    rng_state = break_rng(cards)
    # note that this only works with N as powers of 2 since gen_cards assumes
    # each output produces 2 cards
    oracle_deck = gen_cards(rng_state)

    # compare oracle to actual
    for _ in range(100):
        assert next(hidden_deck) == next(oracle_deck)

    print("The oracle is accurate!")
