# ecb-a-tron-9000

In this challenge, we are presented with a website that encrypts a 16 character long block of data. We are told by the convenient help button that this is using ECB (electronic codebook) encryption, which is a type of block cipher. Block ciphers operate on fixed length sequences of characters, but ECB is unique, as each block is encrypted with the same key. This means that encrypting the same plaintext with the same key will always produce the same ciphertext. This makes it an extremely impractical method of encryption but a very tasty one for hungry CTF players.

We are told that the flag is a 16 character string of uppercase letters appended to our input, surrounded by DUCTF{...}. Additionally, as not all our inputs have lengths that are multiples of 32, incomplete blocks are padded with spaces.

Another feature of this extremely helpful website is the brute-force mode. When used, it tries every uppercase letter in that position and prints all the encrypted text.

If we combine all our knowledge, we can break the encryption one letter at a time by finding the encrypted version of the last letter in the flag, followed by 15 spaces. We can do this by exploiting the vulnerability in ECB, and compare the ciphertext to every possible combination:

![brute-force.png](A screenshot of the brute-force mode working on the first character, with 15 spaces afterwards).

We can then get the encrypted version:

![leak.png](A screenshot of the encryption of the final letter in the flag)

```
7eDO1sulAoTuNImM/PdNgQ 
```

which we can see translates to E.

Continuing the process gives:

![brute-force2.png](A screenshot of the brute-force mode working on the first character, with the previous result E in the second position, and 14 spaces after that)

> We place the E in the second position as the flag is *appended* to our input, meaning that we are effectively working backwards.

![leak2.png](A screenshot of the encryption of the second to last letter in the flag)

```
SNgaro2LvmPJfPxKUR1rXw
```

which is an S.

Repeating this we get `DONTUSEECBPLEASE` and therefore the flag is **`DUCTF{DONTUSEECBPLEASE}`**