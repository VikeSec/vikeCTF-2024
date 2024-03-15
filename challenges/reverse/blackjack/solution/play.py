import rng
from pwn import *

# p = connect("localhost", "12345")
p = process(["./blackjack"])


def place_bet(n: int):
    p.sendline(str(n).encode())
    p.recvline_startswith(b"house: X")


def read_balance() -> int:
    p.recvuntil(b"balance:")
    return int(p.recvline().decode())


def parse_card(card: str) -> int:
    if card[0] == "K":
        rank = 13
    elif card[0] == "Q":
        rank = 12
    elif card[0] == "J":
        rank = 11
    else:
        rank = int(card[:-1])
    suit = "shcd".find(card[-1])
    return (rank + suit * 13) - 1


def read_final_hands():
    p.recvuntil(b":")
    player_hand = list(
        map(parse_card, (p.recvuntil(b"(")[:-1].strip()).decode().split())
    )
    p.recvuntil(b":")
    house_hand = list(
        map(parse_card, (p.recvuntil(b"(")[:-1].strip()).decode().split())
    )
    return player_hand, house_hand


games_left = 50

card_history = []

# while games_left:
for i in range(games_left):
    print("standing until we break the RNG...")
    print(f"balance={read_balance()}")
    place_bet(1)
    p.sendline(b"s")
    player_hand, house_hand = read_final_hands()
    card_history += player_hand[:2]
    card_history += house_hand[:2]
    card_history += player_hand[2:]
    card_history += house_hand[2:]
    # print(read_final_hands())
    games_left -= 1

    # give it a few games and avoid odd numbers
    if i > 3 and len(card_history) % 2 == 0:
        break

print("The RNG is broken!")
deck = rng.gen_cards(rng.break_rng(card_history))

def card_value(n: int):
    return min((n % 13) + 1, 10)

# cards = []
top = card_value(next(deck))


def draw() -> int:
    global top
    card = top
    top = card_value(next(deck))
    return card


def peek() -> int:
    return top


# greedy strategy should be good enough to at least know if we can win
def simulate() -> tuple[bool, list[str]]:
    player_hand = [draw() for _ in range(2)]
    house_hand = [draw() for _ in range(2)]

    inputs = []

    while True:
        # draw until we would hit >21
        hit_score = sum(player_hand) + peek()
        if hit_score <= 21:
            inputs += "h"
            player_hand.append(draw())
        else:
            inputs += "s"
            break

    # simulate house, they can't peek
    while True:
        if sum(house_hand) > 21:
            return True, inputs
        if sum(house_hand) >= 17:
            break
        else:
            house_hand.append(draw())

    return sum(house_hand) < sum(player_hand), inputs


while games_left > 0:
    games_left -= 1

    balance = read_balance()
    will_win, inputs = simulate()
    if will_win:
        place_bet(balance)
        balance *= 2
    else:
        place_bet(1)
        balance -= 1
    for c in inputs:
        p.sendline(c.encode())
print(p.recvall().decode())
