# Norse Cryptogram

**Author: [`Joshua Machado`](https://github.com/JoshoTheMosho)**

**Category: `Crypto Easy`**

## Description

Delve into the realm of Norse mythology and unlock the secrets of the runic script in this cryptic challenge. Armed with your wits and keen eye, decrypt the ancient messages hidden within the runes. Will you prove yourself worthy of Odin's wisdom or fall prey to the tricks of Loki? Prepare to embark on a journey through Viking lore as you unravel the Runebound Riddles!

## Organizers

Provide the text file `runicTranscript.txt`

## Solution

[CyberChef Decode](<https://gchq.github.io/CyberChef/#recipe=From_Binary('Space',8)From_Base64('A-Za-z0-9%2B/%3D',true,false)From_Base64('A-Za-z0-9%2B/%3D',true,false)From_Decimal('Space',false)From_Base64('A-Za-z0-9%2B/%3D',true,false)From_Hex('Auto')From_Hexdump()From_Base32('A-Z2-7%3D',true)ROT13_Brute_Force(true,true,false,100,0,true,'')>)
|
[CyberChef Encode](<https://gchq.github.io/CyberChef/#recipe=ROT13(true,true,false,12)To_Base32('A-Z2-7%3D')To_Hexdump(16,false,false,false)To_Hex('Space',0)To_Base64('A-Za-z0-9%2B/%3D')To_Decimal('Space',false)To_Base64('A-Za-z0-9%2B/%3D')To_Base64('A-Za-z0-9%2B/%3D')To_Binary('Space',8)&input=dmlrZUNURntyNDFEM3I1XzBGX3JVTjFDX0tOMFcxM0Q2M30>)

Start off with `01010100 011...`, Binary

We then get `TnpjZ01...5qRT0=`, Base64 as it ends with `=`

From `NzcgMT...gNjE=`, Base64

We see `77 122 65 103...78 68 99 103 78...`, we may have thought it was in Octal, but because of the 9's it's Decimal.

From this we get `MzAgMzAgMz...MzUgN2M=`, Base64

From `30 30...33 35 7c`, Hex

From `00000000  4e 42 32 58 4f 34 4b 50 49 5a 4a 48 57 5a 42 55  |NB2XO4KPIZJHWZBU|...` its in the format of a Hexdump, so convert from that

From `NB2XO4...` we might notice all chars are uppercase, an identifier of a base32 encoding.

From `}36P31I0ZW_O1ZGd_R0_5d3P14d{RFOqwuh` we can recognize it is similar to a flag format with the brackets, so we just reverse it.

From `huwqOFR{d41P3d5_0R_dGZ1O_WZ0I13P63}` This kinda looks like a flag, so we assume some type of rotation cipher was used. We can use ROT13 Brute Force with vikeCTF as our search, and get the flag from a rotation of 14.

## Flag

```
vikeCTF{r41D3r5_0F_rUN1C_KN0W13D63}
```
