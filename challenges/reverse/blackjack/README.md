# Blackjack

**Author: [`Malcolm Seyd`](https://github.com/malcolmseyd)**

**Category: `Reversing Hard`**

## Description

As I stepped into the bustling casino, the air was thick with anticipation. My eyes scanned the room until they landed on the blackjack table. Sitting across from me was the dealer, their movements precise and mechanical. With each shuffle and deal, there was something eerily robotic about them, sending a chill down my spine. Yet, I couldn't resist the allure of the cards spread out before me, beckoning me to take a chance.

## Organizers

Host the Dockerfile (it exposes a TCP socket on port 12345). Also distribute the binary `blackjack` at the top level.

## Solution

This challenge requires the player to win over $100 million in blackjack after 50 games to get the flag. The intended solution uses cards revealed to break the RNG to predict cards and bet accordingly.

The binary was stripped, but no obfuscation is present and the code paths are mostly straightforward, so the reversing is pretty trivial. I'll mostly talk about the code that I think is important.

This is the function for drawing cards from the deck. It generates 16-bits from the RNG on demand every second call, and uses the lower and upper bits of the output as the first and second cards respectively (modulo 52 of course). Here's the Ghidra decompilation with some nice variable names:

```c
int draw(void) {
  uint card;

  if (cards_left == 0) {
    cards_left = 1;
    seed = seed * 881361583 + 961021159;
    card = (uint)((ushort)((uint)seed >> 16) & 0x7fff);
  }
  else {
    card = (uint)card_bits;
    cards_left = cards_left + -1;
  }
  card_bits = (ushort)card >> 8;
  return (card & 0xff) + ((card & 0xff) / 52) * -52;
}
```

The RNG is a [linear congruential generator](https://en.wikipedia.org/wiki/Linear_congruential_generator) with a = 881361583, c = 961021159, and m = 2^32 (the assembly uses EAX which is 32 bits). We can actually model this in Z3 and break it! I actually got the idea for this challenge from [an article on this very topic](https://alephsecurity.com/2019/09/02/z3-for-webapp-security/), where they break Java's `java.util.Random.next()` and MSVC's `rand()` which are also LGCs.

See [rng.py](./solution/rng.py) for an re-implementation and breaking of the RNG in Python using Z3. I've given it 10 cards to create an oracle that guesses the next cards, and it does so reliably. I've tried to make the code as readable as possible, but read [this article](https://alephsecurity.com/2019/09/02/z3-for-webapp-security/) if you'd like a good introduction to the subject.

See [play.py](./solution/play.py) for a solver that can break the game reliably, getting the flag in under a second on my machine if I run blackjack locally. It basically just plays at least 3 rounds to look at cards drawn, cracks the RNG to make an oracle, and then uses the oracle with a super simple algorithm to predict wins/losses and bet accordingly. You'll need `pwntools` and `z3` to run these scripts.


### Bonus unintended solution
I'm adding this after the challenge, but I just had to mention it since it's much simpler. Both [firekern](https://f1r3k3rn.github.io/wr1t3upz/writeups/vikeCTF/blackjack.html) and [Krauq](https://ctf.krauq.com/vikectf-2024#blackjack-14-solves) mentioned this in their writeups, so credit where credit is due.

The seed is just the current time in seconds (I didn't read the manual and assumed it was milliseconds!), so any two games that start within one second of each other have an identical seed. You can simply start two games at once, and both games will have identical decks. You can use one game as an oracle to reveal the cards, and use the other game to bet with future-sight.

firekern did this by opening two connections at once, and Krauq used the binary to run a local game at the same time as the real game.

I'm impressed by this solution, and that's totally on me for missing it. This is a pretty strong case for not using the time as a random seed, so remember to use `/dev/urandom` everyone!

## Flag

```
vikeCTF{h4v3_y0u_b33n_C0un71NG_c4Rd5}
```
