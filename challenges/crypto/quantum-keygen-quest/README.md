# Quantum Keygen Quest

**Author: [`Joshua Machado`](https://github.com/JoshoTheMosho)**

**Category: `Crypto Medium`**

## Description

Gather 'round, ye stout-hearted souls, for within these sacred gates lie the keys to unlock the mysteries of the cosmos. Let not the symbols deceive thee, for they hold the power to unravel the very fabric of reality itself.

With nimble fingers and minds sharp as Mjölnir's edge, apply the ancient enchantments to thy ciphered scrolls. Dance with the shadows of uncertainty, for it is within the darkness that the true light of knowledge shall be revealed.

As the stars guide our course through the endless expanse, let us embark on this odyssey with courage in our hearts and the spirit of adventure blazing in our souls. For today, we embark on a voyage beyond the realms of mortal comprehension. Today, we harness the power of the quantum seas and emerge victorious, as legends of old. Skál!

## Organizers

Provide the text file `patternsAndEnchantments.txt`

## Setup

Use the encrypt.py script, modifying the flag variable for your purposes.

## Solution

Essentially, for every matched H or X, we extract the bit from the binary sequence. We then convert this from binary which will give us our flag.

Run the solution.py script to get the flag from the given txt file.

## Explanation

Quantum Key Distribution is a secure communication method that utilizes quantum mechanics to ensure two parties produce and share a randomized key. This process is protected from third parties eavesdropping during the process, as doing so will raise flags to the two parties that someone is interfering.

Alice generates a random sequence of quantum bits, or qubits, typically encoded in the polarization states of individual photons. She sends these qubits to Bob over a quantum communication channel.

Upon receiving the qubits, Bob randomly measures each qubit's polarization state using a basis chosen from two possible sets (in our case, we use a Hadamard gate or a Not gate). This measurement choice is kept secret from Eve, a potential eavesdropper.

Alice and Bob then publicly compare a subset of their encoded bits to check for discrepancies. If no errors are detected, they generate a cryptographic key from the remaining bits. In our challenges case, we don't worry about this. Essentially, when the basis matches with the quantum gates applied, we extract a classical bit from Astrid's original sequence.

To further enhance security, Alice and Bob apply privacy amplification techniques to the raw key, reducing its size while maintaining its randomness. This step helps to mitigate any information that Eve may have gathered during the transmission.

Finally, Alice and Bob use the resulting shared key to encrypt their communications using conventional cryptographic algorithms, ensuring secure and authenticated communication. We get This binary string right before converting it to our flag format below.

## Flag

```
vikeCTF{QU4N7UM_C0MPU71N6_15_C001}
```
 
